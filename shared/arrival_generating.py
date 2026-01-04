"""
ArrivalGenerating

Module responsible for generating arrivals for an M/M/1 queue.
"""

import numpy as np


class ArrivalGenerating:
    """Generate arrivals according to a Poisson process (exponential inter-arrival times)."""

    def __init__(self, lambda_rate: float) -> None:
        """
        Args:
            lambda_rate: Arrival rate λ (entities per unit time).
        """
        self.lambda_rate = lambda_rate
        self._next_entity_id = 0

    def next_interarrival(self) -> float:
        """Sample the next inter-arrival time ~ Exp(λ)."""
        u = np.random.random()
        return -np.log(1.0 - u) / self.lambda_rate

    def next_entity_id(self) -> int:
        """Return the next entity id (0, 1, 2, ...)."""
        eid = self._next_entity_id
        self._next_entity_id += 1
        return eid


