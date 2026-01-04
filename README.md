# M/M/1 Queuing System Simulation

A simple Python implementation of an M/M/1 queuing system with discrete event simulation, theoretical comparison, and visualization.

**Author:** Abid Hossain

## Overview

An M/M/1 queue is a queuing system that has:
- **Poisson arrival process**: Inter-arrival times follow an exponential distribution
- **Exponential service times**: Service times follow an exponential distribution  
- **Single server**: One server processes entities
- **Infinite queue capacity**: No limit on queue size
- **FIFO policy**: First-in, first-out queuing

## Theoretical Background

For an arrival rate λ and service rate μ, the theoretical mean waiting time in the queue is:

$$W_q = \frac{1}{\mu - \lambda} - \frac{1}{\mu}$$

where:
- $\frac{1}{\mu - \lambda}$ is the mean total time in the system (queue + service)
- $\frac{1}{\mu}$ is the mean service time

## Installation

Required packages:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install numpy matplotlib
```

## Usage

### Simple Example

Run a basic M/M/1 simulation and see convergence over time:

```bash
python mm1/example.py
```

This will:
- Run a simulation with λ = 0.5 and μ = 1.0
- Display results comparing simulated vs theoretical mean **queue** wait times
- Show a plot of the mean queue waiting time converging over time

### ρ Sweep: Waiting Queue Time (simulated vs theoretical)

To sweep ρ in `[0.05, 0.98]` (step 0.05) and plot Wq:

```bash
python mm1/mm1_visualization.py
```

This will:
- Fix μ = 1.0 and use λ = ρ · μ
- Sweep ρ = 0.05, 0.10, …, 0.95
- For each ρ, run a long simulation and compute the simulated mean queue wait time
- Plot **simulated** vs **theoretical** Wq as a function of ρ

### Programmatic Usage (modular API)

```python
from mm1_queue import simulate_mm1, theoretical_waiting_queue_time

result = simulate_mm1(lambda_rate=0.5, mu_rate=1.0, sim_time=10000.0)

wait_queue_times = result["wait_queue_times"]      # waiting in queue
service_times = result["service_times"]            # service durations
system_times = result["system_times"]              # total time in system (queue + service)

mean_wait_queue = sum(wait_queue_times) / len(wait_queue_times)
theory = theoretical_waiting_queue_time(0.5, 1.0)

print(f"Theoretical Wq = {theory:.4f}, Simulated Wq = {mean_wait_queue:.4f}")
```

## Files

- `shared/arrival_generating.py`: ArrivalGenerating class (Poisson arrivals)
- `shared/service_unit.py`: ServiceUnit (exponential) and DeterministicServiceUnit (constant) service models
- `shared/fifo_queue.py`: FIFOQueue class (queue behaviour)
- `mm1/mm1_queue.py`: Core simulation wiring (simulate_mm1 + theoretical Wq helper)
- `mm1/mm1_visualization.py`: ρ sweep and Wq comparison plotting for M/M/1
- `mm1/example.py`: Simple M/M/1 example
- `md1/md1_queue.py`: M/D/1 simulation wiring and theoretical Wq helper
- `md1/md1_example.py`: Verifies M/D/1 targets (ρ=0.5 → Wq=0.5, ρ=0.9 → Wq=4.5)
- `md1/md1_visualization.py`: ρ sweep and Wq comparison plotting for M/D/1
- `requirements.txt`: Python dependencies
- `README.md`: This file

## M/D/1 quick start

Run the two required checkpoints and a convergence plot:

```bash
python md1/md1_example.py
```

Sweep ρ for M/D/1:

```bash
python md1/md1_visualization.py
```

## Layout

- `shared/`: common building blocks reused by MM1 and MD1
- `mm1/`: M/M/1-specific wiring and examples
- `md1/`: M/D/1-specific wiring and examples
```

## Key Features

1. **Discrete Event Simulation**: Efficient event-driven simulation engine using priority queue
2. **Running Statistics**: Tracks mean waiting time over time, showing convergence to theoretical value
3. **Theoretical Comparison**: Compares simulation results with exact theoretical values
4. **Visualization**: Plots showing simulated vs theoretical mean waiting times converging over time

## Implementation Details

- Uses discrete event simulation with a priority queue for event scheduling
- Exponential random variables generated using inverse transform method: `-ln(1-U)/rate`
- Tracks running mean wait time after each entity departure
- FIFO queue implemented using Python's `deque` for efficient operations

## Notes

- The arrival rate (λ) must be less than the service rate (μ) for a stable system
- Longer simulation times provide more accurate results (closer to theoretical values)
- The simulation uses exponential random variables for both inter-arrival and service times
- The running mean wait time converges to the theoretical value as more entities are processed
