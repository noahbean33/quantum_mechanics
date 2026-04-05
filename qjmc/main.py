"""
Main script to run the simulations and generate plots for the paper.
"""

import numpy as np
from qutip import basis, destroy

from src.classical_markov import (
    simulate_markov_chain, calculate_steady_state
)
from src.non_markovian import (
    run_non_markovian_simulation, run_ensemble_non_markovian, simulate_expanded_space
)
from src.quantum_jumps import run_qjmc_simulation
from src.plotting import (
    plot_markov_convergence, plot_markov_network, plot_non_markovian_direct_simulation,
    plot_ensemble_vs_theory, plot_qjmc_convergence
)


def main():
    """Run all simulations and generate all plots."""
    # --- 1. Classical Markov Chain ---
    print("Running Classical Markov Chain simulation...")
    P = np.array([[0.2, 0.6, 0.2],
                  [0.3, 0.4, 0.3],
                  [0.1, 0.3, 0.6]])
    initial_state = np.array([1.0, 0.0, 0.0])
    n_steps_markov = 50

    state_history = simulate_markov_chain(P, initial_state, n_steps_markov)
    steady_state = calculate_steady_state(P)

    plot_markov_convergence(state_history, steady_state, save_path="figures/markov_convergence.png")
    plot_markov_network(P, save_path="figures/markov_network.png")

    # --- 2. Non-Markovian Process ---
    print("Running Non-Markovian simulation...")
    prob_rules = {
        (0, 0): 0.9, (0, 1): 0.3,
        (1, 0): 0.6, (1, 1): 0.1
    }
    n_steps_non_markov = 200
    num_runs_ensemble = 500

    history = run_non_markovian_simulation(prob_rules, n_steps_non_markov)
    plot_non_markovian_direct_simulation(history, save_path="figures/non_markovian_direct_sim.png")

    ensemble_histories = run_ensemble_non_markovian(prob_rules, n_steps_non_markov, num_runs_ensemble)

    P_expanded = np.array([
        [0.9, 0.1, 0.0, 0.0], [0.0, 0.0, 0.3, 0.7],
        [0.6, 0.4, 0.0, 0.0], [0.0, 0.0, 0.1, 0.9]
    ])
    initial_state_expanded = np.array([1.0, 0.0, 0.0, 0.0])
    state_history_expanded = simulate_expanded_space(P_expanded, initial_state_expanded, n_steps_non_markov)
    prob_in_state_1_theoretical = state_history_expanded[:, 1] + state_history_expanded[:, 3]

    plot_ensemble_vs_theory(ensemble_histories, prob_in_state_1_theoretical, num_runs_ensemble, save_path="figures/ensemble_vs_theory.png")

    # --- 3. Quantum Jump Monte Carlo ---
    print("Running QJMC simulation...")
    N = 4
    kappa = 1.0 / 0.129
    nth = 0.063
    tlist = np.linspace(0, 0.6, 100)
    a = destroy(N)
    H = a.dag() * a
    psi0 = basis(N, 1)
    c_ops = [
        np.sqrt(kappa * (1 + nth)) * a, # Decay
        np.sqrt(kappa * nth) * a.dag() # Excitation
    ]
    e_ops = [a.dag() * a]
    ntraj_list = [1, 5, 15, 904]

    mc_results = []
    for n in ntraj_list:
        mc_result, me_result, fexpt = run_qjmc_simulation(H, psi0, tlist, c_ops, e_ops, ntraj=n)
        mc_results.append(mc_result)

    plot_qjmc_convergence(mc_results, me_result, fexpt, tlist, ntraj_list, save_path="figures/qjmc_convergence.png")

    print("All simulations complete. Plots saved to 'figures/' directory.")

if __name__ == "__main__":
    main()
