# benchmark-test.cc — Python Pseudocode

Benchmarking program for sparse Hamiltonian implementations and LAPACK tridiagonal eigensolvers.

```python
import numpy as np

def benchmark_sparse_implementations(space, rng):
    """
    Create dense, sparse, and half-sparse FactorizedHamiltonians.
    Time act_even for 10 iterations on each.
    """
    Jtensor = MajoranaKitaevDisorderParameter(space.N, 1.0, rng)
    print(f"Creating Hamiltonians with Nd={space.Nd} Nd_left={space.left.Nd}")

    dense_H = FactorizedHamiltonian(space, Jtensor)
    sparse_H = SparseFactorizedHamiltonian(space, Jtensor)
    half_sparse_H = HalfSparseFactorizedHamiltonian(space, Jtensor)

    state = get_factorized_random_state(space, rng)
    output = np.zeros((space.left.D, space.right.D), dtype=complex)
    iterations = 10

    timer = Timer()
    print("Running half sparse implementation")
    for _ in range(iterations):
        half_sparse_H.act_even(output, state)
    timer.print_msec()

def benchmark_tridiagonal_eig(rng):
    """Benchmark Eigen SelfAdjointEigenSolver on a random tridiagonal matrix."""
    D = 2000
    diag = get_random_real_vector(D, rng)
    subdiag = get_random_real_vector(D - 1, rng)
    # Build sparse tridiagonal, compute eigenvectors
    pass

def benchmark_lapack_tridiagonal_eig(rng, N):
    """
    Benchmark LAPACK dstedc (divide-and-conquer tridiagonal eigensolver)
    for a random tridiagonal matrix of dimension N, including eigenvectors.
    1. Workspace query (LWORK=-1)
    2. Allocate workspace
    3. Time the actual dstedc call
    """
    diag = get_random_real_vector(N, rng)
    subdiag = get_random_real_vector(N - 1, rng)
    # Call LAPACK dstedc with compz='I'
    timer = Timer()
    # ... dstedc call ...
    timer.print()

def main():
    rng = np.random.RandomState(get_random_seed(""))
    N = int(sys.argv[1])
    benchmark_lapack_tridiagonal_eig(rng, N)

if __name__ == "__main__":
    main()
```
