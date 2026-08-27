import random
from typing import Any

import numpy as np
from faker import Faker


class SeedManager:
    """Centralized deterministic PRNG seeding manager for reproducible generation."""

    @staticmethod
    def reset_seed(seed: int):
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
        try:
            from faker.generator import random as faker_random

            faker_random.seed(seed)
        except Exception:
            pass

    def __init__(self, seed: int):
        self.seed = seed
        self.py_random = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)
        self.faker = Faker()
        Faker.seed(seed)
        self.faker.seed_instance(seed)

    def choice(self, seq: Any) -> Any:
        """Deterministic element choice from sequence."""
        return self.py_random.choice(seq)

    def choices(self, seq: Any, weights: Any = None, k: int = 1) -> Any:
        """Deterministic weighted choice from sequence."""
        return self.py_random.choices(seq, weights=weights, k=k)

    def uniform(self, a: float, b: float) -> float:
        """Deterministic uniform float sampling."""
        return self.py_random.uniform(a, b)

    def randint(self, a: int, b: int) -> int:
        """Deterministic integer sampling [a, b]."""
        return self.py_random.randint(a, b)

    def lognormal(self, mean: float, sigma: float) -> float:
        """Deterministic log-normal distribution sampling."""
        return float(self.np_rng.lognormal(mean, sigma))

    def gamma(self, shape: float, scale: float) -> float:
        """Deterministic gamma distribution sampling."""
        return float(self.np_rng.gamma(shape, scale))

    def sample(self, seq: Any, k: int) -> list:
        """Deterministic unique sampling without replacement."""
        return self.py_random.sample(list(seq), k)
