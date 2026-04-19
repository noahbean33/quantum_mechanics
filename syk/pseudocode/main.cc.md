# main.cc — Python Pseudocode

Main entry point for the SYK program. Parses command-line options and dispatches to the appropriate computation.

```python
import argparse
import numpy as np

rng = None  # global random number generator

class CommandLineOptions:
    def __init__(self):
        self.run_name = ""
        self.data_dir = "data"
        self.N = 0
        self.J = 1.0
        self.real_J = False
        self.seed = 0
        self.majorana = False
        self.compute_2_pt_func = False
        self.compute_2_pt_func_with_fluctuations = False
        self.compute_fermion_matrix = False
        self.compute_anti_commutator = False
        self.betas = []
        self.t0 = 0.0
        self.t1 = 0.0
        self.dt = 0.0
        self.time_type = TIME_TYPE.REAL_TIME

def get_betas_from_beta_range(beta0, beta1, dbeta):
    betas = []
    beta = beta0
    while beta <= beta1:
        betas.append(beta)
        beta += dbeta
    return betas

def get_betas_from_T_range(T0, T1, dT):
    betas = []
    T = T0
    while T <= T1:
        betas.append(1.0 / T)
        T += dT
    return betas

def parse_command_line_options(args) -> CommandLineOptions:
    """
    Parse command-line arguments using boost::program_options equivalent.
    Required: --run-name, --N
    Optional: --data-dir, --J, --real-J, --majorana, --2pt,
              --2pt-with-fluctuations, --compute-fermion-matrix,
              --anti-commutator, --T0/T1/dT, --beta/beta0/beta1/dbeta,
              --t0/t1/dt, --euclidean-t, --seed, --help
    """
    opts = CommandLineOptions()
    # ... argparse setup and validation ...
    # If majorana: N must be even
    # If 2pt: betas and t0 required
    # If seed not given: opts.seed = get_random_seed(opts.run_name)
    return opts

def get_times_vector(opts) -> list:
    times = []
    t = opts.t0
    while t <= opts.t1:
        times.append(t)
        t += opts.dt
    return times

def save_spectrum(H, filename):
    s = Spectrum(H)
    s.save(filename)

def compute_spectrum(opts, full_diagonalization) -> 'KitaevHamiltonian':
    """Create J tensor, build Hamiltonian, diagonalize, save spectrum."""
    print("Creating J tensor")
    Jtensor = KitaevDisorderParameter(opts.N, opts.J, rng, not opts.real_J)

    print("Computing Hamiltonian")
    timer = Timer()
    H = KitaevHamiltonian(opts.N, Jtensor)
    timer.print()

    H.diagonalize(full_diagonalization, print_progress=True)

    filename = get_base_filename(opts.data_dir, opts.run_name) + "-spectrum.tsv"
    save_spectrum(H, filename)
    return H

def compute_majorana_2_pt_function_main(opts):
    """Compute Majorana 2-point function and optionally fluctuations."""
    timer = Timer()
    print("Computing Hamiltonian and diagonalizing")
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    H.diagonalize_full(print_progress=True)
    timer.print()

    print("Computing 2-point functions...")
    times = get_times_vector(opts)
    Z = [0.0] * len(opts.betas)
    correlators = np.zeros((len(times), len(opts.betas)), dtype=complex)
    correlators_squared = np.zeros((len(times), len(opts.betas)), dtype=complex)

    if opts.compute_2_pt_func:
        compute_majorana_2_pt_function(H, opts.betas, times, opts.time_type, correlators, Z, True)
    else:
        compute_majorana_2_pt_function_with_fluctuations(
            H, opts.betas, times, opts.time_type,
            correlators, correlators_squared, Z, True)

    # Write results to TSV file
    filename = get_base_filename(opts.data_dir, opts.run_name) + "-2pt.tsv"
    with open(filename, 'w') as f:
        f.write("#\tbeta\tt\tZ(beta)\tRe<G>\tIm<G>")
        if opts.compute_2_pt_func_with_fluctuations:
            f.write("\tRe<GG*>")
        f.write("\n")
        for ti, t in enumerate(times):
            for bi, beta in enumerate(opts.betas):
                f.write(f"{beta}\t{t}\t{Z[bi]}")
                f.write(f"\t{correlators[ti,bi].real}\t{correlators[ti,bi].imag}")
                if opts.compute_2_pt_func_with_fluctuations:
                    f.write(f"\t{correlators_squared[ti,bi].real}")
                f.write("\n")

def compute_fermion_matrix_main(opts):
    """Compute and save fermion operator in energy eigenbasis."""
    print("Computing Hamiltonian")
    timer = Timer()
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    timer.print()

    print("Diagonalizing")
    H.diagonalize_full(print_progress=True)

    # Save spectrum
    # ...

    print("Computing fermion matrices...")
    timer.reset()
    result = matrix_abs_sqr(H.to_energy_basis(H.chi[0]))
    save_matrix_in_tsv(opts, "chi0", result)
    timer.print()

def compute_majorana_anti_commutator(opts):
    """Compute {chi_1(t), chi_2(0)} and its eigenvalues."""
    print("Computing Hamiltonian")
    timer = Timer()
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    timer.print()

    print("Diagonalizing")
    H.diagonalize_full(print_progress=True)

    print("Computing anti-commutators...")
    times = get_times_vector(opts)
    beta = opts.betas[0]
    exp_betaH = compute_exp_H(H.V, H.evs, -beta)
    Z = abs(np.trace(exp_betaH))

    for t in times:
        tau = get_tau(opts.time_type, t)
        exp_tauH = compute_exp_H(H.V, H.evs, tau)
        chi1_t = exp_tauH @ H.chi[0] @ exp_tauH.conj().T
        anti_comm = 1j * (chi1_t @ H.chi[1] + H.chi[1] @ chi1_t)
        evs = np.linalg.eigvalsh(anti_comm)
        correlator_2pt = np.trace(exp_betaH @ anti_comm) / Z
        correlator_4pt = np.trace(exp_betaH @ anti_comm @ anti_comm) / Z
        # Write t, |<{chi1(t),chi2}>|, |<{chi1(t),chi2}^2>|, max_ev, avg_ev

def compute_majorana_spectrum(opts):
    """Compute and save Majorana spectrum."""
    print("Creating J tensor")
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, rng)

    print("Computing Hamiltonian")
    timer = Timer()
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    timer.print()

    print("Diagonalizing")
    timer.reset()
    H.diagonalize(print_progress=True)
    timer.print()

    filename = get_base_filename(opts.data_dir, opts.run_name) + "-spectrum.tsv"
    with open(filename, 'w') as f:
        f.write("#\tcharge-parity\teigenvalue\n")
        for ev in H.even_charge_parity_evs:
            f.write(f"1\t{ev}\n")
        for ev in H.odd_charge_parity_evs:
            f.write(f"-1\t{ev}\n")

def compute_2_point_function_dirac(N, betas, times, H, time_type, out):
    """Compute and write Dirac 2-point functions."""
    correlators = compute_2_point_function(N, betas, times, H, time_type)
    for bi, beta in enumerate(betas):
        for ti, t in enumerate(times):
            if out is not None:
                out.write(1.0 / beta, t, correlators[bi, ti])

def matrix_abs_sqr(M):
    """Element-wise |M_{ab}|^2."""
    return np.abs(M) ** 2

def save_matrix_in_tsv(opts, suffix, M):
    filename = get_base_filename(opts.data_dir, opts.run_name) + f"-{suffix}.tsv"
    np.savetxt(filename, M, delimiter='\t')


# ========================
# MAIN
# ========================
def main():
    global rng
    opts = parse_command_line_options(sys.argv)
    print(f"Command line options:\n{opts}")
    rng = np.random.RandomState(opts.seed)

    full_diag = opts.compute_2_pt_func or opts.compute_fermion_matrix

    if opts.majorana:
        if opts.compute_2_pt_func or opts.compute_2_pt_func_with_fluctuations:
            compute_majorana_2_pt_function_main(opts)
        elif opts.compute_fermion_matrix:
            compute_fermion_matrix_main(opts)
        elif opts.compute_anti_commutator:
            compute_majorana_anti_commutator(opts)
        else:
            compute_majorana_spectrum(opts)
    else:
        H = compute_spectrum(opts, full_diag)
        if opts.compute_2_pt_func:
            print("Computing 2-point functions...")
            times = get_times_vector(opts)
            filename = get_base_filename(opts.data_dir, opts.run_name) + "-2pt.tsv"
            out = TwoPointFileOutput(filename)
            timer = Timer()
            compute_2_point_function_dirac(opts.N, opts.betas, times, H, opts.time_type, out)
            timer.print()
            out.close()

if __name__ == "__main__":
    main()
```
