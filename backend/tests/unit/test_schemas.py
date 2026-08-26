import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.core.enums import (
    AccountStatus,
    AccountType,
    DeviceType,
    MerchantStatus,
    RiskTier,
)
from app.schemas import (
    AccountCreate,
    DeviceCreate,
    MerchantCreate,
    UserCreate,
)


def test_valid_user_schema():
    """Test valid UserCreate schema validation."""
    user_data = UserCreate(
        synthetic_external_id="SYN_USER_000001",
        account_age=45,
        home_country="SYN_COUNTRY",
        home_region="SYN_REGION",
        home_city="SYN_CITY",
        timezone="UTC",
        risk_tier=RiskTier.LOW,
    )
    assert user_data.synthetic_external_id == "SYN_USER_000001"
    assert user_data.account_age == 45


def test_invalid_user_schema_blank_id():
    """Test invalid UserCreate schema with blank synthetic_external_id."""
    with pytest.raises(ValidationError):
        UserCreate(synthetic_external_id="   ", account_age=10)


def test_invalid_user_schema_negative_age():
    """Test invalid UserCreate schema with negative account_age."""
    with pytest.raises(ValidationError):
        UserCreate(synthetic_external_id="SYN_USER_000001", account_age=-5)


def test_valid_account_schema():
    """Test valid AccountCreate schema validation."""
    user_id = uuid.uuid4()
    account_data = AccountCreate(
        user_id=user_id,
        account_type=AccountType.CONSUMER,
        status=AccountStatus.ACTIVE,
        account_age_days=60,
        synthetic_account_reference="SYN_ACC_000001",
        baseline_balance=Decimal("250.00"),
    )
    assert account_data.user_id == user_id
    assert account_data.baseline_balance == Decimal("250.00")


def test_invalid_account_schema_negative_balance():
    """Test invalid AccountCreate schema with negative balance."""
    with pytest.raises(ValidationError):
        AccountCreate(
            user_id=uuid.uuid4(),
            synthetic_account_reference="SYN_ACC_000001",
            baseline_balance=Decimal("-100.00"),
        )


def test_valid_device_schema():
    """Test valid DeviceCreate schema validation."""
    device_data = DeviceCreate(
        synthetic_device_id="SYN_DEV_000001",
        device_type=DeviceType.DESKTOP,
        operating_system="Windows 11",
        trust_score=0.8,
        reputation_score=0.9,
    )
    assert device_data.trust_score == 0.8
    assert device_data.device_type == DeviceType.DESKTOP


def test_invalid_device_schema_out_of_bounds_trust_score():
    """Test invalid DeviceCreate schema with trust_score > 1.0."""
    with pytest.raises(ValidationError):
        DeviceCreate(
            synthetic_device_id="SYN_DEV_000001",
            trust_score=1.5,
        )

    with pytest.raises(ValidationError):
        DeviceCreate(
            synthetic_device_id="SYN_DEV_000001",
            reputation_score=-0.1,
        )


def test_valid_merchant_schema():
    """Test valid MerchantCreate schema validation."""
    merchant_data = MerchantCreate(
        synthetic_merchant_id="SYN_MERCH_000001",
        name="Synthetic Electronics Store",
        category_code="5732",
        category_name="Electronics Stores",
        region="SYN_REGION",
        status=MerchantStatus.ACTIVE,
        risk_tier=RiskTier.MEDIUM,
    )
    assert merchant_data.name == "Synthetic Electronics Store"
    assert merchant_data.risk_tier == RiskTier.MEDIUM


def test_invalid_merchant_schema_blank_name():
    """Test invalid MerchantCreate schema with blank name."""
    with pytest.raises(ValidationError):
        MerchantCreate(
            synthetic_merchant_id="SYN_MERCH_000001",
            name="  ",
            category_code="5732",
            category_name="Electronics Stores",
        )
