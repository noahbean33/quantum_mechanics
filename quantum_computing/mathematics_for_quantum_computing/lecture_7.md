Chapter 7: EigenStuff
Eigen (pronounced EYE-GUN) is a German prefix to words such as eigentum (property), eigenschaft (a feature or characteristic), and eigensinn (an idiosyncrasy). To sum up, we are looking for some values and vectors that are characteristic, idiosyncratic, and a property of something. What is that something? That something is our old friend the linear operator and its representations as square matrices. But before we get there, we'll need to look at some other concepts such as the matrix inverse and determinant. We'll wrap it all up with the trace of a matrix and some properties that the trace, determinant, and eigenvalues all share. These concepts will allow us to reach even further heights in the chapters that follow.

In this chapter, we are going to cover the following main topics:

The inverse of a matrix
Determinants
Invertible matrix theorem
Eigenvalues and eigenvectors
Trace
The special properties of eigenvalues
day-modeBookmark
The inverse of a matrix
It would be nice to have a way to do algebra on matrices the way we do for simple algebraic expressions, like so:


The inverse of a matrix provides us with a way to do this. It is very similar to the reciprocal for rational numbers. For rational numbers, the following is true:


In a similar way, the inverse of a matrix is defined to be a matrix that when multiplied by the original matrix, you get the identity matrix. Here it is mathematically:


The matrix inverse can then be used when trying to algebraically modify a matrix equation. Let's say we are trying to find the vector |x⟩ in the following equation:


Since we now have a multiplicative inverse of a matrix, we can multiply both sides by it to get the following:


Please remember that matrix multiplication is not commutative, so if you left multiply a matrix on one side of an equation, you must left multiply on the other side. The same applies if you right multiply a matrix. We now have a way to find |x⟩ by using the inverse of matrix A. But there is a catch – not all matrices have an inverse. Determinants will help us here though.

day-modeBookmark
Determinants
Determinants determine whether a square matrix is invertible. This is a huge help to us, as we will see. In the literature, you will see either a function abbreviation for the determinant or vertical bars, like so:


The determinant is a function from ℂn × n to ℂ. In other words, it takes an n × n square matrix as input and spits out a scalar. For a 1 × 1 matrix, the determinant is just the number (easy enough). For a 2 × 2 matrix, this is the formula. You should probably just commit it to memory if you can:


I will give you exercises at the end of this section to help with the memorization part, which will also give you a feel for the determinant itself.

There is a method for calculating determinants for bigger matrices, but it is rather involved, and once you've mastered 2 × 2 matrices, I would suggest using a matrix calculator. It's just like arithmetic; you should know how to do it for small numbers before using a calculator for everything else. Just so you get a glimpse of how it gets increasingly difficult to calculate determinants, here is the formula for a 3 × 3 matrix:


For reference, a good matrix calculator is WolframAlpha's (https://www.wolframalpha.com/calculators/determinant-calculator), as shown here:

Figure 7.1 – The WolframAlpha online determinant calculator
Figure 7.1 – The WolframAlpha online determinant calculator

Okay, let's see this in action and work through a quick example for determinants. What is the determinant of the following matrix?


Using our formula, we can calculate it as follows:


See? Easy-peasy!

So, at the start of this section, we said that the determinant helps to determine whether a matrix is invertible. How is that possible? I'll put this in a callout, as it is quite important:

Determinants and Invertibility

If the determinant of a matrix equals zero, it is not invertible. Otherwise, the matrix is invertible.

If a matrix is not invertible, we call it singular or degenerate. We will now use the determinant in the next sections on calculating the inverse of a matrix and calculating eigenvalues. But first, it leads us to a very important and useful theorem in linear algebra, the invertible matrix theorem.

Exercise one
What is the determinant of the following 2 × 2 matrices?


day-modeBookmark
The invertible matrix theorem
The invertible matrix theorem is a great result in linear algebra because based on the invertibility of a matrix, we can say a great many things about that matrix that are also true. Since we now know a quick way to determine the invertibility of a matrix through the computation of the determinant, we get all these other properties for free!

Here is the actual definition. Let A be a square n × n matrix. If A is invertible (det(A) ≠ 0), then the following properties follow:

The column vectors of A are linearly independent.
The column vectors of A form a basis for ℂn.
The row vectors of A form a basis for ℂn and are also linearly independent.
The linear transformation mapping |x⟩ to A|x⟩ is a bijection from ℂn to ℂn (we studied bijections in Anchor 3, Foundations).
If the matrix A is not invertible (det(A) = 0), then all the preceding properties are false.

