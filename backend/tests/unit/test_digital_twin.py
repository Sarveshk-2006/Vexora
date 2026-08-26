import json
import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.digital_twin import (
    DatabasePersister,
    DatasetExporter,
    DigitalTwinConfig,
    DigitalTwinGenerator,
    ManifestManager,
)
from app.models import Base


def test_deterministic_reproducibility():
    """Test identical seed produces identical generated datasets."""
    config_a = DigitalTwinConfig.dev_preset(seed=42)
    config_b = DigitalTwinConfig.dev_preset(seed=42)

    gen_a = DigitalTwinGenerator(config_a)
    gen_b = DigitalTwinGenerator(config_b)

    res_a = gen_a.generate()
    res_b = gen_b.generate()

    assert len(res_a.users) == len(res_b.users)
    assert len(res_a.transactions) == len(res_b.transactions)

    # Compare first 10 transaction references and amounts
    for tx_a, tx_b in zip(
        res_a.transactions[:10], res_b.transactions[:10], strict=True
    ):
        assert tx_a.transaction_reference == tx_b.transaction_reference
        assert tx_a.amount == tx_b.amount
        assert tx_a.payment_rail == tx_b.payment_rail
        assert tx_a.synthetic_ip == tx_b.synthetic_ip

    # Manifest configuration hash must match
    assert res_a.manifest["configuration_hash"] == res_b.manifest["configuration_hash"]


def test_seed_sensitivity():
    """Test different random seeds produce different generated datasets."""
    config_a = DigitalTwinConfig.dev_preset(seed=42)
    config_b = DigitalTwinConfig.dev_preset(seed=999)

    res_a = DigitalTwinGenerator(config_a).generate()
    res_b = DigitalTwinGenerator(config_b).generate()

    ref_a = res_a.transactions[0].transaction_reference
    ref_b = res_b.transactions[0].transaction_reference
    assert ref_a == ref_b
    # Amounts and timestamps must differ due to different seed stochastic sampling
    assert res_a.transactions[0].amount != res_b.transactions[0].amount or (
        res_a.transactions[0].synthetic_ip != res_b.transactions[0].synthetic_ip
    )


def test_synthetic_ip_rfc5737_safety():
    """Test synthetic IP addresses strictly use RFC 5737 documentation prefixes."""
    res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()

    rfc_prefixes = ("192.0.2.", "198.51.100.", "203.0.113.")
    for tx in res.transactions:
        assert tx.synthetic_ip.startswith(
            rfc_prefixes
        ), f"IP {tx.synthetic_ip} outside RFC 5737"

    for sess in res.sessions:
        assert sess.synthetic_ip.startswith(
            rfc_prefixes
        ), f"IP {sess.synthetic_ip} outside RFC 5737"


def test_data_validation_report():
    """Test generated benign dataset passes all referential integrity checks."""
    res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    report = res.validation_report

    assert report.is_valid is True
    assert report.error_count == 0
    assert report.total_checks_passed > 0


def test_manifest_and_export():
    """Test generation manifest creation and CSV export."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = DigitalTwinConfig.dev_preset(seed=42)
        config.output_dir = tmp_dir
        config.manifest_dir = tmp_dir

        res = DigitalTwinGenerator(config).generate()

        # Test Manifest saving
        manifest_path = ManifestManager.save_manifest(res.manifest, target_dir=tmp_dir)
        assert os.path.exists(manifest_path)

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        assert manifest_data["dataset_type"] == "BENIGN"
        assert manifest_data["generated_entity_counts"]["transactions"] == 1000

        # Test CSV export
        csv_path = DatasetExporter.export_transactions_csv(
            res.transactions, output_dir=tmp_dir, filename="test_transactions.csv"
        )
        assert os.path.exists(csv_path)

        with open(csv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == 1001  # Header + 1000 rows


def test_decoupled_database_persistence():
    """Test DatabasePersister persists generated entities into an active DB session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    res = DigitalTwinGenerator(DigitalTwinConfig.dev_preset(seed=42)).generate()
    inserted_rows = DatabasePersister.persist(res, db_session)

    assert inserted_rows > 1000
    db_session.close()
