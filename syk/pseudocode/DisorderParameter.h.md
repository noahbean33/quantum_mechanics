# DisorderParameter.h — Python Pseudocode

Disorder parameter J_{ij;kl} for the complex SYK (Dirac) model.

```python
import numpy as np
from abc import ABC, abstractmethod

class DisorderParameter(ABC):
    """Abstract base for disorder coupling tensors."""
    @abstractmethod
    def elem(self, i: int, j: int, k: int, l: int) -> complex:
        pass


class KitaevDisorderParameter(DisorderParameter):
    """
    Holds J_{ij;kl} for H ~ J_{ij;kl} c†_i c†_j c_k c_l.

    Symmetries:
        J_{ji;kl} = -J_{ij;kl}
        J_{ij;lk} = -J_{ij;kl}
        J_{kl;ij} = J*_{ij;kl}
        <|J_{ij;kl}|^2> = J^2
    """

    def __init__(self, N: int, J: float, rng, complex_elements=True):
        self.Jelems = np.zeros((N, N, N, N), dtype=complex)
        sigma_diag = J
        sigma_off = J / np.sqrt(2)

        for i in range(N):
            for j in range(i + 1, N):
                for k in range(N):
                    for l in range(k + 1, N):
                        if k == i and l == j:
                            # Diagonal: real
                            self.Jelems[i][j][i][j] = complex(rng.normal(0, sigma_diag), 0)
                        else:
                            # Off-diagonal: complex (or real)
                            re = rng.normal(0, sigma_off)
                            im = rng.normal(0, sigma_off) if complex_elements else 0
                            self.Jelems[i][j][k][l] = complex(re, im)

                        # Apply reality condition: J_{kl;ij} = conj(J_{ij;kl})
                        self.Jelems[k][l][i][j] = np.conj(self.Jelems[i][j][k][l])

                        # Anti-symmetrize both pairs
                        val = self.Jelems[i][j][k][l]
                        self.Jelems[j][i][k][l] = -val
                        self.Jelems[i][j][l][k] = -val
                        self.Jelems[j][i][l][k] = val

                        cval = self.Jelems[k][l][i][j]
                        self.Jelems[l][k][i][j] = -cval
                        self.Jelems[k][l][j][i] = -cval
                        self.Jelems[l][k][j][i] = cval

    def elem(self, i, j, k, l) -> complex:
        return self.Jelems[i][j][k][l]


class MockDisorderParameter(DisorderParameter):
    """J(i,j,k,l) = i - j + k - l (for testing)."""
    def elem(self, i, j, k, l) -> complex:
        return complex(i - j + k - l, 0)
```