While it may not seem that these are a lot of properties, there are many more I did not include because we didn't cover the concepts in this book. But even with the four properties listed here, it should show how powerful the determinant is when it is computed.

day-modeBookmark
Calculating the inverse of a matrix
But wait – there's more! We can use the determinant of a matrix to calculate its inverse. Here is the formula to calculate the inverse of a 2 × 2 matrix:


The first thing to notice is that the reciprocal of the determinant is used. Now, what if the determinant is zero? We can't divide by zero! So the formula is undefined, but remember that if the determinant is zero, it doesn't matter because the matrix is not invertible to begin with!

The other thing to notice is that a and d just switch position. Then, b and c are just multiplied by -1.

That was a lot of words! Let's look at an example with the following matrix:


Let's calculate the determinant first:


Alright, let's use that to calculate the inverse:


And there you have it. Let's make sure that it is the inverse by using the definition we had for the inverse of a matrix:


Now, let's do some exercises.

Exercise two
Calculate the inverse of the following matrices:


You should note that in the last exercise, I included complex numbers in the matrix. You should get used to this now that we have covered complex numbers.

Now let's move on to the main feature, eigenvalues and eigenvectors!

day-modeBookmark
Eigenvalues and eigenvectors
Ah, yes – we have arrived at the meat of this chapter, the eigen-stuff! We know that linear transformations are involved in this somehow, but how? Well, let's start with something we are familiar with, the reflection transformation we covered in Chapter 5, Using Matrices to Transform Space. Here is the diagram that describes it:

Figure 7.2 – Reflection transformation
Figure 7.2 – Reflection transformation

Now, the special vectors we are looking for, called eigenvectors, are the ones that only get multiplied by a scalar when they are transformed. Here's a look at a number of vectors being reflected, with the reflections being the dashed lines. Stare at the diagram and see if you see any reflections that are the same as multiplying by a scalar:

Figure 7.3 – Vectors and their reflections
Figure 7.3 – Vectors and their reflections

Well, I don't want you to stare too long, so here is the first one:

Figure 7.4 – The first eigenvector
Figure 7.4 – The first eigenvector

Any vector along this line going through a reflection transformation is the same as being multiplied by the scalar -1. This scalar is called the eigenvalue.

Did you notice any other eigenvectors? This one is a little harder to tease out, but here it is:

Figure 7.5 – The second eigenvector
Figure 7.5 – The second eigenvector

If you remember in our discussion about reflection, we said that any vector that is on the axis of reflection will be reflected onto itself. In other words, it is multiplied by the scalar 1. The set of eigenvectors is any vector on this line, and the corresponding eigenvalue is 1.

So, there you have it – for reflection, an eigenvector is any vector perpendicular to the axis of reflection with an eigenvalue of -1 or any vector parallel to the axis of reflection with an eigenvalue of 1.

Definition
Let's get rigorous and define eigenvectors and eigenvalues. Given a linear operator Â an eigenvector is a non-zero vector that when transformed by Â is equal to being multiplied by a scalar λ (pronounced lamb-da). This can be written as the following:


This is also true for any matrix A that represents the linear operator, Â:


where A is a matrix. The scalar λ is called an eigenvalue.

Now for some comic relief from all this rigor!

"What is a baby eigensheep?"

"A lamb, duh!"

Example with a matrix
Alright, let's see this eigen-stuff in action with an example matrix. Here's our chosen matrix:


Let's see what it does to a variety of vectors:


Do any of the resultant vectors look like a scalar multiple of the original? If you said the last one, you are correct! Let's write it again with its eigenvalue, 3:


You may have noticed that there is more than one eigenvector for an eigenvalue – in fact, there is a set. This leads us to the fact that an eigenvalue with its set of eigenvectors, plus the zero vector, constitutes a subspace of the overall vector space that a linear operator is transforming. For our matrix B, this happens to be a one-dimensional line through (1,0) if we are dealing with a real vector space. Let's see some more eigenvectors of the eigenvalue 3 to drive the point home:


This subspace of vectors is called the eigenspace. To define the eigenspace mathematically for the matrix B and the eigenvalue 3 in ℝn, it is as follows:


We can also just give the vector (1,0) as a basis vector. When doing this, the basis set of vectors is called the eigenbasis.

The characteristic equation
So, how do we find eigenvalues when given a square matrix? Well, let's start with what we are trying to find:

 (1)

