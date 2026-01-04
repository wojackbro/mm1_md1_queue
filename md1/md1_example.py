"""
M/D/1 Queue Example: verifies two target points and shows convergence.
"""

import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path so we can import shared and md1 modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from md1.md1_queue import simulate_md1, theoretical_waiting_queue_time_md1


def run_case(lam: float, mu: float = 1.0, sim_time: float = 10000.0) -> None:
    print("=" * 70)
    print(f"M/D/1 Queue Simulation: λ = {lam}, μ = {mu}")
    print("=" * 70)
    
    # Compute theoretical value step by step
    rho = lam / mu
    print(f"\nTheoretical Calculation:")
    print(f"  Utilization ρ = λ / μ = {lam} / {mu} = {rho:.4f}")
    print(f"  Formula: Wq = ρ / (2 × μ × (1 - ρ))")
    print(f"  Wq = {rho:.4f} / (2 × {mu} × (1 - {rho:.4f}))")
    print(f"  Wq = {rho:.4f} / (2 × {mu} × {1-rho:.4f})")
    print(f"  Wq = {rho:.4f} / {2*mu*(1-rho):.4f}")
    mean_Wq_theory = theoretical_waiting_queue_time_md1(lam, mu)
    print(f"  Wq = {mean_Wq_theory:.6f}")
    
    # Run simulation
    print(f"\nRunning simulation for {sim_time} time units...")
    result = simulate_md1(lam, mu, sim_time)
    wait_q = result["wait_queue_times"]
    mean_Wq_sim = float(sum(wait_q) / len(wait_q)) if wait_q else 0.0
    
    print(f"\nResults:")
    print(f"  Theoretical Wq: {mean_Wq_theory:.6f}")
    print(f"  Simulated  Wq:  {mean_Wq_sim:.6f}")
    print(f"  Difference:     {abs(mean_Wq_sim - mean_Wq_theory):.6f}")
    print(f"  Relative Error: {abs(mean_Wq_sim - mean_Wq_theory) / mean_Wq_theory * 100:.2f}%")
    print(f"  Number of entities processed: {len(wait_q)}")
    print("=" * 70)
    print()

    mean_vals = result["mean_wait_queue_times"]
    mean_times = result["mean_wait_queue_times_times"]
    if mean_vals:
        plt.figure(figsize=(10, 5))
        plt.plot(mean_times, mean_vals, "b-", label="Simulated Wq (running mean)", linewidth=2)
        plt.axhline(
            y=mean_Wq_theory,
            color="r",
            linestyle="--",
            linewidth=2,
            label=f"Theoretical Wq = {mean_Wq_theory:.4f}",
        )
        plt.xlabel("Time")
        plt.ylabel("Mean Waiting Time in Queue (Wq)")
        plt.title(f"M/D/1 Queue: λ = {lam}, μ = {mu}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        filename = f"md1_lambda_{lam}_mu_{mu}.png"
        plt.savefig(filename, dpi=150)
        print(f"  Plot saved to: {filename}")
        plt.close()  # Close the figure to free memory and continue


def main() -> None:
    # Two required checkpoints
    run_case(lam=0.5, mu=1.0, sim_time=50000.0)
    run_case(lam=0.9, mu=1.0, sim_time=50000.0)


if __name__ == "__main__":
    main()


