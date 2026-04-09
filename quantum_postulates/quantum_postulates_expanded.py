# -*- coding: utf-8 -*-
"""
# The Six Postulates of Quantum Mechanics — Expanded Edition
### Bridging Linear Algebra, Probability, and Differential Equations

This notebook is an expanded treatment of McIntyre's six postulates, extended to include:
  - Reusable QuantumState and QuantumOperator classes
  - Spectral decomposition and projection operators (Postulate 2)
  - Expectation values, variance, and the Robertson uncertainty principle
  - Degenerate collapse and the projection postulate (Postulate 5)
  - Heisenberg picture and Rabi oscillations (Postulate 6)
  - Two-qubit tensor products and Bell entanglement
  - Density matrix formalism (pure vs. mixed states)

Reference: McIntyre, D. H. (2022). Quantum Mechanics: A Paradigms Approach.
           Cambridge University Press.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import expm

# =============================================================================
# Helper Functions and Classes
# =============================================================================

def plot_bloch_sphere(ax, states=[], labels=[], colors=[], title=""):
    """Plots the Bloch sphere and given state vectors."""
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(xs, ys, zs, color='lightcyan', alpha=0.1)
    ax.set_box_aspect([1, 1, 1])
    for axis, lim in [([[-1,1],[0,0],[0,0]], 'gray'),
                      ([[0,0],[-1,1],[0,0]], 'gray'),
                      ([[0,0],[0,0],[-1,1]], 'gray')]:
        ax.plot(axis[0], axis[1], axis[2], color=lim, linestyle='--', alpha=0.5)
    ax.text(0, 0,  1.15, "|0⟩", fontsize=9, ha='center')
    ax.text(0, 0, -1.25, "|1⟩", fontsize=9, ha='center')
    ax.text( 1.15, 0, 0,  "|+⟩", fontsize=9)
    ax.text(-1.35, 0, 0,  "|-⟩", fontsize=9)
    ax.text(0,  1.15, 0,  "|i⟩", fontsize=9)
    ax.text(0, -1.35, 0,  "|-i⟩", fontsize=9)
    for i, state in enumerate(states):
        alpha, beta = state[0, 0], state[1, 0]
        theta = np.pi if np.abs(alpha) < 1e-9 else 2 * np.arccos(np.clip(np.abs(alpha), 0, 1))
        phi = np.angle(beta) - np.angle(alpha)
        xc = np.sin(theta) * np.cos(phi)
        yc = np.sin(theta) * np.sin(phi)
        zc = np.cos(theta)
        lbl = labels[i] if i < len(labels) else ''
        col = colors[i] if i < len(colors) else 'red'
        ax.quiver(0, 0, 0, xc, yc, zc, color=col, length=1,
                  arrow_length_ratio=0.15, label=lbl, linewidth=2)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    if labels:
        ax.legend(loc='upper left', fontsize=8)


def state_to_bloch(state):
    """Convert a 2-component column state vector to Bloch sphere (x,y,z)."""
    alpha, beta = state[0, 0], state[1, 0]
    theta = np.pi if np.abs(alpha) < 1e-9 else 2 * np.arccos(np.clip(np.abs(alpha), 0, 1))
    phi = np.angle(beta) - np.angle(alpha)
    return np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)


class QuantumState:
    """
    A normalized complex column vector representing a pure quantum state.

    Mathematical note: This is an element of the projective Hilbert space CP^(n-1).
    For n=2 (qubits), CP^1 ≅ S^2, which is exactly the Bloch sphere.
    Two states differing only by a global phase e^(iφ) are physically identical.
    """
    def __init__(self, amplitudes):
        arr = np.array(amplitudes, dtype=complex).reshape(-1, 1)
        norm = np.sqrt((arr.conj().T @ arr)[0, 0].real)
        if norm < 1e-12:
            raise ValueError("Cannot normalize the zero vector.")
        self.vec = arr / norm

    @property
    def bra(self):
        return self.vec.conj().T

    def inner(self, other):
        """⟨self|other⟩ — complex inner product."""
        return (self.bra @ other.vec)[0, 0]

    def outer(self, other=None):
        """Outer product |self⟩⟨other| (or |self⟩⟨self| if other is None)."""
        if other is None:
            other = self
        return self.vec @ other.bra

    def norm(self):
        return np.sqrt(self.inner(self).real)

    def expect(self, operator):
        """⟨ψ|A|ψ⟩ — expectation value of an operator."""
        return (self.bra @ operator @ self.vec)[0, 0]

    def variance(self, operator):
        """Var(A) = ⟨A²⟩ - ⟨A⟩² — variance of an observable."""
        exp_A  = self.expect(operator)
        exp_A2 = self.expect(operator @ operator)
        return (exp_A2 - exp_A**2).real

    def prob_of(self, eigenvector):
        """Born rule: P = |⟨eigenvector|ψ⟩|²"""
        if isinstance(eigenvector, QuantumState):
            amp = eigenvector.inner(self)
        else:
            amp = (eigenvector.conj().T @ self.vec)[0, 0]
        return np.abs(amp)**2

    def __repr__(self):
        return f"QuantumState(\n{self.vec}\n)"


class QuantumOperator:
    """
    A linear operator (matrix) on a Hilbert space.

    For observables, the matrix must be Hermitian: A = A†.
    The spectral theorem guarantees real eigenvalues and an orthonormal
    eigenbasis — this is the bridge between Hermitian matrices and
    measurable physical quantities.
    """
    def __init__(self, matrix):
        self.mat = np.array(matrix, dtype=complex)

    def is_hermitian(self, tol=1e-10):
        return np.allclose(self.mat, self.mat.conj().T, atol=tol)

    def is_unitary(self, tol=1e-10):
        n = self.mat.shape[0]
        return np.allclose(self.mat @ self.mat.conj().T, np.eye(n), atol=tol)

    def spectral_decomposition(self):
        """
        For a Hermitian operator A, the spectral theorem gives:
            A = Σ_n  λ_n |ϕ_n⟩⟨ϕ_n|
        where λ_n are real eigenvalues and |ϕ_n⟩ are orthonormal eigenvectors.
        np.linalg.eigh is used (not eig) because it guarantees real, sorted
        eigenvalues for Hermitian matrices.
        """
        if not self.is_hermitian():
            raise ValueError("Spectral decomposition requires a Hermitian operator.")
        eigenvalues, eigenvectors = np.linalg.eigh(self.mat)
        projectors = [np.outer(eigenvectors[:, i], eigenvectors[:, i].conj())
                      for i in range(len(eigenvalues))]
        return eigenvalues, eigenvectors, projectors

    def commutator(self, other):
        """[A, B] = AB - BA. Zero iff A and B share an eigenbasis."""
        return QuantumOperator(self.mat @ other.mat - other.mat @ self.mat)

    def time_evolve(self, t, hbar=1.0):
        """Unitary time evolution operator U(t) = exp(-i H t / ħ)."""
        return QuantumOperator(expm(-1j * self.mat * t / hbar))

    def __matmul__(self, other):
        if isinstance(other, QuantumOperator):
            return QuantumOperator(self.mat @ other.mat)
        return self.mat @ other  # allow A @ state_vec

    def __repr__(self):
        return f"QuantumOperator(\n{self.mat}\n)"


# =============================================================================
# Standard Operators
# =============================================================================
I2   = QuantumOperator([[1, 0], [0, 1]])
Sx   = QuantumOperator([[0,    1   ], [1,    0   ]])
Sy   = QuantumOperator([[0,   -1j  ], [1j,   0   ]])
Sz   = QuantumOperator([[1,    0   ], [0,   -1   ]])
Sp   = QuantumOperator([[0,    1   ], [0,    0   ]])  # raising  σ+ = |0⟩⟨1|
Sm   = QuantumOperator([[0,    0   ], [1,    0   ]])  # lowering σ- = |1⟩⟨0|

# Computational basis and cardinal states
ket0  = QuantumState([1, 0])
ket1  = QuantumState([0, 1])
ket_p = QuantumState([1,  1])   # |+⟩
ket_m = QuantumState([1, -1])   # |-⟩
ket_i = QuantumState([1,  1j])  # |i⟩
ket_mi= QuantumState([1, -1j])  # |-i⟩

sep = "\n" + "="*65 + "\n"

# =============================================================================
# POSTULATE 1: The State of the System
# =============================================================================
print(sep + "POSTULATE 1: The State of the System" + sep)
print("""
Mathematical translation:
  A quantum state is a unit vector in a complex Hilbert space H.
  The notation |ψ⟩ ("ket") is a column vector; ⟨ψ| ("bra") is its
  conjugate transpose.  Normalization requires ⟨ψ|ψ⟩ = 1.

