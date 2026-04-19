# KitaevHamiltonian.h — Python Pseudocode

Complete Dirac Kitaev Hamiltonian as a list of Q-sector blocks.

```python
import numpy as np

class KitaevHamiltonian:
    """
    Complete Hamiltonian as (N+1) blocks sorted by charge Q = 0, ..., N.
    """

    def __init__(self, N: int, J):
        self.N = N
        self.blocks = [KitaevHamiltonianBlock(N, Q, J) for Q in range(N + 1)]

    def dim(self) -> int:
        return 2**self.N

    def diagonalize(self, full_diagonalization=True, print_progress=False):
        """Diagonalize each Q-sector block."""
        for Q in range(self.N + 1):
            if print_progress:
                print(f"Diagonalizing Q={Q} ...")
            timer = Timer()
            self.blocks[Q].diagonalize(full_diagonalization)
            if print_progress:
                print(f"took {timer.seconds()} seconds")

    def is_diagonalized(self) -> bool:
        return self.blocks[0].diagonalized

    def eigenvalues(self) -> np.ndarray:
        """Return all eigenvalues, ordered by Q."""
        assert self.is_diagonalized()
        evs = np.zeros(self.dim())
        k = 0
        for Q in range(self.N + 1):
            block_dim = self.blocks[Q].dim()
            evs[k:k + block_dim] = self.blocks[Q].eigenvalues()
            k += block_dim
        return evs

    def as_matrix(self) -> np.ndarray:
        """Return full block-diagonal Hamiltonian matrix."""
        H = np.zeros((self.dim(), self.dim()), dtype=complex)
        offset = 0
        for Q in range(self.N + 1):
            d = self.blocks[Q].dim()
            H[offset:offset + d, offset:offset + d] = self.blocks[Q].matrix
            offset += d
        return H
```
