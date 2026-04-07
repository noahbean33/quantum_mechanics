# Revision Spec: Quantum Mechanics Notes for Engineers
## "Quantum Systems via Linear Algebra, Differential Equations, and Probability"

---

## Target Audience

General engineer. The prerequisite mathematical core is: complex-valued linear algebra (vectors, matrices, eigendecomposition), first-order ODEs, and basic probability. Analogies from control theory (LTI systems, state-space) and signal processing (Fourier transforms, bandwidth-duration product) are used freely — these should be common to all engineering disciplines. No physics background required.

---

## Universal Notation Substitutions

Apply everywhere throughout the document without exception.

| Physics Term | Engineering Replacement | Notes |
|---|---|---|
| Ket $\vert\psi\rangle$ | Column vector $\mathbf{v} \in \mathbb{C}^n$ | Unit norm: $\mathbf{v}^\dagger\mathbf{v} = 1$ |
| Bra $\langle\psi\vert$ | Conjugate transpose $\mathbf{v}^\dagger$ | Row vector |
| Inner product $\langle\phi\vert\psi\rangle$ | $\mathbf{u}^\dagger\mathbf{v}$ | Standard Hermitian inner product |
| Outer product $\vert\psi\rangle\langle\psi\vert$ | Rank-1 projector $\mathbf{v}\mathbf{v}^\dagger$ | Standard matrix |
| "Hermitian operator" / "observable" | Self-adjoint matrix $M = M^\dagger$ | Real eigenvalues guaranteed |
| Expectation value $\langle M \rangle$ | Quadratic form $\mathbf{v}^\dagger M \mathbf{v}$ | Rayleigh quotient — already known |
| Tensor product $\vert A\rangle\otimes\vert B\rangle$ | Kronecker product $\mathbf{a}\otimes\mathbf{b}$ | Standard in DSP/controls |
| $\sigma_x,\,\sigma_y,\,\sigma_z$ (Pauli matrices) | $X,\,Y,\,Z$ with explicit matrix form | Given as $2\times2$ matrices directly |
| "Qubit," "spin," "up/down" | "Two-level system," $\mathbf{e}_0, \mathbf{e}_1$ | Physics labels demoted to optional parentheticals |
| "Wave function $\psi(x)$" | Signal $v(x) \in L^2(\mathbb{R})$, component representation in position basis | Drop "wave" framing |
| "Hamiltonian $H$" | System matrix $H$ (coefficient matrix of the evolution ODE) | Named after its role first, physical interpretation second |

**Primary notation is $\mathbf{v}^\dagger$ throughout.** Dirac bra-ket notation is introduced once, explicitly, as a shorthand — see Appendix.

---

## Postulates Reframed as Axioms of the Complex State Space

Replace all physics postulate language with the following four axioms. Present these as the *complete* rule set — everything else follows from linear algebra.

**Axiom 1 — State:** The state of a system is a normalized column vector $\mathbf{v}$ in a complex vector space ($\mathbf{v}^\dagger\mathbf{v} = 1$). For a two-level system, $\mathbf{v} \in \mathbb{C}^2$.

**Axiom 2 — Observable:** A measurable quantity is represented by a self-adjoint matrix $M = M^\dagger$. Its eigenvalues $\lambda_i \in \mathbb{R}$ are the only values a measurement can return.

**Axiom 3 — Measurement (Born Rule):** Measuring $M$ on system in state $\mathbf{v}$ returns eigenvalue $\lambda_i$ with probability $P(\lambda_i) = |\mathbf{e}_i^\dagger\mathbf{v}|^2$, where $\mathbf{e}_i$ is the normalized eigenvector corresponding to $\lambda_i$.

**Axiom 4 — Time Evolution:** An isolated system evolves according to the linear ODE
$$i\hbar\,\dot{\mathbf{v}}(t) = H\mathbf{v}(t)$$
where $H = H^\dagger$ is the system matrix. Solution: $\mathbf{v}(t) = e^{-iHt/\hbar}\,\mathbf{v}(0)$.

