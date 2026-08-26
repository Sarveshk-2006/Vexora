import uuid
from datetime import datetime, timedelta

from app.core.enums import SessionType
from app.digital_twin.behavior import BehaviorProfile
from app.digital_twin.seed import SeedManager
from app.models import Account, Device, Session, User

# RFC 5737 Documentation IPv4 Prefixes
RFC5737_PREFIXES = ["192.0.2", "198.51.100", "203.0.113"]


class SessionGenerator:
    """Deterministic Session synthetic interaction period generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) Safari/605.1",
        ]

    def generate_synthetic_ip(self) -> str:
        """Generate a valid RFC 5737 documentation synthetic IP address."""
        prefix = self.seed_mgr.choice(RFC5737_PREFIXES)
        host = self.seed_mgr.randint(1, 254)
        return f"{prefix}.{host}"

    def create_session(
        self,
        user: User,
        account: Account,
        device: Device,
        profile: BehaviorProfile,
        timestamp: datetime,
    ) -> Session:
        """Create a synthetic Session instance for a user interaction period."""
        duration_minutes = self.seed_mgr.randint(3, 45)
        ended_at = timestamp + timedelta(minutes=duration_minutes)

        session_type = self.seed_mgr.choices(
            [
                SessionType.PAYMENT,
                SessionType.BROWSING,
                SessionType.LOGIN,
                SessionType.MIXED,
            ],
            weights=[0.5, 0.25, 0.15, 0.10],
            k=1,
        )[0]

        prefix = self.seed_mgr.choice(RFC5737_PREFIXES)
        host = self.seed_mgr.randint(1, 254)
        ip = f"{prefix}.{host}"

        return Session(
            id=uuid.uuid4(),
            user_id=user.id,
            account_id=account.id,
            device_id=device.id,
            started_at=timestamp,
            ended_at=ended_at,
            session_type=session_type,
            location_country=user.home_country,
            location_region=user.home_region,
            location_city=user.home_city,
            synthetic_ip=ip,
            user_agent_family=self.seed_mgr.choice(self.user_agents),
        )
