from enum import Enum


class AccountStatus(str, Enum):
    """Synthetic account lifecycle status."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


class AccountType(str, Enum):
    """Financial account category."""

    CONSUMER = "CONSUMER"
    BUSINESS = "BUSINESS"


class DeviceType(str, Enum):
    """Synthetic device form factor."""

    MOBILE = "MOBILE"
    DESKTOP = "DESKTOP"
    TABLET = "TABLET"
    OTHER = "OTHER"


class MerchantStatus(str, Enum):
    """Synthetic merchant operational status."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


class RiskTier(str, Enum):
    """Entity or transaction risk classification tier."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
