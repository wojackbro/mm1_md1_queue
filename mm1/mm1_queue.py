"""
M/M/1 Queue Simulation (modular version)

This module wires together:
- ArrivalGenerating (shared/arrival_generating.py)
- ServiceUnit (shared/service_unit.py)
- FIFOQueue (shared/fifo_queue.py)

and exposes a function-based simulation API.
"""

import heapq
from typing import Dict, List, Tuple

import numpy as np

from shared.arrival_generating import ArrivalGenerating
from shared.service_unit import ServiceUnit
from shared.fifo_queue import FIFOQueue


def theoretical_waiting_queue_time(lambda_rate: float, mu_rate: float = 1.0) -> float:
    """Theoretical mean waiting time in queue for M/M/1: 1/(μ-λ) - 1/μ."""
    if lambda_rate >= mu_rate:
        return float("inf")
    return 1.0 / (mu_rate - lambda_rate) - 1.0 / mu_rate


def simulate_mm1(
    lambda_rate: float,
    mu_rate: float = 1.0,
    sim_time: float = 10000.0,
) -> Dict[str, List[float]]:
    """Run a modular M/M/1 simulation.

    Args:
        lambda_rate: Arrival rate λ.
        mu_rate: Service rate μ.
        sim_time: Simulation end time.

    Returns:
        Dictionary with lists:
            - 'wait_queue_times': waiting time in queue (arrival → service start)
            - 'service_times': actual service durations
            - 'system_times': total time in system (arrival → departure)
            - 'mean_wait_queue_times': running mean of queue waiting time
            - 'mean_wait_queue_times_times': times when running mean was computed
    """
    arrivals = ArrivalGenerating(lambda_rate)
    server = ServiceUnit(mu_rate)
    queue = FIFOQueue()

    # Event queue: (event_time, event_type, entity_id)
    events: List[Tuple[float, str, int]] = []

    current_time = 0.0

    # Statistics
    wait_queue_times: List[float] = []
    service_times: List[float] = []
    system_times: List[float] = []
    mean_wait_queue_times: List[float] = []
    mean_wait_queue_times_times: List[float] = []

    # For each entity: track arrival time and service start time
    arrival_time: Dict[int, float] = {}
    service_start_time: Dict[int, float] = {}

    # Schedule first arrival
    first_arrival_time = arrivals.next_interarrival()
    first_entity_id = arrivals.next_entity_id()
    heapq.heappush(events, (first_arrival_time, "arrival", first_entity_id))

    while events and current_time < sim_time:
        current_time, event_type, entity_id = heapq.heappop(events)

        if event_type == "arrival":
            # Record arrival time
            arrival_time[entity_id] = current_time

            if not server.busy:
                # Start service immediately
                server.busy = True
                service_start_time[entity_id] = current_time
                s_time = server.service_time()
                service_times.append(s_time)
                departure_time = current_time + s_time
                heapq.heappush(events, (departure_time, "departure", entity_id))
            else:
                # Join FIFO queue
                queue.push(entity_id)

            # Schedule next arrival
            if current_time < sim_time:
                next_arrival_time = current_time + arrivals.next_interarrival()
                if next_arrival_time <= sim_time:
                    next_entity_id = arrivals.next_entity_id()
                    heapq.heappush(events, (next_arrival_time, "arrival", next_entity_id))

        else:  # departure
            # Compute waiting in queue (arrival → service start)
            start = service_start_time.get(entity_id, current_time)
            arr = arrival_time.get(entity_id, current_time)
            wait_q = max(0.0, start - arr)
            wait_queue_times.append(wait_q)

            # Total time in system (arrival → departure)
            system_times.append(max(0.0, current_time - arr))

            # Update running mean waiting time in queue
            mean_wait_q = float(np.mean(wait_queue_times))
            mean_wait_queue_times.append(mean_wait_q)
            mean_wait_queue_times_times.append(current_time)

            # Clean up
            arrival_time.pop(entity_id, None)
            service_start_time.pop(entity_id, None)

            # Start service for next entity in FIFO queue (if any)
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

