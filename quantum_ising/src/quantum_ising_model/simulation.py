"""Core simulation routines for the Quantum-Ising Page-curve project.

All heavy numerical work—Hamiltonian construction, state propagation, and
entropy calculation—lives here.  Higher-level scripts (e.g. `generate_data.py`)
should import these functions rather than duplicating logic.
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np
import scipy.linalg as la
from numpy import kron

from .config import T_MAX, T_STEPS
from .ops import SIGMA_X, SIGMA_Z, get_operator

__all__ = [
    "build_hamiltonian_from_graph",
    "run_single_realization",
]


# -----------------------------------------------------------------------------
# Hamiltonian helpers
# -----------------------------------------------------------------------------

def build_hamiltonian_from_graph(graph, J: float, g: float) -> np.ndarray:
    """Return the transverse-field Ising Hamiltonian for *graph*.

    Parameters
    ----------
    graph
        A *networkx* graph whose nodes represent qubits and edges represent
        Ising ZZ couplings.
    J
        Strength of the ZZ interaction along each edge.
    g
        Strength of the transverse X field on each qubit.
    """
    n = graph.number_of_nodes()
    dim = 2 ** n
    H = np.zeros((dim, dim), dtype=np.complex128)

    # ZZ terms
    for i, j in graph.edges():
        H -= J * (get_operator(SIGMA_Z, i, n) @ get_operator(SIGMA_Z, j, n))

    # Transverse field terms
    for i in range(n):
        H -= g * get_operator(SIGMA_X, i, n)

    return H


# -----------------------------------------------------------------------------
# Time evolution & entropy
# -----------------------------------------------------------------------------

def _von_neumann_entropy(rho: np.ndarray, eps: float = 1e-12) -> float:
    """Return ``-Tr(ρ log₂ ρ)`` for density matrix *rho* (base-2 logarithm)."""
    eigenvalues = np.linalg.eigvalsh(rho)
    non_zero = eigenvalues[eigenvalues > eps]
    return float(-np.sum(non_zero * np.log2(non_zero)))


def run_single_realization(
    system_graph,
    g_sys_init: float,
    coupling_node: int,
    params: dict,
    seed: int,
) -> Tuple[List[float], List[float]]:
    """Simulate one system-plus-bath realisation and return EE vs time.

    This mirrors the logic previously embedded in the notebook export but is
    cleaned up for reuse.
    """
    n_sys = system_graph.number_of_nodes()
    n_bath = int(params["N_bath"])
    n_total = n_sys + n_bath

    # Ground state of isolated system -------------------------------------------------
    H_sys_isolated = build_hamiltonian_from_graph(
        system_graph, params["J_sys"], g_sys_init
    )
    _, evecs_sys = la.eigh(H_sys_isolated)
    gs_sys = evecs_sys[:, 0]

    # Bath initial |000...〉 -----------------------------------------------------------
    bath_initial = np.zeros(2 ** n_bath)
    bath_initial[0] = 1.0
    psi_0 = kron(gs_sys, bath_initial)

    # Expand operators to full Hilbert space -----------------------------------------
    H_sys_full = kron(H_sys_isolated, np.identity(2 ** n_bath))

    rng = np.random.RandomState(seed)
    H_bath_full = np.zeros((2 ** n_total, 2 ** n_total), dtype=np.complex128)
    for i in range(n_sys, n_total):
        H_bath_full += -params["g_bath"] * get_operator(SIGMA_X, i, n_total)
        H_bath_full += rng.uniform(
            -params["bath_noise_strength"], params["bath_noise_strength"]
        ) * get_operator(SIGMA_Z, i, n_total)

    # ZZ coupling between chosen system qubit and first bath qubit -------------------
    H_coupling = -params["J_couple"] * (
        get_operator(SIGMA_Z, coupling_node, n_total)
        @ get_operator(SIGMA_Z, n_sys, n_total)
    )

    H_total = H_sys_full + H_bath_full + H_coupling

    # Time evolution -----------------------------------------------------------------
    time_points = np.linspace(0.0, T_MAX, T_STEPS)
    entanglement = []

    U_dt_list = [la.expm(-1j * H_total * t) for t in time_points]
    for U_t in U_dt_list:
        psi_t = U_t @ psi_0
        psi_matrix = psi_t.reshape(2 ** n_sys, 2 ** n_bath)
        rho_A = psi_matrix @ psi_matrix.conj().T
        entanglement.append(_von_neumann_entropy(rho_A))

    return time_points.tolist(), entanglement
