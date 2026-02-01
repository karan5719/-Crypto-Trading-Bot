#!/usr/bin/env python3

import argparse
import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.logging_config import setup_logging


class InteractiveCLI:
    
    def __init__(self):
        self.client = None
        self.order_manager = None
        self.logger = None
    
    def print_header(self):
        print("\n" + "="*60)
        print("🤖 BINANCE FUTURES TRADING BOT - TESTNET")
        print("="*60)
    
    def print_menu(self):
        print("\n📋 MAIN MENU")
        print("─"*40)
        print("1. 📈 Place Market Order")
        print("2. 📊 Place Limit Order")
        print("3. 💰 Check Account Balance")
        print("4. 🕐 Get Server Time")
        print("5. 📜 View Recent Orders")
        print("6. ⚙️ Settings")
        print("7. 🚪 Exit")
        print("─"*40)
    
    def get_user_choice(self) -> str:
        while True:
            try:
                choice = input("\n👉 Select an option (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("❌ Invalid choice. Please enter 1-7.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def prompt_symbol(self) -> str:
        print("\n📝 SYMBOL SELECTION")
        print("─"*30)
        print("Popular symbols:")
        print("• BTCUSDT - Bitcoin")
        print("• ETHUSDT - Ethereum")
        print("• ADAUSDT - Cardano")
        print("• SOLUSDT - Solana")
        
        while True:
            symbol = input("\n💱 Enter trading symbol (e.g., BTCUSDT): ").strip().upper()
            if symbol.endswith('USDT') and len(symbol) > 4:
                return symbol
            else:
                print("❌ Invalid symbol. Must end with USDT (e.g., BTCUSDT, ETHUSDT)")
    
    def prompt_side(self) -> str:
        print("\n⬆️⬇️ ORDER SIDE")
        print("─"*20)
        print("BUY  - Long position (profit from price increase)")
        print("SELL - Short position (profit from price decrease)")
        
        while True:
            side = input("\n📊 Enter side (BUY/SELL): ").strip().upper()
            if side in ['BUY', 'SELL']:
                return side
            else:
                print("❌ Invalid side. Must be BUY or SELL")
    
    def prompt_quantity(self, symbol: str) -> str:
        print("\n📊 QUANTITY SELECTION")
        print("─"*30)
        print(f"Symbol: {symbol}")
        print("💡 Tip: Start with small amounts for testing")
        
        while True:
            quantity = input(f"\n🔢 Enter quantity for {symbol}: ").strip()
            try:
                qty = float(quantity)
                if qty > 0:
                    if abs(qty - round(qty, 8)) > 0:
                        print("❌ Too many decimal places. Max 8 decimals.")
                        continue
                    return quantity
                else:
                    print("❌ Quantity must be positive.")
            except ValueError:
                print("❌ Invalid number. Please enter a valid quantity.")
    
    def prompt_price(self, symbol: str, side: str) -> str:
        print("\n💰 PRICE SELECTION")
        print("─"*30)
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        
        if side == 'BUY':
            print("💡 Tip: Set price below current market price for better fills")
        else:
            print("💡 Tip: Set price above current market price for better fills")
        
        while True:
            price = input(f"\n💵 Enter limit price for {symbol}: ").strip()
            try:
                prc = float(price)
                if prc > 0:
                    if abs(prc - round(prc, 8)) > 0:
                        print("❌ Too many decimal places. Max 8 decimals.")
                        continue
                    return price
                else:
                    print("❌ Price must be positive.")
            except ValueError:
                print("❌ Invalid number. Please enter a valid price.")
    
    def confirm_order(self, order_type: str, symbol: str, side: str, quantity: str, price: str = None) -> bool:
        print("\n⚠️ ORDER CONFIRMATION")
        print("="*50)
        print(f"Type:    {order_type}")
        print(f"Symbol:  {symbol}")
        print(f"Side:    {side}")
        print(f"Quantity: {quantity}")
        if price:
            print(f"Price:   ${price}")
        print("="*50)
        
        while True:
            confirm = input("\n✅ Confirm this order? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' or 'n'")
    
    def print_order_result(self, result: Dict):
        if result['success']:
            print("\n✅ ORDER PLACED SUCCESSFULLY!")
            print("─"*40)
            print(f"📋 {result['message']}")
            
            if 'order_response' in result and result['order_response']:
                response = result['order_response']
                print(f"🆔 Order ID: {response.get('orderId', 'N/A')}")
                print(f"📊 Status: {response.get('status', 'N/A')}")
                print(f"💰 Executed: {response.get('executedQty', 'N/A')}")
                if response.get('avgPrice') and response.get('avgPrice') != 'N/A':
                    print(f"💵 Avg Price: ${response.get('avgPrice')}")
        else:
            print("\n❌ ORDER FAILED!")
            print("─"*40)
            print(f"📋 {result['message']}")
            if 'error' in result:
                print(f"🔍 Details: {result['error']}")
    
    def print_balance_info(self, balance_info: Dict):
        if 'error' in balance_info:
            print("\n❌ BALANCE ERROR")
            print("─"*30)
            print(f"🔍 {balance_info['error']}")
            return
        
        print("\n💰 ACCOUNT BALANCE")
        print("="*50)
        print(f"💵 USDT Balance:    ${balance_info['usdt_balance']:.2f}")
        print(f"💼 Total Balance:   ${balance_info['total_wallet_balance']:.2f}")
        print(f"💸 Available:       ${balance_info['available_balance']:.2f}")
        
        if balance_info['open_positions']:
            print(f"\n📊 OPEN POSITIONS ({len(balance_info['open_positions'])})")
            print("─"*50)
            for i, pos in enumerate(balance_info['open_positions'], 1):
                pnl_color = "🟢" if float(pos['unrealized_pnl']) > 0 else "🔴"
                print(f"{i}. {pos['symbol']:<10} {pos['side']:<5} {pos['size']:<12} "
                      f"Entry: ${pos['entry_price']:<10} {pnl_color} PNL: ${pos['unrealized_pnl']}")
        else:
            print("\n📊 No open positions")
        
        print("="*50)
    
    def place_market_order_interactive(self):
        print("\n📈 MARKET ORDER SETUP")
        print("="*40)
        
        symbol = self.prompt_symbol()
        side = self.prompt_side()
        quantity = self.prompt_quantity(symbol)
        
        if self.confirm_order('MARKET', symbol, side, quantity):
            print("\n🚀 Placing market order...")
            result = self.order_manager.place_market_order(symbol, side, quantity)
            self.print_order_result(result)
        else:
            print("\n❌ Order cancelled.")
    
    def place_limit_order_interactive(self):
        print("\n📊 LIMIT ORDER SETUP")
        print("="*40)
        
        symbol = self.prompt_symbol()
        side = self.prompt_side()
        quantity = self.prompt_quantity(symbol)
        price = self.prompt_price(symbol, side)
        
        if self.confirm_order('LIMIT', symbol, side, quantity, price):
            print("\n🚀 Placing limit order...")
            result = self.order_manager.place_limit_order(symbol, side, quantity, price)
            self.print_order_result(result)
        else:
            print("\n❌ Order cancelled.")
    
    def show_settings(self):
        print("\n⚙️ SETTINGS")
        print("="*40)
        print(f"📝 Log Level: {self.logger.level if self.logger else 'Not set'}")
        print(f"🔗 API Base URL: {self.client.base_url if self.client else 'Not connected'}")
        print(f"🔑 API Key: {'✅ Set' if self.client and self.client.api_key else '❌ Not set'}")
        print("="*40)
        print("💡 To change settings, use command line arguments:")
        print("   --log-level DEBUG|INFO|WARNING|ERROR")
        print("   --api-key YOUR_KEY")
        print("   --api-secret YOUR_SECRET")
    
    def run_interactive_mode(self):
        self.print_header()
        
        while True:
            self.print_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.place_market_order_interactive()
            elif choice == '2':
                self.place_limit_order_interactive()
            elif choice == '3':
                print("\n💰 Checking account balance...")
                balance_info = self.order_manager.check_account_balance()
                self.print_balance_info(balance_info)
            elif choice == '4':
                print("\n🕐 Getting server time...")
                try:
                    server_time = self.client.get_server_time()
                    print(f"✅ Server Time: {server_time}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif choice == '5':
                print("\n📜 Recent Orders")
                print("─"*30)
                print("💡 Order history feature coming soon!")
                print("📁 Check log files for order details.")
            elif choice == '6':
                self.show_settings()
            elif choice == '7':
                print("\n� Thank you for using Trading Bot!")
                print("🚀 Happy trading!")
                break
            
            input("\n⏸️ Press Enter to continue...")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot - Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python cli.py
  
  # Quick commands
  python cli.py market BTCUSDT BUY 0.001
  python cli.py limit BTCUSDT SELL 0.001 65000.50
  python cli.py balance
  python cli.py time
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    market_parser = subparsers.add_parser('market', help='Place market order')
    market_parser.add_argument('symbol', help='Symbol (e.g., BTCUSDT)')
    market_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    market_parser.add_argument('quantity', help='Order quantity')
    
    limit_parser = subparsers.add_parser('limit', help='Place limit order')
    limit_parser.add_argument('symbol', help='Symbol (e.g., BTCUSDT)')
    limit_parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    limit_parser.add_argument('quantity', help='Order quantity')
    limit_parser.add_argument('price', help='Order price')
    
    subparsers.add_parser('balance', help='Check account balance')
    subparsers.add_parser('time', help='Get server time')
    
    parser.add_argument('--api-key', help='Binance API key')
    parser.add_argument('--api-secret', help='Binance API secret')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Logging level')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Launch interactive mode (default when no command specified)')
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    logger = setup_logging(args.log_level)
    
    try:
        client = BinanceFuturesClient(api_key=args.api_key, api_secret=args.api_secret)
        order_manager = OrderManager(client)
        
        cli = InteractiveCLI()
        cli.client = client
        cli.order_manager = order_manager
        cli.logger = logger
        
        # Interactive mode (default or explicit)
        if not args.command or args.interactive:
            cli.run_interactive_mode()
            return
        
        # Quick command mode
        if args.command == 'market':
            print(f"\n📈 Market Order: {args.side} {args.quantity} {args.symbol}")
            result = order_manager.place_market_order(args.symbol, args.side, args.quantity)
            cli.print_order_result(result)
        
        elif args.command == 'limit':
            print(f"\n📊 Limit Order: {args.side} {args.quantity} {args.symbol} @ {args.price}")
            result = order_manager.place_limit_order(args.symbol, args.side, args.quantity, args.price)
            cli.print_order_result(result)
        
        elif args.command == 'balance':
            print(f"\n💰 Account Balance")
            balance_info = order_manager.check_account_balance()
            cli.print_balance_info(balance_info)
        
        elif args.command == 'time':
            print(f"\n🕐 Server Time")
            try:
                server_time = client.get_server_time()
                print(f"✅ {server_time}")
            except Exception as e:
                print(f"❌ {e}")
    
    except ValueError as e:
        print(f"❌ Config error: {e}")
        print("\n💡 Set API credentials:")
        print("   export BINANCE_API_KEY='your_key'")
        print("   export BINANCE_API_SECRET='your_secret'")
        print("   Or use --api-key and --api-secret arguments")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
