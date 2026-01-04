"""
ServiceUnit

Module responsible for service times in an M/M/1 queue.
"""

import numpy as np


class ServiceUnit:
    """Single service unit with exponential service times."""

    def __init__(self, mu_rate: float) -> None:
        """
        Args:
            mu_rate: Service rate μ (entities per unit time).
        """
        self.mu_rate = mu_rate
        self.busy = False

    def service_time(self) -> float:
        """Sample a service time ~ Exp(μ)."""
        u = np.random.random()
        return -np.log(1.0 - u) / self.mu_rate


class DeterministicServiceUnit:
    """Single service unit with deterministic service times (M/D/1)."""

    def __init__(self, mu_rate: float) -> None:
        """
        Args:
            mu_rate: Service rate μ (entities per unit time).
        """
        self.mu_rate = mu_rate
        self.busy = False

    def service_time(self) -> float:
        """Return constant service time 1/μ."""
        return 1.0 / self.mu_rate


