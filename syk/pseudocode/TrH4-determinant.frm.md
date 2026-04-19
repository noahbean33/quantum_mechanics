# TrH4-determinant.frm — Pseudocode

FORM symbolic algebra script for computing Tr(H^n) in the SYK model.
FORM is a computer algebra system for high-energy physics.

```
Purpose:
  Symbolically compute traces of products of SYK Hamiltonian operators
  Tr(op^1), Tr(op^2), ..., Tr(op^7) where each 'op' is a sum of two
  antisymmetric operators A(tt1,tt2,t1,t2).

Key steps:
  1. Define local expressions [tr_op1] through [tr_op7] as products of
     op(tt1,tt2,tt3,tt4,t1,t2) with contracted time indices.

  2. Expand op into a sum of antisymmetric terms A:
       op(tt1,tt2,tt3,tt4,t1,t2) = A(tt1,tt2,t1,t2) + A(tt3,tt4,t1,t2)

  3. Expand A into signed delta-operator products:
       A(tt1,tt2,t1,t2) = signDeltaOp(tt1,tt2,t1,t2) - signDeltaOp(tt2,tt1,t1,t2)
       signDeltaOp(tt1,tt2,t1,t2) = sign(t1,tt1) * delta(t2,tt2)

  4. Contract all Kronecker deltas.

  5. Simplify sign functions using:
     - sign(t,t) = 0
     - sign(t1,t2)^2 = 1
     - Canonical ordering: sign(tti,ttj) with i<j (flip introduces minus)
     - Time ordering convention: sign(tt1,tt2)=-1, sign(tt1,tt3)=-1, etc.
     - Lemma: sign(t,tt3)*sign(t,tt4) = 1 - sign(t,tt3) + sign(t,tt4)

  6. Print the simplified result.

This computes the "determinantal" structure of Tr(H^4) used in
moment calculations of the SYK model.
```
