import uuid
from typing import Dict, List, Tuple

from app.core.enums import MerchantStatus, RiskTier
from app.digital_twin.seed import SeedManager
from app.models import Merchant

MCC_MAP: Dict[str, Tuple[str, str]] = {
    "GROCERY": ("5411", "Grocery Stores and Supermarkets"),
    "FOOD": ("5812", "Eating Places and Restaurants"),
    "TRAVEL": ("4722", "Travel Agencies and Tour Operators"),
    "ENTERTAINMENT": ("7832", "Motion Picture Theaters"),
    "UTILITIES": ("4900", "Electric, Gas, Sanitary and Water Utilities"),
    "ECOMMERCE": ("5311", "Department Stores / Online Retail"),
    "HEALTHCARE": ("8099", "Health and Medical Services"),
    "EDUCATION": ("8299", "Schools and Educational Services"),
    "SERVICES": ("7299", "Miscellaneous Personal Services"),
    "OTHER": ("5999", "Miscellaneous Specialty Retail"),
}


class MerchantGenerator:
    """Deterministic Merchant synthetic population generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr
        self.regions = ["SYN_NORTH", "SYN_SOUTH", "SYN_EAST", "SYN_WEST", "SYN_CENTRAL"]

    def generate_merchants(self, count: int) -> List[Merchant]:
        """Generate N synthetic Merchant entities with realistic MCC categories."""
        merchants: List[Merchant] = []
        categories = list(MCC_MAP.keys())

        for i in range(1, count + 1):
            category_name = self.seed_mgr.choice(categories)
            mcc_code, mcc_desc = MCC_MAP[category_name]
            merch_ref = f"SYN_MERCH_{i:06d}"

            risk_tier = self.seed_mgr.choices(
                [RiskTier.LOW, RiskTier.MEDIUM, RiskTier.HIGH],
                weights=[0.85, 0.12, 0.03],
                k=1,
            )[0]

            merchant = Merchant(
                id=uuid.uuid4(),
                synthetic_merchant_id=merch_ref,
                name=f"Synthetic {category_name.capitalize()} Store #{i}",
                category_code=mcc_code,
                category_name=category_name,
                region=self.seed_mgr.choice(self.regions),
                status=MerchantStatus.ACTIVE,
                risk_tier=risk_tier,
            )
            merchants.append(merchant)

        return merchants