We want to find λ. So, let's start with manipulating Equation (1) algebraically. Let's subtract λ|x⟩ from both sides of the equation:


Okay, after doing that, let's take out the vector |x⟩:


Hmm – this is not a valid equation because λ is a scalar and A is a matrix. What should we do? Let's multiply λ by the identity matrix so that we are subtracting two matrices:

 (2)

Okay, we now have one vector multiplied by the difference of two matrices on the left side of our equation and the zero vector on the other. It just so happens that a part of the invertible matrix theorem that I left unstated says that for Equation (2) to have a non-trivial solution (a solution other than the zero vector), the determinant of the matrix on the left side has to equal zero:

 (3)

Equation (3) is called the characteristic equation of matrix A. If we can solve it, we will get all the eigenvalues of A! Let's see how we can do it with an example.

Example
Okay, let's use the matrix A, defined as follows:


Now, let's solve its characteristic equation by first finding the matrix on the left in Equation (3):


Okay, now that we've found that, let's set the determinant of that matrix to 0 and solve for λ:


The polynomial we have found in the preceding equation is called the characteristic polynomial of the matrix A for reference. There seems to be a lot of characteristics floating around, which gets back to our discussion of what eigen stands for in German! If we put the characteristic polynomial into the quadratic formula, we will find that our two eigenvalues for the matrix A are as follows:


And there you go – you now know how to find eigenvalues for 2 × 2 matrices. What about bigger matrices? Well, the characteristic polynomials get harder and harder to solve symbolically, and we have to rely on computers to find them numerically. Once again, a handy matrix calculator comes to save the day. For getting eigenvalues and eigenvectors, I'd like to recommend Symbolab (https://www.symbolab.com/) as an online calculator as well (another tool in your toolbelt); a screenshot is shown in the following figure:

Figure 7.6 – The Symbolab online calculator
Figure 7.6 – The Symbolab online calculator

Now that we have found the eigenvalues, how do we find the eigenvectors?

Finding eigenvectors
In this section, we will answer that question. In a nutshell, we put the eigenvalues back into the definition and solve for the eigenvectors. Let's say I use the linear operator Y, which is a common gate in quantum computing. Here it is in the computational basis:


I'll go ahead and tell you that the eigenvalues are 1 and -1. The definition for eigenvalues is as follows:


Now, let's solve for the eigenvalue 1, to find its eigenvectors. First, we put in the matrix and eigenvalue:


Multiplying this out gives us the following:


This is a system of two linear equations, which is pretty simple to solve:


This means that we can choose any value for x2 and derive x1. Putting this back into the vector |x⟩, we get the following:


So, any vector that has the components of |x⟩ will be an eigenvector for the eigenvalue of 1 for the matrix Y. Let's set one component to get a "representative eigenvector" for the eigenvalue:


To find the other set of eigenvectors for Y, you repeat the process with the other eigenvalue of -1.

Multiplicity
Sometimes, when we compute the characteristic polynomial for a matrix, it can output something like this:


In this case, the only eigenvalue is 1, but it is the root of the characteristic polynomial twice. Therefore, this particular eigenvalue has an algebraic multiplicity of 2. In general, the algebraic multiplicity of a particular eigenvalue is the number of times it appears as a root of the characteristic polynomial.

day-modeBookmark
Trace
The trace of a matrix is very easy to compute, but it helps to have its value, as it has special properties. It is defined as the sum of the values on the main diagonal of a matrix. So, let's say we have the following:


The trace of A will then be the following:


In general, the definition of the trace for an n × n square matrix is as follows:


The trace of a linear operator is the same for any matrix that represents it.

day-modeBookmark
The special properties of eigenvalues
Now that we have gone through the concept of the trace and determinant, let's quickly look at some cool properties they have in relation to eigenvalues.

It happens that the sum of the eigenvalues of a matrix equals the trace of the matrix:


Additionally, the product of all the eigenvalues of a matrix is equal to the determinant:



I encourage you to go back to the matrices we have used as examples with their eigenvalues and prove to yourself that this is indeed true!

day-modeBookmark
Summary
We have covered quite a bit of ground here in relatively few pages. We saw how to calculate the determinant and how it plays a role in finding the inverse of matrices. Many types of eigen-stuff were discussed, and ways to find them were also given. Finally, we saw how the trace is calculated and how it relates to everything else we covered in this chapter. These concepts will equip you to do serious linear algebra and quantum computing going forward. In the next chapter, we will bring everything together that we learned in the last seven chapters to explore the space where qubits live!