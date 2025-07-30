"""Command-line interface for obk using classes."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .containers import Container
from .services import DivisionByZeroError, FatalError


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


class ObkCLI:
    """Class-based CLI implementation using dependency injection."""

    def __init__(self, log_file: Path = LOG_FILE, container: Container | None = None) -> None:
        self.container = container or Container()
        self.container.config.log_file.from_value(log_file)
        self.log_file = log_file

    # command implementations -------------------------------------------------
    def _cmd_hello_world(self, _: argparse.Namespace) -> None:
        greeter = self.container.greeter()
        print(greeter.hello())

    def _cmd_divide(self, args: argparse.Namespace) -> None:
        divider = self.container.divider()
        result = divider.divide(args.a, args.b)
        logging.getLogger(__name__).info(
            "Divide %s by %s = %s", args.a, args.b, result
        )
        print(result)

    def _cmd_fail(self, _: argparse.Namespace) -> None:
        raise FatalError("intentional failure")

    # parser / runner ---------------------------------------------------------
    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="obk")
        parser.add_argument(
            "--logfile",
            type=Path,
            default=self.log_file,
            help="Path to the log file",
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        hello_parser = subparsers.add_parser(
            "hello-world", help="Print hello world", description="Print hello world"
        )
        hello_parser.set_defaults(func=self._cmd_hello_world)

        divide_parser = subparsers.add_parser(
            "divide",
            help="Divide two numbers",
            description="Divide a by b",
        )
        divide_parser.add_argument("a", type=float, help="Dividend")
        divide_parser.add_argument("b", type=float, help="Divisor")
        divide_parser.set_defaults(func=self._cmd_divide)

        fail_parser = subparsers.add_parser(
            "fail",
            help="Trigger a fatal error",
            description="Trigger a fatal error",
        )
        fail_parser.set_defaults(func=self._cmd_fail)
        return parser

    def run(self, argv: list[str] | None = None) -> None:
        parser = self.build_parser()
        args = parser.parse_args(argv)
        self.container.config.log_file.from_value(args.logfile)
        configure_logging(self.container.config.log_file())
        try:
            args.func(args)
        except DivisionByZeroError as exc:
            logging.getLogger(__name__).exception("Division error")
            print(f"[ERROR] {exc}", file=sys.stderr)
            sys.exit(2)


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m obk``."""
    ObkCLI().run(argv)
