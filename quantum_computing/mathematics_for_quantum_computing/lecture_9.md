Chapter 9: Advanced Concepts
In this chapter, we will go into some advanced linear algebra concepts. These will not come up all the time in quantum computing, but when they do, you should know what they are and where to find information about them. Almost all the topics are about decomposing a matrix. This becomes important in quantum computing because when we come up with a unitary transformation that we'd like to do on a quantum computer, we will only have certain unitary operators to use on it. Then, it becomes a question of which combination of available operators we should use so that we can perform our overall unitary transformation. Along the way, we will also look at important inequalities and how to represent functions that have matrices in them.

In this chapter, we are going to cover the following main topics:

Gram-Schmidt
Cauchy-Schwarz and triangle inequalities
Spectral decomposition
Singular value decomposition
Polar decomposition
Operator functions and the matrix exponential
day-modeBookmark
Gram-Schmidt
The Gram-Schmidt process is an algorithm in which you input a basis set of vectors and it outputs a basis set that is orthogonal. We can then normalize that set of vectors, and suddenly, we have an orthonormal set of basis vectors! This is very helpful in quantum computing and other areas of applied math, as an orthonormal basis is usually the best basis for computations and representing vectors with coordinates.

Gram-Schmidt Is a Decomposition Tool

While we won't go into it in this book, the Gram-Schmidt process is used in certain decompositions, so it's good to know from that vantage point too.

Let's look at an example before getting into the nitty-gritty of the actual procedure (which can be dry and dull). Let's say I have a basis for ℂ2, such as the following:


These vectors are not orthogonal, since their inner product does not equal 0:


They are also not normalized. Now, I want to get an orthonormal basis for ℂ2 using these two vectors. Here's the process. The first step is the easiest; we just choose the first vector in our set, |x1⟩, to be the first vector in our soon to be orthogonal basis set (denoted by |v1⟩):


That was easy enough. This is the easiest step of Gram-Schmidt, which is always the first step. Now for the second step. Here is the formula:


Let's calculate the numerator of the right part of the equation first:


Now for the denominator:


Finally, let's put it all together!


So, our new orthogonal basis for ℂ2 is the following basis set:


You should calculate their inner product to ensure it is zero and that they are indeed orthogonal. So, now all we need to do is normalize them to get an orthonormal basis! Let's do |v1⟩ first:


Now for |v2⟩:


We now have an orthonormal basis for ℂ2, as shown in the following:


And this all started from two linearly independent vectors using the Gram-Schmidt process. Pretty cool, eh?

Now, it's time to lay out the entire process:




This algorithm will give us an orthogonal basis; then, all we have to do is normalize each vector, and we get an orthonormal basis! Let's move on to two important inequalities.

day-modeBookmark
Cauchy-Schwarz and triangle inequalities
The Cauchy-Schwarz inequality is one of the most important inequalities in mathematics. Succinctly stated, it says that the absolute value of the inner product of two vectors is less than or equal to the norm of those two vectors multiplied together. In fact, they are only equal if the two vectors are linearly dependent:


There are several proofs of this inequality, which I encourage you to seek out if you are interested. But, in the totality of things, knowing this inequality is all that is really required for quantum computing.

The other major inequality is the triangle inequality. It comes from our old friend Euclid in his book The Elements. Succinctly stated, it says that the length of two sides of a triangle must always be more than the length of one side. They will only be equal in the corner case when the triangle has zero area. It is very intuitive once you see some example triangles. Here are some triangles that show how the side z is less than the sum of sides x and y:


Figure 9.1 – Three example triangles for the triangle inequality [1]

Now, let's state the triangle inequality:


You'll notice that the way it is notated is using the norms of vectors. Let's look at an example. Let's say we have the two following kets:


Their corresponding bras (that is, their conjugate transpose) are:


Now, the norm of |x⟩ is:


The norm of |y⟩ is:


So, the right side of the triangle inequality is:



Let's calculate the left side of the triangle inequality:


So, the triangle equality holds for our two kets |x⟩ and |y⟩ since 4.24 ≤ 5.84. Now, we will move to look at decompositions of matrices.

