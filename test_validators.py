#!/usr/bin/env python3
"""
Test script to demonstrate input validation functionality.
"""

import sys
import os

# Add the bot module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.validators import (
    ValidationError,
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_limit_order_params,
    validate_market_order_params
)


def test_validation():
    """Test various validation scenarios."""
    
    print("🧪 Testing Input Validation")
    print("=" * 50)
    
    # Test valid inputs
    print("\n✅ Testing Valid Inputs:")
    
    try:
        symbol = validate_symbol("btcusdt")
        print(f"Symbol: btcusdt -> {symbol}")
    except ValidationError as e:
        print(f"❌ Symbol validation failed: {e}")
    
    try:
        side = validate_side("buy")
        print(f"Side: buy -> {side}")
    except ValidationError as e:
        print(f"❌ Side validation failed: {e}")
    
    try:
        order_type = validate_order_type("market")
        print(f"Order Type: market -> {order_type}")
    except ValidationError as e:
        print(f"❌ Order type validation failed: {e}")
    
    try:
        quantity = validate_quantity("0.001")
        print(f"Quantity: 0.001 -> {quantity}")
    except ValidationError as e:
        print(f"❌ Quantity validation failed: {e}")
    
    try:
        price = validate_price("65000.50")
        print(f"Price: 65000.50 -> {price}")
    except ValidationError as e:
        print(f"❌ Price validation failed: {e}")
    
    # Test complete order validation
    try:
        market_params = validate_market_order_params("BTCUSDT", "BUY", "MARKET", "0.001")
        print(f"Market Order Params: {market_params}")
    except ValidationError as e:
        print(f"❌ Market order validation failed: {e}")
    
    try:
        limit_params = validate_limit_order_params("ETHUSDT", "SELL", "LIMIT", "0.01", "3500.00")
        print(f"Limit Order Params: {limit_params}")
    except ValidationError as e:
        print(f"❌ Limit order validation failed: {e}")
    
    # Test invalid inputs
    print("\n❌ Testing Invalid Inputs:")
    
    test_cases = [
        ("Invalid Symbol", lambda: validate_symbol("INVALID")),
        ("Invalid Side", lambda: validate_side("INVALID")),
        ("Invalid Order Type", lambda: validate_order_type("INVALID")),
        ("Invalid Quantity", lambda: validate_quantity("-0.001")),
        ("Invalid Price", lambda: validate_price("0")),
        ("Too Many Decimals", lambda: validate_quantity("0.123456789")),
    ]
    
    for test_name, test_func in test_cases:
        try:
            test_func()
            print(f"❌ {test_name}: Should have failed but didn't")
        except ValidationError as e:
            print(f"✅ {test_name}: Correctly rejected - {e}")
    
    print("\n🎉 Validation testing completed!")


if __name__ == '__main__':
    test_validation()
