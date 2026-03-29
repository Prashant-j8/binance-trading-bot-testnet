from __future__ import annotations

import argparse
import sys
from typing import Any

from bot.client import BinanceFuturesTestnetClient
from bot.exceptions import BinanceAPIError, NetworkError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import OrderService
from bot.validators import validate_order_inputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price", help="Price for LIMIT orders")
    parser.add_argument("--log-file", default="logs/trading_bot.log", help="Path to log file")
    return parser


def print_summary(validated: dict[str, str]) -> None:
    print("\n=== ORDER REQUEST SUMMARY ===")
    print(f"Symbol     : {validated['symbol']}")
    print(f"Side       : {validated['side']}")
    print(f"Order Type : {validated['order_type']}")
    print(f"Quantity   : {validated['quantity']}")
    if validated.get("price"):
        print(f"Price      : {validated['price']}")



def print_response(response: dict[str, Any]) -> None:
    print("\n=== ORDER RESPONSE ===")
    print(f"Order ID     : {response.get('orderId', 'N/A')}")
    print(f"Status       : {response.get('status', 'N/A')}")
    print(f"Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
    print(f"Symbol       : {response.get('symbol', 'N/A')}")
    print(f"Side         : {response.get('side', 'N/A')}")
    print(f"Type         : {response.get('type', 'N/A')}")



def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging(args.log_file)

    try:
        validated = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print_summary(validated)

        client = BinanceFuturesTestnetClient(logger=logger)
        service = OrderService(client)
        response = service.place_order(validated)
        print_response(response)
        print("\nSUCCESS: Order placed successfully on Binance Futures Testnet.")
        return 0

    except ValidationError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"\nFAILED: Validation error -> {exc}")
        return 2
    except NetworkError as exc:
        logger.error("Network failure: %s", exc)
        print(f"\nFAILED: Network error -> {exc}")
        return 3
    except BinanceAPIError as exc:
        logger.error("Binance API failure: %s", exc)
        print(f"\nFAILED: API error -> {exc}")
        return 4
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"\nFAILED: Unexpected error -> {exc}")
        return 99


if __name__ == "__main__":
    sys.exit(main())