Geometric remark:
  Because global phase e^(iφ)|ψ⟩ is physically indistinguishable from
  |ψ⟩, the true state space for a qubit is the projective space
  CP^1 ≅ S^2 — the Bloch sphere.  The U(1) fiber of global phases
  is quotiented out, leaving a 2-real-dimensional manifold.
""")

psi1 = QuantumState([1/np.sqrt(5), 2j/np.sqrt(5)])
print(f"State |ψ⟩ = (1/√5)|0⟩ + (2i/√5)|1⟩:\n{psi1.vec}\n")
print(f"⟨ψ|ψ⟩ = {psi1.inner(psi1):.6f}  (should be 1)\n")

# Global vs relative phase
psi1_global = QuantumState([1j/np.sqrt(5), -2/np.sqrt(5)])  # e^(iπ/2)|ψ⟩
print("Global phase check:")
print(f"  |⟨ψ_orig|ψ_global⟩|² = {psi1.prob_of(psi1_global):.6f}  (should be 1 — same state)")
psi1_relative = QuantumState([1/np.sqrt(5), -2j/np.sqrt(5)])
print(f"  |⟨ψ_orig|ψ_relative⟩|² = {psi1.prob_of(psi1_relative):.6f}  (< 1 — different state)")

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
plot_bloch_sphere(ax, [psi1.vec], ["|ψ⟩"], ["steelblue"],
                  "Postulate 1: A Quantum State on the Bloch Sphere\n"
                  r"CP$^1 \cong S^2$: relative phase = longitude, $\theta$ = latitude")
plt.tight_layout()
plt.show()

# =============================================================================
# POSTULATE 2: Observables and Operators
# =============================================================================
print(sep + "POSTULATE 2: Observables and Operators" + sep)
print("""
Mathematical translation:
  Every observable A is a Hermitian (self-adjoint) linear operator: A = A†.
  The spectral theorem guarantees:
      1. All eigenvalues are real        → physical measurement results
      2. Eigenvectors of distinct λ are orthogonal → mutually exclusive outcomes
      3. Eigenvectors form a complete basis → any state can be expanded in them

  The spectral decomposition:  A = Σ_n λ_n P_n,   where P_n = |ϕ_n⟩⟨ϕ_n|
  is the projection operator onto the n-th eigenspace.

