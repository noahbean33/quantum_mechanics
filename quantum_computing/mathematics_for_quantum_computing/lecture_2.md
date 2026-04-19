Chapter 2: The Matrix
In the famous movie, The Matrix, Morpheus says, "The Matrix is everywhere. It is all around us. Even now, in this very room." Morpheus was not far off the mark, for there is a theory in physics called the matrix string theory where essentially, reality is governed by a set of matrices. But while a matrix is one entity in the movie, a matrix in physics is a concept that is used again and again to model reality.

Figure 2.1 – This screenshot of the GLmatrix program by Jamie Zawinski is licensed with his permission
Figure 2.1 – This screenshot of the GLmatrix program by Jamie Zawinski is licensed with his permission

As you will see, the definition of a matrix is deceptively simple, but its power derives from all the ways mathematicians have defined that it can be used. It is a central object in quantum mechanics and, hence, quantum computing. Indeed, if I were forced to select the most important mathematical tool in quantum computing, it would be a matrix.

In this chapter, we are going to cover the following main topics:

Defining a matrix
Simple matrix operations
Defining matrix multiplication
Special types of matrices
Quantum gates
day-modeBookmark
Defining a matrix
Mathematicians define a matrix as simply a rectangular array that has m rows and n columns, like the one shown in the following screenshot:


Figure 2.2 – Model of a matrix with m rows and n columns
Figure 2.2 – Model of a matrix with m rows and n columns

In math, matrices are written out a particular way. An example 4 × 5 matrix is shown in the following expression. Notice that it has four rows and five columns:

Figure 2.3 – Example of a 4 x 5 matrix
Figure 2.3 – Example of a 4 x 5 matrix

Notation
In math and quantum computing, matrix variable names are in capital letters, and each entry in a matrix is referred to by a lowercase letter that corresponds to the variable name with subscripts (aij). Subscript i refers to the row the entry is in and subscript j refers to the column it is in. The following formula shows this for a 3 × 3 matrix:



In our example matrix A, a22 = 1. What is a32? Hint—it's the only number that begins with the letter n.

Redefining vectors
One thing we will do in this book is iteratively define things so that we start simple, and as we learn more, we will add or even redefine objects to make them more advanced. So, in our previous chapter, our Euclidean vectors only had two dimensions. What if they have more? Well, we can represent them with n × 1 matrices, like so:



What do we call a 1 × n matrix such as the following one?



Well, we will call it a row vector. To distinguish between the two types, we will call the n × 1 matrix a column vector. Also, while we have been using kets (for example, |x⟩) to notate column vectors so far, we will use something different to notate row vectors. We will introduce the bra, which is the other side of the bra-ket notation. A bra is denoted by an opening angle bracket, the name of the vector, and a pipe or vertical bar. For example, a row vector with the name b would be denoted like this: ⟨b|. This is the other side of the bra-ket notation explained further in the appendix. To make things clearer, here are our definitions of a column vector and a row vector for now:



Important Note

A bra has a deeper definition that we will look at later in this book. For now, this is enough for us to tackle matrix multiplication.

Now that we have introduced how column and row vectors can be represented by one-dimensional (1D) matrices, let's next look at some operations we can do on matrices.

day-modeBookmark
Simple matrix operations
As mentioned in the introduction to this chapter, the power of matrices is the operations defined on them. Here, we go through some of the basic operations for matrices that we will build on as the book progresses. You have already encountered some of these operations with vectors in the previous chapter, but we will now expand them to matrices.

Addition
Addition is one of the easiest operations, along with its inverse subtraction. You basically just perform addition on each entry of one matrix that corresponds with another entry in the other matrix, as shown in the following formula. Addition is only defined for matrices with the same dimensions:



Example
Here is an example of matrix addition:



Exercise 1
What is the sum of the following two matrices? (Answers to exercises are at the end of the chapter.)



Scalar multiplication
Scalar multiplication is also rather easy. A scalar is just a number, and so scalar multiplication is just multiplying a matrix by a number. We define it for a scalar b and matrix A thusly:



Example
As always, an example can definitely help:



Exercise 2
Calculate the following:



Transposing a matrix
An important operation involving matrices and vectors is to transpose them. To transpose a matrix, you essentially convert the rows into columns and the columns into rows. It is denoted by a superscript T. Here is the definition:



