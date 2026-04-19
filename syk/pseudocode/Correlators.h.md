# Correlators.h — Python Pseudocode

Two-point correlation functions for Kitaev and Majorana Hamiltonians.

```python
import numpy as np
from typing import List

def get_tau(time_type, t: float) -> complex:
    """Convert time to the complex parameter tau."""
    if time_type == TIME_TYPE.REAL_TIME:
        return 1j * t
    else:  # EUCLIDEAN_TIME
        return t

def compute_exp_H(V: np.ndarray, evs: np.ndarray, a: complex) -> np.ndarray:
    """
    Compute exp(a * H) = V * diag(exp(a * evs)) * V†.
    V = eigenvector matrix, evs = eigenvalues.
    """
    D = np.diag(np.exp(a * evs))
    return V @ D @ V.conj().T

def compute_partition_function(V: np.ndarray, evs: np.ndarray, beta: float) -> float:
    """Z(beta) = Tr(exp(-beta * H))."""
    return np.sum(np.exp(-beta * evs))


# -------- Dirac (complex) SYK correlators --------

def compute_2_point_function(
    N: int,
    betas: List[float],
    times: List[float],
    H: 'KitaevHamiltonian',
    time_type
) -> np.ndarray:
    """
    Compute <c†_i(t) c_i> = (1/NZ) Tr(e^{-bH} e^{tauH} c†_i e^{-tauH} c_i)
    summed over i.
    Returns matrix[beta_idx, time_idx].
    """
    correlators = np.zeros((len(betas), len(times)), dtype=complex)

    for bi, beta in enumerate(betas):
        Z = 0.0
        for Q in range(H.N + 1):
            Z += np.sum(np.exp(-beta * H.blocks[Q].eigenvalues()))

        for ti, t in enumerate(times):
            tau = get_tau(time_type, t)
            G = 0.0 + 0j

            for i in range(N):
                # For each fermion site i, compute the Q-resolved contribution
                for Q in range(1, N + 1):
                    # exp((tau-beta)*E_Q) and exp(-tau*E_{Q-1}) diagonal matrices
                    # c_i connects Q -> Q-1 sector
                    # G += (1/NZ) sum_{m,n} |<m|c_i|n>|^2 * exp((tau-b)*E_n - tau*E_m)
                    pass  # (matrix element computation)

            correlators[bi, ti] = G

    return correlators


# -------- Majorana SYK correlators --------

def compute_majorana_2_pt_function(
    H: 'MajoranaKitaevHamiltonian',
    betas: List[float],
    times: List[float],
    time_type,
    correlators: np.ndarray,
    Z: List[float],
    print_progress: bool = False
):
    """
    Compute (1/N) sum_a Tr(e^{-bH} chi_a(t) chi_a(0)) / Z.
    chi_a(t) = e^{tau H} chi_a e^{-tau H}.
    Uses energy eigenbasis: chi_energy = V† chi V, then trace becomes
    sum over diagonal of exp-weighted matrix products.
    """
    D = H.dim()
    mN = H.mN

    # Transform all chi_a to energy eigenbasis
    chi_energy = [H.to_energy_basis(H.chi[a]) for a in range(mN)]

    for bi, beta in enumerate(betas):
        Z[bi] = np.sum(np.exp(-beta * H.evs))

        for ti, t in enumerate(times):
            tau = get_tau(time_type, t)
            G = 0.0 + 0j

            for a in range(mN):
                # G_a = sum_{m,n} |chi_energy[a](m,n)|^2 * exp((tau-b)*E_m - tau*E_n)
                for m in range(D):
                    for n in range(D):
                        G += (chi_energy[a][m, n]
                              * chi_energy[a][n, m]
                              * np.exp((tau - beta) * H.evs[m] - tau * H.evs[n]))

            correlators[ti, bi] = G / (mN * Z[bi])


def compute_majorana_2_pt_function_with_fluctuations(
    H, betas, times, time_type,
    correlators, correlators_squared,
    Z, print_progress=False
):
    """
    Also compute <G G*> for studying fluctuations.
    <GG*> = (1/N^2) sum_{a,b} Tr(e^{-bH} chi_a(t) chi_a) * Tr(e^{-bH} chi_b(t) chi_b)^*
    Uses the A-matrix formulation:
        A_mn = (1/N) sum_a chi_energy_a(m,n) * chi_energy_a(n,m)
    """
    # ... (same as above plus the GG* computation using A matrix)
    pass


def compute_majorana_2pt_long_time(
    H, chi_energy, beta, times, time_type, correlators
):
    """
    Long-time correlator: precompute the boltzmann-weighted chi products
    and evaluate via matrix multiplications, more efficient for many time points.
    """
    pass


def compute_A_matrix(H, chi_energy) -> np.ndarray:
    """
    A(m,n) = (1/N) sum_a chi_energy_a(m,n) * chi_energy_a(n,m)
    Used for computing GG* fluctuations.
    """
    D = H.dim()
    A = np.zeros((D, D), dtype=complex)
    for a in range(H.mN):
        for m in range(D):
            for n in range(D):
                A[m, n] += chi_energy[a][m, n] * chi_energy[a][n, m]
    A /= H.mN
    return A
```