Expectation value:
  ⟨A⟩_ψ = ⟨ψ|A|ψ⟩  =  Σ_n λ_n |⟨ϕ_n|ψ⟩|²
  This is the Born rule probability-weighted average of eigenvalues.

Commutators and compatibility:
  [A, B] = AB - BA.
  If [A, B] = 0, A and B share an eigenbasis and are simultaneously
  measurable ("compatible observables").  The Pauli matrices satisfy
  [σ_i, σ_j] = 2i ε_ijk σ_k, so no two are compatible.
""")

for name, op in [("σ_x", Sx), ("σ_y", Sy), ("σ_z", Sz)]:
    print(f"{name}:  Hermitian = {op.is_hermitian()}")

print()
comm_xy = Sx.commutator(Sy)
print(f"[σ_x, σ_y] = \n{comm_xy.mat.real}  (should be 2*i*σ_z)")
print(f"2i*σ_z = \n{(2j * Sz.mat).real}\n")

# Spectral decomposition of σ_z
eigenvalues_z, eigenvectors_z, projectors_z = Sz.spectral_decomposition()
print("Spectral decomposition of σ_z:")
for i, (lam, P) in enumerate(zip(eigenvalues_z, projectors_z)):
    print(f"  λ_{i} = {lam:.0f},  P_{i} = |ϕ_{i}⟩⟨ϕ_{i}| =\n{P.real}")

# Expectation value and variance
print(f"\nFor |ψ⟩ = {psi1.vec.T}:")
exp_z  = psi1.expect(Sz.mat)
var_z  = psi1.variance(Sz.mat)
print(f"  ⟨σ_z⟩ = {exp_z.real:.4f}")
print(f"  Var(σ_z) = ⟨σ_z²⟩ - ⟨σ_z⟩² = {var_z:.4f}")
print(f"  σ(σ_z)  = {np.sqrt(var_z):.4f}  (standard deviation)")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Show the action of each Pauli on |0⟩
for ax_i, (op, name, color) in zip(axes[:2], [(Sx,"σ_x acts on |0⟩","darkorange"),
                                               (Sz,"σ_z acts on |+⟩","purple")]):
    init_state = ket0 if 'x' in name else ket_p
    final_vec  = op.mat @ init_state.vec
    final_state = QuantumState(final_vec)
    fig3 = plt.figure(figsize=(6, 6))
    ax3 = fig3.add_subplot(111, projection='3d')
    plot_bloch_sphere(ax3, [init_state.vec, final_state.vec],
                     ["Initial", "After operator"], ["green", color], name)
    plt.tight_layout()
    plt.show()

# =============================================================================
# POSTULATE 3: Possible Outcomes of a Measurement
# =============================================================================
print(sep + "POSTULATE 3: Possible Outcomes of a Measurement" + sep)
print("""
Mathematical translation:
  The only possible results when measuring observable A are the
  eigenvalues {λ_n} of the corresponding Hermitian operator.
  For Hermitian operators these are guaranteed real by the spectral theorem.

Discrete vs. continuous spectra:
  Finite-dimensional systems (like qubits) have discrete spectra.
  For operators like position X̂ or momentum P̂ acting on L²(ℝ), the
  spectrum is continuous and the eigenstates are not normalizable
  in the usual sense (they are Dirac δ-distributions).
  In that case the Born rule uses probability *density*: dP = |ψ(x)|² dx.

Degenerate eigenvalues:
  If multiple eigenvectors share the same eigenvalue λ (degenerate case),
  any vector in that eigenspace is a valid post-measurement state.
  The appropriate projector is P_λ = Σ_{n∈λ} |ϕ_n⟩⟨ϕ_n|.