Notice how the subscripts for the diagonal entries stay the same, but the subscripts for all other entries are switched (for example, the entry at a12 becomes a21). Also, as a consequence of this operation, the dimensions of the matrix are switched. A 2 × 4 matrix becomes a 4 × 2 matrix.

Examples
Here is an example of a 3 × 4 matrix transposed:



Here is an example of a square matrix transposed:



Now, let's move on to matrix multiplication.

day-modeBookmark
Defining matrix multiplication
Matrix multiplication can be a complicated procedure, and we will build up to it gradually. It is defined as an operation between an m × n matrix and an n × p matrix that produces an m × p matrix. The following screenshot shows this well:

Figure 2.4 – Schematic of matrix multiplication
Figure 2.4 – Schematic of matrix multiplication

Notice that matrix multiplication is only defined if the number of columns in the first matrix equals the number of rows in the second matrix—or, in other words, the ns have to match in our preceding figure. This is so important that we will give it a special name: the matrix multiplication definition rule, or definition rule for short. Based on this, the first thing you should do when presented with two matrices to multiply is to make sure they pass the definition rule. Otherwise, the operation is undefined. For example, do the following two matrices pass the definition rule?



The answer is no because you have a 2 × 2 matrix being multiplied by a 3 × 3 matrix. The number of columns of the first matrix does not equal the number of rows of the second matrix. What about the following matrix multiplication?


(1)

Yes, it is defined! It is a 2 × 3 matrix multiplied by a 3 × 2 matrix. The number of columns in the first equals the number of rows in the second!

If the matrices pass the definition rule, the second step you should take when multiplying two matrices is to draw out the answer's dimensions. For instance, when presented with the preceding matrix multiplication from Equation (1) of a 2 × 3 matrix and a 3 × 2 matrix, we would draw out a 2 × 2 matrix, like so. I like to write the dimensions of each matrix on the top:


Figure 2.5 – Writing dimensions of matrix multiplication
Figure 2.5 – Writing dimensions of matrix multiplication

Remember—the number of rows in the first matrix determines the number in rows of the product or resultant matrix. The number of columns in the second matrix determines the number of columns in the product.

Okay—to summarize, here are the first two steps you should take when doing matrix multiplication:

Does it pass the definition rule? Do the number of columns in the first matrix equal the number of rows in the second matrix?
Draw out the dimensions of the product matrix. For an m × n matrix and an n × p matrix, the dimensions of the resulting matrix will be m × p.
Based on all of this, do you think matrix multiplication is commutative (that is, A ⋅ B = B ⋅ A)? Think about it—I'll give you the answer later in this chapter. Now, let's look at how to multiply two vectors to produce a scalar.

Multiplying vectors
Earlier, we defined column and row vectors as one-dimensional matrices. Since they are one-dimensional, they are the easiest matrices to multiply. A bracket, denoted by ⟨x|y⟩, is essentially matrix multiplication of a row vector and a column vector. Here is our definition:


Important Note

A bracket has a deeper definition that we will look at later in this book. For now, this is enough for us to tackle matrix multiplication.

Let's look at an example to make this more concrete.

Examples
Let's say ⟨y| and |x⟩ are defined this way:



Now, let's calculate the bracket ⟨y| x⟩:



Here are two more examples of matrix multiplication of a row vector with a column vector:





Exercise 3
What is the answer to the matrix multiplication of this row vector and column vector?



Matrix-vector multiplication
We are building up to pure matrix multiplication, and the next step to getting there is matrix-vector multiplication. Let's look at a typical expression for matrix-vector multiplication:



Now, this is a 3 × 2 matrix multiplied by a 2 × 1 column vector. Does this pass the matrix multiplication rule? Yes! 2=2. What are the dimensions of the product? Well, taking the outer dimensions of the two matrices involved in the product, it will be a 3 × 1 column vector. If the matrix and column vector are variables, we can write out the product this way:


(2)

This denotes the matrix A multiplying the vector |x⟩.

Alright—how do we actually do the multiplication? Well, first, we separate the rows of the matrix into row vectors. Wait—there are vectors in matrices?! Yes—you can see a matrix as a set of row vectors or column vectors when it is convenient to do so. Let's look at an example of doing this:


