"""
Unit tests for the quantum_jumps module.
"""

import unittest
import numpy as np
from qutip import basis, destroy, Qobj
from src.quantum_jumps import run_qjmc_simulation

class TestQuantumJumps(unittest.TestCase):

    def setUp(self):
        """Set up a simple quantum system for testing."""
        self.N = 2
        self.kappa = 1.0
        self.nth = 0.05
        self.tlist = np.linspace(0, 0.1, 2)
        a = destroy(self.N)
        self.H = a.dag() * a
        self.psi0 = basis(self.N, 1)
        self.c_ops = [np.sqrt(self.kappa) * a]
        self.e_ops = [a.dag() * a]
        self.ntraj = 5

    def test_run_qjmc_simulation_output_types(self):
        """Test that the QJMC simulation returns objects of the correct type."""
        mc_result, me_result, fexpt = run_qjmc_simulation(
            self.H, self.psi0, self.tlist, self.c_ops, self.e_ops, self.ntraj
        )
        self.assertIsInstance(mc_result, Qobj)
        self.assertIsInstance(me_result, Qobj)
        self.assertIsInstance(fexpt, float)

    def test_run_qjmc_simulation_output_shape(self):
        """Test that the QJMC simulation output has the correct shape."""
        mc_result, _, _ = run_qjmc_simulation(
            self.H, self.psi0, self.tlist, self.c_ops, self.e_ops, self.ntraj
        )
        self.assertEqual(len(mc_result.expect[0]), len(self.tlist))

if __name__ == '__main__':
    unittest.main()
