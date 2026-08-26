import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

from app.core.enums import DeviceType
from app.digital_twin.seed import SeedManager
from app.models import Device, User


class DeviceGenerator:
    """Deterministic Device synthetic population generator."""

    def __init__(self, seed_mgr: SeedManager):
        self.seed_mgr = seed_mgr
        self.operating_systems = [
            "Android 14",
            "iOS 17.4",
            "Windows 11",
            "macOS Sonoma",
            "Linux Ubuntu",
        ]

    def generate_devices(
        self, users: List[User], target_device_count: int
    ) -> Tuple[List[Device], Dict[uuid.UUID, List[Device]]]:
        """Generate synthetic Device entities associated with users."""
        devices: List[Device] = []
        user_devices: Dict[uuid.UUID, List[Device]] = {}

        now_utc = datetime.now(timezone.utc)
        device_seq_id = 1

        # Step 1: Assign at least 1 primary device to each user
        for user in users:
            dev_id = uuid.uuid4()
            dev_ref = f"SYN_DEV_{device_seq_id:06d}"
            device_seq_id += 1

            first_seen = now_utc - timedelta(days=user.account_age)
            trust_score = round(self.seed_mgr.uniform(0.85, 1.0), 2)
            rep_score = round(self.seed_mgr.uniform(0.90, 1.0), 2)

            device = Device(
                id=dev_id,
                synthetic_device_id=dev_ref,
                device_type=self.seed_mgr.choice(
                    [DeviceType.MOBILE, DeviceType.DESKTOP, DeviceType.TABLET]
                ),
                operating_system=self.seed_mgr.choice(self.operating_systems),
                first_seen_at=first_seen,
                last_seen_at=now_utc,
                trust_score=trust_score,
                reputation_score=rep_score,
            )
            devices.append(device)
            user_devices[user.id] = [device]

        # Step 2: Distribute remaining secondary devices across users
        remaining_count = max(0, target_device_count - len(users))
        for _ in range(remaining_count):
            user = self.seed_mgr.choice(users)
            dev_id = uuid.uuid4()
            dev_ref = f"SYN_DEV_{device_seq_id:06d}"
            device_seq_id += 1

            first_seen = now_utc - timedelta(
                days=self.seed_mgr.randint(1, user.account_age)
            )
            trust_score = round(self.seed_mgr.uniform(0.50, 0.95), 2)
            rep_score = round(self.seed_mgr.uniform(0.60, 0.95), 2)

            device = Device(
                id=dev_id,
                synthetic_device_id=dev_ref,
                device_type=self.seed_mgr.choice(list(DeviceType)),
                operating_system=self.seed_mgr.choice(self.operating_systems),
                first_seen_at=first_seen,
                last_seen_at=now_utc,
                trust_score=trust_score,
                reputation_score=rep_score,
            )
            devices.append(device)
            user_devices[user.id].append(device)

        return devices, user_devices