""")

# Demonstrate with a degenerate operator
H_degen = QuantumOperator([[1, 0, 0], [0, 1, 0], [0, 0, -1]])  # λ=1 doubly degenerate
evals, evecs, projs = H_degen.spectral_decomposition()
print("3×3 operator with degenerate spectrum:")
print(f"  Eigenvalues: {evals}")
print(f"  Distinct outcomes: {np.unique(evals.round(10))}\n")

# Standard qubit example
psi3 = QuantumState([1/np.sqrt(5), 2/np.sqrt(5)])
print(f"Measuring σ_z on |ψ⟩ = (1/√5)|0⟩ + (2/√5)|1⟩:")
for lam, evec in zip(eigenvalues_z, eigenvectors_z.T):
    p = psi3.prob_of(evec.reshape(-1,1))
    print(f"  P(λ={lam:+.0f}) = {p:.4f}")

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
plot_bloch_sphere(ax,
                  [psi3.vec, eigenvectors_z[:, 0].reshape(-1,1),
                             eigenvectors_z[:, 1].reshape(-1,1)],
                  ["|ψ⟩", "|0⟩ (λ=+1)", "|1⟩ (λ=−1)"],
                  ["steelblue", "black", "dimgray"],
                  "Postulate 3: State and Eigenvectors of σ_z")
plt.tight_layout()
plt.show()

# =============================================================================
# POSTULATE 4: Born Rule — Probability of Measurement Outcomes
# =============================================================================
print(sep + "POSTULATE 4: Born Rule — Probability of Outcomes" + sep)
print("""
Mathematical translation:
  Given observable A with eigenvalues λ_n and projectors P_n = |ϕ_n⟩⟨ϕ_n|:

      P(λ_n) = |⟨ϕ_n|ψ⟩|² = ⟨ψ|P_n|ψ⟩

  The second form makes the geometry clear: probability is the squared
  length of the projection of |ψ⟩ onto the eigenspace.

Expectation value from Born rule:
  ⟨A⟩ = Σ_n λ_n P(λ_n) = ⟨ψ|A|ψ⟩

  This connects Born rule probability to linear algebra: the expectation
  value is simply the inner product ⟨ψ|A|ψ⟩, a weighted average over
  the spectral decomposition.

Completeness check: Σ_n P(λ_n) = Σ_n ⟨ψ|P_n|ψ⟩ = ⟨ψ|(Σ_n P_n)|ψ⟩ = ⟨ψ|I|ψ⟩ = 1
""")

psi4 = QuantumState([1/np.sqrt(5), 2j/np.sqrt(5)])
print(f"State |ψ⟩:\n{psi4.vec}\n")

print("Measuring σ_x on |ψ⟩:")
evals_x, evecs_x, projs_x = Sx.spectral_decomposition()
probs_x = []
for lam, P in zip(evals_x, projs_x):
    prob = (psi4.bra @ P @ psi4.vec)[0, 0].real
    probs_x.append(prob)
    print(f"  P(λ={lam:+.0f}) = ⟨ψ|P_n|ψ⟩ = {prob:.4f}")

print(f"\nProbabilities sum to: {sum(probs_x):.6f}")
print(f"⟨σ_x⟩ = {psi4.expect(Sx.mat).real:.4f}")
print(f"⟨σ_y⟩ = {psi4.expect(Sy.mat).real:.4f}")
print(f"⟨σ_z⟩ = {psi4.expect(Sz.mat).real:.4f}")

fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(12, 5))
for ax_bar, (op_name, op, evals_op, projs_op) in zip(
    [ax_l, ax_r],
    [("σ_x", Sx, evals_x, projs_x),
     ("σ_z", Sz, *Sz.spectral_decomposition()[:2],
      Sz.spectral_decomposition()[2])]):
    probs = [(psi4.bra @ P @ psi4.vec)[0,0].real for P in projs_op]
    ax_bar.bar([f"λ={v:+.0f}" for v in evals_op], probs,
               color=['steelblue', 'salmon'])
    ax_bar.set_ylim(0, 1)
    ax_bar.set_ylabel("Probability")
    ax_bar.set_title(f"Born Rule: Measuring {op_name}")
plt.tight_layout()
plt.show()

# =============================================================================
# POSTULATE 5: State Collapse (Projection Postulate)
# =============================================================================
print(sep + "POSTULATE 5: State Collapse (Projection Postulate)" + sep)
print("""
Mathematical translation:
  After measuring observable A and obtaining result λ_n, the state
  collapses to the normalized projection onto the λ_n eigenspace:

      |ψ⟩  →  P_n|ψ⟩ / √⟨ψ|P_n|ψ⟩

  For a non-degenerate eigenvalue this is just |ϕ_n⟩.
  For a degenerate eigenvalue, P_n projects onto a subspace; the
  post-measurement state retains the component of |ψ⟩ within that subspace.

Immediate re-measurement:
  After collapse, P(λ_n again) = ⟨ψ_after|P_n|ψ_after⟩ = 1.
  The state is now an eigenvector of A — the eigenvalue equation A|ϕ_n⟩ = λ_n|ϕ_n⟩
  is precisely the condition for certainty.

Note: This "projection postulate" (von Neumann) is the standard treatment.
  More general measurements are described by Positive Operator-Valued Measures
  (POVMs), where the measurement operators M_k satisfy Σ M_k†M_k = I but
  are not necessarily projectors.  POVMs are essential in quantum information
  (e.g., unambiguous state discrimination).
