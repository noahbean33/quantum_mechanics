# SYK Model — MVP C++ Implementation Spec

## 1. What This Is

Exact diagonalization (ED) of the Sachdev-Ye-Kitaev model for small N (up to ~32 Majorana fermions). The SYK₄ Hamiltonian:

$$H = \sum_{1 \le i < j < k < l \le N} J_{ijkl}\, \chi_i \chi_j \chi_k \chi_l$$

where $\chi_i$ are Majorana fermion operators satisfying $\{\chi_i, \chi_j\} = \delta_{ij}$ and $J_{ijkl}$ are i.i.d. Gaussian with variance $\sigma^2 = 3! J^2 / N^3$.

**Target**: Reproduce the known spectral density, thermal Green's function $G(\tau)$, and thermodynamic quantities (energy, entropy, specific heat) for benchmarking against the large-N Schwinger-Dyson solution.

---

## 2. Scope — What's In, What's Out

### In (MVP)
- Majorana representation via Jordan-Wigner transform → sparse 2^(N/2) × 2^(N/2) matrices
- Hamiltonian construction for arbitrary even N, q=4 (generalizable to q=2 as sanity check)
- Full diagonalization (dense) for N ≤ 20
- Lanczos/Arnoldi for partial spectrum at N = 24–32
- Disorder averaging over M realizations of J
- Observables: spectral density ρ(E), partition function Z(β), thermal two-point function G(τ), entropy S(β), specific heat C(β)
- CLI interface, results to stdout/CSV

### Out (Post-MVP)
- Large-N Schwinger-Dyson solver (separate module, Python is fine)
- Real-time correlators / spectral function A(ω)
- SYK₂ + SYK₄ mixed model (sparse-dense crossover)
- GPU offload
- Complex SYK (Dirac fermions, U(1) charge)
- Coupled SYK / traversable wormhole protocol
- GUI / notebook integration

---

## 3. Architecture

```
syk/
├── CMakeLists.txt
├── include/
│   ├── syk/majorana.h        // Majorana operator construction
│   ├── syk/hamiltonian.h     // H assembly from couplings
│   ├── syk/couplings.h       // Random J generation + storage
│   ├── syk/diagonalizer.h    // Dense ED + Lanczos wrapper
│   ├── syk/observables.h     // G(τ), Z(β), S(β), ρ(E)
│   └── syk/types.h           // Typedefs, constants
├── src/
│   ├── majorana.cpp
│   ├── hamiltonian.cpp
│   ├── couplings.cpp
│   ├── diagonalizer.cpp
│   ├── observables.cpp
│   └── main.cpp
├── tests/
│   ├── test_clifford.cpp     // {χ_i, χ_j} = δ_ij verification
│   ├── test_q2.cpp           // SYK_2 analytics check
│   └── test_thermo.cpp       // High-T entropy = (N/2) ln 2
└── bench/
    └── scaling.cpp            // Wall-time vs N
```

### Dependencies
- **Eigen 3.4+** — dense linear algebra, eigendecomposition. Header-only, no link hassle.
- **Spectra** (or ARPACK-ng) — Lanczos for N > 20. Spectra is header-only, wraps Eigen.
- **PCG or xoshiro256** — fast PRNG for coupling generation. `std::mt19937_64` is acceptable for MVP.
- **CLI11** or raw `getopt` — argument parsing.
- **No Boost.** Keep the dependency graph tight.

---

## 4. Core Data Structures

### 4.1 `types.h`

```cpp
#pragma once
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <complex>
#include <cstdint>

namespace syk {

// Hilbert space dimension = 2^(N/2) for N Majorana fermions
using Real = double;
using Complex = std::complex<double>;
using DenseMat = Eigen::MatrixXcd;
using SparseMatr = Eigen::SparseMatrix<Complex>;
using VectorC = Eigen::VectorXcd;
using VectorR = Eigen::VectorXd;

struct Params {
    int N;                  // Number of Majorana fermions (must be even)
    int q = 4;              // q-body interaction order
    int num_realizations;   // Disorder averaging samples
    double J = 1.0;         // Coupling scale
    double beta_min = 0.1;  // Inverse temperature range
    double beta_max = 50.0;
    int num_beta = 100;
    int num_tau = 200;      // τ grid points for G(τ)
    uint64_t seed = 42;
};

} // namespace syk
```

### 4.2 Majorana Representation

Jordan-Wigner maps N Majorana operators to $d = 2^{N/2}$ dimensional Hilbert space. Group Majoranas into pairs to define N/2 Dirac fermion modes:

$$c_a = \frac{1}{2}(\chi_{2a-1} + i\chi_{2a}), \quad a = 1, \dots, N/2$$

Then:

