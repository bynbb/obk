"""Service classes for the obk CLI."""

from __future__ import annotations

class ObkError(Exception):
    """Base error for the obk CLI."""

class DivisionByZeroError(ObkError):
    """Raised when attempting to divide by zero."""

class FatalError(ObkError):
    """Raised to trigger a fatal failure."""

class Greeter:
    """Simple greeter service."""

    def hello(self) -> str:
        return "hello world"

class Divider:
    """Divider service."""

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("cannot divide by zero")
        return a / b
