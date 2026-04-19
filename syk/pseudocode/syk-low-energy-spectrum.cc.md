# syk-low-energy-spectrum.cc — Python Pseudocode

CPU Lanczos benchmarking and testing: power iteration, reference Lanczos, factorized Lanczos, and a low-level GPU kernel prototype.

```python
import numpy as np

class CommandLineOptions:
    def __init__(self):
        self.run_name = "test"
        self.data_dir = "data"
        self.N = 0
        self.J = 1.0
        self.seed = 0
        self.rng = None

def compute_lambda(v, v2, mu):
    """Estimate eigenvalue from power iteration: lambda = mean(v2/v) - mu."""
    lam = np.mean(v2 / v) - mu
    return lam

def compute_majorana_leading_ev(opts):
    """
    Power iteration on A = H + mu*I to find the largest eigenvalue.
    Repeat: v2 = A*v; normalize; check convergence every 100 steps.
    """
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, opts.rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    mu = 1.0

    v = get_random_state(Space.from_majorana(opts.N), opts.rng)
    for i in range(100000):
        v2 = (H.matrix + mu * np.eye(H.dim())) @ v
        v2_norm = v2 / np.linalg.norm(v2)
        if i % 100 == 0:
            dist = np.linalg.norm(v2_norm - v)
            lam = compute_lambda(v, v2, mu)
            if dist < epsilon or abs(dist - 2.0) < epsilon:
                break
        v = v2_norm
    print(f"lambda = {lam}")

def run_lanczos(opts):
    """
    Reference Lanczos on A = H + mu*I.
    1. Diagonalize A exactly
    2. Run reference_lanczos for m steps
    3. Compare good Lanczos eigenvalues with exact eigenvalues
    """
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, opts.rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    mu = 1.0
    A_evs = np.linalg.eigvalsh(H.dense_matrix() + mu * np.eye(H.dim()))

    m = 200
    alpha, beta = reference_lanczos(H, mu, m, rng=opts.rng)
    good_evs = find_good_lanczos_evs(alpha, beta)
    # Compare good_evs with A_evs

def run_factorized_lanczos(opts):
    """
    Factorized Lanczos on A = H + mu*I.
    Same comparison as run_lanczos, but using factorized Hamiltonian.
    """
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, opts.rng)
    H = MajoranaKitaevHamiltonian(opts.N, Jtensor)
    mu = 1.0
    A_evs = np.linalg.eigvalsh(H.dense_matrix() + mu * np.eye(H.dim()))

    space = FactorizedSpace.from_majorana(opts.N)
    factH = FactorizedHamiltonianGenericParity(space, Jtensor)
    m = 200
    alpha, beta = factorized_lanczos(factH, mu, m, rng=opts.rng)
    good_evs = find_good_lanczos_evs(alpha, beta)

def benchmark_hamiltonian_memory(opts):
    """Create a factorized Hamiltonian and wait (for memory profiling)."""
    Jtensor = MajoranaKitaevDisorderParameter(opts.N, opts.J, opts.rng)
    space = FactorizedSpace.from_majorana(opts.N)
    H = FactorizedHamiltonian(space, Jtensor)
    input("Done, waiting for input")

def compute_single_action(dressed_coupling, a, b, c, d, input_val, addr, N):
    """
    Compute one term of H*|state> in the global state basis.
    For Majoranas chi_a chi_b chi_c chi_d:
      1. Flip occupancies at Dirac indices i=a//2, j=b//2, k=c//2, l=d//2
      2. Compute sign from odd-parity Majoranas (i-factor for chi_{2i+1})
      3. Compute anti-commutation sign from fermion ordering
    Returns (output_value, output_address).
    """
    i, j, k, l = a // 2, b // 2, c // 2, d // 2
    flipper = (1 << i) | (1 << j) | (1 << k) | (1 << l)
    output_addr = addr ^ flipper

    # Compute sign from odd Majoranas and anti-commutation
    # ... (bit manipulation for sign factors)

    return dressed_coupling * sign_factor * input_val, output_addr

def compute_transformed_state(Jtensor, N, D, state):
    """
    Apply H to state in the global basis using compute_single_action.
    For each basis state |addr>, loop over all (a<b<c<d) and accumulate.
    """
    transformed = np.zeros(D, dtype=complex)
    i_powers = [1, 1j, -1, -1j]

    for addr in range(D):
        # Build anticommutation sign lookup table
        for a in range(N):
            for b in range(a+1, N):
                for c in range(b+1, N):
                    for d in range(c+1, N):
                        i_power = (a%2) + (b%2) + (c%2) + (d%2)
                        dressed = Jtensor.elem(a,b,c,d) * i_powers[i_power] / 4.0
                        out_val, out_addr = compute_single_action(
                            dressed, a, b, c, d, state[addr], addr, N)
                        transformed[out_addr] += out_val
    return transformed

def main():
    opts = parse_command_line_options(sys.argv)
    # Main dispatches to one of the functions above:
    benchmark_hamiltonian_memory(opts)

if __name__ == "__main__":
    main()
```
