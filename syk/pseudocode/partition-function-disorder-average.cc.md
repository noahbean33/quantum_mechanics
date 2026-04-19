# partition-function-disorder-average.cc — Python Pseudocode

Compute disorder average of partition function quantities from multiple single-sample files.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.input_files = []
        self.output_file = ""

def main():
    opts = parse_command_line_options(sys.argv)
    num_samples = len(opts.input_files)
    if num_samples == 0:
        print("No samples provided.")
        return

    betas, times = [], []
    sum_Z, sum_G, sum_ZZ, sum_ZG, sum_Z4 = [], [], [], [], []
    sum_Z_t0, sum_G_t0 = [], []

    for sample_idx, filename in enumerate(opts.input_files):
        file = TSVFile(filename)
        line = 0
        while True:
            beta = file.read_double()
            t = file.read_double()
            re_z = file.read_double()
            im_z = file.read_double()
            Z_t0 = file.read_double()
            if file.eof():
                break

            z = complex(re_z, im_z)
            Z = z * Z_t0

            if sample_idx == 0:
                betas.append(beta); times.append(t)
                sum_Z.append(0j); sum_G.append(0.0)
                sum_ZZ.append(0j); sum_ZG.append(0j); sum_Z4.append(0.0)
                sum_Z_t0.append(0.0); sum_G_t0.append(0.0)

            sum_Z[line] += Z
            sum_G[line] += abs(Z)**2
            sum_ZZ[line] += Z**2
            sum_ZG[line] += Z * abs(Z)**2
            sum_Z4[line] += abs(Z)**4
            sum_Z_t0[line] += Z_t0
            sum_G_t0[line] += Z_t0**2
            line += 1
        file.close()

    with open(opts.output_file, 'w') as out:
        out.write("#\tbeta\tt\t<Re Z>/<Z(0)>\t<Im Z>/<Z(0)>")
        out.write("\tG\tG_c\tG_d\tG4\tG4c\n")
        for line in range(len(betas)):
            n = num_samples
            avg_Z = sum_Z[line] / sum_Z_t0[line]
            avg_G = n * sum_G[line] / sum_Z_t0[line]**2
            avg_Gd = abs(avg_Z)**2
            avg_Gc = avg_G - avg_Gd
            # Fourth-order cumulant (connected)
            avg_G4 = (sum_Z4[line]/n
                       - 4*np.real(sum_ZG[line]*np.conj(sum_Z[line]))/n**2
                       + 4*abs(sum_Z[line])**2*sum_G[line]/n**3
                       + 2*np.real(sum_ZZ[line]*np.conj(sum_Z[line])**2)/n**3
                       - 3*abs(sum_Z[line])**4/n**4
                      ) / (sum_Z_t0[line]**4 / n**4)
            avg_G4c = avg_G4 - avg_Gc**2

            out.write(f"{betas[line]}\t{times[line]}\t{avg_Z.real}\t{avg_Z.imag}")
            out.write(f"\t{avg_G}\t{avg_Gc}\t{avg_Gd}\t{avg_G4}\t{avg_G4c}\n")

if __name__ == "__main__":
    main()
```
