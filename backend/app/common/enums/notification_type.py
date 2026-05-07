from enum import Enum


class NotificationType(str, Enum):
    """Tipo de notificación del sistema."""

    LOAN = "LOAN"
    RESERVATION = "RESERVATION"
    FINE = "FINE"
    SYSTEM = "SYSTEM"
