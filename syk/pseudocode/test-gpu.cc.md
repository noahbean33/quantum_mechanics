# test-gpu.cc — Python Pseudocode

Google Test suite for GPU code: CudaUtils, CudaState, CudaHamiltonian, CudaLanczos.

```python
import unittest
import numpy as np

rng = np.random.RandomState(int(time.time()))
DEFAULT_AVAIL_MEMORY = 4_000_000_000

class CudaUtilsTest(unittest.TestCase):

    def test_copying_matrices(self):
        """Copy matrices to GPU, multiply with cuBLAS Zgemm, copy back, compare."""
        pass

    def test_inverse(self):
        """Test d_inverse kernel: y = 1/x on GPU."""
        pass

    def test_CudaSparseMatrix(self):
        """Create sparse matrix on GPU, multiply with cusparseZcsrmm, compare."""
        pass

class CudaStateTest(unittest.TestCase):

    def test_copying(self):
        """Set CudaEvenState from matrix, get_matrix, compare."""
        pass

    def test_dot(self):
        """Compute <state1|state2> on GPU, compare with host conjugate dot product."""
        pass

    def test_add(self):
        """state1 += alpha*state2 on GPU, compare with host."""
        pass

    def test_norm(self):
        """||state|| on GPU vs host."""
        pass

    def test_set_from_other(self):
        """Copy one CudaEvenState to another, verify equality."""
        pass

    def test_scale(self):
        """state *= alpha on GPU, compare."""
        pass

class CudaHamiltonianTest(unittest.TestCase):

    def test_act_even_single_coupling(self):
        """
        For each left/right operator split (left4/right0 through left0/right4),
        set a single J_{abcd}=1 and verify H*state matches host FactorizedHamiltonian.
        Tested for N=8,10,12,14.
        """
        pass

    def test_act_even_random(self):
        """Full random J tensor, compare GPU vs host for N=8,10,12,14."""
        pass

    def test_act_even_single_chunk_async(self):
        """Test async act_even with a single chunk."""
        pass

    def test_act_even_limited_memory(self):
        """
        Vary available_memory from 20KB to 100KB for N=14,
        verify correctness with multiple chunks.
        """
        pass

    def test_limited_memory_chunks_accounting(self):
        """
        Verify all operators are distributed across chunks and total matches
        num_factorized_hamiltonian_operator_pairs.
        """
        pass

    def test_combining_two_chunks(self):
        """When memory allows 1 big chunk, 2 small chunks get combined into 1."""
        pass

class CudaLanczosTest(unittest.TestCase):

    def test_compute_two_calls_vs_one(self):
        """Running Lanczos in 2 halves gives same alpha/beta as 1 full run."""
        pass

    def test_compute_even_matches_host(self):
        """GPU Lanczos alpha/beta matches host factorized_lanczos for N=8,10,12,14."""
        pass

    def test_load_and_save(self):
        """Save checkpoint, reload, continue, verify same alpha/beta."""
        pass

    def test_full_lanczos_recovers_even_evs(self):
        """
        Run GPU Lanczos for 2*D steps on even charge parity sector,
        verify all even-parity eigenvalues are found.
        Tested for N=10,12,14 with mu=0,1 and limited memory.
        """
        pass

    def test_error_estimates(self):
        """Verify GPU Lanczos error estimates are upper bounds on true errors."""
        pass

if __name__ == "__main__":
    unittest.main()
```
