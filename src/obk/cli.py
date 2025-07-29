"""Command-line interface for obk."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys


class ObkError(Exception):
    """Base error for the obk CLI."""


class DivisionByZeroError(ObkError):
    """Raised when attempting to divide by zero."""


class FatalError(ObkError):
    """Raised to trigger a fatal failure."""


LOG_FILE = Path("obk.log")


def configure_logging(log_file: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
    )


def _global_excepthook(exc_type, exc_value, exc_tb) -> None:
    if issubclass(exc_type, SystemExit):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    logging.getLogger(__name__).critical(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_tb)
    )
    print(
        "[FATAL] Unexpected error occurred. See the log for details.", file=sys.stderr
    )
    sys.exit(1)


sys.excepthook = _global_excepthook


def _cmd_hello_world(_: argparse.Namespace) -> None:
    print("hello world")


def _cmd_divide(args: argparse.Namespace) -> None:
    """Divide two numbers and log the operation."""
    if args.b == 0:
        raise DivisionByZeroError("cannot divide by zero")
    result = args.a / args.b
    logging.getLogger(__name__).info("Divide %s by %s = %s", args.a, args.b, result)
    print(result)


def _cmd_fail(_: argparse.Namespace) -> None:
    """Command that triggers a fatal error."""
    raise FatalError("intentional failure")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obk")
    parser.add_argument(
        "--logfile",
        type=Path,
        default=LOG_FILE,
        help="Path to the log file",
    )
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

    fail_parser = subparsers.add_parser(
        "fail",
        help="Trigger a fatal error",
        description="Trigger a fatal error",
    )
    fail_parser.set_defaults(func=_cmd_fail)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.logfile)
    try:
        args.func(args)
    except DivisionByZeroError as exc:
        logging.getLogger(__name__).exception("Division error")
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(2)
