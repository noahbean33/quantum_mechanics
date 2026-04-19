# RandomMatrix.h — Python Pseudocode

Random matrix ensembles (GUE, GOE, Sparse Hermitian).

```python
import numpy as np
from abc import ABC, abstractmethod

class RandomMatrix(ABC):
    @abstractmethod
    def eigenvalues(self) -> np.ndarray:
        pass

class GUERandomMatrix(RandomMatrix):
    """Gaussian Unitary Ensemble: H_{ij} ~ N(0, sigma) + i*N(0, sigma)."""

    def __init__(self, K: int, rng):
        self.K = K
        sigma = 1.0 / np.sqrt(K)
        sigma_diag = sigma
        sigma_off = sigma / np.sqrt(2)

        H = np.zeros((K, K), dtype=complex)
        for i in range(K):
            H[i, i] = complex(rng.normal(0, sigma_diag), 0)  # real diagonal
            for j in range(i + 1, K):
                H[i, j] = complex(rng.normal(0, sigma_off), rng.normal(0, sigma_off))
                H[j, i] = np.conj(H[i, j])
        self.matrix = H

    def eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvalsh(self.matrix)

class GOERandomMatrix(RandomMatrix):
    """Gaussian Orthogonal Ensemble: real symmetric."""

    def __init__(self, K: int, rng):
        self.K = K
        sigma = 1.0 / np.sqrt(K)
        sigma_off = sigma / np.sqrt(2)

        H = np.zeros((K, K))
        for i in range(K):
            H[i, i] = rng.normal(0, sigma)
            for j in range(i + 1, K):
                H[i, j] = rng.normal(0, sigma_off)
                H[j, i] = H[i, j]
        self.matrix = H

    def eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvalsh(self.matrix)

class SparseHermitianRandomMatrix(RandomMatrix):
    """Sparse Hermitian matrix with a fixed number of non-zero elements."""

    def __init__(self, K: int, num_nonzeros: int, rng):
        self.K = K
        sigma = 1.0 / np.sqrt(K)

        # Pick random positions for non-zero elements
        positions = set()
        while len(positions) < num_nonzeros:
            i = rng.randint(0, K - 1)
            j = rng.randint(0, K - 1)
            if i <= j:
                positions.add((i, j))
            else:
                positions.add((j, i))

        H = np.zeros((K, K), dtype=complex)
        for (i, j) in positions:
            if i == j:
                H[i, i] = complex(rng.normal(0, sigma), 0)
            else:
                H[i, j] = complex(rng.normal(0, sigma / np.sqrt(2)),
                                   rng.normal(0, sigma / np.sqrt(2)))
                H[j, i] = np.conj(H[i, j])
        self.matrix = H

    def eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvalsh(self.matrix)
```
