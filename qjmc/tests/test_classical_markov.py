"""
Unit tests for the classical_markov module.
"""

import unittest
import numpy as np
from src.classical_markov import simulate_markov_chain, calculate_steady_state

class TestClassicalMarkov(unittest.TestCase):

    def setUp(self):
        """Set up a simple transition matrix for testing."""
        self.P = np.array([[0.2, 0.6, 0.2],
                           [0.3, 0.4, 0.3],
                           [0.1, 0.3, 0.6]])
        self.initial_state = np.array([1.0, 0.0, 0.0])
        self.n_steps = 10

    def test_simulate_markov_chain_output_shape(self):
        """Test that the simulation history has the correct shape."""
        history = simulate_markov_chain(self.P, self.initial_state, self.n_steps)
        self.assertEqual(history.shape, (self.n_steps, self.P.shape[0]))

    def test_steady_state_probabilities_sum_to_one(self):
        """Test that the calculated steady-state probabilities sum to 1."""
        steady_state = calculate_steady_state(self.P)
        self.assertAlmostEqual(np.sum(steady_state), 1.0)

if __name__ == '__main__':
    unittest.main()
