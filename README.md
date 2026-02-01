# Binance Futures Trading Bot (Testnet)

A Python trading bot for placing orders on Binance Futures Testnet with enhanced interactive CLI.

## Features

- Place MARKET and LIMIT orders on Binance Futures Testnet
- Support both BUY and SELL orders
- Interactive CLI mode with menus and prompts
- Quick command mode for advanced users
- Input validation with error handling
- Structured logging to files and console
- Account balance and position information

## Setup

### Prerequisites

- Python 3.7+
- Binance Futures Testnet account
- API credentials from Binance Testnet

### Installation

```bash
cd trading_bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

```bash
export BINANCE_API_KEY='your_testnet_api_key'
export BINANCE_API_SECRET='your_testnet_api_secret'
```

## Usage

### Interactive Mode (Recommended)
```bash
python cli.py
```

### Quick Commands
```bash
# Market order
python cli.py market BTCUSDT BUY 0.001

# Limit order
python cli.py limit BTCUSDT SELL 0.001 65000.50

# Check balance
python cli.py balance

# Server time
python cli.py time
```

### Demo Mode
```bash
python demo_interactive.py
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance API client wrapper
│   ├── orders.py            # Order management logic
│   ├── validators.py        # Input validation
│   └── logging_config.py    # Logging configuration
├── cli.py                   # CLI entry point
├── demo_interactive.py      # Demo mode without API keys
├── requirements.txt         # Dependencies
└── README.md
```

## Dependencies

- `requests>=2.31.0` - HTTP client for API calls
- `python-dotenv>=1.0.0` - Environment variable management

## Security Notes

- Never commit API keys to version control
- Use environment variables for credentials
- Only use Testnet API keys (not mainnet)
- This bot only works with Binance Futures Testnet

## License

Educational and testing purposes only. Use at your own risk.
