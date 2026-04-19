# partition-function-single-sample.cc — Python Pseudocode

Compute time-dependent partition function z(t) = Z(beta,t)/Z(beta,0) for a single sample.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.spectrum_file = ""
        self.output_file = ""
        self.betas = [0, 1, 5, 10, 20, 30]
        self.t_provided = False
        self.t_start = 0.1
        self.t_end = 1.0
        self.t_step = 1.0
        self.Z_cutoff = None
        self.scan_for_cutoff = False
        self.log_t_step = False
        self.no_Q_column = False
        self.Q = -1

def compute_sample_Z(beta, t, evs):
    return sum(np.exp(-complex(beta, t) * E) for E in evs)

def process_sample_evs(betas, times, evs, z_t, Z_t0):
    if len(evs) == 0:
        return
    for bi, beta in enumerate(betas):
        Z_t0[bi] = compute_sample_Z(beta, 0, evs)
        for ti, t in enumerate(times):
            z_t[bi][ti] = compute_sample_Z(beta, t, evs) / Z_t0[bi]

def main():
    opts = parse_command_line_options(sys.argv)

    # Build time array
    times = []
    if opts.t_provided:
        t = opts.t_start
        while t <= opts.t_end:
            times.append(t)
            t += (opts.t_step * t) if opts.log_t_step else opts.t_step
    else:
        for t in np.arange(0.02, 200, 0.02):
            times.append(t)
        t = 200.0
        while t < 10_000_000:
            times.append(t)
            t += t * 0.01

    # Read eigenvalues from spectrum file
    file = TSVFile(opts.spectrum_file)
    sample_evs = []
    while True:
        if opts.no_Q_column:
            ev = file.read_double()
            if file.eof(): break
        else:
            Q = file.read_int()
            ev = file.read_double()
            if file.eof(): break
            if opts.Q >= 0 and Q != opts.Q:
                continue
        sample_evs.append(ev)

    if opts.scan_for_cutoff:
        # Just print times where |Z(t)/Z(0)| > cutoff
        beta = opts.betas[0]
        Z_t0 = compute_sample_Z(beta, 0, sample_evs)
        for t in times:
            Z_t = compute_sample_Z(beta, t, sample_evs)
            ratio = abs(Z_t) / abs(Z_t0)
            if ratio > opts.Z_cutoff:
                print(f"{t}\t{ratio}")
    else:
        z_t = np.zeros((len(opts.betas), len(times)), dtype=complex)
        Z_t0 = [0j] * len(opts.betas)
        process_sample_evs(opts.betas, times, sample_evs, z_t, Z_t0)

        with open(opts.output_file, 'w') as out:
            out.write("#\tbeta\tt\tRe(z)\tIm(z)\tZ(t=0)\n")
            for i, beta in enumerate(opts.betas):
                for j, t in enumerate(times):
                    out.write(f"{beta}\t{t}\t{z_t[i][j].real}\t{z_t[i][j].imag}")
                    out.write(f"\t{Z_t0[i].real}\n")

if __name__ == "__main__":
    main()
```
