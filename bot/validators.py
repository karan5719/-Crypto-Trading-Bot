import re
from typing import Dict


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.strip().upper()
    if not re.match(r'^[A-Z]+USDT$', symbol):
        raise ValidationError(f"Invalid symbol: {symbol}. Use format like BTCUSDT")
    
    return symbol


def validate_side(side: str) -> str:
    if not side:
        raise ValidationError("Side cannot be empty")
    
    side = side.strip().upper()
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL")
    
    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValidationError("Order type cannot be empty")
    
    order_type = order_type.strip().upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
    
    return order_type


def validate_quantity(quantity: str) -> float:
    if not quantity:
        raise ValidationError("Quantity cannot be empty")
    
    try:
        qty = float(quantity.strip())
    except ValueError:
        raise ValidationError(f"Invalid quantity: {quantity}")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive: {qty}")
    
    if abs(qty - round(qty, 8)) > 0:
        raise ValidationError(f"Too many decimals: {quantity}. Max 8")
    
    return qty


def validate_price(price: str) -> float:
    if not price:
        raise ValidationError("Price cannot be empty")
    
    try:
        prc = float(price.strip())
    except ValueError:
        raise ValidationError(f"Invalid price: {price}")
    
    if prc <= 0:
        raise ValidationError(f"Price must be positive: {prc}")
    
    if abs(prc - round(prc, 8)) > 0:
        raise ValidationError(f"Too many decimals: {price}. Max 8")
    
    return prc


def validate_limit_order_params(symbol: str, side: str, order_type: str, 
                               quantity: str, price: str) -> Dict:
    return {
        'symbol': validate_symbol(symbol),
        'side': validate_side(side),
        'type': validate_order_type(order_type),
        'quantity': validate_quantity(quantity),
        'price': validate_price(price)
    }


def validate_market_order_params(symbol: str, side: str, order_type: str, 
                                quantity: str) -> Dict:
    return {
        'symbol': validate_symbol(symbol),
        'side': validate_side(side),
        'type': validate_order_type(order_type),
        'quantity': validate_quantity(quantity)
    }
