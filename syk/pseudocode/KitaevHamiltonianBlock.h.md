# KitaevHamiltonianBlock.h — Python Pseudocode

A block of the Kitaev Hamiltonian at fixed U(1) charge Q.

```python
import numpy as np

class KitaevHamiltonianBlock:
    """
    A block of the Kitaev Hamiltonian with charge Q.
    H = (1/2N)^{3/2} sum_{i!=j, k!=l} J_{ijkl} c†_i c†_j c_k c_l
    """

    def __init__(self, N: int, Q: int, J=None, block=None):
        self.N = N
        self.Q = Q
        self.diagonalized = False
        self.U = None  # eigenvectors
        self.evs = None  # eigenvalues

        if block is not None:
            self.matrix = block
        elif J is not None:
            self._initialize_block_matrix(J)
        else:
            self.matrix = np.zeros((self.dim(), self.dim()), dtype=complex)

    def _initialize_block_matrix(self, J):
        """Build the Hamiltonian matrix. Only iterate over non-vanishing states."""
        self.matrix = np.zeros((self.dim(), self.dim()), dtype=complex)
        coefficient = 1.0 / (2.0 * self.N)**1.5 * 4.0

        for i in range(self.N):
            for j in range(i + 1, self.N):
                for k in range(self.N):
                    for l in range(k + 1, self.N):
                        self._add_hamiltonian_term_contribution(J, i, j, k, l)

        self.matrix *= coefficient

    def _add_hamiltonian_term_contribution(self, J, i, j, k, l):
        """
        For each (i,j,k,l) term, loop only over ket states that won't be
        annihilated. Uses combinatorial tricks based on index overlaps
        (i==k, j==l, etc.) to minimize iteration.
        """
        # Determine which indices overlap and iterate over the
        # appropriate number of basis states (N-2 choose Q-2, etc.)
        # For each valid ket, compute bra = c†_i c†_j c_k c_l |ket>
        # and accumulate matrix(bra_n, ket_n) += J(i,j,k,l) * sign
        pass  # (see full implementation in .cc)

    def act_with_c_operators(self, i, j, k, l, ket):
        """Compute c†_i c†_j c_k c_l |ket>."""
        ket.annihilate(l)
        ket.annihilate(k)
        ket.create(j)
        ket.create(i)
        return ket

    def dim(self) -> int:
        return binomial(self.N, self.Q)

    def diagonalize(self, full_diagonalization=True):
        """Diagonalize: H = U D U†. If not full, only eigenvalues."""
        if self.diagonalized:
            return
        if full_diagonalization:
            self.evs, self.U = np.linalg.eigh(self.matrix)
        else:
            self.evs = np.linalg.eigvalsh(self.matrix)
        self.diagonalized = True

    def is_diagonalized(self) -> bool:
        return self.diagonalized

    def eigenvalues(self) -> np.ndarray:
        assert self.diagonalized
        return self.evs

    def D_matrix(self) -> np.ndarray:
        assert self.diagonalized
        return np.diag(self.evs)

    def U_matrix(self) -> np.ndarray:
        assert self.diagonalized
        return self.U


class NaiveKitaevHamiltonianBlock(KitaevHamiltonianBlock):
    """Naive (slow) implementation — loops over all kets and all (i,j,k,l)."""

    def __init__(self, N: int, Q: int, J):
        super().__init__(N, Q)
        self._initialize_naive(J)

    def _initialize_naive(self, J):
        self.matrix = np.zeros((self.dim(), self.dim()), dtype=complex)
        coefficient = 1.0 / (2.0 * self.N)**1.5 * 4.0

        for ket_n in range(self.dim()):
            ket = BasisState(ket_n, self.Q)
            for i in range(self.N):
                for j in range(i + 1, self.N):
                    for k in range(self.N):
                        for l in range(k + 1, self.N):
                            bra = self.act_with_c_operators(i, j, k, l, BasisState(ket.indices[:], ket.coefficient))
                            if not bra.is_zero():
                                bra_n = bra.get_state_number()
                                self.matrix[bra_n, ket_n] += J.elem(i, j, k, l) * bra.coefficient

        self.matrix *= coefficient
```
