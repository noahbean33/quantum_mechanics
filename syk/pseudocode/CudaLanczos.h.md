# CudaLanczos.h — Python Pseudocode

GPU-accelerated Lanczos algorithm using CudaHamiltonian.

```python
import numpy as np

class CudaLanczos:
    """
    Lanczos algorithm running entirely on the GPU.
    States (v_i) are CudaEvenStates; alpha/beta coefficients live on the device.
    Supports checkpointing (save/load state to resume).
    """

    def __init__(self, max_steps_or_space, initial_state_or_filename=None, max_steps=None):
        if isinstance(initial_state_or_filename, FactorizedParityState):
            # Initialize from an initial state
            initial_state = initial_state_or_filename
            assert initial_state.charge_parity == ChargeParity.EVEN_CHARGE
            self.space = initial_state.space
            self.iter = 1
            self.m = max_steps_or_space  # max_steps

            self._alloc_states()
            self._alloc_coeffs()
            self.vi.set(initial_state.matrix)
        else:
            # Load from checkpoint file
            self.space = max_steps_or_space
            self._alloc_states()
            self._load_state(initial_state_or_filename, max_steps)

        self.minus_one = CudaScalar(-1.0, 0.0)

    def _alloc_states(self):
        """Allocate 4 CudaEvenStates (vi_minus_1, vi, u, work) + scalar d_s."""
        zero = np.zeros((self.space.left.D, self.space.right.D), dtype=complex)
        self.vi_minus_1 = CudaEvenState(self.space, zero)
        self.vi = CudaEvenState(self.space, zero)
        self.u = CudaEvenState(self.space, zero)
        self.work = CudaEvenState(self.space, zero)
        self.d_s = d_alloc(8)  # sizeof(double)
        self.zero_state = zero

    def _alloc_coeffs(self):
        """Allocate device arrays for alpha (length m) and beta (length m+1)."""
        self.d_alpha = d_alloc(16 * self.m)       # cucpx * m
        self.d_beta = d_alloc(16 * (self.m + 1))  # cucpx * (m+1)
        # Zero them out
        cuda_memset(self.d_alpha, 0, 16 * self.m)
        cuda_memset(self.d_beta, 0, 16 * (self.m + 1))

    def compute(self, handle, handle_sp, H: CudaHamiltonianInterface,
                mu: float, steps: int):
        """
        Run 'steps' Lanczos iterations on the GPU.

        For each iteration i:
            u = H * vi                              # GPU Hamiltonian action
            u -= beta[i-1] * vi_minus_1             # cuBLAS axpy
            u += mu * vi                            # shift
            alpha[i] = Re(<u, vi>)                  # cuBLAS Zdotc
            u -= alpha[i] * vi                      # cuBLAS axpy
            beta[i] = ||u||                         # cuBLAS Dznrm2
            vi_minus_1, vi = vi, u / beta[i]        # swap + scale
        """
        d_mu = CudaScalar(mu, 0.0)
        target = self.iter + steps

        for _ in range(self.iter, target):
            # u = H * vi
            H.act_even(self.u, self.vi)

            # work = beta[iter-1] * vi_minus_1
            self.work.set(self.zero_state)
            self.work.add(handle, self.d_beta + self.iter - 1, self.vi_minus_1)

            # u -= work
            self.u.add(handle, self.minus_one.ptr, self.work)

            # u += mu * vi
            self.u.add(handle, d_mu.ptr, self.vi)

            # alpha[iter-1] = <u, vi>.real
            self.u.dot(handle, self.d_alpha + self.iter - 1, self.vi)
            # Set imaginary part to zero (take real part only)

            # u -= alpha[iter-1] * vi
            self.work.set(self.zero_state)
            self.work.add(handle, self.d_alpha + self.iter - 1, self.vi)
            self.u.add(handle, self.minus_one.ptr, self.work)

            # beta[iter] = ||u||
            self.u.norm(handle, self.d_beta + self.iter)

            # swap: vi_minus_1, vi = vi, u/beta[iter]
            self.vi_minus_1, self.vi = self.vi, self.vi_minus_1
            d_inverse(self.d_s, self.d_beta + self.iter)
            self.vi.set(self.u)
            self.vi.scale(handle, self.d_s)

            self.iter += 1

    def read_coeffs(self) -> tuple:
        """Copy alpha, beta from device to host as real vectors."""
        n = self.iter - 1
        alpha = np.zeros(n)
        beta = np.zeros(n - 1)
        # Copy real parts from interleaved complex device arrays
        return alpha, beta

    def compute_eigenvalues(self) -> np.ndarray:
        """Compute good Lanczos eigenvalues from current coefficients."""
        alpha, beta = self.read_coeffs()
        return find_good_lanczos_evs(alpha, beta)

    def compute_eigenvalues_with_errors(self, rng) -> tuple:
        """Compute good eigenvalues + error estimates."""
        alpha, extended_beta = self._read_coeffs_extended()
        errors = np.zeros(0)
        evs = find_good_lanczos_evs_and_errs(alpha, extended_beta, errors, rng)
        return evs, errors

    def save_state(self, filename: str):
        """Save current state to binary file for checkpointing."""
        vi_mat = self.vi.get_matrix()
        vi_m1_mat = self.vi_minus_1.get_matrix()
        alpha = self._read_device_vec(self.d_alpha, self.m)
        beta = self._read_device_vec(self.d_beta, self.m + 1)
        with open(filename, 'wb') as f:
            f.write(self.iter.to_bytes(4, 'little'))
            f.write(self.m.to_bytes(4, 'little'))
            write_matrix_binary(f, vi_mat)
            write_matrix_binary(f, vi_m1_mat)
            write_vector_binary(f, alpha)
            write_vector_binary(f, beta)

    @staticmethod
    def get_state_info(filename: str) -> tuple:
        """Read (num_steps, max_steps) from a checkpoint file without loading."""
        with open(filename, 'rb') as f:
            iter_val = int.from_bytes(f.read(4), 'little')
            max_steps = int.from_bytes(f.read(4), 'little')
        return iter_val - 1, max_steps

    def _load_state(self, filename: str, max_steps: int):
        """Load state from a checkpoint file."""
        with open(filename, 'rb') as f:
            self.iter = int.from_bytes(f.read(4), 'little')
            self.m = int.from_bytes(f.read(4), 'little')
            self.d_alloc_size = int.from_bytes(f.read(8), 'little')
            vi_mat = read_matrix_binary(f)
            vi_m1_mat = read_matrix_binary(f)
            alpha = read_vector_binary(f)
            beta = read_vector_binary(f)
        self.m = max(self.m, max_steps)
        self.vi.set(vi_mat)
        self.vi_minus_1.set(vi_m1_mat)
        self._alloc_coeffs()
        # Copy alpha, beta to device

    def current_step(self) -> int:
        return self.iter - 1

    def max_steps(self) -> int:
        return self.m
```
