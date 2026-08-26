import uuid
from decimal import Decimal
from typing import Dict, List, Tuple

from app.core.enums import AccountStatus, AccountType, RiskTier
from app.digital_twin.behavior import (
    BehaviorArchetype,
    BehaviorProfile,
    get_archetype_profiles,
)
from app.digital_twin.seed import SeedManager
from app.models import Account, User


class PopulationGenerator:
    """Deterministic User & Account synthetic population generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr
        self.archetype_profiles = get_archetype_profiles()
        self.countries = ["SYN_INDIA", "SYN_US", "SYN_UK", "SYN_SINGAPORE"]
        self.regions = ["SYN_NORTH", "SYN_SOUTH", "SYN_EAST", "SYN_WEST", "SYN_CENTRAL"]
        self.cities = ["SYN_METRO_A", "SYN_METRO_B", "SYN_CITY_C", "SYN_TOWN_D"]
        self.timezones = ["Asia/Kolkata", "UTC", "America/New_York", "Europe/London"]

    def generate_population(
        self, count: int
    ) -> Tuple[List[User], List[Account], Dict[uuid.UUID, BehaviorProfile]]:
        """Generate N synthetic Users, associated Accounts, and behavioral profiles."""
        users: List[User] = []
        accounts: List[Account] = []
        user_profiles: Dict[uuid.UUID, BehaviorProfile] = {}

        archetype_list = list(BehaviorArchetype)
        account_seq_id = 1

        for i in range(1, count + 1):
            user_id = uuid.uuid4()
            ref = f"SYN_USER_{i:06d}"
            archetype = self.seed_mgr.choice(archetype_list)
            profile = self.archetype_profiles[archetype]

            risk_tier = self.seed_mgr.choices(
                [RiskTier.LOW, RiskTier.MEDIUM, RiskTier.HIGH],
                weights=[0.85, 0.12, 0.03],
                k=1,
            )[0]

            user = User(
                id=user_id,
                synthetic_external_id=ref,
                account_age=self.seed_mgr.randint(30, 1800),
                home_country=self.seed_mgr.choice(self.countries),
                home_region=self.seed_mgr.choice(self.regions),
                home_city=self.seed_mgr.choice(self.cities),
                timezone=self.seed_mgr.choice(self.timezones),
                risk_tier=risk_tier,
            )
            users.append(user)
            user_profiles[user_id] = profile

            # Generate 1 to 2 accounts per user
            num_accounts = 1 if self.seed_mgr.uniform(0, 1) < 0.85 else 2
            for _ in range(num_accounts):
                acc_id = uuid.uuid4()
                acc_ref = f"SYN_ACC_{account_seq_id:06d}"
                account_seq_id += 1

                bal = round(self.seed_mgr.lognormal(8.0, 1.0), 2)  # ~3,000 baseline
                account = Account(
                    id=acc_id,
                    user_id=user_id,
                    account_type=(
                        AccountType.CONSUMER
                        if profile.archetype != BehaviorArchetype.BUSINESS
                        else AccountType.BUSINESS
                    ),
                    status=AccountStatus.ACTIVE,
                    account_age_days=user.account_age,
                    synthetic_account_reference=acc_ref,
                    baseline_balance=Decimal(str(bal)),
                )
                accounts.append(account)

        return users, accounts, user_profiles
