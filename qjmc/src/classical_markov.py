"""
Functions for simulating a classical discrete-time Markov chain.
"""

import numpy as np
from typing import Tuple

def simulate_markov_chain(P: np.ndarray, initial_state: np.ndarray, n_steps: int) -> np.ndarray:
    """Simulates the evolution of a Markov chain over n_steps."""
    state_history = np.zeros((n_steps, P.shape[0]))
    state_history[0] = initial_state
    current_state = initial_state

    for i in range(1, n_steps):
        current_state = np.dot(current_state, P)
        state_history[i] = current_state

    return state_history

def calculate_steady_state(P: np.ndarray) -> np.ndarray:
    """Calculates the steady-state distribution of a Markov chain."""
    eigenvalues, eigenvectors = np.linalg.eig(P.T)
    steady_state_vector = np.real(eigenvectors[:, np.isclose(eigenvalues, 1)])
    steady_state_vector = steady_state_vector[:, 0]
    steady_state = steady_state_vector / np.sum(steady_state_vector)
    return steady_state
