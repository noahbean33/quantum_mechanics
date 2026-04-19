# CudaState.h — Python Pseudocode

Even-parity state stored on the GPU as two dense blocks.

```python
import numpy as np

class CudaEvenState:
    """
    A state with even charge parity, stored on the GPU.
    Only the non-zero blocks are stored: top-left and bottom-right
    of the factorized state matrix. They are contiguous in GPU memory.
    """

    def __init__(self, space: 'FactorizedSpace', init=None, rng=None):
        self.space = space
        self.block_rows = space.left.D // 2
        self.block_cols = space.right.D // 2
        self.block_size = self.block_rows * self.block_cols
        self.block_alloc_size = 16 * self.block_size  # sizeof(complex128)
        self.device_id = cuda_get_device()

        # Allocate one contiguous chunk for both blocks on the GPU
        self.d_top_left_block = d_alloc(self.block_alloc_size * 2)
        self.d_bottom_right_block = self.d_top_left_block  # offset by block_size

        if isinstance(init, np.ndarray):
            self.set(init)
        elif rng is not None:
            random_state = get_factorized_random_state(space, ChargeParity.EVEN_CHARGE, rng)
            self.set(random_state)

    def destroy(self):
        if self.d_top_left_block is not None:
            d_free(self.d_top_left_block)
            self.d_top_left_block = None
            self.d_bottom_right_block = None

    def size(self) -> int:
        return self.block_size * 2

    def get_matrix(self) -> np.ndarray:
        """Copy state from GPU back to host as a full matrix."""
        matrix = np.zeros((self.block_rows * 2, self.block_cols * 2), dtype=complex)
        matrix[:self.block_rows, :self.block_cols] = \
            copy_matrix_device_to_host(self.d_top_left_block, self.block_rows, self.block_cols)
        matrix[self.block_rows:, self.block_cols:] = \
            copy_matrix_device_to_host(self.d_bottom_right_block, self.block_rows, self.block_cols)
        return matrix

    def set(self, matrix_or_state):
        """Set from a full matrix or another CudaEvenState."""
        if isinstance(matrix_or_state, np.ndarray):
            matrix = matrix_or_state
            top = matrix[:self.block_rows, :self.block_cols]
            bottom = matrix[self.block_rows:, self.block_cols:]
            copy_matrix_host_to_device(self.d_top_left_block, top)
            copy_matrix_host_to_device(self.d_bottom_right_block, bottom)
        elif isinstance(matrix_or_state, CudaEvenState):
            # Device-to-device copy
            cuda_memcpy_d2d(self.d_top_left_block, matrix_or_state.d_top_left_block,
                            16 * self.block_size * 2)

    def set_async(self, other: 'CudaEvenState', stream):
        """Async device-to-device copy."""
        cuda_memcpy_async_d2d(self.d_top_left_block, other.d_top_left_block,
                              16 * self.block_size * 2, stream)

    def set_to_zero(self):
        cuda_memset(self.d_top_left_block, 0, 16 * self.block_size)
        cuda_memset(self.d_bottom_right_block, 0, 16 * self.block_size)

    def add(self, handle, alpha, other: 'CudaEvenState'):
        """self += alpha * other (cuBLAS Zaxpy on both blocks contiguously)."""
        add_vector_times_scalar(handle, self.d_top_left_block, alpha,
                                other.d_top_left_block, self.block_size * 2)

    def dot(self, handle, result, other: 'CudaEvenState'):
        """<self | other> (conjugated dot product), written to device result."""
        # cuBLAS Zdotc on contiguous blocks
        pass

    def norm(self, handle, result):
        """||self||_2 into device result."""
        # cuBLAS Dznrm2
        pass

    def scale(self, handle, alpha):
        """self *= alpha (cuBLAS Zdscal)."""
        pass
```
