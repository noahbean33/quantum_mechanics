"""
Functions for simulating a non-Markovian process with memory and its
state-space expansion.
"""

import numpy as np
import random
from typing import Dict, List, Tuple

def run_non_markovian_simulation(prob_rules: Dict[Tuple[int, int], float], n_steps: int) -> List[int]:
    """Runs a single direct simulation of the non-Markovian process."""
    history = [0, 0]
    for _ in range(n_steps):
        last_two = tuple(history[-2:])
        prob_0 = prob_rules[last_two]

        if random.random() < prob_0:
            history.append(0)
        else:
            history.append(1)
    return history

def run_ensemble_non_markovian(
    prob_rules: Dict[Tuple[int, int], float], n_steps: int, num_runs: int
) -> np.ndarray:
    """Runs an ensemble of direct simulations and returns the histories."""
    ensemble_histories = []
    for _ in range(num_runs):
        ensemble_histories.append(run_non_markovian_simulation(prob_rules, n_steps))
    return np.array(ensemble_histories)

def simulate_expanded_space(
    P_expanded: np.ndarray, initial_state: np.ndarray, n_steps: int
) -> np.ndarray:
    """Simulates the evolution of the expanded Markov chain."""
    state_history = np.zeros((n_steps + 2, P_expanded.shape[0]))
    state_history[0] = initial_state
    current_state_dist = initial_state

    for i in range(1, n_steps + 2):
        current_state_dist = np.dot(current_state_dist, P_expanded)
        state_history[i] = current_state_dist

    return state_history
