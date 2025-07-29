"""Command-line interface for obk."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


class ObkError(Exception):
    """Base exception for the obk CLI."""


class CalculationError(ObkError):
    """Raised when a calculation cannot be performed."""



def _cmd_hello_world(_: argparse.Namespace) -> None:
    print("hello world")


def _cmd_divide(args: argparse.Namespace) -> None:
    if args.b == 0:
        raise CalculationError("Cannot divide by zero")
    result = args.a / args.b
    print(result)


def _cmd_fail(_: argparse.Namespace) -> None:
    raise RuntimeError("boom")



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obk")
    parser.add_argument(
        "--logfile",
        type=Path,
        default=Path("obk.log"),
        help="Path to log file",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello_parser = subparsers.add_parser(
        "hello-world", help="Print hello world", description="Print hello world"
    )
    hello_parser.set_defaults(func=_cmd_hello_world)

    divide_parser = subparsers.add_parser(
        "divide", help="Divide two numbers", description="Divide A by B"
    )
    divide_parser.add_argument("a", type=float)
    divide_parser.add_argument("b", type=float)
    divide_parser.set_defaults(func=_cmd_divide)

    fail_parser = subparsers.add_parser(
        "fail", help="Trigger an unhandled exception", description="Fail hard"
    )
    fail_parser.set_defaults(func=_cmd_fail)

    return parser


def _setup_logging(logfile: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def _global_excepthook(exc_type, exc_value, exc_tb) -> None:
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_tb))
    print("[FATAL] Unexpected crash, see log", file=sys.stderr)
    sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    sys.excepthook = _global_excepthook
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.logfile)
    try:
        args.func(args)
    except ObkError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        logging.getLogger(__name__).exception("Domain error")
        sys.exit(2)
