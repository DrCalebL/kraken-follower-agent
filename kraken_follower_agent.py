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

# CRITICAL: Force unbuffered output for real-time logs on Render/Railway
import os
import sys
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

import asyncio
import aiohttp
import time
import ccxt
from datetime import datetime
from typing import Optional, Dict
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

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

# Configure logging with immediate flush
import logging.handlers

class FlushStreamHandler(logging.StreamHandler):
    """StreamHandler that flushes after every emit"""
    def emit(self, record):
        super().emit(record)
        self.flush()

logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for verbose output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[FlushStreamHandler(sys.stdout)]
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
        
        print("=" * 60, flush=True)
        print("🚀 NIKE ROCKET FOLLOWER AGENT", flush=True)
        print("=" * 60, flush=True)
        print(f"API URL: {FOLLOWER_API_URL}", flush=True)
        print(f"Mode: {'TESTNET (Demo)' if USE_TESTNET else 'LIVE (Real Money)'}", flush=True)
        print(f"Exchange: Kraken Futures (via CCXT)", flush=True)
        
        # Check API key
        if USER_API_KEY:
            print(f"🔑 User API Key: {USER_API_KEY[:10]}...{USER_API_KEY[-4:]}", flush=True)
        else:
            print("⚠️  WARNING: USER_API_KEY not set!", flush=True)
            print("⚠️  Set USER_API_KEY environment variable", flush=True)
        
        print("💰 Account balance will be fetched when signal arrives", flush=True)
        print("=" * 60, flush=True)
    
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
                url = f"{FOLLOWER_API_URL}/api/signals/latest"
                headers = {"X-API-Key": USER_API_KEY}
                
                logger.debug(f"Polling: {url}")
                logger.debug(f"API Key: {USER_API_KEY[:10]}..." if USER_API_KEY else "API Key: NOT SET")
                
                async with session.get(url, headers=headers) as response:
                    logger.debug(f"Response status: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        logger.debug(f"Response data: {data}")
                        
                        if data.get('has_new_signal'):
                            logger.info("🎯 NEW SIGNAL DETECTED!")
                            return data['signal']
                        else:
                            logger.debug("No new signal")
                    elif response.status == 401:
                        logger.error("❌ Authentication failed - check USER_API_KEY")
                    elif response.status == 403:
                        logger.error("❌ Access forbidden - check API key permissions")
                    else:
                        logger.warning(f"⚠️ Unexpected status: {response.status}")
                        response_text = await response.text()
                        logger.warning(f"Response: {response_text}")
                    
                    return None
            except Exception as e:
                logger.error(f"❌ Error polling API: {e}")
                import traceback
                logger.error(traceback.format_exc())
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
            # Handle both 'action' (from API/curl) and 'signal' (from master algo)
            action = signal.get('action') or signal.get('signal')
            
            print("\n" + "=" * 60, flush=True)
            print("📡 NEW SIGNAL RECEIVED", flush=True)
            print("=" * 60, flush=True)
            print(f"Action: {action}", flush=True)
            print(f"Symbol: {signal['symbol']}", flush=True)
            print(f"Entry: ${signal['entry_price']}", flush=True)
            print(f"Stop Loss: ${signal['stop_loss']}", flush=True)
            print(f"Take Profit: ${signal['take_profit']}", flush=True)
            print(f"Leverage: {signal['leverage']}x", flush=True)
            print("=" * 60, flush=True)
            
            # GET REAL-TIME ACCOUNT BALANCE (same as master algo!)
            print("\n💰 Fetching account balance...", flush=True)
            current_equity = self.get_current_equity()
            
            if current_equity <= 0:
                print("❌ No funds detected in account!", flush=True)
                return
            
            # Convert symbol to Kraken format
            kraken_symbol = self.convert_symbol(signal['symbol'])
            print(f"🔄 Converted symbol: {signal['symbol']} → {kraken_symbol}", flush=True)
            
            # CHECK IF WE ALREADY HAVE A POSITION
            print("\n🔍 Checking for existing positions...", flush=True)
            positions = self.exchange.fetch_positions([kraken_symbol])
            
            has_position = False
            for pos in positions:
                if pos['symbol'] == kraken_symbol and float(pos.get('contracts', 0)) > 0:
                    has_position = True
                    print(f"⚠️ Existing position found: {pos['contracts']} contracts", flush=True)
                    break
            
            if has_position:
                print("⚠️ Already have a position, skipping signal", flush=True)
                return
            
            print("✅ No existing position found, proceeding with execution", flush=True)
            
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
            
            print(f"\n🎯 POSITION SIZING:", flush=True)
            print(f"Account Equity: ${current_equity:,.2f}", flush=True)
            print(f"Risk Amount (2%, flush=True): ${risk_amount:,.2f}", flush=True)
            print(f"Risk Per Unit: ${risk_per_unit:.4f}", flush=True)
            print(f"Base Position: {base_position_size:.2f}", flush=True)
            print(f"With Leverage: {quantity:.2f}", flush=True)
            
            # PLACE ORDERS SEQUENTIALLY (SAME AS MASTER ALGO)
            print(f"\n🚀 EXECUTING 3-ORDER BRACKET...", flush=True)
            
            # 1. Place entry order (market)
            print("📝 Placing entry order...", flush=True)
            side = action.lower()  # 'buy' or 'sell' - from either 'action' or 'signal' field
            entry_order = self.exchange.create_market_order(kraken_symbol, side, quantity)
            print(f"✅ Entry order placed: {entry_order['id']}", flush=True)
            
            # 2. Wait a moment for fill
            await asyncio.sleep(2)
            
            # 3. Place take-profit order
            print("📝 Placing take-profit order...", flush=True)
            exit_side = 'sell' if side == 'buy' else 'buy'
            tp_price = float(self.exchange.price_to_precision(kraken_symbol, signal['take_profit']))
            tp_order = self.exchange.create_limit_order(
                kraken_symbol, exit_side, quantity, tp_price,
                params={'reduceOnly': True}
            )
            print(f"✅ Take-profit order placed: {tp_order['id']}", flush=True)
            
            # 4. Place stop-loss order
            print("📝 Placing stop-loss order...", flush=True)
            sl_price = float(self.exchange.price_to_precision(kraken_symbol, signal['stop_loss']))
            sl_order = self.exchange.create_order(
                kraken_symbol, 'stop', exit_side, quantity,
                params={'stopPrice': sl_price, 'reduceOnly': True}
            )
            print(f"✅ Stop-loss order placed: {sl_order['id']}", flush=True)
            
            print(f"\n🎉 TRADE EXECUTED SUCCESSFULLY!", flush=True)
            print(f"Position opened with full TP/SL protection", flush=True)
            print("=" * 60, flush=True)
            
        except Exception as e:
            logger.error(f"❌ Error executing signal: {e}")
            import traceback
            traceback.print_exc()


# ==================== MAIN LOOP ====================

async def main():
    """Main polling loop"""
    print("🎯 Starting Nike Rocket Follower Agent...", flush=True)
    
    follower = NikeRocketFollower()
    
    # Verify access
    access_result = await follower.verify_access()
    if not access_result.get('access_granted'):
        print("❌ Access denied! Check your API key", flush=True)
        return
    
    print("✅ Access verified", flush=True)
    print(f"📡 Polling for signals every {POLL_INTERVAL} seconds...", flush=True)
    print("Press Ctrl+C to stop\n", flush=True)
    
    poll_count = 0
    while True:
        try:
            poll_count += 1
            logger.info(f"📡 Poll #{poll_count} - Checking for signals...")
            
            # Poll for new signal
            signal = await follower.poll_for_signal()
            
            if signal:
                logger.info(f"✨ Signal detected on poll #{poll_count}!")
                # Execute the signal
                await follower.execute_signal(signal)
            else:
                logger.info(f"✓ Poll #{poll_count} complete - No new signals")
            
            # Wait before next poll
            logger.debug(f"⏳ Waiting {POLL_INTERVAL} seconds until next poll...")
            await asyncio.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n⛔ Stopping follower agent...", flush=True)
            break
        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    # Start health check server in background for Render
    health_thread = Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Run main polling loop
    asyncio.run(main())
