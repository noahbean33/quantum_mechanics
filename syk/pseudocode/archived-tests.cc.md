# archived-tests.cc — Python Pseudocode

Comprehensive Google Test suite for all CPU-side SYK classes (moved from test-kitaev.cc for faster compilation).

```python
import unittest
import numpy as np

rng = np.random.RandomState(int(time.time()))

class BasisStateTest(unittest.TestCase):
    def test_constructor(self):
        """BasisState from index list matches BasisState from array."""
        pass
    def test_create_coefficient(self):
        """Creating same fermion twice gives 0; anti-commutation gives -1."""
        pass
    def test_create(self):
        """Creating operators in different orders yields correct signs."""
        pass
    def test_annihilate(self):
        """Annihilating occupied/unoccupied sites gives correct sign/zero."""
        pass
    def test_state_numbers(self):
        """state_number ↔ occupation list round-trips correctly."""
        pass
    def test_next_state(self):
        """next_state({0,1,2}) = {0,1,3}."""
        pass
    def test_global_state_number(self):
        """Global state number (binary encoding) round-trips."""
        pass

class KitaevDisorderParameterTest(unittest.TestCase):
    def test_antisymmetry(self):
        """J_{ijkl} is antisymmetric under i↔j and k↔l; J_{ijkl} = conj(J_{klij})."""
        pass

class KitaevHamiltonianBlockTest(unittest.TestCase):
    def test_hermitian(self):
        """H - H† = 0."""
        pass
    def test_computed_element(self):
        """Specific matrix element matches analytic formula."""
        pass
    def test_diagonalize(self):
        """U D U† = H after diagonalization."""
        pass
    def test_fast_vs_naive(self):
        """Fast (index-based) and naive (operator-based) construction match."""
        pass

class KitaevHamiltonianTest(unittest.TestCase):
    def test_basics(self):
        """N+1 blocks, sum of block dims = total dim, diagonalization works."""
        pass
    def test_eigenvalues(self):
        """Last eigenvalue matches Q=N block eigenvalue."""
        pass

class SpectrumTest(unittest.TestCase):
    def test_save_and_load(self):
        """Save spectrum to TSV, reload, compare eigenvalues per Q."""
        pass

class MajoranaDisorderParameterTest(unittest.TestCase):
    def test_antisymmetry(self):
        """J_{ijkl} fully antisymmetric under all adjacent transpositions."""
        pass

class NaiveMajoranaKitaevHamiltonianTest(unittest.TestCase):
    def test_hermitian(self):
        """H = H†."""
        pass
    def test_explicit_matrix_N4(self):
        """For N=4, H is diagonal with entries ±J_{0123}/4."""
        pass
    def test_diagonalize(self):
        """Eigenvalues match analytic result for N=4."""
        pass
    def test_charge_parity_conservation(self):
        """Off-diagonal elements between even/odd charge parity sectors vanish."""
        pass

class MajoranaKitaevHamiltonianTest(unittest.TestCase):
    def test_matches_naive(self):
        """Sparse Majorana H matches dense naive H for N=10."""
        pass
    def test_charge_parity_conservation(self):
        pass
    def test_hermitian_charge_parity_blocks(self):
        """Even and odd charge parity blocks are individually Hermitian."""
        pass
    def test_diagonalize(self):
        """Eigenvalues match naive implementation for N=4..12."""
        pass

class CorrelatorsTest(unittest.TestCase):
    def test_c_matrix_anti_commutators(self):
        """{c†_i, c_i} = I and {c†_i, c_j} = 0 for i≠j."""
        pass
    def test_c_matrix_sum_gives_charge(self):
        """sum_i c†_i c_i = Q * I in charge-Q sector."""
        pass
    def test_exp_H(self):
        """exp(a*H) matches precomputed reference matrix."""
        pass
    def test_exp_H_fast_vs_naive(self):
        pass
    def test_2pt_function_t0_beta0(self):
        """G(t=0, beta=0) = N/2."""
        pass
    def test_2pt_function_t0_is_charge_density(self):
        """G(t=0, beta) = <Q>/Z."""
        pass
    def test_naive_vs_fast_2pt(self):
        pass
    def test_euclidean_periodicity(self):
        """G(tau=0) + G(tau=beta) = N (anti-periodic)."""
        pass
    def test_majorana_2pt_vs_reference(self):
        pass
    def test_majorana_2pt_fluctuations(self):
        """<G G*> computed via full trace matches optimized implementation."""
        pass

class FactorizedHamiltonianTest(unittest.TestCase):
    def test_act_even_matches_unfactorized(self):
        """Factorized H*state matches unfactorized H*state for N=8..14."""
        pass
    def test_all_sparse_implementations_match(self):
        """Dense, sparse, and half-sparse factorized act_even all agree."""
        pass

class RandomMatrixTest(unittest.TestCase):
    def test_GUE_hermitian(self):
        pass
    def test_GOE_symmetric(self):
        pass

if __name__ == "__main__":
    unittest.main()
```