""")

# Simulate repeated measurements
evals_z, evecs_z, projs_z = Sz.spectral_decomposition()
probs_z = [(psi4.bra @ P @ psi4.vec)[0,0].real for P in projs_z]

rng = np.random.default_rng(42)
N_trials = 10000
outcomes = rng.choice(evals_z, size=N_trials, p=probs_z)
print(f"Monte Carlo ({N_trials} trials) of measuring σ_z on |ψ⟩:")
for lam, prob in zip(evals_z, probs_z):
    freq = np.mean(outcomes == lam)
    print(f"  λ={lam:+.0f}:  theoretical P={prob:.4f},  observed freq={freq:.4f}")

# Simulate single measurement → collapse → re-measure
outcome_idx = rng.choice(len(evals_z), p=probs_z)
collapsed_vec = projs_z[outcome_idx] @ psi4.vec
collapsed_vec /= np.linalg.norm(collapsed_vec)
collapsed_state = QuantumState(collapsed_vec)
print(f"\nSingle measurement outcome: λ = {evals_z[outcome_idx]:+.0f}")
print(f"Collapsed state:\n{collapsed_state.vec}")
probs_after = [(collapsed_state.bra @ P @ collapsed_state.vec)[0,0].real
               for P in projs_z]
print(f"P(same outcome on re-measurement) = {probs_after[outcome_idx]:.6f}  (should be 1)")

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
plot_bloch_sphere(ax,
                  [psi4.vec, collapsed_state.vec],
                  ["Before: |ψ⟩", f"After: λ={evals_z[outcome_idx]:+.0f} collapse"],
                  ["steelblue", "crimson"],
                  "Postulate 5: Collapse to Eigenstate")
plt.tight_layout()
plt.show()

# =============================================================================
# POSTULATE 6: Time Evolution — Schrödinger Equation
# =============================================================================
print(sep + "POSTULATE 6: Time Evolution" + sep)
print("""
Mathematical translation:
  iħ d/dt |ψ(t)⟩ = H|ψ(t)⟩   (Schrödinger equation)

  With constant H, the formal solution is the unitary operator:
      |ψ(t)⟩ = U(t)|ψ(0)⟩,   U(t) = exp(-iHt/ħ)

  U(t) is unitary (U†U = I), so it preserves the norm of |ψ⟩.
  Geometrically, it rotates the state vector — on the Bloch sphere,
  H = ω·n̂·σ⃗/2 generates precession around the axis n̂ at angular
  frequency ω.

  In the energy eigenbasis (H|E_n⟩ = E_n|E_n⟩):
      |ψ(t)⟩ = Σ_n c_n e^(-iE_n t/ħ) |E_n⟩   where c_n = ⟨E_n|ψ(0)⟩
  Energy eigenstates are stationary states — only their phase evolves.

Heisenberg picture:
  Equivalently, operators evolve and states stay fixed:
      A_H(t) = U†(t) A_S U(t),   d/dt A_H = i/ħ [H, A_H]
  Both pictures give identical expectation values and probabilities.
""")

omega = 2.0  # Larmor frequency
H_larmor = QuantumOperator(omega * Sz.mat)  # Precession around Z
psi6 = QuantumState([1, 1])  # |+⟩, pointing along X

times = np.linspace(0, 2*np.pi/omega, 200)
states_t = []
exp_x, exp_y, exp_z_t = [], [], []

for t in times:
    U = H_larmor.time_evolve(t)
    psi_t = QuantumState(U.mat @ psi6.vec)
    states_t.append(psi_t)
    exp_x.append(psi_t.expect(Sx.mat).real)
    exp_y.append(psi_t.expect(Sy.mat).real)
    exp_z_t.append(psi_t.expect(Sz.mat).real)

# Plot expectation value precession
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(times, exp_x, label="⟨σ_x⟩", color='steelblue')
ax.plot(times, exp_y, label="⟨σ_y⟩", color='darkorange')
ax.plot(times, exp_z_t, label="⟨σ_z⟩", color='green', linestyle='--')
ax.set_xlabel("Time t (ħ = 1)")
ax.set_ylabel("Expectation value")
ax.set_title("Postulate 6: Larmor Precession  H = ωσ_z/2\n"
             "⟨σ_x⟩ and ⟨σ_y⟩ oscillate; ⟨σ_z⟩ is conserved (commutes with H)")
ax.legend(); ax.set_ylim(-1.1, 1.1); ax.axhline(0, color='k', alpha=0.3)
plt.tight_layout()
plt.show()

# 3D trajectory on Bloch sphere
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
path_x, path_y, path_z_path = zip(*[state_to_bloch(s.vec) for s in states_t])
plot_bloch_sphere(ax, [psi6.vec], ["|ψ(0)⟩ = |+⟩"], ["green"],
                  "Postulate 6: Precession Trajectory on Bloch Sphere")
ax.plot(path_x, path_y, path_z_path, color='purple', linewidth=1.5,
        label="Path of |ψ(t)⟩", alpha=0.8)
ax.legend()
plt.tight_layout()
plt.show()

# Heisenberg picture comparison
print("Heisenberg picture vs Schrödinger picture at t = π/(2ω):")
t_check = np.pi / (2 * omega)
U_check = H_larmor.time_evolve(t_check)
psi_t_check = QuantumState(U_check.mat @ psi6.vec)

# Schrödinger: state evolves, operator fixed
exp_sx_schrodinger = psi_t_check.expect(Sx.mat).real

# Heisenberg: operator evolves, state fixed
Sx_H = U_check.mat.conj().T @ Sx.mat @ U_check.mat
exp_sx_heisenberg = psi6.expect(Sx_H).real

print(f"  Schrödinger: ⟨ψ(t)|σ_x|ψ(t)⟩ = {exp_sx_schrodinger:.6f}")
print(f"  Heisenberg:  ⟨ψ(0)|σ_x(t)|ψ(0)⟩ = {exp_sx_heisenberg:.6f}")
print(f"  Identical: {np.isclose(exp_sx_schrodinger, exp_sx_heisenberg)}")

# =============================================================================
# BONUS 1: Robertson Uncertainty Principle
# =============================================================================
print(sep + "BONUS 1: Robertson Uncertainty Principle" + sep)
print("""
The Heisenberg uncertainty principle is a consequence of the commutator
structure of quantum mechanics, not a statement about measurement disturbance.