$$\chi_{2a-1} = \prod_{b<a}(-\sigma_z^{(b)}) \otimes \sigma_x^{(a)} \otimes I^{(\text{rest})}$$
$$\chi_{2a} = \prod_{b<a}(-\sigma_z^{(b)}) \otimes \sigma_y^{(a)} \otimes I^{(\text{rest})}$$

**Storage**: Each $\chi_i$ is a $d \times d$ sparse matrix. For N=20, d=1024 — each $\chi_i$ has exactly d nonzero entries (it's a signed permutation matrix), so sparse storage is efficient. Pre-compute and cache all N operators at initialization.

```cpp
class MajoranaAlgebra {
public:
    explicit MajoranaAlgebra(int N);

    int N() const;
    int dim() const;  // 2^(N/2)

    // Returns χ_i as sparse matrix, 0-indexed
    const SparseMatr& chi(int i) const;

    // Verify Clifford algebra: {χ_i, χ_j} = δ_ij * I
    bool verify_anticommutation(double tol = 1e-12) const;

private:
    int N_;
    int dim_;
    std::vector<SparseMatr> chi_;  // length N
};
```

### 4.3 Coupling Tensor

For q=4, the independent couplings are $\binom{N}{4}$ real numbers. Store as a flat vector indexed by the sorted 4-tuple $(i,j,k,l)$ with $i<j<k<l$.

```cpp
class Couplings {
public:
    Couplings(int N, int q, double J, std::mt19937_64& rng);

    // J_{i,j,k,l} for sorted indices
    Real operator()(int i, int j, int k, int l) const;

    // Iterate over all q-tuples: calls f(indices, J_val)
    template<typename F>
    void for_each(F&& f) const;

    int num_terms() const;  // C(N, q)

private:
    int N_, q_;
    std::vector<Real> data_;
    // Index mapping: sorted tuple → flat index
};
```

Variance: $\langle J_{ijkl}^2 \rangle = \frac{(q-1)! \, J^2}{N^{q-1}}$. For q=4, N=20: $\sigma = J\sqrt{6/N^3} \approx 0.0274 J$.

---

## 5. Hamiltonian Construction

```cpp
class Hamiltonian {
public:
    Hamiltonian(const MajoranaAlgebra& algebra, const Couplings& couplings);

    // Build H as dense matrix (for ED)
    DenseMat build_dense() const;

    // Build H as sparse matrix (for Lanczos)
    SparseMatr build_sparse() const;

    // Matrix-vector product H|v⟩ without storing H explicitly
    // (for iterative solvers at large N)
    VectorC matvec(const VectorC& v) const;

private:
    const MajoranaAlgebra& algebra_;
    const Couplings& couplings_;
};
```

**Critical optimization**: Don't form the 4-fold sparse product $\chi_i \chi_j \chi_k \chi_l$ as an intermediate matrix. Since each $\chi$ is a signed permutation, the product is also a signed permutation. Compose the permutations and signs directly:

```cpp
// Each chi_i acts as: |n⟩ → sign(i, n) * |perm(i, n)⟩
// Product of 4: compose permutations, multiply signs
// This avoids allocating any intermediate sparse matrices
```

This is the single biggest performance lever in the code. For N=20 with $\binom{20}{4} = 4845$ terms, you're doing 4845 rank-1-like updates to a dense matrix instead of 4845 sparse matrix multiplications.

---

## 6. Diagonalization

```cpp
struct Spectrum {
    VectorR eigenvalues;     // sorted ascending
    DenseMat eigenvectors;   // columns = eigenstates (optional, needed for G(τ))
};

class Diagonalizer {
public:
    // Full ED — use for N ≤ 20 (d ≤ 1024)
    static Spectrum full(const DenseMat& H, bool compute_eigvecs = true);

    // Lanczos — k lowest eigenvalues/vectors for N > 20
    static Spectrum lanczos(const SparseMatr& H, int k, double tol = 1e-10);

    // Lanczos via matvec functor (matrix-free, for largest N)
    static Spectrum lanczos_free(
        std::function<VectorC(const VectorC&)> matvec,
        int dim, int k, double tol = 1e-10
    );
};
```

**N scaling reality check**:

| N  | d = 2^(N/2) | Dense H (complex, bytes) | ED time (approx)  |
|----|-------------|-------------------------|--------------------|
| 12 | 64          | 64 KB                   | < 1 ms             |
| 16 | 256         | 1 MB                    | ~10 ms             |
| 20 | 1024        | 16 MB                   | ~1 s               |
| 24 | 4096        | 256 MB                  | ~30 s              |
| 28 | 16384       | 4 GB                    | Lanczos only       |
| 32 | 32768       | 16 GB                   | Lanczos only       |

Dense ED is `Eigen::SelfAdjointEigenSolver` — H is Hermitian by construction.

---

## 7. Observables

### 7.1 Spectral Density

$$\rho(E) = \frac{1}{d} \sum_n \delta(E - E_n)$$

Bin eigenvalues into histogram. At large N, should converge to the Schwarzian/Gaussian shape. For disorder averaging, accumulate histograms across realizations.

### 7.2 Partition Function and Thermodynamics

$$Z(\beta) = \sum_n e^{-\beta E_n}$$

$$\langle E \rangle = -\frac{\partial \ln Z}{\partial \beta} = \frac{\sum_n E_n e^{-\beta E_n}}{Z}$$

$$S(\beta) = \beta \langle E \rangle + \ln Z$$

$$C(\beta) = \beta^2 (\langle E^2 \rangle - \langle E \rangle^2)$$

**Sanity checks**:
- $\beta \to 0$: $S \to \frac{N}{2} \ln 2$ (maximally mixed state over d states)
- $\beta \to \infty$: $S \to 0$ (or $\ln(\text{ground state degeneracy})$)
- Specific heat $C \ge 0$ always

### 7.3 Thermal Two-Point Function

$$G(\tau) = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{Z} \text{Tr}\left[ e^{-(\beta - \tau)H}\, \chi_i\, e^{-\tau H}\, \chi_i \right]$$

With eigenstates $|n\rangle$:

$$G(\tau) = \frac{1}{N} \sum_i \frac{1}{Z} \sum_{m,n} |\langle m | \chi_i | n \rangle|^2 \, e^{-(\beta-\tau)E_m - \tau E_n}$$

**Pre-compute** the matrix elements $\langle m | \chi_i | n \rangle$ once per realization. Since $\chi_i$ is a signed permutation in the computational basis, these are cheap in the eigenbasis: it's $U^\dagger \chi_i U$ where $U$ is the eigenvector matrix. Cost: N matrix multiplies of size $d \times d$.

At low temperature, $G(\tau)$ should show conformal behavior:

$$G(\tau) \sim \frac{1}{|\sin(\pi \tau / \beta)|^{2\Delta}}, \quad \Delta = 1/q$$

For q=4, $\Delta = 1/4$. Checking this scaling is a key validation target.

```cpp
class Observables {
public:
    Observables(const Spectrum& spectrum, const MajoranaAlgebra& algebra);

    // Spectral density histogram
    VectorR spectral_density(int num_bins) const;

    // Thermodynamic quantities at inverse temperature β
    struct Thermo {
        Real Z, energy, entropy, specific_heat;
    };
    Thermo thermodynamics(Real beta) const;

    // G(τ) on uniform grid τ ∈ [0, β]
    VectorR green_function(Real beta, int num_tau) const;

private:
    const Spectrum& spec_;
    // chi_mn_[i] = matrix elements of χ_i in eigenbasis, dim d×d
    std::vector<DenseMat> chi_mn_;
};
```

---

## 8. Disorder Averaging

Run `num_realizations` independent samples. For each:
1. Draw new $J_{ijkl}$
2. Build H
3. Diagonalize
4. Compute observables
5. Accumulate running mean and variance (Welford's algorithm)

Realizations are embarrassingly parallel — use `std::thread` or OpenMP `parallel for`. Each thread gets its own PRNG seeded from the master.

```cpp
struct DisorderAverage {
    VectorR mean;
    VectorR variance;
    int count;

    void update(const VectorR& sample);  // Welford online
};
```

**Minimum realization counts** (rule of thumb):
- Spectral density: 100–1000 (smooth quickly)
- G(τ): 50–200
- Thermodynamics: 50–100

---

## 9. Validation Targets

These are non-negotiable before trusting any new results:

| Test | Expected | Tolerance |
|------|----------|-----------|
| Clifford algebra | $\{\chi_i, \chi_j\} = \delta_{ij} I$ | machine ε |
| Tr(H) = 0 | Traceless for q=4 | ~1e-10 |
| H = H† | Hermiticity | machine ε |
| SYK₂ spectrum | Semicircle law | Visual + KS test |
| High-T entropy | $(N/2) \ln 2$ | < 1% at β=0.01 |
| G(τ) symmetry | $G(\beta - \tau) = -G(\tau)$ for Majorana | 1e-10 |
| G(τ) conformal scaling | $\Delta \approx 0.25$ for q=4 | ±0.02 at N≥16, low T |

For the SYK₂ check: set q=2, the model is a random quadratic Hamiltonian. Eigenvalues of the single-particle matrix follow Wigner semicircle, and the many-body spectrum is all possible sums of ±(single-particle eigenvalues)/2. This is analytically tractable and is your primary debugging tool.

---

## 10. CLI Interface

```
./syk_ed --N 20 --q 4 --J 1.0 --realizations 100 \
         --beta-min 0.1 --beta-max 50 --num-beta 100 \
         --num-tau 200 --seed 42 \
         --output-dir results/ \
         --observables spectrum,thermo,green
```

Output files:
- `spectrum_N20_q4.csv` — columns: bin_center, rho_mean, rho_std
- `thermo_N20_q4.csv` — columns: beta, energy_mean, energy_std, entropy_mean, entropy_std, Cv_mean, Cv_std
- `green_N20_q4.csv` — columns: tau/beta, G_mean, G_std (one file per β value, or a β column)

---

## 11. Build

```cmake
cmake_minimum_required(VERSION 3.16)
project(syk_ed CXX)

set(CMAKE_CXX_STANDARD 20)

find_package(Eigen3 3.4 REQUIRED NO_MODULE)
find_package(OpenMP)

add_executable(syk_ed
    src/main.cpp
    src/majorana.cpp
    src/hamiltonian.cpp
    src/couplings.cpp
    src/diagonalizer.cpp
    src/observables.cpp
)

target_include_directories(syk_ed PRIVATE include)
target_link_libraries(syk_ed Eigen3::Eigen)

if(OpenMP_CXX_FOUND)
    target_link_libraries(syk_ed OpenMP::OpenMP_CXX)
endif()

# Spectra (header-only, for Lanczos)
# FetchContent or find_package depending on preference
include(FetchContent)
FetchContent_Declare(spectra
    GIT_REPOSITORY https://github.com/yixuan/spectra.git
    GIT_TAG v1.0.1
)
FetchContent_MakeAvailable(spectra)
target_link_libraries(syk_ed Spectra::Spectra)
```

---

## 12. Performance Budget

Target: Full ED for N=20, 100 realizations, all observables, under 5 minutes on a single modern core.

Breakdown per realization (N=20, d=1024):
- Coupling generation: negligible
- Hamiltonian build: ~5000 rank-1 updates to 1024×1024 matrix → ~50 ms
- Eigendecomposition: ~500 ms (dominant cost)
- Matrix element computation (N=20 matrix products): ~200 ms
- G(τ) evaluation: ~50 ms
- **Total per realization: ~800 ms**
- **100 realizations: ~80 s** single-threaded, ~10 s with 8 threads

This is comfortably within budget. N=24 (d=4096) will be ~100× slower per realization — still feasible with Lanczos for partial spectrum.

---

## 13. Extension Points (Post-MVP Hooks)

Design decisions that keep the door open:

1. **q-generality**: `Couplings` is templated on q, not hardcoded to 4. The tuple iteration and Hamiltonian assembly work for any even q.

2. **Fermion parity sectors**: H commutes with $(-1)^F = \prod_i (2c_i^\dagger c_i - 1)$. Block-diagonalizing into even/odd parity halves the matrix dimension — implement as a flag, not a refactor. This is actually the single easiest optimization to get N=24 into dense ED range (d → d/2 = 2048 per sector).

3. **Complex SYK**: Replace real $J_{ijkl}$ with complex, add U(1) charge conservation → block-diagonalize by charge sector. The `Couplings` class should use `Complex` type with a `bool is_real` flag.

4. **Spectral form factor**: $|Z(\beta + it)|^2$ — just needs eigenvalues, which you already have. This is the cleanest probe of quantum chaos (ramp + plateau) and costs zero additional diagonalization.

5. **Entanglement entropy**: Partition Majoranas into subsystems A, B. Reduced density matrix from eigenstates → von Neumann entropy. Needs eigenvectors, which you're already storing.

---

## 14. Known Pitfalls

- **Sign errors in Jordan-Wigner**: The JW string $\prod_{b<a}(-\sigma_z^{(b)})$ is the #1 source of bugs. Validate exhaustively with the Clifford algebra test before touching anything else. Every sign error will produce a Hamiltonian that looks plausible but gives wrong physics.

- **Numerical stability of Z(β) at large β**: $e^{-\beta E_n}$ underflows for excited states. Shift all eigenvalues by $E_0$ (ground state energy) before exponentiation: $Z(\beta) = e^{-\beta E_0} \sum_n e^{-\beta(E_n - E_0)}$. Entropy formula picks up a compensating $\beta E_0$ term.

- **G(τ) at τ = 0 and τ = β**: Formally divergent or discontinuous depending on ordering convention. Use the Euclidean time-ordered definition and be explicit about the $\tau \to 0^+$ limit.

- **Finite-size effects**: N=12 is a toy. N=16 starts to show large-N features. N=20 is where you can meaningfully extract $\Delta$. Don't over-interpret small-N results.

- **PRNG quality**: `std::mt19937_64` is fine for coupling generation. Don't use `rand()`. If you're doing >10⁴ realizations, consider splitting the PRNG state properly across threads (jump-ahead or independent seeds via seed_seq).
