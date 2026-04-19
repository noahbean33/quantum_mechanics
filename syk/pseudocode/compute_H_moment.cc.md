# compute_H_moment.cc — Python Pseudocode

Compute Tr(H^2) = sum_{i<j<k<l} J_{ijkl}^2 for a Majorana Hamiltonian (without constructing H).

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.N = 0
        self.J = 1.0
        self.seed_file = ""

def parse_command_line_options(args) -> CommandLineOptions:
    """Parse: --N (required), --J, --seed-file (required)."""
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def main():
    opts = parse_command_line_options(sys.argv)

    # Read seed from file
    with open(opts.seed_file, 'r') as f:
        seed = int(f.read().strip())

    rng = np.random.RandomState(seed)
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, rng)

    # Compute Tr(H^2) = sum_{i<j<k<l} J_{ijkl}^2
    TrH2 = 0.0
    for i in range(opts.N):
        for j in range(i + 1, opts.N):
            for k in range(j + 1, opts.N):
                for l in range(k + 1, opts.N):
                    Jijkl = Jtensor.elem(i, j, k, l)
                    TrH2 += Jijkl * Jijkl

    print(TrH2)

if __name__ == "__main__":
    main()
```
