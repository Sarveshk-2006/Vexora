from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from app.core.enums import PaymentRail


class BehaviorArchetype(str, Enum):
    """Legitimate behavioral archetypes for synthetic user activity simulation."""

    LOW_ACTIVITY = "LOW_ACTIVITY"
    REGULAR = "REGULAR"
    HIGH_ACTIVITY = "HIGH_ACTIVITY"
    BUSINESS = "BUSINESS"
    TRAVELER = "TRAVELER"
    NIGHT_OWL = "NIGHT_OWL"
    SUBSCRIPTION_HEAVY = "SUBSCRIPTION_HEAVY"
    DIGITAL_NATIVE = "DIGITAL_NATIVE"


@dataclass
class BehaviorProfile:
    """Simulation parameters defining a user's behavioral patterns."""

    archetype: BehaviorArchetype
    daily_tx_rate: float
    amount_log_mean: float
    amount_log_sigma: float
    active_hour_weights: List[float]
    merchant_category_weights: Dict[str, float]
    rail_weights: Dict[PaymentRail, float]
    device_reuse_prob: float = 0.90


def get_archetype_profiles() -> Dict[BehaviorArchetype, BehaviorProfile]:
    """Factory returning simulation profiles for all 8 behavioral archetypes."""
    # Standard diurnal hours (peak 9 AM - 9 PM)
    daytime_hours = [
        0.05,
        0.02,
        0.01,
        0.01,
        0.02,
        0.05,
        0.1,
        0.3,
        0.6,
        0.9,
        1.0,
        0.9,
        0.8,
        0.8,
        0.8,
        0.8,
        0.9,
        1.0,
        0.9,
        0.7,
        0.5,
        0.3,
        0.2,
        0.1,
    ]
    # Night owl diurnal hours (peak 8 PM - 3 AM)
    night_hours = [
        0.9,
        0.8,
        0.7,
        0.4,
        0.1,
        0.05,
        0.02,
        0.02,
        0.05,
        0.1,
        0.2,
        0.3,
        0.3,
        0.4,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.0,
        0.9,
        0.9,
    ]

    return {
        BehaviorArchetype.LOW_ACTIVITY: BehaviorProfile(
            archetype=BehaviorArchetype.LOW_ACTIVITY,
            daily_tx_rate=0.3,
            amount_log_mean=5.5,  # ~INR 250
            amount_log_sigma=0.6,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "GROCERY": 0.5,
                "UTILITIES": 0.3,
                "HEALTHCARE": 0.2,
            },
            rail_weights={
                PaymentRail.UPI: 0.6,
                PaymentRail.CARD: 0.3,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.98,
        ),
        BehaviorArchetype.REGULAR: BehaviorProfile(
            archetype=BehaviorArchetype.REGULAR,
            daily_tx_rate=1.2,
            amount_log_mean=6.2,  # ~INR 500
            amount_log_sigma=0.7,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "GROCERY": 0.35,
                "FOOD": 0.25,
                "ECOMMERCE": 0.2,
                "ENTERTAINMENT": 0.1,
                "UTILITIES": 0.1,
            },
            rail_weights={
                PaymentRail.UPI: 0.7,
                PaymentRail.CARD: 0.2,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.92,
        ),
        BehaviorArchetype.HIGH_ACTIVITY: BehaviorProfile(
            archetype=BehaviorArchetype.HIGH_ACTIVITY,
            daily_tx_rate=3.5,
            amount_log_mean=6.8,  # ~INR 900
            amount_log_sigma=0.8,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "FOOD": 0.3,
                "ECOMMERCE": 0.3,
                "SERVICES": 0.2,
                "ENTERTAINMENT": 0.1,
                "TRAVEL": 0.1,
            },
            rail_weights={
                PaymentRail.UPI: 0.5,
                PaymentRail.CARD: 0.4,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.88,
        ),
        BehaviorArchetype.BUSINESS: BehaviorProfile(
            archetype=BehaviorArchetype.BUSINESS,
            daily_tx_rate=5.0,
            amount_log_mean=8.5,  # ~INR 5000
            amount_log_sigma=1.0,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "SERVICES": 0.4,
                "ECOMMERCE": 0.3,
                "TRAVEL": 0.2,
                "UTILITIES": 0.1,
            },
            rail_weights={
                PaymentRail.CARD: 0.6,
                PaymentRail.UPI: 0.3,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.95,
        ),
        BehaviorArchetype.TRAVELER: BehaviorProfile(
            archetype=BehaviorArchetype.TRAVELER,
            daily_tx_rate=2.0,
            amount_log_mean=7.5,  # ~INR 1800
            amount_log_sigma=0.9,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "TRAVEL": 0.5,
                "FOOD": 0.3,
                "SERVICES": 0.1,
                "ENTERTAINMENT": 0.1,
            },
            rail_weights={
                PaymentRail.CARD: 0.5,
                PaymentRail.UPI: 0.4,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.85,
        ),
        BehaviorArchetype.NIGHT_OWL: BehaviorProfile(
            archetype=BehaviorArchetype.NIGHT_OWL,
            daily_tx_rate=1.5,
            amount_log_mean=6.4,  # ~INR 600
            amount_log_sigma=0.7,
            active_hour_weights=night_hours,
            merchant_category_weights={
                "FOOD": 0.4,
                "ENTERTAINMENT": 0.4,
                "ECOMMERCE": 0.2,
            },
            rail_weights={
                PaymentRail.UPI: 0.8,
                PaymentRail.WALLET: 0.15,
                PaymentRail.CARD: 0.05,
            },
            device_reuse_prob=0.94,
        ),
        BehaviorArchetype.SUBSCRIPTION_HEAVY: BehaviorProfile(
            archetype=BehaviorArchetype.SUBSCRIPTION_HEAVY,
            daily_tx_rate=0.8,
            amount_log_mean=5.8,  # ~INR 330
            amount_log_sigma=0.5,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "ENTERTAINMENT": 0.5,
                "UTILITIES": 0.3,
                "EDUCATION": 0.2,
            },
            rail_weights={
                PaymentRail.CARD: 0.5,
                PaymentRail.UPI: 0.4,
                PaymentRail.WALLET: 0.1,
            },
            device_reuse_prob=0.96,
        ),
        BehaviorArchetype.DIGITAL_NATIVE: BehaviorProfile(
            archetype=BehaviorArchetype.DIGITAL_NATIVE,
            daily_tx_rate=2.5,
            amount_log_mean=5.9,  # ~INR 360
            amount_log_sigma=0.6,
            active_hour_weights=daytime_hours,
            merchant_category_weights={
                "FOOD": 0.35,
                "ENTERTAINMENT": 0.35,
                "ECOMMERCE": 0.2,
                "SERVICES": 0.1,
            },
            rail_weights={
                PaymentRail.UPI: 0.85,
                PaymentRail.WALLET: 0.1,
                PaymentRail.CARD: 0.05,
            },
            device_reuse_prob=0.90,
        ),
    }