(3)

See how I separated the three rows of the matrix into three row vectors? I even gave them names, with the letter R standing for row and the subscript number showing which row it came from. So, after performing the first two steps of matrix multiplication, the next step is:

Separate the matrix on the left into row vectors, ⟨R1|, ⟨R2|, … , ⟨Rm|.
From there, we will calculate the bracket between each row vector from the separated matrix and the column vector we are multiplying by. Let's see an example.

Let's say we are trying to find the answer to the matrix-vector multiplication between matrix A and vector |x⟩ as in Equation (2) and matrix A is the one defined in Equation (3). We will create a simple vector |x⟩ to give us:



Okay—so, how do we figure out what a, b, and c are? Let's calculate the brackets!



Now that we have seen an example, let's generalize this for the final step of matrix-vector multiplication:

For a matrix-vector multiplication, A|x⟩, compute the bracket for each row in A with the column vector |x⟩. Put the result of the bracket in the corresponding row for the resultant column vector.
So, let's write this all out for our example:



Now, let's put this all together for a proper definition of matrix-vector multiplication.

Matrix-vector multiplication definition
Given an m × n matrix A and an n × 1 vector |x⟩, where A is made up of m row vectors, like so:



Matrix-vector multiplication is defined as:



Now, let's apply this to an example with real numbers:



Now, it's your turn to do matrix-vector multiplication.

Exercise 4
If you have matrices A, B, and C defined as so:



and three vectors defined as so:



what are the following matrix-vector products? If the operation is undefined, say so.



Matrix multiplication
Alright—we have finally arrived at matrix multiplication! Trust me, it is worth the wait because matrix multiplication is used all over quantum computing and you now have the basis to do the calculations correctly and succinctly.

Remember in the previous section that I said you could view a matrix as a set of row vectors? Well, it ends up you can view them as set of column vectors as well. Let's take our matrix from before and repurpose it to see matrices as a set of column vectors:



So, this time, I separated the matrix into three column vectors. I gave each one a name with the letter C, standing for column, and the subscript number showing which column it came from.

We will use the first three steps we have defined so far for matrix multiplication as well and replace the fourth step from matrix-vector multiplication. Here are the first four steps of matrix multiplication:

Does it pass the definition rule? Do the number of columns in the first matrix equal the number of rows in the second matrix?
Draw out the dimensions of the product matrix. For an m × n matrix and an n × p matrix, the dimensions of the resulting matrix will be m × p.
Separate the matrix on the left into row vectors, ⟨R1|, ⟨R2|, … , ⟨Rm|.
Separate the matrix on the right into column vectors, |C1⟩, |C2⟩,…,|Cp⟩.
Alright—we have arrived at the last step! Can you guess what it is? Well, it definitely involves brackets. Without further ado, here it is:

For each entry aij in the resultant matrix, compute the bracket of the ith row vector and the jth column vector, ⟨Ri|Cj⟩.
If matrix A is the left matrix and matrix B is the right matrix (that is, A ⋅ B), then the following diagram is a good way to look at Step 5 graphically:

Figure 2.6 – Depiction of the matrix product AB [1]
Figure 2.6 – Depiction of the matrix product AB [1]

Let's look at an example.

Example
Say we have the following two matrices:



Let's go through our five steps.

Does it pass the definition rule? Do the number of columns in the first matrix equal the number of rows in the second matrix?
Yes! A is a 2 × 2 matrix and B is a 2 × 3 matrix. So, the operation is defined.

Draw out the dimensions of the product matrix. For an m × n matrix and an n × p matrix, the dimensions of the resulting matrix will be m × p.


Separate the matrix on the left into row vectors, ⟨R1|, ⟨R2|, … , ⟨Rm|.


Separate the matrix on the right into column vectors, |C1⟩, |C2⟩,…,|Cp⟩.


For each entry aij in the resultant matrix, compute the bracket of the ith row vector and the jth column vector, ⟨Ri|Cj⟩.


So, the computations will look like this:



And there's our answer! That may have taken a while, but it will become quicker and more intuitive as you practice it. Speaking of practice…

Exercise 5
Given the following three matrices:



what are the following products? Follow the steps! And if the operation is undefined, say so.



