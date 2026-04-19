# syk-gpu-lanczos.cc — Python Pseudocode

GPU Lanczos program: find the low-energy spectrum of SYK via cuBLAS Lanczos. Supports checkpointing.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.run_name = ""
        self.data_dir = "data/lanczos"
        self.checkpoint_dir = "data/lanczos-checkpoints"
        self.N = 8
        self.J = 1.0
        self.mu = 0.0
        self.num_steps = 0
        self.checkpoint_steps = 0
        self.ev_steps = 0
        self.resume = False
        self.debug = False
        self.profile = False
        self.seed = 0
        self.rng = None

def parse_command_line_options(args) -> CommandLineOptions:
    """
    Parse: --run-name (required), --N (required), --num-steps (required),
           --data-dir, --checkpoint-dir, --J, --mu, --checkpoint-steps,
           --ev-steps, --resume, --debug, --profile, --seed, --help.
    N must be even. ev-steps must be multiple of checkpoint-steps.
    num-steps must be multiple of ev-steps.
    """
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def file_exists(filename: str) -> bool:
    import os
    return os.path.exists(filename)

def get_seed_filename(opts) -> str:
    return get_base_filename(opts.checkpoint_dir, opts.run_name) + "-seed"

def save_seed(opts):
    with open(get_seed_filename(opts), 'w') as f:
        f.write(f"{opts.seed}\n")

def load_seed(opts) -> bool:
    filename = get_seed_filename(opts)
    if file_exists(filename):
        with open(filename, 'r') as f:
            opts.seed = int(f.read().strip())
        return True
    return False

def get_lanczos_state_filename(opts) -> str:
    return get_base_filename(opts.checkpoint_dir, opts.run_name) + "-state"

def save_lanczos_results(opts, evs, errs):
    filename = get_base_filename(opts.data_dir, opts.run_name) + ".tsv"
    with open(filename, 'w') as out:
        out.write("# i eigenvalue error-estimate\n")
        for i in range(len(evs)):
            out.write(f"{i}\t{evs[i]}\t{errs[i]}\n")

def count_evs(opts, space, errs):
    """Count how many eigenvalues have error < epsilon at low and high ends."""
    num_low = sum(1 for i in range(len(errs)) if errs[i] <= epsilon)
    num_high = sum(1 for i in range(len(errs)-1, -1, -1) if errs[i] <= epsilon)
    print(f"Found {num_low} good evs at low energy")
    print(f"Found {num_high} good evs at high energy")

def run_lanczos(opts, handle, handle_sp):
    """
    Main Lanczos loop:
    1. Create J tensor and factorized space
    2. Create or resume CudaLanczos
    3. Create CudaHamiltonian (single or multi-GPU)
    4. Loop: run checkpoint_steps, save state, compute eigenvalues at ev_steps
    """
    space = FactorizedSpace.from_majorana(opts.N)
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, opts.rng)

    if opts.resume:
        lanczos = CudaLanczos(space, get_lanczos_state_filename(opts), opts.num_steps)
        print(f"Resuming from step {lanczos.current_step()}")
    else:
        initial = FactorizedParityState(space, ChargeParity.EVEN_CHARGE, opts.rng)
        lanczos = CudaLanczos(opts.num_steps, initial)

    if lanczos.current_step() >= opts.num_steps:
        print("Already done.")
        return

    mem_overhead = 500_000_000  # 0.5 GB

    if cuda_get_num_devices() == 1:
        avail = cuda_get_device_memory() - lanczos.d_alloc_size - mem_overhead
        H = CudaHamiltonian(space, Jtensor, avail, False, opts.debug)
    else:
        mem_per_device = []
        for i in range(cuda_get_num_devices()):
            m = cuda_get_device_memory(i) - mem_overhead
            if i == 0:
                m -= lanczos.d_alloc_size
            mem_per_device.append(m)
        H = CudaMultiGpuHamiltonian(space, Jtensor, mem_per_device, False, opts.debug)

    while lanczos.current_step() < opts.num_steps:
        print(f"Running Lanczos for {opts.checkpoint_steps} steps")
        timer = Timer()
        lanczos.compute(handle, handle_sp, H, opts.mu, opts.checkpoint_steps)
        timer.print()

        lanczos.save_state(get_lanczos_state_filename(opts))

        if lanczos.current_step() % opts.ev_steps == 0:
            print("Computing eigenvalues")
            evs, errs = lanczos.compute_eigenvalues_with_errors(opts.rng)
            save_lanczos_results(opts, evs, errs)
            count_evs(opts, space, errs)

    print(f"Reached {lanczos.current_step()} steps, quitting.")

def main():
    opts = parse_command_line_options(sys.argv)
    cuda_print_device_properties()
    handle = cublas_init()
    handle_sp = cusparse_init()

    if opts.resume and load_seed(opts):
        if file_exists(get_lanczos_state_filename(opts)):
            opts.resume = True
        else:
            opts.resume = False
    else:
        opts.resume = False

    opts.rng = np.random.RandomState(opts.seed)
    save_seed(opts)
    print(f"Options:\n{opts}")

    run_lanczos(opts, handle, handle_sp)

    cublas_destroy(handle)
    cusparse_destroy(handle_sp)

if __name__ == "__main__":
    main()
```