day-modeBookmark
Spectral decomposition
The spectrum of a square matrix is the set of its eigenvalues. There is a cool theorem in linear algebra that states that all matrices representing a linear operator have the same spectrum. Before we use the spectrum though, we need to talk about diagonal matrices.

Diagonal matrices
The main diagonal of a matrix is every entry where the row index equals the column index. Examples make this very easy to see. All the following matrices have the letter d on their main diagonal:


Now, a diagonal matrix has zero on all entries outside the main diagonal. Here are examples of diagonal matrices:


Here are two cool features of diagonal matrices that make them all the rage at linear algebra parties. One, all their eigenvalues are on their main diagonal. Two, they are very easy to exponentiate. Let's see the latter in action real quick:


Try to exponentiate any regular old random matrix… it'll take you a while! Now, back to the main feature – spectral decomposition.

Spectral theory
The spectral theorem lets us know when an operator can be represented by a diagonal matrix. These operators and all the matrices that represent them are called diagonalizable. This means that we can factor a diagonalizable matrix A into:


where P is an invertible matrix and D is a diagonal matrix.

If you remember from the last chapter, all normal operators and their associated normal matrices are diagonalizable. If this is the case, then we can decompose a matrix A into even more special factors:


Looks like a fraternity name, right? Well, U is a unitary matrix, and the capital Greek letter lambda (Λ) is a diagonal matrix with all the eigenvalues of A on its main diagonal! Remember that we used the lowercase lambda (λ) for each eigenvalue, so it makes sense to use the uppercase lambda for all of them together in one matrix. Now, here comes the kicker – the column vectors making up U are the eigenvectors of A!

Putting this all together means that we can decompose any normal matrix into a unitary matrix U, its conjugate transpose, and a diagonal matrix Λ that has the eigenvalues down its main diagonal. Please note that the eigenvalues placement on the main diagonal must correspond with its eigenvector's placement in U. Since the set of eigenvalues is called the spectrum, I hope you can see why this is called spectral decomposition.

Okay, enough talk – more action! Let's do an example.

Diagonalizable Matrices

Please note that there are diagonalizable matrices that are not normal, but we do not often come across these matrices in quantum computing.

Example
Let's use spectral decomposition to decompose the quantum gate Y. Here is its matrix in the computational basis:


Now, I will go ahead and tell you that the eigenvalues of Y are 1 and -1. The eigenvectors are as follows where "+" denotes the eigenvector for the eigenvalue of 1 and "–" denotes the eigenvector of -1:


So, according to the spectral theorem, I can represent Y in terms of a matrix U that has its eigenvectors as the columns, a diagonal matrix with the eigenvalues down its main diagonal, and the conjugate transpose of U. So, here is U and U dagger:


Here is the eigenvalue matrix:


Putting this all together, we can now decompose Y into:


I encourage you to work out the matrix multiplication and make sure I'm right!

But, hey – wait a minute. We're in quantum computing and we like bra-ket notation! So, let's do it in bra-ket notation!

Bra-ket notation
All the way back in Chapter 2, The Matrix, we talked about how you can represent a matrix as a set of column vectors (kets) or row vectors (bras). Well, we're going to use that here. I'll prove this using 2 × 2 matrices, and then you'll have to trust me that it works for n × n matrices. I can represent the unitary matrix U that has eigenvectors for its column vectors like so:


U dagger then becomes:


The eigenvalue matrix will look like this:


Putting it all together, it looks like:


Multiplying the first two matrices, we get:


Then, when we do the final multiplication, we get:


And this is the bra-ket equation for spectral decomposition! For an n × n matrix, it becomes:


This is a very important result! It means that any normal operator can be represented as a linear combination of outer products composed of just its eigenvalues and eigenvectors! Let's see how this plays out with our Y operator.

Example take two
You may have noticed that the eigenvectors of Y look eerily familiar; that's because they are the i and minus i states!


So, using spectral decomposition, we can represent the quantum Y gate this way:

(1)


If you want to express this in the computational basis, you have to write i and minus i in it:


Then, substitute this with Equation (1) and work out the math. You will get:


Now, let's look at another decomposition.

day-modeBookmark
Singular value decomposition
Singular Value Decomposition (SVD) is probably the most famous decomposition you can do for linear operators and matrices. It is at the core of search engines and machine learning algorithms. Additionally, it can be used on any type of matrix, even rectangular ones. However, we will only look at square matrices.

