Appendix 1: Bra–ket Notation
Bra-ket notation was introduced by Paul Dirac in 1939 and is sometimes called Dirac notation consequently. Kets are denoted by a pipe ("|") and right-angle bracket ("⟩"), like so – |Label⟩, while bras are denoted by a left-angle bracket ("⟨") and pipe ("|"), like so ⟨Label|. Kets represent vectors in a Hilbert space and bras represent their covectors in a dual Hilbert space. The labels for kets and bras can be lowercase letters, numbers, and greek letters. Uppercase letters are usually reserved for operators, which we will get to later.

The computational basis vectors are represented by |0⟩ and |1⟩. It is important to note that the zero vector is denoted by 0 and is totally different than |0⟩. The zero vector, sometimes referred to as the null vector, is the only one that is not represented as a ket.

An inner product between two kets, |ϕ⟩ and |ψ⟩, is notated this way – ⟨ϕ|ψ⟩. This can be called a "bracket" and brings the notation full circle.

Other notations used are shown in the following table:


day-modeBookmark
Operators
Operators are represented by capital letters such as A, B, and C. Operators can be represented by matrices numerically, as shown in the following diagram:



The rest of bra-ket notation will be explained as the book progresses. The next section is a very advanced treatise on bras and is optional.

Bras
A bra is a linear functional. We talk about these in Chapter 5, Transforming Space with Matrices. To help jog your memory, they are a special case of linear transformation that takes in a vector and spits out a scalar:


For instance, I could define a linear functional for every vector in ℝ2:


So that:


There are many linear functionals that can be defined for a vector space. Here's another one:


The set of all linear functionals that can be defined on a vector space actually form their own vector space called the dual vector space.

Instead of using the usual function notation for these linear functionals, Paul Dirac came up with a notation that he called a bra:


Since every vector has its own linear functional (called its dual vector or covector), the label between the angle bracket and vertical bar or pipe is the dual vector for the ket with the same label. In other words, every ket |v⟩ has a linear functional 〈v| defined for it.

Now the big question is, what is the function that is defined for each ket? That, my friend, is the inner product, defined as follows and explained in Chapter 8, Our Place in the Universe:


day-mode