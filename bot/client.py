import os
import time
import hmac
import hashlib
import requests
from typing import Dict
from .logging_config import setup_logging


class BinanceFuturesClient:
    
    def __init__(self, api_key: str = None, api_secret: str = None, 
                 base_url: str = "https://testnet.binancefuture.com"):
        self.base_url = base_url
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.logger = setup_logging()
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials required")
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, 
                     signed: bool = False) -> Dict:
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
            params['signature'] = self._generate_signature(query_string)
        
        try:
            response = getattr(self.session, method.lower())(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            raise
    
    def get_server_time(self) -> Dict:
        return self._make_request('GET', '/fapi/v1/time')
    
    def get_account_info(self) -> Dict:
        return self._make_request('GET', '/fapi/v2/account', signed=True)
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None) -> Dict:
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': f"{quantity:.8f}".rstrip('0').rstrip('.')
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price required for LIMIT orders")
            params['price'] = f"{price:.8f}".rstrip('0').rstrip('.')
            params['timeInForce'] = 'GTC'
        
        return self._make_request('POST', '/fapi/v1/order', params, signed=True)
    
    def get_position_info(self, symbol: str = None) -> Dict:
        params = {'symbol': symbol} if symbol else {}
        return self._make_request('GET', '/fapi/v2/positionRisk', params, signed=True)
