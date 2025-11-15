"""
Nike Rocket - Kraken Follower Agent (CCXT Version)
===================================================

Automated trading agent that:
1. Polls Nike Rocket API for signals
2. Executes trades on Kraken Futures using CCXT
3. Uses EXACT SAME methods as master algorithm
4. Manages positions with TP/SL

Author: Nike Rocket Team
"""

import asyncio
import aiohttp
import time
import ccxt
import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== CONFIGURATION ====================

# Nike Rocket API
FOLLOWER_API_URL = os.getenv("FOLLOWER_API_URL", "https://nike-rocket-api-production.up.railway.app")
USER_API_KEY = os.getenv("USER_API_KEY", "")

# Kraken API credentials
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY", "")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET", "")

# Trading settings
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"
PYTHONUNBUFFERED = os.getenv("PYTHONUNBUFFERED", "1")

# Polling interval
POLL_INTERVAL = 10  # seconds

# ==================== LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('FOLLOWER')

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
        pass  # Suppress HTTP logs


def start_health_server():
    """Start health check server in background thread"""
    port = int(os.getenv("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"🏥 Health check server started on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"⚠️ Health server error: {e}")


# ==================== KRAKEN EXCHANGE (USING CCXT - SAME AS MASTER) ====================

def initialize_kraken_exchange():
    """
    Initialize Kraken Futures using CCXT
    EXACT SAME METHOD AS MASTER ALGORITHM
    """
    exchange_config = {
        'apiKey': KRAKEN_API_KEY,
        'secret': KRAKEN_API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    }
    
    if USE_TESTNET:
        exchange_config['urls'] = {
            'api': {
                'public': 'https://demo-futures.kraken.com/derivatives',
                'private': 'https://demo-futures.kraken.com/derivatives',
            }
        }
        logger.info("🧪 Kraken DEMO mode enabled - using testnet")
    else:
        logger.info("🔴 Kraken LIVE mode enabled - REAL MONEY!")
    
    exchange = ccxt.krakenfutures(exchange_config)
    
    # Test connection
    try:
        exchange.load_markets()
        logger.info(f"✅ Connected to Kraken Futures")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Kraken: {e}")
        raise
    
    return exchange


# ==================== FOLLOWER AGENT ====================

class NikeRocketFollower:
    """Nike Rocket follower agent using CCXT (same as master algo)"""
    
    def __init__(self):
        self.exchange = initialize_kraken_exchange()
        self.session = None
        self.current_position = None
        self.entry_signal = None
        
        print("=" * 60)
        print("🚀 NIKE ROCKET FOLLOWER AGENT")
        print("=" * 60)
        print(f"API URL: {FOLLOWER_API_URL}")
        print(f"Mode: {'TESTNET (Demo)' if USE_TESTNET else 'LIVE (Real Money)'}")
        print(f"Exchange: Kraken Futures (via CCXT)")
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
                        logger.error(f"❌ Access verification failed: {response.status}")
                        return {"access_granted": False}
            except Exception as e:
                logger.error(f"❌ Error verifying access: {e}")
                return {"access_granted": False}
    
    async def poll_for_signal(self) -> Optional[Dict]:
        """Poll Nike Rocket API for new signals"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{FOLLOWER_API_URL}/api/signals/latest",
                    headers={"X-API-Key": USER_API_KEY}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('has_new_signal'):
                            return data['signal']
                    return None
            except Exception as e:
                logger.error(f"❌ Error polling API: {e}")
                return None
    
    def get_current_equity(self) -> float:
        """
        Get current futures account equity
        EXACT SAME METHOD AS MASTER ALGORITHM
        """
        try:
            balance = self.exchange.fetch_balance()
            
            # Try multiple currency options (Kraken multi-collateral)
            for currency in ['USD', 'USDT', 'USDC']:
                if 'total' in balance and currency in balance['total']:
                    equity = float(balance['total'][currency])
                    if equity > 0:
                        logger.info(f"💰 Current equity: ${equity:,.2f} {currency}")
                        return equity
            
            # Try free balance as fallback
            for currency in ['USD', 'USDT', 'USDC']:
                if 'free' in balance and currency in balance['free']:
                    equity = float(balance['free'][currency])
                    if equity > 0:
                        logger.info(f"💰 Current available: ${equity:,.2f} {currency}")
                        return equity
            
            logger.warning("⚠️ No balance found in USD, USDT, or USDC")
            return 0.0
                
        except Exception as e:
            logger.error(f"❌ Error fetching balance: {e}")
            return 0.0
    
    def convert_symbol(self, signal_symbol: str) -> str:
        """
        Convert signal symbol format to Kraken format
        
        Signal format: BTC/USDT, ETH/USDT, etc.
        Kraken format: BTC/USD:USD, ETH/USD:USD (linear perpetuals)
        """
        # Remove /USDT and add /USD:USD
        base = signal_symbol.split('/')[0]
        kraken_symbol = f"{base}/USD:USD"
        return kraken_symbol
    
    async def execute_signal(self, signal: Dict):
        """Execute trading signal on Kraken using CCXT"""
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
            current_equity = self.get_current_equity()
            
            if current_equity <= 0:
                print("❌ No funds detected in account!")
                return
            
            # Convert symbol to Kraken format
            kraken_symbol = self.convert_symbol(signal['symbol'])
            print(f"🔄 Converted symbol: {signal['symbol']} → {kraken_symbol}")
            
            # CHECK IF WE ALREADY HAVE A POSITION
            print("\n🔍 Checking for existing positions...")
            positions = self.exchange.fetch_positions([kraken_symbol])
            
            has_position = False
            for pos in positions:
                if pos['symbol'] == kraken_symbol and float(pos.get('contracts', 0)) > 0:
                    has_position = True
                    print(f"⚠️ Existing position found: {pos['contracts']} contracts")
                    break
            
            if has_position:
                print("⚠️ Already have a position, skipping signal")
                return
            
            print("✅ No existing position found, proceeding with execution")
            
            # CALCULATE POSITION SIZE
            risk_percentage = 0.02  # 2% risk per trade
            entry_price = signal['entry_price']
            stop_loss = signal['stop_loss']
            leverage = signal['leverage']
            
            # Calculate risk per unit
            if signal['action'].upper() == 'BUY':
                risk_per_unit = abs(entry_price - stop_loss)
            else:
                risk_per_unit = abs(stop_loss - entry_price)
            
            # Calculate position size
            risk_amount = current_equity * risk_percentage
            base_position_size = risk_amount / risk_per_unit if risk_per_unit > 0 else 0
            leveraged_position_size = base_position_size * leverage
            
            # Round to exchange precision
            quantity = float(self.exchange.amount_to_precision(kraken_symbol, leveraged_position_size))
            
            print(f"\n🎯 POSITION SIZING:")
            print(f"Account Equity: ${current_equity:,.2f}")
            print(f"Risk Amount (2%): ${risk_amount:,.2f}")
            print(f"Risk Per Unit: ${risk_per_unit:.4f}")
            print(f"Base Position: {base_position_size:.2f}")
            print(f"With Leverage: {quantity:.2f}")
            
            # PLACE ORDERS SEQUENTIALLY (SAME AS MASTER ALGO)
            print(f"\n🚀 EXECUTING 3-ORDER BRACKET...")
            
            # 1. Place entry order (market)
            print("📝 Placing entry order...")
            side = signal['action'].lower()  # 'buy' or 'sell'
            entry_order = self.exchange.create_market_order(kraken_symbol, side, quantity)
            print(f"✅ Entry order placed: {entry_order['id']}")
            
            # 2. Wait a moment for fill
            await asyncio.sleep(2)
            
            # 3. Place take-profit order
            print("📝 Placing take-profit order...")
            exit_side = 'sell' if side == 'buy' else 'buy'
            tp_price = float(self.exchange.price_to_precision(kraken_symbol, signal['take_profit']))
            tp_order = self.exchange.create_limit_order(
                kraken_symbol, exit_side, quantity, tp_price,
                params={'reduceOnly': True}
            )
            print(f"✅ Take-profit order placed: {tp_order['id']}")
            
            # 4. Place stop-loss order
            print("📝 Placing stop-loss order...")
            sl_price = float(self.exchange.price_to_precision(kraken_symbol, signal['stop_loss']))
            sl_order = self.exchange.create_order(
                kraken_symbol, 'stop', exit_side, quantity,
                params={'stopPrice': sl_price, 'reduceOnly': True}
            )
            print(f"✅ Stop-loss order placed: {sl_order['id']}")
            
            print(f"\n🎉 TRADE EXECUTED SUCCESSFULLY!")
            print(f"Position opened with full TP/SL protection")
            print("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Error executing signal: {e}")
            import traceback
            traceback.print_exc()


# ==================== MAIN LOOP ====================

async def main():
    """Main polling loop"""
    print("🎯 Starting Nike Rocket Follower Agent...")
    
    follower = NikeRocketFollower()
    
    # Verify access
    access_result = await follower.verify_access()
    if not access_result.get('access_granted'):
        print("❌ Access denied! Check your API key")
        return
    
    print("✅ Access verified")
    print(f"📡 Polling for signals every {POLL_INTERVAL} seconds...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Poll for new signal
            signal = await follower.poll_for_signal()
            
            if signal:
                # Execute the signal
                await follower.execute_signal(signal)
            else:
                print(f"⏳ No new signals (polling...)", end='\r')
            
            # Wait before next poll
            await asyncio.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n⛔ Stopping follower agent...")
            break
        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    # Start health check server in background for Render
    health_thread = Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Run main polling loop
    asyncio.run(main())
