# kitaev-thermodynamics.cc — Python Pseudocode

Compute thermodynamic quantities (F, E, S, Var(E)) from a spectrum file.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.spectrum_file = ""
        self.output_file = ""
        self.T_start = 0.0
        self.T_end = 0.0
        self.T_step = 0.0
        self.majorana = False

def parse_command_line_options(args) -> CommandLineOptions:
    """
    Parse: --spectrum-file (required), --output-file (required),
           --T-start (required), --T-end (required), --T-step (required),
           --majorana.
    """
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def compute_partition_function(evs: np.ndarray, beta: float) -> float:
    """Z = sum_i exp(-beta * E_i)."""
    return np.sum(np.exp(-beta * evs))

def write_thermodynamic_quantities(output, evs: np.ndarray, N: int, T: float):
    """Compute and write S/N, E/N, F/N, Var(E), Var(E)/<E-E0>^2 at temperature T."""
    beta = 1.0 / T
    Z = compute_partition_function(evs, beta)

    # Free energy
    F = -np.log(Z) / beta

    # <E> and <E^2>
    weights = np.exp(-beta * evs)
    E = np.sum(evs * weights) / Z
    Esqr = np.sum(evs**2 * weights) / Z
    E0 = np.min(evs)

    # Entropy
    S = beta * (E - F)

    # Variance
    var_E = Esqr - E**2

    output.write(f"{T}\t{S/N}\t{E/N}\t{F/N}\t{var_E}\t{var_E / (E - E0)**2}\n")

def main():
    opts = parse_command_line_options(sys.argv)

    if opts.majorana:
        s = MajoranaSpectrum(opts.spectrum_file)
        evs = s.all_eigenvalues()
        N = s.majorana_N
    else:
        s = Spectrum(opts.spectrum_file)
        evs = s.all_eigenvalues()
        N = s.N

    with open(opts.output_file, 'w') as output:
        output.write("# T/J S/N E/N F/N Var(E) Var(E)/<E-E0>^2\n")
        T = opts.T_start
        while T <= opts.T_end:
            write_thermodynamic_quantities(output, evs, N, T)
            T += opts.T_step

if __name__ == "__main__":
    main()
```
