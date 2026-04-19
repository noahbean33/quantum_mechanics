Chapter 8: Our Space in the Universe
Our space in the universe is called a Hilbert space. A Hilbert space is a type of vector space that has certain properties – properties that we will develop in this chapter. The most important will be defining an inner product. Once this is done, we will be able to measure distance and angles between vectors in an n-dimensional complex space. We will also be able to measure the length of vectors in these spaces. Later in the chapter, we will look at putting these Hilbert spaces together into even bigger Hilbert spaces through the tensor product!

The other main topic of this chapter is linear operators. We will go through many types, showing the distinct properties of each.

In this chapter, we are going to cover the following main topics:

The inner product
Orthonormality
The outer product
Operators
Types of operators
Tensor products
day-modeBookmark
The inner product
An inner product can actually be any function that follows a few properties, but we are going to zero in on one definition of the inner product that we will use in quantum computing. Here it is:


Mathematicians use the preceding notation for the inner product, but Dirac defined it with a bra and ket, calling it a bracket:



Now, if we define a bra to be the conjugate transpose of its corresponding ket, so that if:


Then, ⟨x| is now:



We can then define a bracket as just matrix multiplication!


Pretty cool, eh? That is one of the reasons why bra-ket notation is so convenient! You should notice something else too. The bra ⟨x| is a linear functional. It will take any vector |y⟩ and give you a scalar according to the inner product formula!

Let's look at an example. Let's say |x⟩ and |y⟩ are defined this way:


Then, the bras are going to be:



Now, let's calculate the inner product ⟨y|x⟩:



Let's reverse the inner product and calculate ⟨x|y⟩:


You might have noticed that the preceding answers are complex conjugates of each other; that's because:


Since bras are linear functionals, brackets are left-distributive (α and β are scalars):


(1)

And they are also right-distributive:



Let's test the left-distributive property in an example where we evaluate both sides of Equation (1) separately. We will define all the variables first. Our two scalars will be α = 3 and β = 2. Our vectors are defined as follows:


Alright, here we go. Let's evaluate the left side of Equation (1) first:


And now for the right side of Equation (1):


Luckily, our answers match. Whew! I didn't want to have to go back and do that again! Let's move on to see how the inner product can be used in vector spaces.

day-modeBookmark
Orthonormality
In this section, we will look at the concepts of the norm and orthogonality to come up with orthonormality.

The norm
We can define a metric on our vector spaces called the norm and denote it this way, ∥x∥, where x is the vector on which the norm is being measured. In two- and three-dimensional Euclidean spaces, it is often called the length of a vector, but in higher dimensions, we use the term norm. It gives us a way to measure vectors.

We define the norm using our inner product from the previous section, like so:



As always, let's look at an example. What is the norm of the vector |x⟩ here?


Well, let's work it out:


As you can see, the norm, ∥x∥, of |x⟩ is the square root of 29.

Normalization and unit vectors
Oftentimes, especially in quantum computing, we will want to represent our vectors by something called a unit vector. The word unit refers to the fact that the norm of these vectors is one. How do we achieve this? Well, we divide a vector by its norm in a process called normalization.

A unit vector |u⟩ is found for the vector |v⟩ using the following formula:



What is the unit vector for the vector |x⟩ from the previous section? Well, we just divide |x⟩ by its norm to obtain:


You should take the norm of |u⟩ to ensure that it is indeed 1.

Orthogonality
Orthogonal may not be a word you've seen before, but I bet you are familiar with the word perpendicular. For instance, the two vectors in the following graph are perpendicular to each other:

Figure 8.1 – Two perpendicular vectors
Figure 8.1 – Two perpendicular vectors

Orthogonality is taking the concept of vectors being perpendicular to each other to higher dimensions of ℂn.

The inner product is helpful in this regard as well. If two vectors are orthogonal to each other, their inner product will be 0. Let's see whether the two vectors in Figure 8.1 are orthogonal according to the inner product:


Indeed, they are orthogonal, as their inner product is zero. Are the next two vectors orthogonal?


Well, let's see!


So, no – they're not! Now, it's your turn.

Exercise one
Determine whether each pair of vectors is orthogonal using the inner product:



Orthonormal vectors
So, if we combine the concept of orthogonality and normalization, we get orthonormal vectors. These are very important in the study of vector spaces and quantum computing.

Let's see whether we can come up with some orthonormal vectors in ℂ2. We'll try the computational basis vectors:



Are they orthogonal?



