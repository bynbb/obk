"""Command-line interface for obk."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

LOG_FILE = Path("obk.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
)


def _cmd_hello_world(_: argparse.Namespace) -> None:
    print("hello world")


def _cmd_divide(args: argparse.Namespace) -> None:
    """Divide two numbers and log the operation."""
    result = args.a / args.b
    logging.getLogger(__name__).info("Divide %s by %s = %s", args.a, args.b, result)
    print(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obk")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello_parser = subparsers.add_parser(
        "hello-world", help="Print hello world", description="Print hello world"
    )
    hello_parser.set_defaults(func=_cmd_hello_world)

    divide_parser = subparsers.add_parser(
        "divide",
        help="Divide two numbers",
        description="Divide a by b",
    )
    divide_parser.add_argument("a", type=float, help="Dividend")
    divide_parser.add_argument("b", type=float, help="Divisor")
    divide_parser.set_defaults(func=_cmd_divide)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