Robertson's theorem:
    ΔA · ΔB ≥ ½ |⟨[A, B]⟩|

where ΔA = √(⟨A²⟩ - ⟨A⟩²) is the standard deviation of A.

For position and momentum:  [X̂, P̂] = iħ  →  ΔX · ΔP ≥ ħ/2
For spin-1/2: [σ_x, σ_y] = 2iσ_z  →  Δσ_x · Δσ_y ≥ |⟨σ_z⟩|

The bound is *state-dependent* through ⟨σ_z⟩ — it is tight only for
coherent spin states.
""")

# Sweep θ on the Bloch sphere and verify Robertson bound
thetas = np.linspace(0, np.pi, 100)
delta_x_arr, delta_y_arr, bound_arr = [], [], []

for theta in thetas:
    psi_theta = QuantumState([np.cos(theta/2), np.sin(theta/2)])
    dX = np.sqrt(max(psi_theta.variance(Sx.mat), 0))
    dY = np.sqrt(max(psi_theta.variance(Sy.mat), 0))
    exp_comm = psi_theta.expect(Sx.commutator(Sy).mat)  # = 2i⟨σ_z⟩
    bound = 0.5 * np.abs(exp_comm)
    delta_x_arr.append(dX)
    delta_y_arr.append(dY)
    bound_arr.append(bound)

product = np.array(delta_x_arr) * np.array(delta_y_arr)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(np.degrees(thetas), product,    label="Δσ_x · Δσ_y", color='steelblue', linewidth=2)
ax.plot(np.degrees(thetas), bound_arr,  label="|⟨[σ_x,σ_y]⟩|/2 (Robertson bound)",
        color='crimson', linestyle='--', linewidth=2)
ax.fill_between(np.degrees(thetas), bound_arr, product, alpha=0.15, color='steelblue')
ax.set_xlabel("Polar angle θ on Bloch sphere (degrees)")
ax.set_ylabel("Value")
ax.set_title("Robertson Uncertainty Principle: Δσ_x · Δσ_y ≥ |⟨[σ_x, σ_y]⟩|/2")
ax.legend()
plt.tight_layout()
plt.show()

all_satisfied = np.all(product >= bound_arr - 1e-10)
print(f"Robertson bound satisfied for all θ? {all_satisfied}")

# =============================================================================
# BONUS 2: Entanglement and Tensor Products (Two-Qubit Systems)
# =============================================================================
print(sep + "BONUS 2: Entanglement and Tensor Products" + sep)
print("""
For composite systems, the Hilbert space is the tensor product:
    H = H_A ⊗ H_B

A two-qubit state lives in C² ⊗ C² ≅ C⁴.
The computational basis is: |00⟩, |01⟩, |10⟩, |11⟩.

A state |ψ⟩ ∈ H_A ⊗ H_B is SEPARABLE if it can be written as |a⟩⊗|b⟩.
Otherwise it is ENTANGLED.

Bell states — maximally entangled orthonormal basis:
    |Φ+⟩ = (|00⟩ + |11⟩)/√2
    |Φ-⟩ = (|00⟩ - |11⟩)/√2
    |Ψ+⟩ = (|01⟩ + |10⟩)/√2
    |Ψ-⟩ = (|01⟩ - |10⟩)/√2

Entanglement detection via partial trace:
  For a pure state |ψ⟩, compute the reduced density matrix:
      ρ_A = Tr_B(|ψ⟩⟨ψ|)
  If ρ_A is a mixed state (Tr(ρ_A²) < 1), the state is entangled.
  Maximally entangled ↔ ρ_A = I/2 ↔ Tr(ρ_A²) = 1/2.
