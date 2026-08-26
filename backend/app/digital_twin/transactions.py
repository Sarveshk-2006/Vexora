import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from app.core.enums import (
    TransactionStatus,
    TransactionType,
)
from app.digital_twin.behavior import BehaviorProfile
from app.digital_twin.seed import SeedManager
from app.digital_twin.sessions import SessionGenerator
from app.models import (
    Account,
    Device,
    Merchant,
    PaymentAgent,
    Session,
    Transaction,
    User,
)


class TransactionGenerator:
    """Deterministic, relationally coherent synthetic Transaction generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr
        self.session_gen = SessionGenerator(seed_mgr)

    def generate_transactions(
        self,
        count: int,
        users: List[User],
        user_accounts: Dict[uuid.UUID, List[Account]],
        user_devices: Dict[uuid.UUID, List[Device]],
        user_profiles: Dict[uuid.UUID, BehaviorProfile],
        merchants: List[Merchant],
        agents: List[PaymentAgent],
        time_window_days: int,
    ) -> Tuple[List[Transaction], List[Session]]:
        """Generate relationally consistent benign synthetic transactions."""
        transactions: List[Transaction] = []
        sessions: List[Session] = []

        now_utc = datetime.now(timezone.utc)
        start_bound = now_utc - timedelta(days=time_window_days)

        # Pre-group merchants by category name for fast lookup
        merchant_by_cat: Dict[str, List[Merchant]] = {}
        for m in merchants:
            merchant_by_cat.setdefault(m.category_name, []).append(m)

        # Pre-calculate user selection weights based on daily_tx_rate
        user_weights = [user_profiles[u.id].daily_tx_rate for u in users]

        # Map user_id to active agent (if any)
        user_agents_map: Dict[uuid.UUID, List[PaymentAgent]] = {}
        for agent in agents:
            user_agents_map.setdefault(agent.owner_user_id, []).append(agent)

        for i in range(1, count + 1):
            tx_ref = f"SYN_TXN_{i:08d}"

            # 1. Select User & Profile
            user = self.seed_mgr.choices(users, weights=user_weights, k=1)[0]
            profile = user_profiles[user.id]

            # 2. Select Account (must belong to user)
            accounts = user_accounts[user.id]
            account = self.seed_mgr.choice(accounts)

            # 3. Select Device (primary device continuity)
            devices = user_devices[user.id]
            if (
                len(devices) == 1
                or self.seed_mgr.uniform(0, 1) <= profile.device_reuse_prob
            ):
                device = devices[0]
            else:
                device = self.seed_mgr.choice(devices[1:])

            # 4. Temporal Sampling (Day + Diurnal Hour)
            day_offset = self.seed_mgr.randint(0, max(0, time_window_days - 1))
            hour = self.seed_mgr.choices(
                list(range(24)), weights=profile.active_hour_weights, k=1
            )[0]
            minute = self.seed_mgr.randint(0, 59)
            second = self.seed_mgr.randint(0, 59)

            tx_timestamp = start_bound + timedelta(
                days=day_offset, hours=hour, minutes=minute, seconds=second
            )

            # 5. Session Reuse or Creation
            # 70% of transactions reuse/start a Session
            session: Optional[Session] = None
            if self.seed_mgr.uniform(0, 1) < 0.70:
                session = self.session_gen.create_session(
                    user=user,
                    account=account,
                    device=device,
                    profile=profile,
                    timestamp=tx_timestamp,
                )
                sessions.append(session)

            # 6. Merchant Selection
            cat_weights = profile.merchant_category_weights
            cats = list(cat_weights.keys())
            weights = list(cat_weights.values())

            chosen_cat = self.seed_mgr.choices(cats, weights=weights, k=1)[0]
            candidate_merchants = merchant_by_cat.get(chosen_cat, merchants)
            merchant = self.seed_mgr.choice(candidate_merchants)

            # 7. Payment Rail Selection
            rails = list(profile.rail_weights.keys())
            r_weights = list(profile.rail_weights.values())
            payment_rail = self.seed_mgr.choices(rails, weights=r_weights, k=1)[0]

            # 8. Payment Agent (Rare, 5% of txs for agent owners)
            payment_agent: Optional[PaymentAgent] = None
            if user.id in user_agents_map and self.seed_mgr.uniform(0, 1) < 0.20:
                payment_agent = self.seed_mgr.choice(user_agents_map[user.id])

            # 9. Amount Sampling (Log-Normal Distribution)
            raw_amount = self.seed_mgr.lognormal(
                profile.amount_log_mean, profile.amount_log_sigma
            )
            amount = Decimal(str(max(1.00, round(raw_amount, 2))))

            # 10. Status & Type
            tx_status = self.seed_mgr.choices(
                [
                    TransactionStatus.APPROVED,
                    TransactionStatus.DECLINED,
                    TransactionStatus.PENDING,
                    TransactionStatus.REVERSED,
                    TransactionStatus.REFUNDED,
                ],
                weights=[0.95, 0.03, 0.01, 0.006, 0.004],
                k=1,
            )[0]

            tx_type = self.seed_mgr.choices(
                [
                    TransactionType.PURCHASE,
                    TransactionType.TRANSFER,
                    TransactionType.BILL_PAYMENT,
                    TransactionType.SUBSCRIPTION,
                ],
                weights=[0.70, 0.15, 0.10, 0.05],
                k=1,
            )[0]

            synthetic_ip = (
                session.synthetic_ip
                if session
                else self.session_gen.generate_synthetic_ip()
            )

            tx = Transaction(
                id=uuid.uuid4(),
                transaction_reference=tx_ref,
                account_id=account.id,
                user_id=user.id,
                merchant_id=merchant.id,
                device_id=device.id,
                session_id=session.id if session else None,
                payment_rail=payment_rail,
                payment_agent_id=payment_agent.id if payment_agent else None,
                timestamp=tx_timestamp,
                amount=amount,
                currency="INR",
                transaction_status=tx_status,
                transaction_type=tx_type,
                location_country=user.home_country,
                location_region=user.home_region,
                location_city=user.home_city,
                synthetic_ip=synthetic_ip,
                metadata_json={
                    "archetype": profile.archetype.value,
                    "dataset_type": "BENIGN",
                    "simulation_batch": 1,
                },
            )
            transactions.append(tx)

        return transactions, sessions
