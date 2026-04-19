# 2pt-function-disorder-average.cc — Python Pseudocode

Compute the disorder average of Majorana 2-point functions from multiple sample files.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.input_files = []
        self.output_file = ""

def parse_command_line_options(args) -> CommandLineOptions:
    """Parse: --output-file (required), positional input files."""
    opts = CommandLineOptions()
    # ... argparse ...
    return opts

def main():
    opts = parse_command_line_options(sys.argv)
    num_samples = len(opts.input_files)

    if num_samples == 0:
        print("No samples provided.")
        return

    betas = []
    times = []
    sum_Z = []
    sum_G = []
    sum_G_over_Z = []
    sum_GGstar = []

    for sample_idx, filename in enumerate(opts.input_files):
        file = TSVFile(filename)
        line = 0

        while True:
            beta = file.read_double()
            t = file.read_double()
            samp_Z = file.read_double()
            samp_re_G = file.read_double()
            samp_im_G = file.read_double()
            samp_GGstar = file.read_double()

            if file.eof():
                break

            samp_G = complex(samp_re_G, samp_im_G)

            # First sample: initialize accumulators
            if sample_idx == 0:
                betas.append(beta)
                times.append(t)
                sum_Z.append(0.0)
                sum_G.append(0j)
                sum_G_over_Z.append(0j)
                sum_GGstar.append(0.0)

            sum_Z[line] += samp_Z
            sum_G[line] += samp_G
            sum_G_over_Z[line] += samp_G / samp_Z
            sum_GGstar[line] += samp_GGstar

            line += 1

        file.close()

    # Write disorder-averaged results
    with open(opts.output_file, 'w') as out:
        out.write("#\tbeta\tt\t<Z>\tRe<G>/<Z>\tIm<G>/<Z>")
        out.write("\tRe<G/Z>\tIm<G/Z>\t<GG*>/<Z>")
        out.write("\t(<GG*>/<Z>-|<G>/<Z>|^2)/(|<G>/<Z>|^2)\n")

        for line_idx in range(len(betas)):
            avg_Z = sum_Z[line_idx] / num_samples
            avg_G = sum_G[line_idx] / num_samples
            avg_G_over_Z = sum_G_over_Z[line_idx] / num_samples
            avg_GGstar = sum_GGstar[line_idx] / num_samples

            G_corr_norm_sqr = abs(avg_G)**2 / avg_Z**2
            fractional_variance = (avg_GGstar / avg_Z - G_corr_norm_sqr) / G_corr_norm_sqr

            out.write(f"{betas[line_idx]}\t{times[line_idx]}\t{avg_Z}")
            out.write(f"\t{avg_G.real / avg_Z}\t{avg_G.imag / avg_Z}")
            out.write(f"\t{avg_G_over_Z.real}\t{avg_G_over_Z.imag}")
            out.write(f"\t{avg_GGstar / avg_Z}\t{fractional_variance}\n")

if __name__ == "__main__":
    main()
```
