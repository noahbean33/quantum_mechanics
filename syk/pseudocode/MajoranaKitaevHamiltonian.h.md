# MajoranaKitaevHamiltonian.h — Python Pseudocode

Complete Majorana Kitaev Hamiltonian using chi (Majorana) matrices.

```python
import numpy as np

class MajoranaKitaevHamiltonian:
    """
    H = sum_{a<b<c<d} J_{abcd} chi_a chi_b chi_c chi_d
    Constructed using sparse chi matrices and their pairwise products.
    """

    def __init__(self, mN: int, J):
        assert mN % 2 == 0
        self.mN = mN
        self.dirac_N = mN // 2
        self._diagonalized = False
        self._fully_diagonalized = False

        D = self.dim()
        self.chi = compute_chi_matrices(mN)

        # Pre-compute pairwise products chi_a * chi_b for a < b
        chi_prods = {}
        for a in range(mN):
            for b in range(a + 1, mN):
                chi_prods[(a, b)] = self.chi[a] @ self.chi[b]

        # Build H = sum_{a<b} chi_prods[a,b] * (sum_{c<d, c>b} J_{abcd} * chi_prods[c,d])
        self.matrix = sparse.csc_matrix((D, D), dtype=complex)
        for a in range(mN):
            for b in range(a + 1, mN):
                prods_cd = sparse.csc_matrix((D, D), dtype=complex)
                for c in range(b + 1, mN):
                    for d in range(c + 1, mN):
                        prods_cd += chi_prods[(c, d)] * J.elem(a, b, c, d)
                self.matrix += chi_prods[(a, b)] @ prods_cd

        self.even_charge_parity_evs = None
        self.odd_charge_parity_evs = None
        self.evs = None
        self.V = None

    def dim(self) -> int:
        return 2**self.dirac_N

    def diagonalize(self, print_progress=False):
        """Diagonalize by charge-parity blocks (even/odd)."""
        if self._diagonalized:
            return
        even_block, odd_block = self._prepare_charge_parity_blocks()

        self.even_charge_parity_evs = np.linalg.eigvalsh(even_block.toarray())

        if self.dirac_N % 2 == 0:
            self.odd_charge_parity_evs = np.linalg.eigvalsh(odd_block.toarray())
        else:
            # Degeneracy: odd block has same spectrum as even
            self.odd_charge_parity_evs = self.even_charge_parity_evs.copy()

        self._diagonalized = True

    def diagonalize_full(self, print_progress=False):
        """Full diagonalization: eigenvalues + eigenvectors."""
        if self._fully_diagonalized:
            return
        self.evs, self.V = np.linalg.eigh(self.matrix.toarray())
        self._fully_diagonalized = True

    def _prepare_charge_parity_blocks(self):
        """Split matrix into even and odd charge-parity blocks."""
        D = self.dim()
        charge_parity = [bin(a).count('1') % 2 for a in range(D)]
        # ... partition rows/cols by parity and extract sub-blocks ...
        # Returns (even_block_sparse, odd_block_sparse)
        pass

    def is_diagonalized(self) -> bool:
        return self._diagonalized

    def is_fully_diagonalized(self) -> bool:
        return self._fully_diagonalized

    def eigenvalues(self) -> np.ndarray:
        assert self._fully_diagonalized
        return self.evs

    def all_eigenvalues(self) -> np.ndarray:
        """Even parity evs first, then odd."""
        assert self._diagonalized
        return np.concatenate([self.even_charge_parity_evs, self.odd_charge_parity_evs])

    def all_eigenvalues_sorted(self) -> np.ndarray:
        return np.sort(self.all_eigenvalues())

    def to_energy_basis(self, M):
        """Convert matrix M to energy eigenbasis: V† M V."""
        return self.V.conj().T @ M @ self.V

    def dense_matrix(self) -> np.ndarray:
        return self.matrix.toarray()
```
