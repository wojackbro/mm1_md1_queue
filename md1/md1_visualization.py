"""
M/D/1 Queue – ρ sweep visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path so we can import shared and md1 modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from md1.md1_queue import simulate_md1, theoretical_waiting_queue_time_md1


def sweep_rho_and_plot(mu: float = 1.0, sim_time: float = 10000.0) -> None:
    """Plot Wq (simulated vs theoretical) for ρ in [0.05, 0.95] with step 0.05."""
    rhos = np.arange(0.05, 0.96, 0.05)

    simulated_wq = []
    theoretical_wq = []

    for rho in rhos:
        lam = rho * mu
        result = simulate_md1(lam, mu, sim_time)
        wait_q = result["wait_queue_times"]
        sim_mean = float(sum(wait_q) / len(wait_q)) if wait_q else 0.0
        theory = theoretical_waiting_queue_time_md1(lam, mu)

        simulated_wq.append(sim_mean)
        theoretical_wq.append(theory)

        print(f"ρ={rho:.2f}, λ={lam:.3f}: simulated Wq={sim_mean:.4f}, theoretical Wq={theory:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(rhos, simulated_wq, "bo-", label="Simulated Wq")
    plt.plot(rhos, theoretical_wq, "r--", label="Theoretical Wq")
    plt.xlabel("ρ = λ / μ")
    plt.ylabel("Mean Waiting Time in Queue (Wq)")
    plt.title("M/D/1 Queue: Simulated vs Theoretical Wq over ρ")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sweep_rho_and_plot()


