# test-multi-gpu.cc — Python Pseudocode

Google Test suite for multi-GPU code. Requires >= 2 GPUs.

```python
import unittest
import numpy as np

rng = np.random.RandomState(int(time.time()))

class CudaMultiGpuHamiltonianTest(unittest.TestCase):

    def test_sanity(self):
        """Create CudaMultiGpuHamiltonian on 2 GPUs without crash."""
        assert cuda_get_num_devices() > 1
        space = FactorizedSpace.from_majorana(30)
        Jtensor = MajoranaKitaevDisorderParameter(space.N, 1.0, rng)
        H = CudaMultiGpuHamiltonian(space, Jtensor, [50_000_000, 50_000_000])

    def test_sanity_and_act(self):
        """Create H and call act_even 3 times without crash."""
        pass

    def test_act_even_2devices(self):
        """
        Compare multi-GPU act_even output with host FactorizedHamiltonian.
        Test for N=22,24 and with chunk combining (N=18).
        """
        pass

    def test_act_even_allDevices(self):
        """Same as 2-device test but uses all available GPUs."""
        pass

    def test_full_lanczos_2devices(self):
        """
        Full Lanczos on 2 GPUs for N=16,18.
        Compare eigenvalues with exact diagonalization (even parity sector).
        """
        pass

    def test_full_lanczos_allDevices(self):
        """Same as 2-device full Lanczos but uses all GPUs."""
        pass

    def test_alloc_and_memset(self):
        """Allocate on device 0 and 1, memset on correct devices."""
        pass

class CudaMultiGpuHamiltonianNaiveTest(unittest.TestCase):

    def test_sanity(self):
        """Create CudaMultiGpuHamiltonianNaive on 2 GPUs."""
        pass

    def test_act_even(self):
        """Compare naive multi-GPU act_even with host for N=22,24."""
        pass

    def test_act_even_two_remaining_chunks(self):
        """Test chunk combining for N=18 with limited memory."""
        pass

    def test_full_lanczos(self):
        """Full Lanczos on 2 GPUs using naive approach for N=16,18."""
        pass

class CudaStateTest(unittest.TestCase):

    def test_allocation_cross_device(self):
        """Allocate CudaEvenState on device 0, delete from device 1."""
        pass

class CudaResourceManagerTest(unittest.TestCase):

    def test_allocation_cross_device(self):
        """Create CudaResourceManager on device 0, delete from device 1."""
        pass

if __name__ == "__main__":
    unittest.main()
```
