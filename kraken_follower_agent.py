"""
Nike Rocket - Kraken Follower Agent
====================================

Automated trading agent that:
1. Polls Nike Rocket API for signals
2. Executes trades on Kraken Futures
3. Manages positions with TP/SL
4. Reports P&L back to API

Users deploy this on Render with their own Kraken API keys.

Author: Nike Rocket Team
"""

import asyncio
import aiohttp
import time
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
from typing import Optional, Dict
import os
import sys
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== CONFIGURATION ====================

# Nike Rocket API
FOLLOWER_API_URL = os.getenv("FOLLOWER_API_URL", "https://your-railway-app.up.railway.app")
USER_API_KEY = os.getenv("USER_API_KEY", "")

# Kraken API credentials
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY", "")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET", "")

# Trading settings
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"

# Kraken API URLs
if USE_TESTNET:
    KRAKEN_API_URL = "https://demo-futures.kraken.com"
else:
    KRAKEN_API_URL = "https://futures.kraken.com"

# Polling interval
POLL_INTERVAL = 10  # seconds

# ==================== HEALTH CHECK SERVER FOR RENDER ====================

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP server for Render health checks"""
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            status = b'Nike Rocket Follower Agent - Running\n'
            status += f'Mode: {"TESTNET" if USE_TESTNET else "LIVE"}\n'.encode()
            status += f'Polling: Active\n'.encode()
            self.wfile.write(status)
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs to keep output clean
        pass


def start_health_server():
    """Start health check server in background thread"""
    port = int(os.getenv("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"🏥 Health check server started on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Health server error: {e}")

# ==================== KRAKEN API CLIENT ====================

class KrakenFuturesAPI:
    """Kraken Futures API client"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://demo-futures.kraken.com" if testnet else "https://futures.kraken.com"
    
    def _generate_signature(self, endpoint: str, postdata: str, nonce: str) -> str:
        """Generate authentication signature"""
        if endpoint.startswith("/derivatives"):
            endpoint = endpoint[len("/derivatives"):]
        
        message = postdata + nonce + endpoint
        message_hash = hashlib.sha256(message.encode()).digest()
        secret_decoded = base64.b64decode(self.api_secret)
        signature = hmac.new(secret_decoded, message_hash, hashlib.sha512)
        return base64.b64encode(signature.digest()).decode()
    
    async def _private_request(self, endpoint: str, data: Dict = None) -> Dict:
        """Make authenticated API request"""
        if data is None:
            data = {}
        
        nonce = str(int(time.time() * 1000))
        data["nonce"] = nonce
        
        postdata = urllib.parse.urlencode(data)
        signature = self._generate_signature(endpoint, postdata, nonce)
        
        headers = {
            "APIKey": self.api_key,
            "Authent": signature,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                data=postdata
            ) as response:
                result = await response.json()
                
                print(f"🔍 Kraken API Response Status: {response.status}")
                print(f"🔍 Kraken API Response Body: {result}")
                
                if result.get("result") == "success":
                    return result
                else:
                    error_msg = result.get('error', result.get('errors', 'Unknown error'))
                    print(f"❌ Kraken API returned error: {error_msg}")
                    raise Exception(f"Kraken API error: {error_msg}")
    
    async def get_accounts(self) -> Dict:
        """Get account information"""
        return await self._private_request("/api/v3/accounts")
    
    async def fetch_balance(self) -> Dict:
        """
        Get account balance in CCXT-compatible format
        Fetches from Kraken Futures accounts endpoint and formats the response
        """
        try:
            print("🔍 Calling Kraken API: /api/v3/accounts")
            accounts_data = await self._private_request("/api/v3/accounts")
            
            print(f"📦 Kraken API Response: {accounts_data}")
            
            # Kraken returns: {"result": "success", "accounts": {...}}
            if accounts_data.get("result") == "success" and "accounts" in accounts_data:
                accounts = accounts_data["accounts"]
                
                # Format as CCXT-style balance
                balance = {
                    'total': {},
                    'free': {},
                    'used': {}
                }
                
                # Kraken Futures flex account shows balances
                if "flex" in accounts:
                    flex = accounts["flex"]
                    
                    # Get available currencies
                    if "currencies" in flex:
                        for currency, data in flex["currencies"].items():
                            currency_upper = currency.upper()
                            
                            # Total balance (including positions)
                            if "quantity" in data:
                                balance['total'][currency_upper] = float(data["quantity"])
                            
                            # Available balance (not in use)
                            if "available" in data:
                                balance['free'][currency_upper] = float(data["available"])
                
                # Also check if there's a balance key directly
                if "balanceValue" in accounts.get("flex", {}):
                    balance_value = float(accounts["flex"]["balanceValue"])
                    balance['total']['USD'] = balance_value
                    balance['free']['USD'] = balance_value
                
                return balance
            
            return {'total': {}, 'free': {}, 'used': {}}
            
        except Exception as e:
            print(f"❌ Error fetching balance from Kraken: {e}")
            print(f"🔍 Exception type: {type(e).__name__}")
            import traceback
            print(f"🔍 Traceback: {traceback.format_exc()}")
            return {'total': {}, 'free': {}, 'used': {}}
    
    async def send_bracket_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        entry_price: Optional[float],
        stop_loss: float,
        take_profit: float
    ) -> Dict:
        """
        Send bracket order (entry + TP + SL)
        
        Args:
            symbol: Trading pair (e.g., "pf_adausd")
            side: "buy" or "sell"
            quantity: Position size
            entry_price: Entry price (None for market order)
            stop_loss: Stop loss price
            take_profit: Take profit price
        """
        # Prepare order batch
        batch_order = {
            "batchorder": [
                {
                    "order": "send",
                    "order_type": "lmt" if entry_price else "mkt",
                    "symbol": symbol,
                    "side": side,
                    "size": quantity,
                    "limitPrice": entry_price,
                    "cliOrdId": f"nike_entry_{int(time.time())}"
                },
                {
                    "order": "send",
                    "order_type": "stp",
                    "symbol": symbol,
                    "side": "sell" if side == "buy" else "buy",
                    "size": quantity,
                    "stopPrice": stop_loss,
                    "triggerSignal": "mark",
                    "cliOrdId": f"nike_sl_{int(time.time())}"
                },
                {
                    "order": "send",
                    "order_type": "take_profit",
                    "symbol": symbol,
                    "side": "sell" if side == "buy" else "buy",
                    "size": quantity,
                    "limitPrice": take_profit,
                    "triggerSignal": "mark",
                    "cliOrdId": f"nike_tp_{int(time.time())}"
                }
            ]
        }
        
        return await self._private_request(
            "/api/v3/batchorder",
            {"json": str(batch_order).replace("'", '"')}
        )
    
    async def get_open_positions(self) -> Dict:
        """Get all open positions"""
        return await self._private_request("/api/v3/openpositions")
    
    async def cancel_all_orders(self, symbol: str = None) -> Dict:
        """Cancel all orders (optionally for specific symbol)"""
        data = {}
        if symbol:
            data["symbol"] = symbol
        return await self._private_request("/api/v3/cancelallorders", data)