Succinctly stated, it guarantees that for any matrix A, it can be decomposed into three matrices:


Whereas U is a unitary matrix, Σ (sigma) is a diagonal matrix with what is known as the singular values of A on its diagonal, and V is also a unitary matrix. It should be noted that this decomposition is not unique, and different matrices can be used for U, Σ, and V.

Let's look at an example. We have the following matrix A:


Without going through the math, I'm going to tell you that SVD can be used to get this decomposition:


Let's make sure that U and V are unitary matrices:




Since V is the identity matrix, I think we can safely assume it is unitary.

Now for these pesky singular values on the main diagonal of Σ. How do we get those? Those are found by taking the square root of the eigenvalues of A multiplied by its conjugate transpose. So for us, this is:



The eigenvalues are on the main diagonal, and they are 4 and 0. So, the singular values of A are the square root of these eigenvalues, namely 2 and 0. If you look at the middle matrix, Σ, you'll notice that it has these singular values on its main diagonal. Your next question might be, how do we find U and V? Well, you may be disappointed, but I'm not going to go through the algorithm here. Suffice it to say that it involves finding an orthonormal set of eigenvectors for AA†. If you are interested in learning more, I encourage you to look into one of the linear algebra books in my appendix of references. Though, to be quite truthful, we almost always use computers to calculate SVD. Let's move onto another decomposition – polar decomposition.

day-modeBookmark
Polar decomposition
Polar decomposition allows you to factor any matrix into unitary and positive semi-definite Hermitian matrices. It can be seen as breaking down a linear transformation into a rotation or reflection and scaling in ℝn. Formally, it is as follows:


for any matrix A. U is a unitary matrix and P is a positive semi-definite matrix. Let's look at an example:


Using polar decomposition, this matrix can be decomposed into:


This may not seem like much, but we took a random matrix and turned it into a reflection matrix times a scaling matrix. Pretty cool!

Again, I will not go through the algorithm here because we will use calculators. Calculators for polar decomposition are not as plentiful as SVD, but I have found using the SciPy Python library to be the best way.

day-modeBookmark
Operator functions and the matrix exponential
Now, we get to look at functions that involve an operator and their matrix representations. What types of functions are we talking about? Well, really any function that can be defined, such as the sine of x. You have probably never seen a function like this:


where A is a matrix. The first question is, does this even make sense? Well, mathematicians have come up with ways for this to make sense, and it has applications in quantum computing.

As we have said, if a matrix A is diagonalizable, it can be decomposed into an invertible matrix P and diagonal matrix D as:


(2)

Given that, we can represent a function involving such a matrix like so:


(3)

where the matrix in the middle is the diagonal matrix D in Equation (2). The function is evaluated for every value on the main diagonal of D.

Let's look at an example. Let's do the easiest case, where we are already dealing with a diagonal matrix:


Now, we want to find the sine of A. Following the process from Equation (3), this is what we get:


How about we check our answer by finding the cosine of A as well and then summing their squares? Here is the cosine of A:


We know the trigonometric identity:


The number 1 in that identity becomes the identity matrix for us when dealing with matrices. Now, let's verify our calculations for sine and cosine!


So, our calculations are correct and this makes sense!

A function that comes up a lot in quantum computing is the exponential function:


You'll notice that we use exp(x) to also denote the exponential function, as it is easier to write sometimes. If the matrix is diagonal, such as the Z operator, this becomes easy to calculate:


Let's see a slightly harder example. What is exp(A) when A is:


Well, first we need to diagonalize it, and the first step of that is finding its eigenvalues:


Then, we have to find its eigenvectors. I will go ahead and tell you that they are:


Given all of this, we can write its diagonal representation like so:


Evaluating the exponential function on the main diagonal of D gives us:


Multiplying this all out gives us:


While this was a long example, it should show you the power of being able to calculate the functions of operators.

day-modeBookmark
Summary
Well, that wraps up this chapter. I hope you can see all the wonderful decompositions you can do with matrices and some of the more advanced things you can do with them. This chapter also concludes the book. I hope you have enjoyed it and learned as much as I did. Take this math and go forth to infinity and beyond in the universe of quantum computing!