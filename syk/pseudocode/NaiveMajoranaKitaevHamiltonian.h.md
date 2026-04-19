# NaiveMajoranaKitaevHamiltonian.h — Python Pseudocode

Naive (slow) Majorana Hamiltonian — expands each chi as (c ± c†)/√2 explicitly.

```python
import numpy as np

class NaiveMajoranaKitaevHamiltonian:
    """
    Naive implementation: for each ket, expand chi_a chi_b chi_c chi_d
    into all 2^4 combinations of c and c†, apply each to the ket.
    """

    def __init__(self, N: int, J):
        assert N % 2 == 0
        self.N = N
        self.dirac_N = N // 2
        self._diagonalized = False
        self.evs = None
        D = self.dim()
        self.matrix = np.zeros((D, D), dtype=complex)

        for ket_n in range(D):
            for a in range(N):
                for b in range(a + 1, N):
                    for c in range(b + 1, N):
                        for d in range(c + 1, N):
                            self._add_majorana_term(ket_n, a, b, c, d, J)

    def _add_majorana_term(self, ket_n, a, b, c, d, J):
        """Loop over 2^4 choices of c vs c† for each of the 4 Majoranas."""
        for a_c in range(2):
            for b_c in range(2):
                for c_c in range(2):
                    for d_c in range(2):
                        coeff = 1.0 + 0j
                        bra = BasisState(ket_n)

                        coeff *= self._act_dirac(bra, d, d_c)
                        if bra.is_zero(): continue
                        coeff *= self._act_dirac(bra, c, c_c)
                        if bra.is_zero(): continue
                        coeff *= self._act_dirac(bra, b, b_c)
                        if bra.is_zero(): continue
                        coeff *= self._act_dirac(bra, a, a_c)
                        if bra.is_zero(): continue

                        bra_n = bra.get_global_state_number()
                        # Factor of 1/4 from (1/sqrt(2))^4
                        self.matrix[bra_n, ket_n] += (
                            J.elem(a, b, c, d) / 4.0 * coeff * bra.coefficient
                        )

    def _act_dirac(self, state, majorana_index, c_or_cstar) -> complex:
        """Act with c or c† depending on c_or_cstar, return phase coefficient."""
        dirac_index = majorana_index // 2
        if c_or_cstar == 0:
            coeff = 1.0 if majorana_index % 2 == 0 else 1j
            state.annihilate(dirac_index)
        else:
            coeff = 1.0 if majorana_index % 2 == 0 else -1j
            state.create(dirac_index)
        return coeff

    def dim(self) -> int:
        return 2**self.dirac_N

    def diagonalize(self):
        if self._diagonalized:
            return
        self.evs = np.linalg.eigvalsh(self.matrix)
        self._diagonalized = True

    def is_diagonalized(self) -> bool:
        return self._diagonalized

    def all_eigenvalues(self) -> np.ndarray:
        assert self._diagonalized
        return self.evs
```
