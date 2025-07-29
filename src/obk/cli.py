"""Command-line interface for obk."""

from __future__ import annotations

import argparse


def _cmd_hello_world(_: argparse.Namespace) -> None:
    print("hello world")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obk")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello_parser = subparsers.add_parser(
        "hello-world", help="Print hello world", description="Print hello world"
    )
    hello_parser.set_defaults(func=_cmd_hello_world)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
