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


class PaymentRail(str, Enum):
    """Supported payment rail types."""

    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"


class SessionType(str, Enum):
    """Synthetic user interaction session type."""

    LOGIN = "LOGIN"
    PAYMENT = "PAYMENT"
    BROWSING = "BROWSING"
    MIXED = "MIXED"


class TransactionStatus(str, Enum):
    """Synthetic transaction execution status."""

    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    REVERSED = "REVERSED"
    REFUNDED = "REFUNDED"
    PENDING = "PENDING"


class TransactionType(str, Enum):
    """Synthetic payment transaction behavioral category."""

    PURCHASE = "PURCHASE"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    SUBSCRIPTION = "SUBSCRIPTION"
    WITHDRAWAL = "WITHDRAWAL"
    OTHER = "OTHER"


class AgentType(str, Enum):
    """Synthetic autonomous payment agent category."""

    PERSONAL_ASSISTANT = "PERSONAL_ASSISTANT"
    SHOPPING_AGENT = "SHOPPING_AGENT"
    BILLING_AGENT = "BILLING_AGENT"
    SUBSCRIPTION_AGENT = "SUBSCRIPTION_AGENT"
    OTHER = "OTHER"


class AgentStatus(str, Enum):
    """Synthetic payment agent operational status."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"


# Phase 2C Enums: Threat Intelligence & Fraud Genome Taxonomies
class AttackFamily(str, Enum):
    """Core synthetic payment fraud attack family categories."""

    ACCOUNT_TAKEOVER = "ACCOUNT_TAKEOVER"
    SYNTHETIC_IDENTITY = "SYNTHETIC_IDENTITY"
    DEVICE_MIMICRY = "DEVICE_MIMICRY"
    BEHAVIORAL_MIMICRY = "BEHAVIORAL_MIMICRY"
    AMOUNT_FRAGMENTATION = "AMOUNT_FRAGMENTATION"
    VELOCITY_MANIPULATION = "VELOCITY_MANIPULATION"
    MERCHANT_HOPPING = "MERCHANT_HOPPING"
    COORDINATED_NETWORK = "COORDINATED_NETWORK"
    MULE_NETWORK = "MULE_NETWORK"
    CROSS_RAIL = "CROSS_RAIL"
    MICROTRANSACTION_PROBING = "MICROTRANSACTION_PROBING"
    ADAPTIVE_EVASION = "ADAPTIVE_EVASION"
    AGENTIC_PAYMENT_ABUSE = "AGENTIC_PAYMENT_ABUSE"


class ThreatSeverity(str, Enum):
    """Threat severity classification."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatStatus(str, Enum):
    """Threat taxonomy status."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class CampaignStatus(str, Enum):
    """Synthetic attack campaign execution status."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"


class AttackGenerationStatus(str, Enum):
    """Attack generation evolutionary state."""

    INITIAL = "INITIAL"
    MUTATED = "MUTATED"
    EVALUATED = "EVALUATED"
    ARCHIVED = "ARCHIVED"


# Fraud Genome Dimension Enums
class IdentityState(str, Enum):
    """Genome dimension 3: Identity compromise state."""

    NORMAL = "NORMAL"
    COMPROMISED = "COMPROMISED"
    SYNTHETIC = "SYNTHETIC"
    HIJACKED = "HIJACKED"
    UNKNOWN = "UNKNOWN"


class DeviceStrategy(str, Enum):
    """Genome dimension 4: Device strategy."""

    KNOWN_DEVICE = "KNOWN_DEVICE"
    NEW_DEVICE = "NEW_DEVICE"
    DEVICE_MIMICRY = "DEVICE_MIMICRY"
    DEVICE_ROTATION = "DEVICE_ROTATION"
    SHARED_DEVICE = "SHARED_DEVICE"
    UNKNOWN = "UNKNOWN"


class LocationStrategy(str, Enum):
    """Genome dimension 5: Location strategy."""

    NORMAL = "NORMAL"
    FAMILIAR = "FAMILIAR"
    NOVEL = "NOVEL"
    RAPID_SHIFT = "RAPID_SHIFT"
    DISTRIBUTED = "DISTRIBUTED"


class AmountPattern(str, Enum):
    """Genome dimension 6: Amount pattern."""

    NORMAL = "NORMAL"
    SPIKE = "SPIKE"
    FRAGMENTED = "FRAGMENTED"
    MICROTRANSACTION = "MICROTRANSACTION"
    GRADUAL_ESCALATION = "GRADUAL_ESCALATION"
    DISTRIBUTED = "DISTRIBUTED"


class VelocityPattern(str, Enum):
    """Genome dimension 7: Velocity pattern."""

    NORMAL = "NORMAL"
    LOW_AND_SLOW = "LOW_AND_SLOW"
    BURST = "BURST"
    GRADUAL_INCREASE = "GRADUAL_INCREASE"
    HIGH_VELOCITY = "HIGH_VELOCITY"
    DISTRIBUTED = "DISTRIBUTED"


class TimingPattern(str, Enum):
    """Genome dimension 8: Timing pattern."""

    NORMAL = "NORMAL"
    OFF_HOURS = "OFF_HOURS"
    PERIODIC = "PERIODIC"
    RANDOMIZED = "RANDOMIZED"
    CAMPAIGN_ALIGNED = "CAMPAIGN_ALIGNED"


class MerchantStrategy(str, Enum):
    """Genome dimension 9: Merchant selection strategy."""

    FAMILIAR = "FAMILIAR"
    NOVEL = "NOVEL"
    HOPPING = "HOPPING"
    CONCENTRATED = "CONCENTRATED"
    DISTRIBUTED = "DISTRIBUTED"


class NetworkCoordination(str, Enum):
    """Genome dimension 11: Network coordination level."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    COORDINATED = "COORDINATED"


class EvasionStrategy(str, Enum):
    """Genome dimension 13: Evasion technique strategy."""

    NONE = "NONE"
    BEHAVIORAL_MIMICRY = "BEHAVIORAL_MIMICRY"
    FEATURE_AVOIDANCE = "FEATURE_AVOIDANCE"
    DISTRIBUTION_MIMICRY = "DISTRIBUTION_MIMICRY"
    VELOCITY_MANIPULATION = "VELOCITY_MANIPULATION"
    MULTI_VECTOR = "MULTI_VECTOR"
