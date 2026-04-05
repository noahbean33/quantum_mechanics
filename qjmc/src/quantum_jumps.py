"""
Functions for simulating Quantum Jump Monte Carlo (QJMC) for an open quantum system.
"""

import numpy as np
from qutip import (
    basis, destroy, mcsolve, mesolve, steadystate, expect, Qobj, Options
)
from typing import List, Tuple

def run_qjmc_simulation(
    H: Qobj,
    psi0: Qobj,
    tlist: np.ndarray,
    c_ops: List[Qobj],
    e_ops: List[Qobj],
    ntraj: int,
) -> Tuple:
    """Runs a QJMC simulation and the corresponding master equation evolution."""
    # Monte Carlo solver
    mc_result = mcsolve(H, psi0, tlist, c_ops, e_ops, ntraj=ntraj)

    # Master equation solver
    me_result = mesolve(H, psi0, tlist, c_ops, e_ops)

    # Steady state solver
    final_state = steadystate(H, c_ops)
    fexpt = expect(e_ops[0], final_state)

    return mc_result, me_result, fexpt
