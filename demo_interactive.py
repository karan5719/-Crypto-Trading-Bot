#!/usr/bin/env python3
"""
Demo script to showcase the enhanced interactive CLI features
without requiring actual API credentials.
"""

import sys
import os

# Add the bot module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import InteractiveCLI


class DemoCLI(InteractiveCLI):
    """Demo version that doesn't require API credentials"""
    
    def __init__(self):
        super().__init__()
        # Mock client and order manager for demo
        self.client = type('MockClient', (), {
            'base_url': 'https://testnet.binancefuture.com',
            'api_key': 'demo_key_***'
        })()
        self.order_manager = type('MockOrderManager', (), {
            'place_market_order': self.mock_market_order,
            'place_limit_order': self.mock_limit_order,
            'check_account_balance': self.mock_balance
        })()
        self.logger = type('MockLogger', (), {'level': 'INFO'})()
    
    def mock_market_order(self, symbol, side, quantity):
        return {
            'success': True,
            'order_response': {
                'orderId': 12345678,
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'status': 'FILLED',
                'executedQty': quantity,
                'avgPrice': '64250.50'
            },
            'message': f"Market {side} order placed"
        }
    
    def mock_limit_order(self, symbol, side, quantity, price):
        return {
            'success': True,
            'order_response': {
                'orderId': 87654321,
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'status': 'NEW',
                'executedQty': '0',
                'avgPrice': '0'
            },
            'message': f"Limit {side} order placed at {price}"
        }
    
    def mock_balance(self):
        return {
            'usdt_balance': 10000.0,
            'total_wallet_balance': 10000.0,
            'available_balance': 9500.0,
            'open_positions': [
                {
                    'symbol': 'BTCUSDT',
                    'side': 'LONG',
                    'size': '0.001',
                    'entry_price': '64000.00',
                    'unrealized_pnl': '25.50'
                }
            ]
        }


def main():
    print("🎮 DEMO MODE - No API credentials required")
    print("📝 This showcases the enhanced interactive CLI features")
    print("⚠️  Orders are simulated - no real trading occurs\n")
    
    demo = DemoCLI()
    demo.run_interactive_mode()


if __name__ == '__main__':
    main()
