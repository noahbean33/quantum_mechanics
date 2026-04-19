# syk-gpu-benchmark.cc — Python Pseudocode

GPU benchmarking suite for SYK Hamiltonian, Lanczos, cuBLAS gemm, and memcpy.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.run_name = "test"
        self.data_dir = "data/lanczos"
        self.N = 8
        self.N2 = 8
        self.J = 1.0
        self.mu = 0.0
        self.available_memory_gb = 5.0
        self.available_memory = int(5e9)
        self.steps = 20
        self.streams = False
        self.seed = 0
        self.mock_hamiltonian = False
        self.debug = False
        self.profile = False
        self.rng = None

def benchmark_single_lanczos(opts, handle, handle_sp, space):
    """Time creating H and running 'steps' Lanczos iterations."""
    Jtensor = MajoranaKitaevDisorderParameter(space.N, 1.0, opts.rng)
    initial = FactorizedParityState(space, ChargeParity.EVEN_CHARGE, opts.rng)
    timer = Timer()
    H = CudaHamiltonian(space, Jtensor, opts.available_memory, opts.mock_hamiltonian, opts.debug)
    H_time = timer.seconds()
    timer.reset()
    lanczos = CudaLanczos(opts.steps, initial)
    lanczos.compute(handle, handle_sp, H, 1.0, opts.steps)
    lanc_time = timer.msecs()
    print(f"N={space.N}  H={H_time:.0f}s  lanczos={lanc_time/opts.steps:.1f}ms/step")

def benchmark_lanczos(opts, handle, handle_sp, min_N, max_N):
    for N in range(min_N, max_N + 1, 2):
        benchmark_single_lanczos(opts, handle, handle_sp, FactorizedSpace.from_majorana(N))

def benchmark_act(opts):
    """Benchmark H.act_even repeated 'steps' times."""
    space = FactorizedSpace.from_majorana(opts.N)
    Jtensor = MajoranaKitaevDisorderParameter(space.N, 1.0, opts.rng)
    state = CudaEvenState(space)
    output = CudaEvenState(space)
    H = CudaHamiltonian(space, Jtensor, opts.available_memory, opts.mock_hamiltonian)
    H.act_even(output, state)  # warmup
    timer = Timer()
    for _ in range(opts.steps):
        H.act_even(output, state)
    print(f"N={space.N}  time={timer.msecs()/opts.steps:.1f} ms/act")

def benchmark_act_multi_gpu(opts):
    """Same as benchmark_act but on multiple GPUs."""
    space = FactorizedSpace.from_majorana(opts.N)
    Jtensor = MajoranaKitaevDisorderParameter(space.N, 1.0, opts.rng)
    state = CudaEvenState(space)
    output = CudaEvenState(space)
    H = CudaMultiGpuHamiltonian(space, Jtensor, opts.available_memory, opts.mock_hamiltonian)
    H.act_even(output, state)  # warmup
    timer = Timer()
    for _ in range(opts.steps):
        H.act_even(output, state)
    print(f"Multi-GPU: N={space.N}  time={timer.msecs()/opts.steps:.1f} ms/act")

def benchmark_hemm(opts, handle):
    """Benchmark cuBLAS Zhemm and Zgemm on 4096x4096 matrices."""
    pass

def benchmark_memcpy(opts):
    """Benchmark host→device memcpy for pageable and pinned memory."""
    pass

def benchmark_gemm_and_memcpy(opts, handle, handle_sp):
    """Benchmark concurrent gemm + memcpy with/without CUDA streams."""
    pass

def benchmark_multiply_right_dense(opts, handle, handle_sp):
    """Benchmark batched Zgemm (the core of CudaHamiltonian::multiply_right_dense)."""
    pass

def main():
    opts = parse_command_line_options(sys.argv)
    cuda_print_device_properties()
    handle = cublas_init()
    handle_sp = cusparse_init()

    if opts.profile:
        pass  # profile_act or benchmark_gemm_and_memcpy
    else:
        benchmark_act_multi_gpu(opts)

    cublas_destroy(handle)
    cusparse_destroy(handle_sp)

if __name__ == "__main__":
    main()
```