""")

# Construct Bell states as 4-component vectors in C^4
# Basis ordering: |00⟩=e0, |01⟩=e1, |10⟩=e2, |11⟩=e3
bell_Phi_plus  = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
bell_Phi_minus = np.array([1, 0, 0,-1], dtype=complex) / np.sqrt(2)
bell_Psi_plus  = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
bell_Psi_minus = np.array([0, 1,-1, 0], dtype=complex) / np.sqrt(2)

def partial_trace_B(psi_AB, dim_A=2, dim_B=2):
    """
    Compute reduced density matrix ρ_A = Tr_B(|ψ⟩⟨ψ|).
    psi_AB is a (dim_A * dim_B,) vector.
    """
    rho_AB = np.outer(psi_AB, psi_AB.conj())
    # Reshape to (dim_A, dim_B, dim_A, dim_B), then trace over B
    rho_reshaped = rho_AB.reshape(dim_A, dim_B, dim_A, dim_B)
    return np.einsum('ibjb->ij', rho_reshaped)

def purity(rho):
    """Tr(ρ²) — equals 1 for pure states, 1/d for maximally mixed."""
    return np.trace(rho @ rho).real

# Separable state for comparison
sep_state = np.kron(np.array([1, 0]), np.array([1, 1])/np.sqrt(2))  # |0⟩⊗|+⟩

print(f"{'State':<12}  {'Tr(ρ_A²)':<12}  {'Entangled?'}")
print("-" * 40)
for name, state in [("Separable", sep_state), ("|Φ+⟩", bell_Phi_plus),
                    ("|Φ-⟩", bell_Phi_minus), ("|Ψ+⟩", bell_Psi_plus)]:
    rho_A = partial_trace_B(state)
    pur   = purity(rho_A)
    entangled = pur < 0.999
    print(f"{name:<12}  {pur:<12.4f}  {entangled}")

# Orthonormality of Bell states
bell_states = [bell_Phi_plus, bell_Phi_minus, bell_Psi_plus, bell_Psi_minus]
bell_names  = ["|Φ+⟩", "|Φ-⟩", "|Ψ+⟩", "|Ψ-⟩"]
gram = np.array([[np.abs(b1 @ b2.conj()) for b2 in bell_states] for b1 in bell_states])
fig, ax = plt.subplots(figsize=(5, 4))
im = ax.imshow(gram, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(4)); ax.set_yticks(range(4))
ax.set_xticklabels(bell_names); ax.set_yticklabels(bell_names)
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{gram[i,j]:.1f}", ha='center', va='center', fontsize=12)
ax.set_title("|⟨Bell_i|Bell_j⟩|  (should be identity)")
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.show()

# =============================================================================
# BONUS 3: Density Matrix Formalism
# =============================================================================
print(sep + "BONUS 3: Density Matrix Formalism" + sep)
print("""
A pure state |ψ⟩ is an idealization. In practice, quantum systems are
often in a STATISTICAL MIXTURE of pure states — e.g., an ensemble from
a thermal source, or a subsystem of an entangled pair.

The density matrix ρ encodes both cases:
    Pure state:   ρ = |ψ⟩⟨ψ|,   Tr(ρ) = 1,   Tr(ρ²) = 1
    Mixed state:  ρ = Σ_k p_k |ψ_k⟩⟨ψ_k|,   Tr(ρ) = 1,   Tr(ρ²) < 1

Validity conditions:   ρ = ρ†,   Tr(ρ) = 1,   ρ ≥ 0 (positive semidefinite)

Expectation values:   ⟨A⟩ = Tr(ρ A)
Born rule (general):  P(λ_n) = Tr(ρ P_n)
Time evolution:       dρ/dt = -i/ħ [H, ρ]   (von Neumann equation)

