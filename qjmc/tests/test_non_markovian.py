"""
Unit tests for the non_markovian module.
"""

import unittest
import numpy as np
from src.non_markovian import run_non_markovian_simulation, simulate_expanded_space

class TestNonMarkovian(unittest.TestCase):

    def setUp(self):
        """Set up rules and parameters for testing."""
        self.prob_rules = {
            (0, 0): 0.9, (0, 1): 0.3,
            (1, 0): 0.6, (1, 1): 0.1
        }
        self.n_steps = 100
        self.P_expanded = np.array([
            [0.9, 0.1, 0.0, 0.0], [0.0, 0.0, 0.3, 0.7],
            [0.6, 0.4, 0.0, 0.0], [0.0, 0.0, 0.1, 0.9]
        ])
        self.initial_state_expanded = np.array([1.0, 0.0, 0.0, 0.0])

    def test_run_non_markovian_simulation_length(self):
        """Test that the simulation history has the correct length."""
        history = run_non_markovian_simulation(self.prob_rules, self.n_steps)
        self.assertEqual(len(history), self.n_steps + 2) # +2 for initial history

    def test_simulate_expanded_space_output_shape(self):
        """Test that the expanded space simulation has the correct shape."""
        history = simulate_expanded_space(self.P_expanded, self.initial_state_expanded, self.n_steps)
        self.assertEqual(history.shape, (self.n_steps + 2, self.P_expanded.shape[0]))

if __name__ == '__main__':
    unittest.main()