> **Derivation note (show this, don't hide it):** Hermiticity of $H$ is not a separate postulate — it falls out of Axiom 4 plus norm preservation. If $\mathbf{v}^\dagger\mathbf{v} = 1$ must hold at all times, then $e^{-iHt/\hbar}$ must be unitary ($U^\dagger U = I$), which requires $H = H^\dagger$. The axiom structure is: norm preservation $\Rightarrow$ unitarity $\Rightarrow$ Hermitian generator. Present in this order.

---

## Measurement: Update Rule + Non-Commutativity

The collapse postulate is handled in two parts. Both must be present.

**Part 1 — State update rule:** Upon measuring $M$ and obtaining $\lambda_i$, reset
$$\mathbf{v} \leftarrow \mathbf{e}_i$$
This is Bayesian conditioning: you observed an outcome, so you update to the state consistent with that outcome. The update is instantaneous and deterministic given the result.

**Part 2 — Non-commutativity (required, not optional):** Sequential measurements of *different* observables are order-dependent. This has no classical probability analog and must be stated explicitly.

> **Example to include:** Let $Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$ and $X = \begin{pmatrix}0&1\\1&0\end{pmatrix}$. Prepare $\mathbf{v} = \mathbf{e}_0$ (eigenvector of $Z$, eigenvalue $+1$).
>
> *Path A:* Measure $Z$ → get $+1$ with certainty → state stays $\mathbf{e}_0$ → measure $Z$ again → get $+1$ with certainty.
>
> *Path B:* Measure $X$ → get $\pm 1$ each with probability $\tfrac{1}{2}$ (since $|\mathbf{e}_{\pm}^\dagger \mathbf{e}_0|^2 = \tfrac{1}{2}$) → state collapses to eigenvector of $X$ → measure $Z$ → result is now random.
>
> The act of measuring $X$ destroyed the definite value of $Z$. This happens because $[Z, X] = ZX - XZ \neq 0$, so they share no common eigenbasis. Any state that is an eigenvector of $Z$ is a superposition in the eigenbasis of $X$, and vice versa.

**The general rule:** Two observables $M$ and $N$ can be simultaneously measured (have simultaneous definite values) if and only if $[M, N] = 0$. This is a pure linear algebra statement: commutativity $\Leftrightarrow$ shared eigenbasis.

---

## Schrödinger Equation as an LTI System

Present the dynamics section in this order:

1. Write the ODE: $i\hbar\,\dot{\mathbf{v}} = H\mathbf{v}$. This is a first-order linear system with constant coefficients. Engineers solve these routinely.
2. Solution via matrix exponential: $\mathbf{v}(t) = e^{-iHt/\hbar}\mathbf{v}(0)$. Call $U(t) = e^{-iHt/\hbar}$ the evolution operator.
3. Since $H$ is Hermitian, $U$ is unitary: $U^\dagger U = I$. This is the norm-preservation condition — total probability is conserved at all times.
4. Energy eigenstates $H\mathbf{e}_k = E_k\mathbf{e}_k$ are stationary: if $\mathbf{v}(0) = \mathbf{e}_k$, then $\mathbf{v}(t) = e^{-iE_kt/\hbar}\mathbf{e}_k$ — a phase rotation, no change in measurement probabilities.
5. General solution: expand $\mathbf{v}(0) = \sum_k \alpha_k\mathbf{e}_k$, then $\mathbf{v}(t) = \sum_k \alpha_k e^{-iE_kt/\hbar}\mathbf{e}_k$. Observable dynamics come from interference between terms with different $E_k$.

> **Engineering sidebar:** Computing $e^{-iHt/\hbar}$ numerically: diagonalize $H = V\Lambda V^\dagger$, then $e^{-iHt/\hbar} = V\,e^{-i\Lambda t/\hbar}\,V^\dagger$ where $e^{-i\Lambda t/\hbar}$ is diagonal with entries $e^{-i\lambda_k t/\hbar}$. In Python: `scipy.linalg.expm(-1j * H * t / hbar)`.

---

## Uncertainty Principle as Fourier Duality

Do not present this as a physics mystery. Present it as follows:

Position-space signal $v(x)$ and momentum-space signal $\tilde{v}(p)$ are related by the Fourier transform — exactly as time-domain and frequency-domain signals in signal processing. The uncertainty inequality
$$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$$
is the Gabor limit (bandwidth-duration product) applied to this transform pair. A narrow pulse in $x$ has broad frequency content in $p$, and vice versa. This is a mathematical property of the Fourier transform, not a statement about measurement disturbance.

The *algebraic* version: $[\hat{x}, \hat{p}] = i\hbar$ (with $\hat{p} = -i\hbar\frac{d}{dx}$ acting on $L^2(\mathbb{R})$), and the uncertainty bound $\Delta x\,\Delta p \geq \hbar/2$ follows from this commutator by a standard algebraic argument (quadratic form non-negativity). Both derivations should appear.

---

## Entanglement as Rank Condition

For two two-level systems, the composite state lives in $\mathbb{C}^2 \otimes \mathbb{C}^2 = \mathbb{C}^4$. Write the coefficient matrix:
$$\Psi = \begin{pmatrix}\alpha_{00} & \alpha_{01} \\ \alpha_{10} & \alpha_{11}\end{pmatrix}$$

- **Product state** (unentangled): $\text{rank}(\Psi) = 1$, i.e., $\Psi = \mathbf{a}\mathbf{b}^\top$ for some $\mathbf{a}, \mathbf{b} \in \mathbb{C}^2$.
- **Entangled state:** $\text{rank}(\Psi) \geq 2$. Cannot be written as a Kronecker product.

The Schmidt decomposition is the SVD of $\Psi$. The singular values $\sigma_i$ quantify the degree of entanglement. For a pure state, $\text{Tr}(\rho_A^2) = \sum_i \sigma_i^4 / (\sum_i \sigma_i^2)^2$ — maximal entanglement corresponds to equal singular values.

The reduced density matrix (subsystem description when the other half is inaccessible) is obtained by partial trace: $\rho_A = \text{Tr}_B(\mathbf{v}\mathbf{v}^\dagger)$. This is marginalization — summing out the degrees of freedom you cannot observe.

---

## Experimental Motivation: Side Blurbs

Rather than restructuring the notes around experimental derivation, include short clearly-labeled "Experiment says:" sidebars that state the experimental fact and point to the mathematical axiom it motivates. These replace the long apparatus/detector narrative sections.

Example format:

> **Experiment says:** When a two-level system is prepared and immediately re-measured with the same observable, the result is always the same. *(Motivates: state update rule — measuring $M$ and obtaining $\lambda_i$ resets the state to $\mathbf{e}_i$, so the next measurement of $M$ is deterministic.)*

> **Experiment says:** Measuring one component of spin randomizes the other. A system prepared with definite $Z$-value gives $\pm 1$ with equal probability when $X$ is measured. *(Motivates: $[Z, X] \neq 0$ — no shared eigenbasis, so a $Z$-eigenstate is an equal superposition in the $X$-eigenbasis.)*

> **Experiment says:** The average result of many identical measurements of $M$ on state $\mathbf{v}$ converges to $\mathbf{v}^\dagger M\mathbf{v}$. *(Motivates: Born rule — this is exactly $\sum_i \lambda_i|\mathbf{e}_i^\dagger\mathbf{v}|^2$.)*

This keeps the experimental grounding without letting it drive the logical structure. The math is primary; the experiments confirm it.

---

## Content to Cut Entirely

- Classical coins/dice/die logic of propositions (AND/OR/NOT as set operations)
- Apparatus, detector, pointer, "black box" physical metaphors
- "Prisoners of neural architecture" visualization warning
- Susskind references and physics history narrative
- Dirac sea / negative energy section (belongs in QFT)
- All extended 3D spin-direction geometry ("the qubit has directionality in all three dimensions of space")
- Wheeler's "machine" metaphor for operators
- "Expectation value is a misnomer" tangent

---

## Content to Keep

- The six eigenvector column vectors for $X$, $Y$, $Z$ — rename "Eigenvectors of the Three Standard Observables," give explicit column form
- Pauli matrix algebraic properties ($X^2 = Y^2 = Z^2 = I$, $XY = iZ$ and cyclic, $[X,Y] \neq 0$) — keep, these are used constantly
- Commutator derivations via explicit matrix multiplication — keep, this is exactly how engineers should verify things
- Density matrix and partial trace — keep, stated in terms of marginalization
- No-signaling theorem proof — keep, the unitarity argument is clean and instructive
- Ehrenfest theorem — keep as bridge to classical limit, presented as expectation-value ODE

---

## Continuous Systems (Lectures 9–10)

Lead with: $L^2(\mathbb{R})$ is an infinite-dimensional Hilbert space. Position and momentum bases are related by the Fourier transform — same mathematics as time/frequency in signal processing. Then:

- Momentum operator $\hat{p} = -i\hbar\frac{d}{dx}$ is the generator of spatial translations — it is the operator whose eigenfunctions are plane waves $e^{ipx/\hbar}$ with eigenvalue $p$.
- $[\hat{x}, \hat{p}] = i\hbar$ — derive this by applying $\hat{x}\hat{p} - \hat{p}\hat{x}$ to an arbitrary $v(x)$, one line of calculus.
- Dirac delta $\delta(x - x_0)$ is the continuum limit of an orthonormal basis vector — the "position eigenstate" with eigenvalue $x_0$.
- Transition from discrete to continuous: $\sum_i \rightarrow \int dx$, Kronecker $\delta_{ij} \rightarrow \delta(x - x')$, column vector $\rightarrow$ function $v(x)$.

---

## Engineering Bridge Statements

Include these explicitly in the text as labeled connections, not footnotes.

| QM Concept | Engineering Analog |
|---|---|
| Energy eigenstates | Normal modes of a coupled oscillator system |
| Eigenvalues of $H$ | Natural frequencies / poles of the system |
| Unitary evolution $U^\dagger U = I$ | Lossless network / power-preserving two-port ($S^\dagger S = I$) |
| Heisenberg uncertainty | Gabor limit / time-bandwidth product |
| Partial trace | Marginalization over latent variables |
| Schmidt decomposition | SVD of the coefficient matrix |
| Non-commuting observables | Non-commuting transfer functions in feedback loops |

---

## Appendix: Dirac Notation Translation

Include once at the end as a reference section. Framing: "You will encounter this notation in all quantum mechanics literature. It is a shorthand for the matrix-vector operations used throughout these notes."

| Dirac notation | Matrix notation used in these notes |
|---|---|
| $\vert\psi\rangle$ | $\mathbf{v}$ |
| $\langle\psi\vert$ | $\mathbf{v}^\dagger$ |
| $\langle\phi\vert\psi\rangle$ | $\mathbf{u}^\dagger\mathbf{v}$ |
| $\vert\psi\rangle\langle\psi\vert$ | $\mathbf{v}\mathbf{v}^\dagger$ |
| $\langle\psi\vert M\vert\psi\rangle$ | $\mathbf{v}^\dagger M\mathbf{v}$ |
| $M\vert\psi\rangle = \lambda\vert\psi\rangle$ | $M\mathbf{v} = \lambda\mathbf{v}$ |
| $\sum_i \vert i\rangle\langle i\vert = I$ | $\sum_i \mathbf{e}_i\mathbf{e}_i^\dagger = I$ (resolution of identity) |
| $\vert A\rangle\otimes\vert B\rangle$ | $\mathbf{a}\otimes\mathbf{b}$ (Kronecker product) |

No further use of Dirac notation in the main text.