Well, their inner product is zero, so they are orthogonal! Are they unit vectors?


Yes! The square root of their own inner product (aka their norm) is one. So |0⟩ and |1⟩ are orthonormal (hint: that's one of the reasons they were chosen as the canonical 0 and 1 vectors).

Let's look at another set of vectors that are important in quantum computing. They are labeled with plus and minus signs:


What do you think? Orthonormal? Or just normal? How do we know? That's right – we use our formulas. Let's see whether they are orthogonal first:


Okay, so their inner product is zero. Therefore, they are orthogonal. Are they normal or abnormal (he-he)?


Looks like they're normal! So |+⟩ and |-⟩ are orthonormal vectors.

The Kronecker delta function
Almost all vectors in quantum computing are unit vectors and many are orthogonal to each other. When you are dealing with orthonormal vectors and doing computations, it is convenient to use the Kronecker delta function. It is defined thusly:


So, when you see that symbol, if the indices of i and j are equal, then it is one. Otherwise, it is zero.

A good example is the identity matrix. If you replace the entries with the Kronecker delta function, you will get ones on the main diagonal when the indices of the entries equal each other:


More importantly, when you have a basic set of orthonormal vectors, the inner product of a vector with itself is one because they are normalized. The inner product is zero when you use any other basis vector because they are orthogonal. For instance, take the basis set B with orthonormal vectors:



We can then use the Kronecker delta function to succinctly represent their inner product:



I want you to know this function because you will see it in quantum computing literature, and it helps us in succinctly describing computations.

day-modeBookmark
The outer product
The outer product is interesting because it is again the matrix multiplication of two vectors, but this time, the vectors are reversed, producing a matrix. The inner product uses the matrix multiplication of two vectors to get a scalar. The outer product uses two vectors to produce a matrix. Formally, the outer product is defined to be:


If you remember matrix multiplication from Chapter 2, The Matrix, we have the following situation when multiplying an m × n matrix and an n × p matrix. They produce an m × p matrix, as shown in the following diagram. Since we are dealing with vectors, we have an m × 1 matrix and a 1 × p matrix:

Figure 8.2 – The schematics of matrix multiplication
Figure 8.2 – The schematics of matrix multiplication

Let's look at an example. First, we have two vectors |u⟩ and |v⟩:


Now, let's do the outer product with them:


Is the outer product commutative? Well, let's try:


Apparently not! So, in general, |u⟩⟨v| ≠|v⟩⟨u|. Look closely at the matrices for the final answers though. Do you see any similarities? That's right – they are the transpose of each other! This leads us to the following property of the outer product:



You should also note that the outer product is distributive over addition, so:



(2)


So, let's try out Equation (2) on our friends |0⟩ and |1⟩. Here's the left side of the equation:


As an exercise, compute the right side of Equation (2), and make sure that you get the same answer as you just got for the left side.

Exercise two
Compute the following:



day-modeBookmark
Operators
In this section, we will consider linear operators. We first described these in Chapter 5, Transforming Space with Matrices. To reiterate, linear operators are linear transformations that map vectors from and to the same vector space. They are represented by square matrices. For just this section, I will put a "hat" or caret on the top of operators and use just the uppercase letter for matrices, as I want to be deliberate when referencing operators.

For instance, let's look at the X̂ operator that transforms the zero and one states:





Now, let's come up with a matrix that represents this operator. The question becomes, which basis will we use? Let's use the computational basis, which is |0⟩ and |1⟩. I will denote this set of basis vectors by the letter C. So, the X̂ operator in the C basis is represented by:



Now, I want to come up with a matrix representation of X̂ in the |+⟩, |-⟩ basis, which I will denote as +,-. Here is the matrix representation of the X̂ operator in the +,- basis:


Now that we have refreshed our knowledge around linear operators (which I will sometimes just call operators), let's look at another way we can represent an operator.

Representing an operator using the outer product
Can we use the outer product to represent an operator? Well, since the computation of an outer product results in a matrix, we most certainly can. But, given the previous discussion, since the outer product is a matrix, multiple outer products can represent an operator.

Let's show that we can by writing an equation in which a matrix A transforms a vector:


(3)

Now, let's try to represent our matrix A by an outer product between two vectors |u⟩ and |v⟩:



Okay, let's rewrite Equation (3) using our new outer product representation of the matrix A:



Due to the properties of the inner product and outer product that we have enumerated in the previous sections, we can rewrite this as:



Due to bra-ket notation, we can rewrite this with a bracket:


(4)

We know that a bracket denotes an inner product and therefore produces a scalar, like so:



We can take our scalar α and put it back into Equation (4) and rearrange it:



We now see that the ket |y⟩ that was a product of the matrix multiplication in Equation (3) is just another ket proportional to |u⟩. This is great because it shows that we can represent a linear operator with an outer product in bra-ket notation. Not only that, the resulting ket will be proportional to the ket we use in the outer product.

So, how can this be used? Let's say we have an operator Ô defined with our plus and minus kets from before. This gives us a matrix O defined in an outer product, like so:



Now, we want to know what our new operator Ô does to the minus ket. We can do it without ever resorting to matrices, like so:







So, our operator Ô turns the minus ket into the plus ket. You try it now.

Exercise 3
What does the operator Ô do to the plus ket? In other words, what is the following?



The completeness relation
The following relation goes under a few names (the closure relation and the resolution of identity), but I will go with the name completeness relation. I will just state it without proving it, as the proof is rather laborious. We start with an orthonormal basis B where:



Then, the identity operator Î can be written as an outer product, like so:

 (5)

That's it. Doesn't seem like much, does it? But it is used over and over again in quantum computing to manipulate bra-ket expressions.

So, let's apply this to an example. Let's take our basis to be the plus and minus kets {|+⟩,|-⟩}. How then do we write the identity operator in this basis using the outer product representation? Well, using Equation (5), we get:



Now, let's test the completeness relation. If we apply the identity operator to the plus ket, we should get the plus ket back. Let's see:


Indeed, we do get the plus ket back, and hence, we can see how the completeness relation works in a simple example.

The adjoint of an operator
As we saw, we can manipulate operators using bra-ket notation without resorting to a matrix representation. We also saw the use of the dagger symbol when looking at the conjugate transpose. Now, I'd like to take a step back and put this all together to define the adjoint of an operator.

In this definition, we need to remember that for every ket |x⟩, there is a bra ⟨x|. Let's say we have an operator Â that acts on |x⟩ to give us |y⟩:



Is there an associated operator we can use on the bra ⟨x| to give us the associated bra ⟨y|of the ket |y⟩? It happens that there is, and it is named the adjoint of the operator Â and written this way:



Now, there are rules when manipulating adjoint operators that you must keep in mind. First, the adjoint of a scalar is its complex conjugate:





You can distribute the adjoint operation amongst scalar multiplication of operators, like so:



I will reiterate that bras and kets are the adjoints of each other:





If you take the adjoint of an adjoint, you get back the original operator:



You cannot distribute the adjoint across the multiplication of operators; rather, they anti-commute:



Finally, the adjoint can be distributed across a sum of operators:



I know this seems like a lot of rules, but you will need them when you manipulate bra-ket expressions in quantum computing.

Finally, if an operator is expressed as an outer product, we can take its adjoint in the following way:





When an operator is represented as a matrix on an orthonormal basis, then its adjoint is the conjugate transpose of the matrix:



Let's look at a quick example. The X̂ operator we have looked at previously can be represented in the computational basis as an outer product thusly:



Now, let's take the adjoint of X:







If you look closely, you should notice that the adjoint of X is equal to the original X. That's because X̂ is Hermitian, which we will discuss in our next section.

day-modeBookmark
Types of operators
There are certain types of linear operators that are special and need to be defined so that we can refer to them later in the book. You will also hear of them all the time in quantum computing.

Normal operators
Normal operators are ones that commute with their adjoint. For an operator Â, if:

 (6)

then Â is normal. They are important because a normal operator is diagonalizable, which is something we will consider later in the book. The following operators (Hermitian, unitary, positive, and positive semi-definite) are all normal operators.

A normal matrix represents a normal operator, and it commutes with its conjugate transpose. Let's look at an example normal matrix A:


Its conjugate transpose is:


Now, let's see if A commutes with its conjugate transpose. We'll calculate the left side of Equation (6) first:







And now we do the same for the right side of Equation (6):







And there you go – the answers match and, therefore, our example matrix A is a normal matrix!

Normal operators and matrices have special properties, namely:

They are diagonalizable; this will come up in the next chapter.
Their eigenvalues are the conjugates of the eigenvalues of their adjoints.
The eigenvectors associated with different eigenvalues are orthogonal.
A vector space can be defined by an orthogonal basis set of these eigenvectors.
The operators that follow are all special types of normal operators.

Hermitian operators
The definition of a Hermitian operator is rather terse and simple as well. A Hermitian operator is an operator that is equal to its adjoint:



You will also hear these referred to as self-adjoint operators.

Since Hermitian operators are normal, they have all their properties plus one more:

All their eigenvalues are real numbers
Hermitian operators play an important part in quantum computing, as all measurements of a quantum state are done via a Hermitian operator.

Unitary operators
Unitary operators are very important, as they describe the evolution of a quantum state and therefore all gates in quantum computing are unitary. They also have a very simple definition:



Using this definition, we can also derive that:





Unitary operators have two unique properties. First, their eigenvalues are complex numbers of modulus one:



And they preserve the inner product.

Let's quickly prove that they preserve the inner product using bra-ket notation:







A consequence of unitary operators preserving the inner product is that they also preserve the norm of transformed vectors.

Unitary operators are represented by unitary matrices, and similarly:



In general, unitary matrices are expressed this way:


The determinant is:



Since all quantum computing gates are unitary, let's look at one and test it. The phase shift gate is represented in the computational basis by the following matrix:


To find the inverse of a matrix, we use our formula from Chapter 7, Eigen-Stuff:


So, first, we have to find its determinant:



Now, we just plug and play:


Now for the moment of truth – is it unitary?


Indeed, it is! Let's move on to projection operators.

Projection operators
We covered projection linear transformations in Chapter 5, Using Matrices to Transform Space. In that chapter, we defined a projection this way. If you have a linear transformation P, then if the following condition holds, it is a projection:

(7)


In quantum computing, they are defined a little differently:



(8)


Equation (7) still holds for projection operators, but given the definition in Equation (8), you also get that the projection operator is Hermitian:



All Projections Are Orthogonal in Quantum Computing

While there are non-orthogonal projection transformations in mathematics, we do not use them in quantum computing, so when you hear projection, assume that it is an orthogonal projection unless explicitly told otherwise.

If two projection operators commute, then their product is also a projection operator:





In quantum computing, we often project one vector space onto another. Let's say I have a vector in an n-dimensional vector space defined by the basis {|0⟩,|1⟩,…|n⟩} and I want to project it onto an m-dimensional subspace defined by the basis {|0⟩,|1⟩,…|m⟩}. Both bases are orthonormal. Then, the projection operator that projects onto our subspace is defined by:



The only eigenvalues a projection operator can have are zero and one. Now, let's move on to positive operators.

Positive operators
Positive operators are happy and optimistic, always looking on the bright side of life. Okay, maybe that's a joke :) Mathematically, positive operators are Hermitian. There are actually two types of positive operators, and they are only slightly different.

An operator Â is said to be positive definite if:


(9)

Please consult the appendix on Bra-Ket notation if you are unfamiliar with the notation in Equation (9).

An operator Â is said to be positive semidefinite if:



So the only difference is that positive definite operators do not include zero in their definition. All eigenvalues of positive operators are non-negative.

Okay, well, we're done with types of operators! There are quite a few, but they will come up in different segments of quantum computing, so try to keep them all straight.

No More Hats

As I said at the beginning of the section on operators, I will drop the hat or caret on top of operators, and you should be able to derive whether I mean an operator or a matrix from the context in which it is used.

day-modeBookmark
Tensor products
Tensor products are a way to combine vector spaces. One of the postulates of quantum mechanics is that the state of a qubit is completely described by a unit vector in a Hilbert space. The problem then becomes how to deal with more than one qubit. This is where a tensor product comes in. Each qubit has its own Hilbert space, and to describe many qubits as a system, we need to combine all their Hilbert spaces into one bigger Hilbert space.

Mathematically, that means that if we have a Hilbert space H and another Hilbert space J, we denote their tensor product as:



If H is an h dimensional space and J is a j dimensional space, then the dimension of the combined space M is h ⋅ j. In other words:



Before we go any farther, let's look at the tensor product of two vectors.

The tensor product of vectors
The tensor product of two vectors is denoted in the following way in bra-ket notation. You'll notice that there are four different ways to notate it, so be careful when you come across it in quantum computing literature and know exactly what you are dealing with:



Here are some of the properties of the tensor product:

For a scalar s and a vector |u⟩ in U and vector |v⟩ in V, then:


It is both right and left distributive. For vectors |v⟩ and |w⟩ in V and vectors |u⟩ and |z⟩ in U, then:




It is not commutative, so in general:


Now, let's look at how we do the tensor product for actual column vectors. When the tensor product is implemented with arrays of numbers, it is actually the Kronecker product. Keep this in mind when researching and reading about the tensor product.

So, here is the Kronecker product defined mathematically for vectors. The tensor product of vectors is defined as:


In other words, take the first component of |x⟩ and multiply it by every component of |y⟩, then take the second component of |x⟩ and multiply it by every component of |y⟩, and repeat this procedure until all of the components of |x⟩ are exhausted! That's a lot to say! Let's look at a definition with just 1 × 2 vectors:


That's not bad, right? By the way, if you noticed, the tensor product of two vectors always produces another vector. Here is an example for you:


Alright, how about some examples with our two favorite vectors |0⟩ and |1⟩? Let's do a tensor product between them:


Exercise four
What is |11⟩?
What is |10⟩?
The basis of tensor product space
You will remember that we can completely describe a vector space by its basis. The same is true of a tensor product space. To get the basis of the tensor product space, you take the tensor product of each basis vector in one space with every basis vector in the other space involved in the tensor product. I hope you remember the Cartesian product from Chapter 3, Foundations. A quick reminder is that if I have two sets A={x, y, z} and B={1, 2, 3}, their Cartesian product is all the ordered pairs shown in the following graphic:

Figure 8.3 – An example of the Cartesian product of A × B [1]
Figure 8.3 – An example of the Cartesian product of A × B [1]

So, another way to describe the basis of the new tensor product space is to first take the Cartesian product of all basis vectors and then do the tensor product between all the ordered pairs. And there you go!

Let's look at an example. What if we had two vector spaces, U and V, that were both two-dimensional? The basis for U is {|0⟩,|1⟩}, and the basis for V is {|+⟩,|-⟩}. Then, what is the basis for the tensor product of U and V? We have to calculate all the following tensor products:


So let's look at one of these and calculate it using the Kronecker product:


So, that is one of the four vectors that are in the basis of our tensor product. Of course, once we have a basis, we can describe every vector in the space as a linear combination of our new basis vectors.

Exercise five
Calculate the Kronecker product of the following:


The tensor product of operators
In bra-ket notation, there are rules to follow about the tensor product of linear operators. First, let's define the tensor product of operators in bra-ket notation. Let's say we have a vector |v⟩ and linear operator A in vector space V. We also have a vector |u⟩ and linear operator B in vector space U. Then, A ⊗ B on the tensor product space of U ⊗ V is defined as:



Let's look at an example. We'll say we have two familiar linear operators X and Z and vector states |0⟩ and |1⟩. Here is the math of our example:


(10)

The Kronecker product of matrices
When we represent operators with matrices, we can calculate the tensor product using the Kronecker product. It is very similar to the Kronecker product for vectors, as column vectors are just n × 1 matrices. You basically take the first matrix entries and multiply them by the second matrix. Here's the definition. Given an m x n matrix A and a p × q matrix B, then their Kronecker product is an (m ⋅ p) × (n ⋅ q) matrix, like so:


That's pretty abstract; let's look at an example. Let's make matrix A a 2 × 2 matrix and B a 2 × 2 matrix as well. What will be the dimension of their Kronecker product? From the definition, we see it will be 4 × 4. Here's the example:


Exercise six
What is B ⊗ A?

Now, let's redo our example from earlier, Equation (10), in matrix form to double-check our work:


Indeed, we get the same answer, which is assuring! Finally, let's look at the inner product for tensor product spaces.

The inner product of composite vectors
This is actually probably the most important definition when it comes to the tensor product because it enables us to have a Hilbert space as the output of our tensor product. Without further ado, here is the definition of the inner product for the tensor product of two vector spaces.

Two Hilbert spaces V and U create a tensor product space W:



For vectors |v⟩ and |x⟩ in V and vectors |u⟩ and |z⟩ in U, we define two composite vectors in W:



We now define the inner product of these two composite vectors |w⟩ and |y⟩ as:


(11)

We were able to simplify in Equation (11) due to the mixed-product property of the Kronecker product:


The inner product of two of our computation basis vectors in ℂ4 should be zero. Let's check:


Indeed, it is! Whew!

Exercise seven
Calculate the following inner products:


This concludes our discussion of tensor products.

day-modeBookmark
Summary
We have covered a lot of ground in this chapter, but I hope you feel it's been worth it. I think it has because it brings everything we have worked on in the previous chapters together into one framework. Also, we can do real math with quantum computing now that we just couldn't do before. We will build on this in the last chapter to reach new heights in quantum computing that, at first, probably looked unattainable!