Properties of matrix multiplication
It's good to know some general properties of matrix multiplication. These properties assume that the matrices all have the right dimensions to pass the matrix multiplication definition rule. Here they are—matrix multiplication is:

Not commutative: A⋅ B ≠ B⋅ A
Distributive with respect to matrix addition:


Associative:


The transpose of a matrix product A ⋅ B is the product of the transpose of each matrix in reverse:


That concludes our section on matrix multiplication. You might want to take a break—you've been through a lot! When you come back, we'll look at some special matrices that are good to know.

day-modeBookmark
Special types of matrices
In the world of matrices, some are so special that they have been singled out. Here they are.

Square matrices
A special type of matrix is a square matrix. A square matrix is one where the number of rows equals the number of columns. In other words, it is an m × n matrix in which m = n. Square matrices show up all over the place in quantum computing due to special properties that they can have—for example, symmetry, which is discussed later in the book. As we progress in the book, they will become one of the central types of matrices we will use. Some examples of square matrices are:



Identity matrices
An important type of square matrix is an identity matrix, named I. It is defined so that it acts as the number 1 in matrix multiplication so that the following holds true:



It has ones all down its principal diagonal and zeros everywhere else. Its dimensions need to change based on the matrix it is being multiplied by. Here are some examples of I in different dimensions:



You should multiply some of the matrices we have used before with the identity matrix to convince yourself that it does indeed return the matrix it is multiplied by. Now that we've gone over some special matrices, let's get into why matrix multiplication is important in quantum computing.

day-modeBookmark
Quantum gates
In this section, I'd like to take the math you have learned in this chapter around matrices and connect it to actual quantum computing—namely, quantum gates. Please remember that this book is not about teaching you everything in quantum computing, but rather the mathematics needed to do and learn quantum computing. That being said, I want to connect the math to quantum computing and show the motivation for learning it. Do not be frustrated if this does not all make sense, and please consult the reference books in the appendix for more information on quantum gates.

Logic gates
In classical computing, we use logic gates to put together circuits that will implement algorithms, such as, adding two numbers. The logic gates represent Boolean logic. Here are some simple logic operations:

AND
OR
NOT
In a circuit, you have input, output, and logic gates. The input and outputs are represented by a binary number, with 1 being true and 0 being false. Here is an example of a NOT gate:

Figure 2.7 – NOT gate
Figure 2.7 – NOT gate

Truth tables can be created that correspond to the inputs and outputs of the circuit. Here is a truth table for the NOT gate just described:

Figure 2.8 – Truth table for NOT gate
Figure 2.8 – Truth table for NOT gate

A slightly more complicated circuit involves the AND gate, as shown in the following figure:

Figure 2.9 – AND gate
Figure 2.9 – AND gate

Here is a truth table for this circuit:

Figure 2.10 – Truth table for AND gate
Figure 2.10 – Truth table for AND gate

Circuit model
Much of quantum computing is modeled using quantum circuits that are similar to, but not the same as, the classical circuits we just went through. In quantum circuits, the inputs are qubits (vectors), and the gates are matrices. An example quantum logic gate is shown here:

Figure 2.11 – Quantum circuit with NOT gate
Figure 2.11 – Quantum circuit with NOT gate

The output qubit is derived through matrix-vector multiplication! So, if we remember from Chapter 2, Superposition with Euclid, qubits are just vectors and the binary states for qubits are:



The NOT gate in quantum computing is represented by the following matrix:



So, if our input qubit is a |1⟩, then the output would be:



If we did the computation with |0⟩ as the input, the output would be |1⟩. Basically, this is the quantum version of the NOT gate!

There are many quantum gates, but they are all modeled as matrices. Thus, the math you have learned in this chapter is directly applicable to quantum computing!

day-modeBookmark
Summary
In this chapter, we have learned a good number of operations on matrices and vectors. We can now do basic computation with them, and we saw their application to quantum computing. Please note that not all matrices can be used as quantum gates. Please keep reading the book to find out which ones can.

In the next chapter, we start to go deeper and look at the foundations of mathematics.

day-modeBookmark
Answers to exercises
Exercise 1


Exercise 2


Exercise 3
14

Exercise 4


Exercise 5


day-modeBookmark
