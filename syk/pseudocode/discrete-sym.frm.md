# discrete-sym.frm — Pseudocode

FORM symbolic algebra script for checking discrete symmetries of the Kitaev Hamiltonian.

```
Purpose:
  Verify that the complex-conjugated Hamiltonian H* equals H
  (i.e. check when the Hamiltonian is real up to a basis transformation).

Key steps:
  1. Define H - H* (called [HC]) in terms of creation (cd) and annihilation (c)
     operators with coupling J(i,j,k,l) and its conjugate Jstar(i,j,k,l).

  2. Use the identity Jstar(i,j,k,l) = J(k,l,i,j) (Hermiticity of J).

  3. Apply canonical anti-commutation relations:
       c(i) * cd(j) = delta(i,j) - cd(j) * c(i)

  4. Use antisymmetry of J:
       J(i,j,j,k) = -J(j,i,j,k), etc.

  5. Reorder all terms into a canonical form:
       J(i,j,k,l) * cd(i) * cd(j) * c(k) * c(l)
     using various index-relabeling identities.

  6. Print the result.
     If [HC] simplifies to 0, the Hamiltonian has the discrete symmetry H = H*.

This is relevant for determining whether the SYK model falls into the
GOE or GUE random matrix universality class.
```
