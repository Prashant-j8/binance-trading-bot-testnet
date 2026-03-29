# Binance Futures Testnet Trading Bot

A small Python CLI application that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)** using direct REST calls.

## Features

- Places **MARKET** and **LIMIT** orders
- Supports both **BUY** and **SELL**
- Validates CLI input before making requests
- Separates concerns into:
  - API client layer
  - order service layer
  - validation layer
  - CLI layer
- Logs requests, responses, and errors to a log file
- Handles invalid input, Binance API errors, and network failures

## Project Structure

```text
binance_testnet_bot/
  bot/
    __init__.py
    client.py
    exceptions.py
    logging_config.py
    orders.py
    validators.py
  logs/
    market_order.example.log
    limit_order.example.log
  cli.py
  README.md
  requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export Binance Futures Testnet credentials:

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

On Windows PowerShell:

```powershell
$env:BINANCE_API_KEY="your_testnet_api_key"
$env:BINANCE_API_SECRET="your_testnet_api_secret"
```

## Base URL

This app is configured to use:

```text
https://testnet.binancefuture.com
```

## How to Run

### MARKET order example

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### LIMIT order example

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 90000
```

### Custom log file example

```bash
python cli.py --symbol ETHUSDT --side BUY --order-type MARKET --quantity 0.01 --log-file logs/eth_market.log
```

## Expected Output

The CLI prints:

- order request summary
- order response details
- success or failure message

Example output:

```text
=== ORDER REQUEST SUMMARY ===
Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.001

=== ORDER RESPONSE ===
Order ID     : 123456789
Status       : FILLED
Executed Qty : 0.001
Avg Price    : 85750.10
Symbol       : BTCUSDT
Side         : BUY
Type         : MARKET

SUCCESS: Order placed successfully on Binance Futures Testnet.
```

## Assumptions

- The account is already activated on Binance Futures Testnet.
- API keys have permission to trade on testnet.
- The symbol exists on Binance USDT-M Futures Testnet.
- LIMIT orders use `GTC` by default.
- `newOrderRespType=RESULT` is used so the response includes useful execution details when available.

## Notes About Included Logs

The repository includes **illustrative sample logs** in `logs/market_order.example.log` and `logs/limit_order.example.log` to demonstrate format and logging quality.

To generate **real submission logs**, run the commands on your own Binance Futures Testnet account and attach the generated `logs/trading_bot.log` (or custom log files) in your application email.

## Suggested Submission Steps

1. Push this project to a public GitHub repository.
2. Run one MARKET order and one LIMIT order using your own testnet credentials.
3. Attach the real generated log files.
4. Email your resume + GitHub link + log files.

## Why direct REST instead of python-binance?

Using direct REST calls makes the signing flow, request structure, and error handling explicit, which is useful in a take-home task focused on API design, validation, and logging.