The von Neumann entropy:   S = -Tr(ρ log ρ) = -Σ_k λ_k log(λ_k)
measures the mixedness: S=0 for pure states, S=log(d) for maximally mixed.
""")

def density_matrix(state_vec):
    """ρ = |ψ⟩⟨ψ| for a pure state."""
    v = state_vec.reshape(-1, 1)
    return v @ v.conj().T

def von_neumann_entropy(rho):
    """S = -Tr(ρ log ρ), using eigenvalues of ρ."""
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return -np.sum(evals * np.log(evals))

# Pure state density matrix
rho_pure  = density_matrix(psi4.vec)
# Mixed state: 50/50 mixture of |0⟩ and |1⟩
rho_mixed = 0.5 * density_matrix(ket0.vec) + 0.5 * density_matrix(ket1.vec)
# Maximally mixed state
rho_max   = np.eye(2) / 2

for name, rho in [("Pure |ψ⟩", rho_pure), ("Mixed 50/50", rho_mixed),
                  ("Maximally mixed I/2", rho_max)]:
    pur = np.trace(rho @ rho).real
    S   = von_neumann_entropy(rho)
    exp_z_rho = np.trace(rho @ Sz.mat).real
    print(f"{name:<22}  Tr(ρ²)={pur:.4f}  S={S:.4f}  ⟨σ_z⟩={exp_z_rho:.4f}")

# Time evolution of density matrix (von Neumann equation)
# ρ(t) = U(t) ρ(0) U†(t)
rho0 = density_matrix(ket_p.vec)
exp_x_rho, exp_y_rho = [], []
for t in times:
    U = H_larmor.time_evolve(t).mat
    rho_t = U @ rho0 @ U.conj().T
    exp_x_rho.append(np.trace(rho_t @ Sx.mat).real)
    exp_y_rho.append(np.trace(rho_t @ Sy.mat).real)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(times, exp_x_rho, label="Tr(ρ(t)σ_x)", color='steelblue', linewidth=2)
ax.plot(times, exp_y_rho, label="Tr(ρ(t)σ_y)", color='darkorange', linewidth=2)
ax.set_xlabel("Time t"); ax.set_ylabel("Expectation value")
ax.set_title("Von Neumann Equation: ρ(t) = U(t)ρ(0)U†(t)")
ax.legend(); ax.set_ylim(-1.1, 1.1)
plt.tight_layout()
plt.show()

# Visualize density matrices as matrices
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax_i, (name, rho) in zip(axes, [("Pure |ψ⟩", rho_pure),
                                     ("Mixed 50/50", rho_mixed),
                                     ("Maximally mixed", rho_max)]):
    im = ax_i.imshow(np.abs(rho), cmap='viridis', vmin=0, vmax=1)
    for i in range(2):
        for j in range(2):
            ax_i.text(j, i, f"{np.abs(rho[i,j]):.2f}", ha='center', va='center',
                     color='white', fontsize=14)
    ax_i.set_title(f"|ρ_{name}|")
    ax_i.set_xticks([0,1]); ax_i.set_yticks([0,1])
    ax_i.set_xticklabels(["|0⟩",".|1⟩"]); ax_i.set_yticklabels(["⟨0|","⟨1|"])
    plt.colorbar(im, ax=ax_i)
plt.suptitle("Density Matrices: |ρ_ij|  (off-diagonal = quantum coherence)")
plt.tight_layout()
plt.show()

# =============================================================================
# BONUS 4: Rabi Oscillations
# =============================================================================
print(sep + "BONUS 4: Rabi Oscillations — Driven Two-Level System" + sep)
print("""
A driven two-level system has Hamiltonian (in the rotating frame):
    H_Rabi = (Δ/2)σ_z + (Ω_R/2)σ_x
where Δ = ω_laser - ω_0 is the detuning and Ω_R is the Rabi frequency.

At resonance (Δ = 0): H = (Ω_R/2)σ_x
This rotates the Bloch vector around the X-axis at angular frequency Ω_R.
Starting from |0⟩, the system oscillates between |0⟩ and |1⟩ with period
T_Rabi = 2π/Ω_R.

Physical realization: NMR spin flip, atomic transition driven by laser,
superconducting qubit gate operations.
""")

Omega_R = 2.0
detuning = 0.5

for delta, label, color in [(0, "On resonance (Δ=0)", "steelblue"),
                             (detuning, f"Off resonance (Δ={detuning})", "darkorange")]:
    H_rabi = QuantumOperator((delta/2)*Sz.mat + (Omega_R/2)*Sx.mat)
    psi_rabi0 = QuantumState([1, 0])  # Start in |0⟩
    t_rabi = np.linspace(0, 4*np.pi/Omega_R, 300)
    pop1 = []
    for t in t_rabi:
        U = H_rabi.time_evolve(t)
        psi_t = QuantumState(U.mat @ psi_rabi0.vec)
        P1 = psi_t.prob_of(ket1.vec)
        pop1.append(P1)
    plt.plot(t_rabi * Omega_R / np.pi, pop1, label=label, color=color, linewidth=2)

plt.xlabel("Time (units of π/Ω_R)")
plt.ylabel("P(|1⟩) — Population of excited state")
plt.title("Rabi Oscillations: Driven Two-Level System")
plt.legend()
plt.ylim(-0.05, 1.05)
plt.axhline(0.5, color='k', linestyle=':', alpha=0.4)
plt.tight_layout()
plt.show()

print("\n" + "="*65)
print("Summary: Mathematical Connections")
print("="*65)
print("""
Postulate  Mathematical Tool             Key Insight
─────────  ──────────────────────────    ──────────────────────────────────
P1         Complex vector spaces, CP^n   State ↔ ray in Hilbert space
P2         Hermitian matrices,           Spectral theorem → real eigenvalues
           Spectral decomposition        Commutator → compatibility
P3         Eigenvalue equation           Only eigenvalues are measurable
P4         Inner products, projectors    Probability = |projection|²
P5         Projection onto subspace      Collapse = conditional state update
P6         Matrix exponential, ODE       Unitary ↔ norm-preserving flow

Beyond the postulates:
  Uncertainty     Cauchy-Schwarz on Hilbert space → ΔA·ΔB ≥ ½|⟨[A,B]⟩|
  Entanglement    Tensor products, partial trace, Schmidt decomposition
  Mixed states    Density matrices, von Neumann entropy, open systems
  General meas.   POVMs, Kraus operators, quantum channels
""")
