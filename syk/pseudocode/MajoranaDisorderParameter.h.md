# MajoranaDisorderParameter.h — Python Pseudocode

Disorder parameter J_{ijkl} for the Majorana SYK model.

```python
import numpy as np
from abc import ABC, abstractmethod

class MajoranaDisorderParameter(ABC):
    """Abstract base for Majorana disorder couplings."""
    @abstractmethod
    def elem(self, i: int, j: int, k: int, l: int) -> float:
        pass


class MajoranaKitaevDisorderParameter(MajoranaDisorderParameter):
    """
    Holds J_{ijkl} for H ~ J_{ijkl} chi_i chi_j chi_k chi_l.
    J_{ijkl} is real and completely antisymmetric.
    sigma^2 = 3! * J^2 / N^3
    """

    def __init__(self, N: int, J: float = None, rng=None):
        self.N = N
        self.Jelems = np.zeros((N, N, N, N))

        if J is not None and rng is not None:
            sigma = np.sqrt(6 * J**2 / N**3)
            for i in range(N):
                for j in range(i + 1, N):
                    for k in range(j + 1, N):
                        for l in range(k + 1, N):
                            self.Jelems[i][j][k][l] = rng.normal(0, sigma)
        # else: all zeros

        self.antisymmetrize()

    def antisymmetrize(self):
        """Set all permutations of (i,j,k,l) with i<j<k<l using full antisymmetry."""
        N = self.N
        for i in range(N):
            for j in range(i + 1, N):
                for k in range(j + 1, N):
                    for l in range(k + 1, N):
                        val = self.Jelems[i][j][k][l]
                        # Set all 24 permutations with appropriate signs
                        # (complete antisymmetry of a rank-4 tensor)
                        # e.g. swapping any two indices flips the sign
                        for perm, sign in all_signed_permutations(i, j, k, l):
                            self.Jelems[perm] = sign * val

    def elem(self, i, j, k, l) -> float:
        return self.Jelems[i][j][k][l]

    def to_string(self) -> str:
        lines = []
        for i in range(self.N):
            for j in range(i + 1, self.N):
                for k in range(j + 1, self.N):
                    for l in range(k + 1, self.N):
                        lines.append(f"{i},{j},{k},{l}: {self.elem(i,j,k,l)}")
        return "\n".join(lines)


class MockMajoranaDisorderParameter(MajoranaDisorderParameter):
    """J(i,j,k,l) = i - j + k - l (for testing)."""
    def elem(self, i, j, k, l) -> float:
        return float(i - j + k - l)


class MajoranaKitaevDisorderParameterWithoutNeighbors(MajoranaKitaevDisorderParameter):
    """
    Same as MajoranaKitaevDisorderParameter but zeros out couplings
    where neighboring Majoranas translate to the same Dirac fermion.
    Useful for testing GPU code.
    """
    def __init__(self, N: int, J: float, rng):
        super().__init__(N, J, rng)
        # Zero out elements where adjacent Majoranas share a Dirac fermion
        for i in range(N):
            for j in range(i + 1, N):
                for k in range(j + 1, N):
                    for l in range(k + 1, N):
                        if (is_same_dirac_fermion(i, j) or
                            is_same_dirac_fermion(j, k) or
                            is_same_dirac_fermion(k, l)):
                            self.Jelems[i][j][k][l] = 0.0
        self.antisymmetrize()

def is_same_dirac_fermion(i: int, j: int) -> bool:
    """Whether chi_i and chi_j correspond to the same Dirac fermion (i < j)."""
    return (i % 2 == 0) and (j == i + 1)
```
