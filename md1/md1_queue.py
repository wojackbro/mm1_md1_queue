"""
M/D/1 Queue Simulation (modular)

Reuses:
- ArrivalGenerating (shared/arrival_generating.py)
- DeterministicServiceUnit (shared/service_unit.py)
- FIFOQueue (shared/fifo_queue.py)
"""

import heapq
from typing import Dict, List, Tuple

import numpy as np

from shared.arrival_generating import ArrivalGenerating
from shared.fifo_queue import FIFOQueue
from shared.service_unit import DeterministicServiceUnit


def theoretical_waiting_queue_time_md1(lambda_rate: float, mu_rate: float = 1.0) -> float:
    """Theoretical mean waiting time in queue for M/D/1: rho / (2*mu*(1-rho))."""
    if lambda_rate >= mu_rate:
        return float("inf")
    rho = lambda_rate / mu_rate
    return rho / (2.0 * mu_rate * (1.0 - rho))


def simulate_md1(
    lambda_rate: float,
    mu_rate: float = 1.0,
    sim_time: float = 10000.0,
) -> Dict[str, List[float]]:
    """Run an M/D/1 simulation.

    Args:
        lambda_rate: Arrival rate λ.
        mu_rate: Service rate μ.
        sim_time: Simulation end time.
    """
    arrivals = ArrivalGenerating(lambda_rate)
    server = DeterministicServiceUnit(mu_rate)
    queue = FIFOQueue()

    events: List[Tuple[float, str, int]] = []  # (event_time, event_type, entity_id)

    current_time = 0.0

    wait_queue_times: List[float] = []
    service_times: List[float] = []
    system_times: List[float] = []
    mean_wait_queue_times: List[float] = []
    mean_wait_queue_times_times: List[float] = []

    arrival_time: Dict[int, float] = {}
    service_start_time: Dict[int, float] = {}

    first_arrival_time = arrivals.next_interarrival()
    first_entity_id = arrivals.next_entity_id()
    heapq.heappush(events, (first_arrival_time, "arrival", first_entity_id))

    while events and current_time < sim_time:
        current_time, event_type, entity_id = heapq.heappop(events)

        if event_type == "arrival":
            arrival_time[entity_id] = current_time

            if not server.busy:
                server.busy = True
                service_start_time[entity_id] = current_time
                s_time = server.service_time()
                service_times.append(s_time)
                departure_time = current_time + s_time
                heapq.heappush(events, (departure_time, "departure", entity_id))
            else:
                queue.push(entity_id)

            if current_time < sim_time:
                next_arrival_time = current_time + arrivals.next_interarrival()
                if next_arrival_time <= sim_time:
                    next_entity_id = arrivals.next_entity_id()
                    heapq.heappush(events, (next_arrival_time, "arrival", next_entity_id))

        else:  # departure
            start = service_start_time.get(entity_id, current_time)
            arr = arrival_time.get(entity_id, current_time)
            wait_q = max(0.0, start - arr)
            wait_queue_times.append(wait_q)

            system_times.append(max(0.0, current_time - arr))

            mean_wait_q = float(np.mean(wait_queue_times))
            mean_wait_queue_times.append(mean_wait_q)
            mean_wait_queue_times_times.append(current_time)

            arrival_time.pop(entity_id, None)
            service_start_time.pop(entity_id, None)

            next_id = queue.pop()
            if next_id is not None:
                service_start_time[next_id] = current_time
                s_time = server.service_time()
                service_times.append(s_time)
                departure_time = current_time + s_time
                heapq.heappush(events, (departure_time, "departure", next_id))
            else:
                server.busy = False

    return {
        "wait_queue_times": wait_queue_times,
        "service_times": service_times,
        "system_times": system_times,
        "mean_wait_queue_times": mean_wait_queue_times,
        "mean_wait_queue_times_times": mean_wait_queue_times_times,
    }



