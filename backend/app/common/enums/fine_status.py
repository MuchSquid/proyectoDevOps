from enum import Enum


class FineStatus(str, Enum):
    """Estado de una multa."""

    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
