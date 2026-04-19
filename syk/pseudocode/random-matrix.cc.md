# random-matrix.cc — Python Pseudocode

Generate and diagonalize a random matrix from various ensembles.

```python
import numpy as np

class Ensemble:
    GUE = 1
    GOE = 2
    SparseKlogK = 3

class CommandLineOptions:
    def __init__(self):
        self.run_name = ""
        self.data_dir = "data"
        self.K = 0          # matrix rank
        self.ensemble = None
        self.seed = 0

def parse_command_line_options(args) -> CommandLineOptions:
    """Parse: --run-name (required), --K (required), --GUE/--GOE/--SparseKlogK, --data-dir, --seed."""
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def main():
    opts = parse_command_line_options(sys.argv)
    rng = np.random.RandomState(opts.seed)
    print(f"Command line options:\n{opts}")

    print("Constructing Hamiltonian...")
    timer = Timer()

    if opts.ensemble == Ensemble.GUE:
        matrix = GUERandomMatrix(opts.K, rng)
    elif opts.ensemble == Ensemble.GOE:
        matrix = GOERandomMatrix(opts.K, rng)
    elif opts.ensemble == Ensemble.SparseKlogK:
        num_nonzeros = int(opts.K * np.log(opts.K))
        matrix = SparseHermitianRandomMatrix(opts.K, num_nonzeros, rng)

    timer.print()

    print("Diagonalizing Hamiltonian...")
    timer.reset()
    evs = matrix.eigenvalues()
    timer.print()

    filename = get_base_filename(opts.data_dir, opts.run_name) + "-spectrum.tsv"
    print(f"Saving spectrum to {filename}")
    with open(filename, 'w') as f:
        f.write("# eigenvalue\n")
        for ev in evs:
            f.write(f"{ev}\n")

if __name__ == "__main__":
    main()
```