# ==================== FOLLOWER AGENT ====================

class NikeRocketFollower:
    """Nike Rocket follower agent"""
    
    def __init__(self):
        self.kraken = KrakenFuturesAPI(KRAKEN_API_KEY, KRAKEN_API_SECRET, USE_TESTNET)
        self.session = None
        self.current_position = None
        self.entry_signal = None
        
        print("=" * 60)
        print("🚀 NIKE ROCKET FOLLOWER AGENT")
        print("=" * 60)
        print(f"API URL: {FOLLOWER_API_URL}")
        print(f"Mode: {'TESTNET (Demo)' if USE_TESTNET else 'LIVE (Real Money)'}")
        print(f"Kraken API: {KRAKEN_API_URL}")
        print("💰 Account balance will be fetched when signal arrives")
        print("=" * 60)
    
    async def verify_access(self) -> Dict:
        """Verify access with Nike Rocket API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{FOLLOWER_API_URL}/api/users/verify",
                    headers={"X-API-Key": USER_API_KEY}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"❌ Access verification failed: {error_text}")
                        return {"access_granted": False, "reason": "API error"}
            except Exception as e:
                print(f"❌ Error verifying access: {e}")
                return {"access_granted": False, "reason": str(e)}
    
    async def poll_for_signal(self) -> Optional[Dict]:
        """Poll Nike Rocket API for new signals"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{FOLLOWER_API_URL}/api/latest-signal",
                    headers={"X-API-Key": USER_API_KEY}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check access
                        if not data.get("access_granted"):
                            print(f"⚠️ Access suspended: {data.get('reason')}")
                            if data.get("amount_due"):
                                print(f"💰 Payment required: ${data['amount_due']:.2f}")
                            return None
                        
                        # Return signal if present
                        return data.get("signal")
                    else:
                        print(f"❌ Error fetching signal: HTTP {response.status}")
                        return None
            except Exception as e:
                print(f"❌ Error polling API: {e}")
                return None
    
    async def get_current_equity(self) -> float:
        """
        Get current futures account equity from Kraken
        Uses EXACT same method as master algorithm
        Checks multiple currencies (USD, USDT, USDC) for Kraken multi-collateral
        """
        try:
            balance = await self.kraken.fetch_balance()
            
            # Try multiple currency options (Kraken multi-collateral)
            for currency in ['USD', 'USDT', 'USDC']:
                # Check total balance
                if 'total' in balance and currency in balance['total']:
                    equity = float(balance['total'][currency])
                    if equity > 0:
                        print(f"💰 Current equity: ${equity:,.2f} {currency}")
                        return equity
            
            # Try free balance as fallback
            for currency in ['USD', 'USDT', 'USDC']:
                if 'free' in balance and currency in balance['free']:
                    equity = float(balance['free'][currency])
                    if equity > 0:
                        print(f"💰 Current available: ${equity:,.2f} {currency}")
                        return equity
            
            print("⚠️ No balance found in USD, USDT, or USDC")
            print("💡 Make sure you have funds in your Kraken Futures wallet")
            return 0.0
                
        except Exception as e:
            print(f"❌ Error fetching balance: {e}")
            return 0.0
    
    async def execute_signal(self, signal: Dict):
        """Execute trading signal on Kraken"""
        try:
            print("\n" + "=" * 60)
            print("📡 NEW SIGNAL RECEIVED")
            print("=" * 60)
            print(f"Action: {signal['action']}")
            print(f"Symbol: {signal['symbol']}")
            print(f"Entry: ${signal['entry_price']}")
            print(f"Stop Loss: ${signal['stop_loss']}")
            print(f"Take Profit: ${signal['take_profit']}")
            print(f"Leverage: {signal['leverage']}x")
            print("=" * 60)
            
            # GET REAL-TIME ACCOUNT BALANCE (same as master algo!)
            print("\n💰 Fetching account balance...")
            current_equity = await self.get_current_equity()
            
            if current_equity <= 0:
                print("❌ No funds detected in account!")
                print("💡 Please deposit funds to your Kraken Futures wallet")
                return
            
            # CHECK IF WE ALREADY HAVE A POSITION FOR THIS SYMBOL
            print("\n🔍 Checking for existing positions...")
            positions = await self.kraken.get_open_positions()
            
            # Convert symbol to Kraken format for comparison
            kraken_symbol = self.convert_symbol(signal['symbol'])
            
            # Check if position already exists
            for pos in positions.get("openPositions", []):
                if pos.get("symbol") == kraken_symbol:
                    print(f"⚠️ Already have open position for {signal['symbol']}")
                    print(f"⏳ Waiting for TP/SL to close before taking new signals")
                    print(f"   Current position: {pos.get('side')} {pos.get('size')} @ ${pos.get('fillPrice')}")
                    print("=" * 60)
                    return  # Skip this signal
            
            print("✅ No existing position found, proceeding with execution")
            
            # Store signal and equity for P&L reporting later
            self.entry_signal = signal
            self.entry_equity = current_equity
            
            # Convert symbol (ADA/USDT → pf_adausd)
            kraken_symbol = self.convert_symbol(signal['symbol'])
            
            # Calculate position size using REAL account equity
            risk_amount = current_equity * 0.02  # 2% risk per trade
            risk_per_unit = abs(signal['entry_price'] - signal['stop_loss'])
            position_size = risk_amount / risk_per_unit
            
            # Apply leverage
            position_size_with_leverage = position_size * signal['leverage']
            
            print(f"\n🎯 POSITION SIZING:")
            print(f"Account Equity: ${current_equity:,.2f}")
            print(f"Risk Amount (2%): ${risk_amount:.2f}")
            print(f"Risk Per Unit: ${risk_per_unit:.4f}")
            print(f"Base Position: {position_size:.2f}")
            print(f"With Leverage: {position_size_with_leverage:.2f}")
            
            # Determine side
            side = "buy" if signal['action'] == "BUY" else "sell"
            
            # Send bracket order
            print(f"\n🚀 EXECUTING KRAKEN BRACKET ORDER...")
            result = await self.kraken.send_bracket_order(
                symbol=kraken_symbol,
                side=side,
                quantity=position_size_with_leverage,
                entry_price=signal['entry_price'],
                stop_loss=signal['stop_loss'],
                take_profit=signal['take_profit']
            )
            
            print("✅ Order executed successfully!")
            print(f"Result: {result}")
            
            # Store position info
            self.current_position = {
                "signal_id": signal['signal_id'],
                "symbol": signal['symbol'],
                "side": side,
                "entry_price": signal['entry_price'],
                "stop_loss": signal['stop_loss'],
                "take_profit": signal['take_profit'],
                "position_size": position_size_with_leverage,
                "leverage": signal['leverage'],
                "opened_at": datetime.utcnow().isoformat(),
                "kraken_result": result
            }
            
        except Exception as e:
            print(f"❌ Error executing signal: {e}")
            import traceback
            traceback.print_exc()
    
    async def monitor_position(self):
        """Monitor open position and report P&L when closed"""
        if not self.current_position:
            return
        
        try:
            # Check if position is still open
            positions = await self.kraken.get_open_positions()
            
            # Find our position
            our_symbol = self.convert_symbol(self.current_position['symbol'])
            position_still_open = False
            
            for pos in positions.get("openPositions", []):
                if pos.get("symbol") == our_symbol:
                    position_still_open = True
                    break
            
            # If position closed, calculate and report P&L
            if not position_still_open:
                print("\n" + "=" * 60)
                print("💰 POSITION CLOSED - CALCULATING P&L")
                print("=" * 60)
                
                await self.report_pnl()
                
                # Clear position
                self.current_position = None
                self.entry_signal = None
        
        except Exception as e:
            print(f"❌ Error monitoring position: {e}")
    
    async def report_pnl(self):
        """Calculate and report P&L to Nike Rocket API"""
        if not self.current_position:
            return
        
        try:
            # Get account info to find the exit price
            accounts = await self.kraken.get_accounts()
            
            # For simplicity, we'll estimate P&L
            # In production, you'd get the exact fill price from order history
            entry = self.current_position['entry_price']
            
            # Check if position hit TP or SL
            # This is a simplified version - in production, check order fills
            current_price = entry  # Placeholder
            
            # Estimate exit (TP or SL)
            if self.current_position['side'] == "buy":
                # Assume TP if price went up, SL if down
                if abs(entry - self.current_position['take_profit']) < abs(entry - self.current_position['stop_loss']):
                    exit_price = self.current_position['take_profit']
                else:
                    exit_price = self.current_position['stop_loss']
            else:
                if abs(entry - self.current_position['take_profit']) < abs(entry - self.current_position['stop_loss']):
                    exit_price = self.current_position['take_profit']
                else:
                    exit_price = self.current_position['stop_loss']
            
            # Calculate P&L
            if self.current_position['side'] == "buy":
                pnl = (exit_price - entry) * self.current_position['position_size']
            else:
                pnl = (entry - exit_price) * self.current_position['position_size']
            
            profit_percent = ((exit_price - entry) / entry) * 100
            
            print(f"Entry: ${entry}")
            print(f"Exit: ${exit_price}")
            print(f"P&L: ${pnl:.2f}")
            print(f"Return: {profit_percent:.2f}%")
            
            # Report to API
            trade_report = {
                "trade_id": f"nike_{int(time.time())}",
                "signal_id": self.current_position['signal_id'],
                "opened_at": self.current_position['opened_at'],
                "closed_at": datetime.utcnow().isoformat(),
                "symbol": self.current_position['symbol'],
                "side": self.current_position['side'].upper(),
                "entry_price": entry,
                "exit_price": exit_price,
                "position_size": self.current_position['position_size'],
                "leverage": self.current_position['leverage'],
                "profit_usd": pnl,
                "profit_percent": profit_percent
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{FOLLOWER_API_URL}/api/report-pnl",
                    json=trade_report,
                    headers={"X-API-Key": USER_API_KEY}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"\n✅ P&L reported to Nike Rocket API")
                        print(f"Monthly profit: ${result.get('monthly_profit', 0):.2f}")
                        print(f"Monthly fee due: ${result.get('monthly_fee_due', 0):.2f}")
                    else:
                        print(f"❌ Failed to report P&L: HTTP {response.status}")
        
        except Exception as e:
            print(f"❌ Error reporting P&L: {e}")
            import traceback
            traceback.print_exc()
    
    def convert_symbol(self, symbol: str) -> str:
        """Convert symbol format (ADA/USDT → pf_adausd)"""
        # Remove slash and convert to lowercase
        base = symbol.split("/")[0].lower()
        return f"pf_{base}usd"
    
    async def run(self):
        """Main agent loop"""
        print("\n🎯 Starting Nike Rocket Follower Agent...")
        
        # Verify access
        access = await self.verify_access()
        if not access.get("access_granted"):
            print(f"❌ Access denied: {access.get('reason')}")
            print("Please contact support or pay any outstanding fees.")
            return
        
        print("✅ Access verified")
        print("\n📡 Polling for signals every 10 seconds...")
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                # Poll for new signal
                signal = await self.poll_for_signal()
                
                if signal:
                    # Execute signal
                    await self.execute_signal(signal)
                
                # Monitor existing position
                await self.monitor_position()
                
                # Wait before next poll
                await asyncio.sleep(POLL_INTERVAL)
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Stopping agent...")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                await asyncio.sleep(POLL_INTERVAL)
        
        print("👋 Agent stopped")


# ==================== MAIN ====================

async def main():
    """Entry point"""
    # Validate environment variables
    if not USER_API_KEY:
        print("❌ Error: USER_API_KEY not set")
        print("Please set your Nike Rocket API key in environment variables")
        sys.exit(1)
    
    if not KRAKEN_API_KEY or not KRAKEN_API_SECRET:
        print("❌ Error: Kraken API credentials not set")
        print("Please set KRAKEN_API_KEY and KRAKEN_API_SECRET")
        sys.exit(1)
    
    # Create and run agent
    agent = NikeRocketFollower()
    await agent.run()


if __name__ == "__main__":
    # Start health check server in background for Render
    health_thread = Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Run main polling loop
    asyncio.run(main())
