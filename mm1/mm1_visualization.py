"""
M/M/1 Queue – ρ sweep visualization

Plots simulated vs theoretical waiting queue time Wq over a range of ρ values.
"""

import numpy as np
import matplotlib.pyplot as plt

from mm1_queue import simulate_mm1, theoretical_waiting_queue_time


def sweep_rho_and_plot(mu: float = 1.0, sim_time: float = 10000.0) -> None:
    """Plot Wq (simulated vs theoretical) for ρ in [0.05, 0.98] with step 0.05."""
    rhos = np.arange(0.05, 0.99, 0.05)

    simulated_wq = []
    theoretical_wq = []

    for rho in rhos:
        lam = rho * mu
        result = simulate_mm1(lam, mu, sim_time)
        wait_q = result["wait_queue_times"]
        sim_mean = float(sum(wait_q) / len(wait_q)) if wait_q else 0.0
        theory = theoretical_waiting_queue_time(lam, mu)

        simulated_wq.append(sim_mean)
        theoretical_wq.append(theory)

        print(f"ρ={rho:.2f}, λ={lam:.3f}: simulated Wq={sim_mean:.4f}, theoretical Wq={theory:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(rhos, simulated_wq, "bo-", label="Simulated Wq")
    plt.plot(rhos, theoretical_wq, "r--", label="Theoretical Wq")
    plt.xlabel("ρ = λ / μ")
    plt.ylabel("Mean Waiting Time in Queue (Wq)")
    plt.title("M/M/1 Queue: Simulated vs Theoretical Wq over ρ")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sweep_rho_and_plot()

