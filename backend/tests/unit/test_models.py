import uuid
from decimal import Decimal

from app.core.enums import (
    AccountStatus,
    AccountType,
    DeviceType,
    MerchantStatus,
    RiskTier,
)
from app.models import Account, Device, Merchant, User


def test_user_orm_model_instantiation():
    """Verify User ORM model instantiation and default attributes."""
    user = User(
        synthetic_external_id="SYN_USER_000001",
        account_age=30,
        home_country="SYN_COUNTRY",
        home_region="SYN_REGION",
        home_city="SYN_CITY",
        timezone="UTC",
        risk_tier=RiskTier.LOW,
    )
    assert user.synthetic_external_id == "SYN_USER_000001"
    assert user.account_age == 30
    assert user.risk_tier == RiskTier.LOW
    assert user.home_country == "SYN_COUNTRY"


def test_account_orm_model_instantiation():
    """Verify Account ORM model instantiation and user relationship metadata."""
    user_id = uuid.uuid4()
    account = Account(
        user_id=user_id,
        account_type=AccountType.CONSUMER,
        status=AccountStatus.ACTIVE,
        account_age_days=100,
        synthetic_account_reference="SYN_ACC_000001",
        baseline_balance=Decimal("1500.50"),
    )
    assert account.user_id == user_id
    assert account.account_type == AccountType.CONSUMER
    assert account.status == AccountStatus.ACTIVE
    assert account.synthetic_account_reference == "SYN_ACC_000001"
    assert account.baseline_balance == Decimal("1500.50")


def test_device_orm_model_instantiation():
    """Verify Device ORM model instantiation."""
    device = Device(
        synthetic_device_id="SYN_DEV_000001",
        device_type=DeviceType.MOBILE,
        operating_system="iOS 17.4",
        trust_score=0.95,
        reputation_score=0.98,
    )
    assert device.synthetic_device_id == "SYN_DEV_000001"
    assert device.device_type == DeviceType.MOBILE
    assert device.operating_system == "iOS 17.4"
    assert device.trust_score == 0.95
    assert device.reputation_score == 0.98


def test_merchant_orm_model_instantiation():
    """Verify Merchant ORM model instantiation."""
    merchant = Merchant(
        synthetic_merchant_id="SYN_MERCH_000001",
        name="Synthetic Supermarket",
        category_code="5411",
        category_name="Grocery Stores",
        region="SYN_REGION",
        status=MerchantStatus.ACTIVE,
        risk_tier=RiskTier.LOW,
    )
    assert merchant.synthetic_merchant_id == "SYN_MERCH_000001"
    assert merchant.name == "Synthetic Supermarket"
    assert merchant.category_code == "5411"
    assert merchant.status == MerchantStatus.ACTIVE


def test_orm_relationship_metadata():
    """Verify ORM relationship definitions between User and Account."""
    user_mapper = User.__mapper__
    account_mapper = Account.__mapper__

    assert "accounts" in user_mapper.relationships
    assert "user" in account_mapper.relationships

    user_acc_rel = user_mapper.relationships["accounts"]
    assert user_acc_rel.target == Account.__table__

    acc_user_rel = account_mapper.relationships["user"]
    assert acc_user_rel.target == User.__table__


def test_unique_constraint_metadata():
    """Verify unique columns on User, Account, Device, Merchant."""
    assert User.__table__.columns["synthetic_external_id"].unique is True
    assert Account.__table__.columns["synthetic_account_reference"].unique is True
    assert Device.__table__.columns["synthetic_device_id"].unique is True
    assert Merchant.__table__.columns["synthetic_merchant_id"].unique is True
