# partition-function.cc — Python Pseudocode

Compute time-dependent partition function Z(beta, t) and disorder average over samples.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.spectrum_file = ""
        self.output_file = ""
        self.betas = []
        self.t_provided = False
        self.t_start = 0.1
        self.t_end = 1.0
        self.t_step = 1.0
        self.log_t_step = False
        self.no_Q_column = False
        self.Q = -1           # filter by Q sector (-1 = all)
        self.max_samples = -1
        self.single_sample = False

def parse_command_line_options(args) -> CommandLineOptions:
    """
    Parse: --spectrum-file (required), --output-file (required),
           --betas (required, comma-separated), --t-start, --t-end, --t-step,
           --log-t-step, --max-samples, --single-sample, --no-Q-column, --Q.
    """
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def compute_sample_Z(beta: float, t: float, evs: list) -> complex:
    """Z = Tr(exp(-(beta + it) * H)) = sum_i exp(-(beta + it) * E_i)."""
    Z = 0 + 0j
    for Ei in evs:
        Z += np.exp(-complex(beta, t) * Ei)
    return Z

def process_sample_evs(betas, times, evs, z_t, zzstar_t, num_samples):
    """
    For one sample's eigenvalues, compute Z(beta,t)/Z(beta,0) and
    |Z(beta,t)|^2/|Z(beta,0)|^2, accumulate into disorder averages.
    """
    if len(evs) == 0:
        return
    num_samples[0] += 1

    for bi, beta in enumerate(betas):
        Z_t0 = compute_sample_Z(beta, 0, evs)
        for ti, t in enumerate(times):
            sample_Z = compute_sample_Z(beta, t, evs)
            z_t[bi][ti] += sample_Z / Z_t0
            zzstar_t[bi][ti] += abs(sample_Z)**2 / abs(Z_t0)**2

def main():
    opts = parse_command_line_options(sys.argv)

    # Build time array (linear or logarithmic steps)
    times = []
    if opts.t_provided:
        t = opts.t_start
        while t <= opts.t_end:
            times.append(t)
            t += (opts.t_step * t) if opts.log_t_step else opts.t_step
    else:
        # Default: fine grid 0.02..200, then log grid 200..100000
        for t in np.arange(0.02, 200, 0.02):
            times.append(t)
        t = 200.0
        while t < 100000:
            times.append(t)
            t += t * 0.01

    # Read spectrum file sample-by-sample
    file = TSVFile(opts.spectrum_file)
    num_samples = [0]
    z_t = np.zeros((len(opts.betas), len(times)), dtype=complex)
    zzstar_t = np.zeros((len(opts.betas), len(times)), dtype=complex)
    sample_evs = []
    last_sample = -1

    while True:
        if not opts.single_sample:
            sample = file.read_int()

        if opts.no_Q_column:
            ev = file.read_double()
            if file.eof():
                break
        else:
            Q = file.read_int()
            ev = file.read_double()
            if file.eof():
                break
            if opts.Q >= 0 and opts.Q != Q:
                continue

        if not opts.single_sample and last_sample != sample:
            last_sample = sample
            process_sample_evs(opts.betas, times, sample_evs,
                               z_t, zzstar_t, num_samples)
            sample_evs = []
            if 0 <= opts.max_samples <= num_samples[0]:
                break

        sample_evs.append(ev)

    # Process last sample
    process_sample_evs(opts.betas, times, sample_evs, z_t, zzstar_t, num_samples)

    # Normalize by number of samples
    n = num_samples[0]
    z_t /= n
    zzstar_t /= n

    # Write output: beta, t, <Re z(t)>, <Im z(t)>, g=<zz*>, g_c, g_d
    with open(opts.output_file, 'w') as out:
        out.write("#\tbeta\tt\t<Re z(t)>\t<Im z(t)>\tg=<z(t)z*(t)>")
        out.write("\tg_c=<zz*>-<z><z*>\tg_d=|<z>|^2\n")
        for i, beta in enumerate(opts.betas):
            for j, t in enumerate(times):
                g_d = abs(z_t[i][j])**2
                out.write(f"{beta}\t{t}\t{z_t[i][j].real}\t{z_t[i][j].imag}")
                out.write(f"\t{zzstar_t[i][j].real}\t{zzstar_t[i][j].real - g_d}\t{g_d}\n")

if __name__ == "__main__":
    main()
```
