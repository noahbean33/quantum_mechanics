# FockSpaceUtils.h — Python Pseudocode

Fock space utilities: dimensions, creation/annihilation operator matrices, Majorana fermion matrices.

```python
import numpy as np
from scipy import sparse

def dim(N: int) -> int:
    """Hilbert space dimension with N Dirac fermions."""
    return 2**N

def Q_sector_dim(N: int, Q: int) -> int:
    """Dimension of the charge-Q sector."""
    return binomial(N, Q)

def compute_c_matrix_dense(i: int, N: int, Q: int) -> np.ndarray:
    """Dense matrix of annihilation operator c_i between Q and Q-1 sectors."""
    rows = Q_sector_dim(N, Q - 1)
    cols = Q_sector_dim(N, Q)
    c_i = np.zeros((rows, cols), dtype=complex)
    for ket_num in range(cols):
        state = BasisState(ket_num, Q)
        state.annihilate(i)
        if not state.is_zero():
            bra_num = state.get_state_number()
            c_i[bra_num, ket_num] = state.coefficient
    return c_i

def compute_cdagger_matrix_dense(i: int, N: int, Q: int) -> np.ndarray:
    """Dense matrix of creation operator c†_i between Q and Q+1 sectors."""
    rows = Q_sector_dim(N, Q + 1)
    cols = Q_sector_dim(N, Q)
    cd_i = np.zeros((rows, cols), dtype=complex)
    for ket_num in range(cols):
        state = BasisState(ket_num, Q)
        state.create(i)
        if not state.is_zero():
            bra_num = state.get_state_number()
            cd_i[bra_num, ket_num] = state.coefficient
    return cd_i

def compute_c_matrix(i: int, N: int, Q: int = None):
    """Sparse annihilation operator c_i. If Q given: between Q and Q-1 sectors. Otherwise: global."""
    # Similar to dense version but builds sparse triplets
    pass  # (same logic, sparse output)

def compute_cdagger_matrix(i: int, N: int, Q: int = None):
    """Sparse creation operator c†_i."""
    pass  # (same logic, sparse output)

def compute_chi_matrix(a: int, mN: int):
    """Sparse Majorana fermion chi_a matrix. mN = number of Majorana fermions."""
    dirac_N = mN // 2
    if a % 2 == 0:
        i = a // 2
        chi = (compute_c_matrix(i, dirac_N) + compute_cdagger_matrix(i, dirac_N)) / np.sqrt(2)
    else:
        i = (a - 1) // 2
        chi = 1j / np.sqrt(2) * (compute_c_matrix(i, dirac_N) - compute_cdagger_matrix(i, dirac_N))
    return chi

def compute_chi_matrices(mN: int) -> list:
    """Compute all chi_a matrices, a = 0, ..., mN-1."""
    dirac_N = mN // 2
    chi = [None] * mN
    for a in range(0, mN, 2):
        i = a // 2
        c_i = compute_c_matrix(i, dirac_N)
        cd_i = compute_cdagger_matrix(i, dirac_N)
        chi[a] = (c_i + cd_i) * (1.0 / np.sqrt(2))
        chi[a + 1] = (c_i - cd_i) * (1j / np.sqrt(2))
    return chi


class Space:
    """Hilbert space of N Majorana fermions (= N/2 Dirac fermions)."""

    def __init__(self):
        self.N = -1    # num Majorana fermions
        self.Nd = -1   # num Dirac fermions
        self.D = -1    # dimension

    @staticmethod
    def from_majorana(N: int) -> 'Space':
        assert N % 2 == 0
        space = Space()
        space._init_dirac(N // 2)
        return space

    @staticmethod
    def from_dirac(Nd: int) -> 'Space':
        space = Space()
        space._init_dirac(Nd)
        return space

    def _init_dirac(self, Nd: int):
        self.Nd = Nd
        self.N = 2 * Nd
        self.D = dim(Nd)
```
