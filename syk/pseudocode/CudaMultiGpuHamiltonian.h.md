# CudaMultiGpuHamiltonian.h — Python Pseudocode

Multi-GPU Hamiltonian: splits operators evenly across GPUs for parallel execution.

```python
class CudaMultiGpuHamiltonian(HamiltonianTermProcessor, CudaHamiltonianInterface):
    """
    Splits the factorized Hamiltonian operators across multiple GPUs.
    Each GPU holds a CudaHamiltonian with a subset of operator chunks.
    During act_even:
      1. Copy the input state to all GPUs
      2. Each GPU computes its partial H * state in parallel
      3. Collect and sum all partial results on GPU 0
    """

    def __init__(self, space, Jtensor, available_memory_per_device,
                 mock=False, debug=False):
        self.space = space
        self.debug = debug
        self.hamiltonians = []       # one CudaHamiltonian per GPU
        self.input_states = {}       # device_id → CudaEvenState
        self.output_states = {}      # device_id → CudaEvenState

        n_devices = len(available_memory_per_device)

        # Distribute operator pairs round-robin across devices
        self._prepare_op_chunks(space, available_memory_per_device)

        # Generate and distribute terms
        generate_factorized_hamiltonian_terms(space, Jtensor, mock, self)

        # Allocate input/output state buffers on each device
        for device_id in range(n_devices):
            cuda_set_device(device_id)
            self.input_states[device_id] = CudaEvenState(space)
            self.output_states[device_id] = CudaEvenState(space)

    def process(self, left_idx: int, ops_pair: 'FactorizedOperatorPair'):
        """Route each operator pair to the next GPU in round-robin order."""
        target = self._get_next_device_id()
        self.hamiltonians[target].process(left_idx, ops_pair)

    def act_even(self, output: 'CudaEvenState', state: 'CudaEvenState'):
        """
        1. Copy state from GPU 0 to all other GPUs
        2. Each GPU computes partial_output = H_local * state (in parallel)
        3. Copy partial outputs back to GPU 0 and sum into output
        """
        # Step 1: broadcast state
        for device_id, in_state in self.input_states.items():
            in_state.set(state)

        # Step 2: parallel computation (one thread per GPU)
        for device_id, H_local in enumerate(self.hamiltonians):
            cuda_set_device(device_id)
            H_local.act_even(self.output_states[device_id],
                             self.input_states[device_id])

        # Step 3: collect results on GPU 0
        output.set_to_zero()
        for device_id, out_state in self.output_states.items():
            # Copy out_state to GPU 0, add to output
            output.add(handle, one, out_state)

    def total_h_alloc_size(self) -> int:
        return sum(h.total_h_alloc_size() for h in self.hamiltonians)

    def total_d_alloc_size(self) -> int:
        return sum(h.total_d_alloc_size() for h in self.hamiltonians)

    def predicted_total_d_alloc_size(self) -> int:
        return sum(h.predicted_total_d_alloc_size() for h in self.hamiltonians)

    def _prepare_op_chunks(self, space, memory_per_device):
        pass

    def _get_next_device_id(self) -> int:
        pass
```
