from typing import Dict
from .client import BinanceFuturesClient
from .validators import ValidationError, validate_limit_order_params, validate_market_order_params
from .logging_config import setup_logging


class OrderManager:
    
    def __init__(self, client: BinanceFuturesClient):
        self.client = client
        self.logger = setup_logging()
    
    def place_market_order(self, symbol: str, side: str, quantity: str) -> Dict:
        try:
            params = validate_market_order_params(symbol, side, 'MARKET', quantity)
            
            self.logger.info(f"Market {params['side']} {params['quantity']} {params['symbol']}")
            response = self.client.place_order(
                symbol=params['symbol'],
                side=params['side'],
                order_type=params['type'],
                quantity=params['quantity']
            )
            
            return {
                'success': True,
                'order_response': response,
                'message': f"Market {params['side']} order placed"
            }
            
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            return {'success': False, 'error': str(e), 'message': f"Validation failed: {e}"}
        except Exception as e:
            self.logger.error(f"Order failed: {e}")
            return {'success': False, 'error': str(e), 'message': f"Order failed: {e}"}
    
    def place_limit_order(self, symbol: str, side: str, quantity: str, price: str) -> Dict:
        try:
            params = validate_limit_order_params(symbol, side, 'LIMIT', quantity, price)
            
            self.logger.info(f"Limit {params['side']} {params['quantity']} {params['symbol']} @ {params['price']}")
            response = self.client.place_order(
                symbol=params['symbol'],
                side=params['side'],
                order_type=params['type'],
                quantity=params['quantity'],
                price=params['price']
            )
            
            return {
                'success': True,
                'order_response': response,
                'message': f"Limit {params['side']} order placed at {params['price']}"
            }
            
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            return {'success': False, 'error': str(e), 'message': f"Validation failed: {e}"}
        except Exception as e:
            self.logger.error(f"Order failed: {e}")
            return {'success': False, 'error': str(e), 'message': f"Order failed: {e}"}
    
    def get_order_summary(self, order_response: Dict) -> str:
        if not order_response:
            return "No order response"
        
        order_id = order_response.get('orderId', 'N/A')
        symbol = order_response.get('symbol', 'N/A')
        side = order_response.get('side', 'N/A')
        order_type = order_response.get('type', 'N/A')
        quantity = order_response.get('origQty', 'N/A')
        price = order_response.get('price', 'N/A')
        status = order_response.get('status', 'N/A')
        executed_qty = order_response.get('executedQty', 'N/A')
        avg_price = order_response.get('avgPrice', 'N/A')
        
        return f"""
Order ID: {order_id}
Symbol: {symbol}
Side: {side}
Type: {order_type}
Quantity: {quantity}
Price: {price}
Status: {status}
Executed: {executed_qty}
Avg Price: {avg_price}
        """.strip()
    
    def check_account_balance(self) -> Dict:
        try:
            account_info = self.client.get_account_info()
            positions = self.client.get_position_info()
            
            usdt_balance = 0.0
            for asset in account_info.get('assets', []):
                if asset.get('asset') == 'USDT':
                    usdt_balance = float(asset.get('walletBalance', 0))
                    break
            
            open_positions = []
            for pos in positions:
                if float(pos.get('positionAmt', 0)) != 0:
                    open_positions.append({
                        'symbol': pos.get('symbol'),
                        'side': 'LONG' if float(pos.get('positionAmt', 0)) > 0 else 'SHORT',
                        'size': pos.get('positionAmt'),
                        'entry_price': pos.get('entryPrice'),
                        'unrealized_pnl': pos.get('unrealizedPnl')
                    })
            
            return {
                'usdt_balance': usdt_balance,
                'total_wallet_balance': float(account_info.get('totalWalletBalance', 0)),
                'available_balance': float(account_info.get('availableBalance', 0)),
                'open_positions': open_positions
            }
            
        except Exception as e:
            self.logger.error(f"Balance check failed: {e}")
            return {
                'error': str(e),
                'usdt_balance': 0,
                'total_wallet_balance': 0,
                'available_balance': 0,
                'open_positions': []
            }
