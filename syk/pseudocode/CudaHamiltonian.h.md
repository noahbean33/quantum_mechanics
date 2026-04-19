# CudaHamiltonian.h — Python Pseudocode

GPU-accelerated factorized Hamiltonian: stores operator blocks on device, acts via cuBLAS/cuSPARSE.

```python
from abc import ABC, abstractmethod

class CudaHamiltonianInterface(ABC):
    """Abstract interface for GPU Hamiltonians."""

    @abstractmethod
    def act_even(self, output: 'CudaEvenState', state: 'CudaEvenState'):
        """Act with H on even-parity state. Result goes to device memory."""
        pass

    @abstractmethod
    def total_h_alloc_size(self) -> int:
        """Total host memory allocated."""
        pass

    @abstractmethod
    def total_d_alloc_size(self) -> int:
        """Total device memory allocated."""
        pass


class ActionContext:
    """Holds CUDA streams for async chunk processing."""
    def __init__(self, manager: 'CudaResourceManager'):
        self.memcpy_stream = manager.get_stream()
        self.kernel_stream = manager.get_stream()
        self.resident_chunk = 0


class CudaHamiltonian(HamiltonianTermProcessor, CudaHamiltonianInterface):
    """
    GPU factorized Hamiltonian. Splits operators into chunks that fit in device memory.
    Each chunk contains left/right operator pairs stored as sparse + dense blocks.

    Key workflow:
    1. Generate factorized terms (O_L ⊗ O_R pairs)
    2. Split into chunks based on available GPU memory
    3. For each chunk: copy to device, multiply sparse*state*dense, sum results
    """

    def __init__(self, space, Jtensor, available_device_memory,
                 mock=False, debug=False):
        self.space = space
        self.device_id = 0
        self.op_chunks = []  # list of HamiltonianData chunks
        self.debug = debug

        # Generate all operator pairs and distribute into chunks
        self._basic_init(space, 0, debug)
        self._prepare_op_chunks(available_device_memory)
        generate_factorized_hamiltonian_terms(space, Jtensor, mock, self)
        self._finalize_construction(available_device_memory)

    def process(self, left_idx: int, ops_pair: 'FactorizedOperatorPair'):
        """Callback: store each operator pair into the appropriate chunk."""
        # Find which chunk this operator belongs to and add it
        pass

    def act_even(self, output: 'CudaEvenState', state: 'CudaEvenState'):
        """
        Act with H on state. For each chunk:
          1. Copy chunk data to device (if not already resident)
          2. For each block (top/bottom):
             a. Multiply sparse_left * state_block → intermediate
             b. Multiply intermediate * dense_right → term_contribution
             c. Sum all term contributions
          3. Add chunk result to output
        """
        output.set_to_zero()
        for chunk in self.op_chunks:
            self._launch_chunk_kernels(output, state, chunk)

    def _launch_chunk_kernels(self, output, state, chunk):
        """
        For a single chunk of operators, compute the contribution to output.
        Uses cuSPARSE for sparse*dense products and cuBLAS for dense*dense.
        """
        for block_pos in [TOP_BLOCK, BOTTOM_BLOCK]:
            # For left-sparse terms: sparse_L * state * dense_R
            # For right-sparse terms: dense_L * state * sparse_R (via transpose trick)
            pass

    def act_even_chunk_async(self, output, state, context: ActionContext) -> bool:
        """Start async processing of one chunk. Returns False when done."""
        if context.resident_chunk >= len(self.op_chunks):
            return False
        # Launch kernels, advance context
        context.resident_chunk += 1
        return True

    def _basic_init(self, space, device_id, debug):
        self.space = space
        self.device_id = device_id

    def _prepare_op_chunks(self, available_memory):
        """Decide how to split operators into device-memory-sized chunks."""
        pass

    def total_h_alloc_size(self) -> int:
        return sum(c.h_alloc_size for c in self.op_chunks)

    def total_d_alloc_size(self) -> int:
        return sum(c.d_alloc_size for c in self.op_chunks)

    def predicted_total_d_alloc_size(self) -> int:
        return sum(c.predicted_d_alloc_size() for c in self.op_chunks)


class PinnedRowMajorSpMat:
    """Sparse matrix in CSR format, stored in pinned (page-locked) host memory."""
    def __init__(self, sp_matrix):
        self.rows = sp_matrix.shape[0]
        self.cols = sp_matrix.shape[1]
        self.nz_elems = sp_matrix.nnz
        # Store values, row_ptr, col_ind in pinned memory for fast H→D transfer


class HamiltonianData:
    """
    One chunk of Hamiltonian operator data (host + device).
    Contains left/right operators as sparse + dense blocks,
    plus working memory for intermediate products.
    """

    def __init__(self, space):
        self.space = space
        self.num_operators = {}  # left_idx → count
        self.h_alloc_size = 0
        self.d_alloc_size = 0

    def total_num_operators(self) -> int:
        return sum(self.num_operators.values())

    def alloc_host_memory(self):
        """Allocate pinned host memory based on num_operators."""
        pass

    def add_op_pair(self, left_idx, idx, ops_pair):
        """Add an operator pair to this chunk's host memory."""
        pass

    def finalize_host_memory(self):
        """Prepare sparse matrices and copy dense ones to pinned memory."""
        pass

    def predicted_d_alloc_size(self) -> int:
        """Estimate required device memory for stored operators."""
        pass

    def copy_to_device(self, allocator, stream=None):
        """Copy all host data to device memory."""
        pass

    def free_device_objects(self):
        pass

    def free_host_memory(self):
        pass


class SomeHamiltonianTermBlocks:
    """
    GPU working memory for one set of operator blocks (top or bottom).
    Stores sparse operator data, dense operator data, intermediate products,
    and the final sum.
    """
    def __init__(self):
        self.d_sparse_values = None
        self.d_sparse_row_ptr = None
        self.d_sparse_col_ind = None
        self.d_dense_ops = None
        self.d_sparse_prod = None   # sparse * state intermediate
        self.d_final_prod = None    # sparse * state * dense intermediate
        self.d_sum = None           # sum of all term contributions
        self.num_blocks = 0
```
