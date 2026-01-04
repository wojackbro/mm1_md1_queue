"""
M/M/1 Queue Example (single parameter set)

Uses the modular simulation in mm1_queue.py.
"""

import matplotlib.pyplot as plt

from mm1_queue import simulate_mm1, theoretical_waiting_queue_time


def main() -> None:
    # Simulation parameters
    lam, mu, T = 0.5, 1.0, 10000.0

    print(f"M/M/1 Queue: λ={lam}, μ={mu}, Time={T}\n")

    result = simulate_mm1(lam, mu, T)
    wait_q = result["wait_queue_times"]      # waiting in queue only
    service = result["service_times"]        # pure service times
    system = result["system_times"]          # total time in system (queue + service)

    # --- Simulated means ---
    mean_Wq_sim = float(sum(wait_q) / len(wait_q)) if wait_q else 0.0
    mean_S_sim = float(sum(service) / len(service)) if service else 0.0
    mean_W_sim = float(sum(system) / len(system)) if system else 0.0

    # --- Theoretical means ---
    mean_Wq_theory = theoretical_waiting_queue_time(lam, mu)
    mean_S_theory = 1.0 / mu
    mean_W_theory = 1.0 / (mu - lam)

    print("Queue waiting time Wq (queue only):")
    print(f"  Theoretical: {mean_Wq_theory:.6f}")
    print(f"  Simulated : {mean_Wq_sim:.6f}")
    print(f"  Difference: {abs(mean_Wq_sim - mean_Wq_theory):.6f}\n")

    print("Service time S (server only):")
    print(f"  Theoretical: {mean_S_theory:.6f}")
    print(f"  Simulated : {mean_S_sim:.6f}")
    print(f"  Difference: {abs(mean_S_sim - mean_S_theory):.6f}\n")

    print("Total time in system W = Wq + S:")
    print(f"  Theoretical: {mean_W_theory:.6f}")
    print(f"  Simulated : {mean_W_sim:.6f}")
    print(f"  Difference: {abs(mean_W_sim - mean_W_theory):.6f}\n")

    # Plot convergence of mean wait time in queue
    mean_vals = result["mean_wait_queue_times"]
    mean_times = result["mean_wait_queue_times_times"]
    if mean_vals:
        plt.figure(figsize=(12, 6))
        plt.plot(mean_times, mean_vals, "b-", label="Simulated Wq (running mean)", linewidth=2)
        plt.axhline(
            y=mean_Wq_theory,
            color="r",
            linestyle="--",
            linewidth=2,
            label=f"Theoretical Wq = {mean_Wq_theory:.4f}",
        )
        plt.xlabel("Time")
        plt.ylabel("Mean Waiting Time in Queue")
        plt.title(f"M/M/1 Queue: λ = {lam}, μ = {mu}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()

