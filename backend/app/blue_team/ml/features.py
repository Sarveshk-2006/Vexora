import math
from typing import Any, Dict, List, Optional


class FeatureExtractor:
    """Feature extractor converting synthetic entities into feature vectors."""

    # Explicit list of safe feature keys
    FEATURE_NAMES: List[str] = [
        "amount",
        "log_amount",
        "payment_rail_encoded",
        "user_account_age_days",
        "user_risk_tier_encoded",
        "user_daily_tx_rate",
        "user_mean_amount",
        "account_balance",
        "device_trust_score",
        "device_reputation_score",
        "known_device_flag",
        "merchant_risk_tier_encoded",
        "merchant_category_encoded",
        "hour",
        "weekday",
        "is_weekend",
        "session_duration_minutes",
        "session_tx_count",
        "amount_ratio_to_user_mean",
        "velocity_deviation",
        "merchant_novelty_flag",
        "device_novelty_flag",
        "timing_off_hours_flag",
        "payment_rail_novelty_flag",
    ]

    @staticmethod
    def to_feature_matrix(feature_dicts: List[Dict[str, Any]]) -> List[List[float]]:
        """Convert list of feature dicts to 2D matrix of floats matching FEATURE_NAMES."""
        matrix = []
        for fd in feature_dicts:
            row = [float(fd.get(k, 0.0)) for k in FeatureExtractor.FEATURE_NAMES]
            matrix.append(row)
        return matrix

    @staticmethod
    def extract_features(
        tx: Any,
        digital_twin_result: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Extract a feature dictionary from a synthetic Transaction instance."""
        # 1. Transaction Features
        amount = float(tx.amount)
        log_amount = math.log(max(1.0, amount))

        rail_map = {"UPI": 0.0, "CARD": 1.0, "WALLET": 2.0}
        pr = tx.payment_rail
        rail_val = pr.value if hasattr(pr, "value") else str(pr)
        rail_encoded = rail_map.get(rail_val, 0.0)

        # Lookup entity baselines from Digital Twin if available
        user_profiles = getattr(digital_twin_result, "user_profiles", {})
        users_by_id = {u.id: u for u in getattr(digital_twin_result, "users", [])}
        accounts_by_id = {a.id: a for a in getattr(digital_twin_result, "accounts", [])}
        devices_by_id = {d.id: d for d in getattr(digital_twin_result, "devices", [])}
        merchants_by_id = {
            m.id: m for m in getattr(digital_twin_result, "merchants", [])
        }
        sessions_by_id = {s.id: s for s in getattr(digital_twin_result, "sessions", [])}

        # 2. User Features
        user_profile = user_profiles.get(tx.user_id)
        user_obj = users_by_id.get(tx.user_id)

        account_age = float(user_obj.account_age) if user_obj else 180.0
        risk_map = {"LOW": 0.0, "MEDIUM": 0.5, "HIGH": 1.0, "CRITICAL": 1.0}
        user_risk = risk_map.get(
            (
                user_obj.risk_tier.value
                if (user_obj and hasattr(user_obj.risk_tier, "value"))
                else "LOW"
            ),
            0.0,
        )
        daily_tx_rate = float(user_profile.daily_tx_rate) if user_profile else 1.5
        user_mean_amt = (
            math.exp(
                user_profile.amount_log_mean + (user_profile.amount_log_sigma**2) / 2.0
            )
            if user_profile
            else 500.0
        )

        # 3. Account Features
        acc_obj = accounts_by_id.get(tx.account_id)
        acc_balance = float(acc_obj.baseline_balance) if acc_obj else 5000.0

        # 4. Device Features
        dev_obj = devices_by_id.get(tx.device_id)
        dev_trust = float(dev_obj.trust_score) if dev_obj else 0.85
        dev_rep = float(dev_obj.reputation_score) if dev_obj else 0.90
        known_dev = 1.0 if dev_trust >= 0.5 else 0.0

        # 5. Merchant Features
        merch_obj = merchants_by_id.get(tx.merchant_id)
        merch_risk = risk_map.get(
            (
                merch_obj.risk_tier.value
                if (merch_obj and hasattr(merch_obj.risk_tier, "value"))
                else "LOW"
            ),
            0.0,
        )
        mcc_map = {
            "GROCERY": 1.0,
            "FOOD": 2.0,
            "TRAVEL": 3.0,
            "ENTERTAINMENT": 4.0,
            "UTILITIES": 5.0,
            "ECOMMERCE": 6.0,
            "HEALTHCARE": 7.0,
            "EDUCATION": 8.0,
            "SERVICES": 9.0,
            "OTHER": 10.0,
        }
        merch_cat = mcc_map.get(merch_obj.category_name if merch_obj else "OTHER", 10.0)

        # 6. Temporal Features
        ts = tx.timestamp
        hour = float(ts.hour)
        weekday = float(ts.weekday())
        is_weekend = 1.0 if weekday in (5, 6) else 0.0

        # 7. Session Features
        sess_obj = sessions_by_id.get(tx.session_id)
        sess_duration = 15.0
        sess_tx_count = 1.0
        if sess_obj and sess_obj.started_at:
            end = sess_obj.ended_at or sess_obj.started_at
            dur = (end - sess_obj.started_at).total_seconds() / 60.0
            sess_duration = max(1.0, dur)

        # 8. Behavioral Derived Features
        amt_ratio = amount / max(1.0, user_mean_amt)
        velocity_dev = sess_tx_count / max(0.5, daily_tx_rate)
        merch_novelty = (
            1.0
            if (merch_obj and merch_obj.risk_tier.value in ("HIGH", "CRITICAL"))
            else 0.0
        )
        device_novelty = 1.0 if dev_trust < 0.4 else 0.0
        timing_off_hours = 1.0 if (1 <= hour <= 4) else 0.0
        rail_novelty = (
            1.0
            if (
                user_profile
                and rail_encoded != 0.0
                and user_profile.rail_weights.get("UPI", 0) > 0.8
            )
            else 0.0
        )

        features = {
            "amount": amount,
            "log_amount": round(log_amount, 4),
            "payment_rail_encoded": rail_encoded,
            "user_account_age_days": account_age,
            "user_risk_tier_encoded": user_risk,
            "user_daily_tx_rate": daily_tx_rate,
            "user_mean_amount": user_mean_amt,
            "account_balance": acc_balance,
            "device_trust_score": dev_trust,
            "device_reputation_score": dev_rep,
            "known_device_flag": known_dev,
            "merchant_risk_tier_encoded": merch_risk,
            "merchant_category_encoded": merch_cat,
            "hour": hour,
            "weekday": weekday,
            "is_weekend": is_weekend,
            "session_duration_minutes": sess_duration,
            "session_tx_count": sess_tx_count,
            "amount_ratio_to_user_mean": round(amt_ratio, 4),
            "velocity_deviation": round(velocity_dev, 4),
            "merchant_novelty_flag": merch_novelty,
            "device_novelty_flag": device_novelty,
            "timing_off_hours_flag": timing_off_hours,
            "payment_rail_novelty_flag": rail_novelty,
        }

        # ANTI-LEAKAGE SANITIZATION: Verify zero Red Team metadata keys
        forbidden_keys = {
            "scenario_id",
            "genome_reference",
            "generation_number",
            "target_flag",
            "mutation_dimensions",
            "applied_mutations",
            "label",
            "target",
            "baseline_transaction_id",
        }
        for k in forbidden_keys:
            if k in features:
                del features[k]

        return features

    @classmethod
    def extract_feature_vector(
        cls,
        tx: Any,
        digital_twin_result: Optional[Any] = None,
    ) -> List[float]:
        """Convert transaction into ordered numerical feature vector."""
        feat_dict = cls.extract_features(tx, digital_twin_result)
        return [float(feat_dict.get(name, 0.0)) for name in cls.FEATURE_NAMES]
