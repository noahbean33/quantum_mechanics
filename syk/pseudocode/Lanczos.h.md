# Lanczos.h — Python Pseudocode

Lanczos algorithm for finding eigenvalues of large symmetric matrices.

```python
import numpy as np
from typing import Tuple, Optional

def reference_lanczos(
    H: 'MajoranaKitaevHamiltonian',
    max_steps: int,
    mu: float = 0.0,
    initial_state: Optional[np.ndarray] = None,
    rng=None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Standard Lanczos algorithm for a Majorana Hamiltonian.
    Returns (alpha, beta) arrays = diagonal and sub-diagonal
    of the tridiagonal Lanczos matrix T.

    Algorithm:
        v_0 = 0
        v_1 = random_normalized_state (or initial_state)
        for i = 1..max_steps:
            u = (H + mu*I) * v_i - beta_{i-1} * v_{i-1}
            alpha_i = <u, v_i>
            u -= alpha_i * v_i
            beta_i = ||u||
            v_{i+1} = u / beta_i
    """
    D = H.dim()
    if initial_state is None:
        v = get_random_state(D, rng)
    else:
        v = initial_state / np.linalg.norm(initial_state)

    alpha = np.zeros(max_steps)
    beta = np.zeros(max_steps - 1)
    v_old = np.zeros(D, dtype=complex)

    for i in range(max_steps):
        u = H.matrix @ v + mu * v
        if i > 0:
            u -= beta[i - 1] * v_old

        alpha[i] = np.real(np.vdot(v, u))
        u -= alpha[i] * v

        if i < max_steps - 1:
            beta[i] = np.linalg.norm(u)
            v_old = v.copy()
            v = u / beta[i]

    return alpha, beta


def factorized_lanczos(
    H,  # FactorizedHamiltonian or similar
    space: 'FactorizedSpace',
    charge_parity,
    max_steps: int,
    mu: float = 0.0,
    initial_state=None,
    rng=None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Lanczos algorithm for factorized Hamiltonians (acts on
    factorized states — matrices instead of vectors).
    Same algorithm as reference_lanczos, but state is a matrix
    and H acts via act_even/act_odd.
    """
    pass  # (same Lanczos iteration, using matrix-form states)


def find_good_lanczos_evs(alpha: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Compute 'good' eigenvalues of the Lanczos tridiagonal matrix.
    Good = eigenvalues that appear in T_m but not in T_{m-1}.
    Based on Cullum-Willoughby criterion for identifying spurious eigenvalues.
    """
    # Build tridiagonal matrix T from alpha (diagonal) and beta (sub-diagonal)
    T_full = build_tridiagonal(alpha, beta)
    evs_full = np.linalg.eigvalsh(T_full)

    # Build T_{m-1} (one smaller)
    T_smaller = build_tridiagonal(alpha[:-1], beta[:-1])
    evs_smaller = np.linalg.eigvalsh(T_smaller)

    # Good eigenvalues: those in evs_full that don't appear in evs_smaller
    good_evs = [ev for ev in evs_full
                 if not any(abs(ev - ev2) < epsilon for ev2 in evs_smaller)]

    return np.array(sorted(good_evs))


def find_good_lanczos_evs_and_errs(
    alpha: np.ndarray,
    extended_beta: np.ndarray,
    error_estimates: np.ndarray,
    rng
) -> np.ndarray:
    """
    Find good eigenvalues and estimate errors using
    beta_{m+1} * |last component of eigenvector|.
    Uses inverse iteration to find the last component.
    """
    pass  # (same as find_good_lanczos_evs + error estimation)


def build_tridiagonal(alpha: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Build tridiagonal matrix from diagonal alpha and sub-diagonal beta."""
    n = len(alpha)
    T = np.diag(alpha)
    for i in range(n - 1):
        T[i, i + 1] = beta[i]
        T[i + 1, i] = beta[i]
    return T
```
