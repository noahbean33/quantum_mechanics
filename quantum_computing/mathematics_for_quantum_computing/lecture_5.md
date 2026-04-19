Chapter 5: Using Matrices to Transform Space
Linear transformations are one of the most central topics in linear algebra. Now that we have defined vectors and vector spaces, we need to be able to do things with them. In Chapter 3, Foundations, we manipulated mathematical objects with functions. When we manipulate vectors in vector spaces, mathematicians use the term linear transformations. Why the change of terminology? As with most things in linear algebra, the wording is inspired by Euclidean geometry. We will see that, geometrically, these "functions" actually "transform" vectors from one direction and length to another. But this visual transformation has been generalized algebraically to all types of vectors (n-tuples of numbers, functions, and so on).

We also go through the crucial link between linear transformations and matrices. The most important point of this chapter is that linear transformations can always be represented by matrices when the vector spaces are finite (which are the only ones we use in this book). The only caveat is that this is not a one-to-one relationship but rather a one-to-many relationship in that each linear transformation can be represented by multiple matrices.

A word of caution about terminology. Some mathematicians call a linear transformation a linear mapping. Physicists and quantum computing practitioners use the term linear operator, which we will consider as a special type of linear transformation at the end of this chapter.

In this chapter, we are going to cover the following main topics:

Linearity
What is a linear transformation?
Representing linear transformations with matrices
Transformations inspired by Euclid
Linear operators
Linear functionals
A change of basis
day-modeBookmark
Linearity
What makes a transform linear? This question gets to the heart of linear algebra. The concept of linearity ties together all the other concepts we have considered so far and the ones to come. Indeed, quantum mechanics is a linear theory. That's what makes linear algebra crucial to understanding quantum computing.

Before I define linearity, let's look at what it is not. Real-life examples of non-linearity abound. For example, exercising 1 hour a day for 24 days does not give the same result as exercising 24 hours in 1 day. Watering a plant is another good non-linear example. Giving a plant 1 gallon of water a day for 100 days will be much better than giving it 100 gallons in 1 day. These are both examples of non-linear relationships. How much you put in does not always translate to what you get out.

Linear relationships, on the other hand, are proportional. Speed is a good example. If you go 20 mph for 1 hour, you'll cover 20 miles. If you go 1 mph for 20 hours, you'll still cover 20 miles. Exchange rates for money are also a good example. If the current rate is 2 dollars to a euro, then if I give you 4 dollars, you'll give me 2 euros. I can also give you 1 dollar 4 times and get the same result.

Graphs for these types of relationships are straight lines, such as this one for the euro example:

Figure 5.1 – A graph of the dollars to euros function
Figure 5.1 – A graph of the dollars to euros function

Crucially though, linearity requires functions to return 0 if 0 is the input to the function. So, straight-line functions that don't pass through the origin do not get ascribed the property of linearity. In other words, if I go 0 mph, I should cover 0 miles, and hopefully, you won't give me euros back if I give you 0 dollars (but you'd be my best friend if you did).

In mathematics, we want to generalize this concept so that it works in many situations. We are all familiar with a line through the origin. Let's take the simplest example, y = x, as shown in the following graph:

Figure 5.2 – The line y = x
Figure 5.2 – The line y = x

What can we generalize about this line? Well, the line has a constant slope, namely one, so that if I increase its slope, it consequently raises the output by a proportional amount. For example, let's say I increase the slope to three (y = 3x). Well, now instead of y being 3 at x = 1, it will be 3 Ÿ 3 or 9. This property has been generalized into something called homogeneity and is defined thusly:


Here is a small table showing values for our function y = x and the different values of α:

Table 5.1 – αf(x) and f(αx) at different values of x and α
Table 5.1 – αf(x) and f(αx) at different values of x and α

What else can we generalize about our line y = x? Well, if I added the value of y at x = 3 to the value of y at x = 4, it would equal the value of y at x = 7. This works no matter what slope I give the line, too. Here's another table of values to prove it to you:

Table 5.2 – f(x), f(z), and f(x+z) at different values of x and z
Table 5.2 – f(x), f(z), and f(x+z) at different values of x and z

This property is called additivity and is defined this way:


These two properties, additivity and homogeneity, define linearity. To be a linear transformation, a transformation must have linearity.

day-modeBookmark
What is a linear transformation?
To be precise, a linear transformation is a function T from a vector space U to a vector space V. A capital letter "T" is traditionally used by mathematicians to denote a generic transformation, and we use the same syntax that we introduced for functions in Anchor 3, Foundations:


Similarly, the vector space U is the domain, and the vector space V is the codomain. Each vector that is transformed is called the image of the original vector in the domain. The set of all images is the range.

To be linear, the transformation must preserve the operations of vector addition and scalar multiplication by meeting the conditions for linearity. Here, we express them in terms of vectors:


It follows from these axioms that for any linear transformation T, T (0) has to equal the zero vector 0. Let's look at how we describe transformations in the next section.

Describing linear transformations
There are many ways to describe a linear transformation. In the case of Euclidean vectors, you can describe a linear transformation geometrically. If you are dealing with n-tuples of numbers, you can describe the effect of the transformation on those numbers. Due to the concept of linear combinations, you can also describe how the transformation changes just the basis vectors. Let's go through each of these in depth.

A geometric description
To show an example of a geometric description, let's use reflection. Reflection is a very easy and intuitive transformation, as seen in the following diagram. We will call our reflection transformation "R":

Figure 5.3 – A graphical depiction of the reflection transformation
Figure 5.3 – A graphical depiction of the reflection transformation

One vector is the axis of reflection, and you reflect vectors about it by drawing a dashed line that is perpendicular to the axis of reflection from the tip of the original vector (|x⟩ in the diagram). Then, place the tip of the reflected vector R(|x⟩) equidistant from the axis of reflection.

Okay, now that we've described this transformation, let's check to see whether it is linear. First, we'll check for homogeneity. Homogeneity for vector transformations is defined as:


We will set s = 2, and you can see in the following diagram that our reflection transformation, R, does indeed pass the test for homogeneity:

Figure 5.4 – A test reflection for homogeneity
Figure 5.4 – A test reflection for homogeneity

Now, let's test the other condition for linearity, additivity. As you should recall, additivity for a linear transformation is defined as:


The following diagram shows a reflection for two vectors, |x⟩ and |y⟩. Note that R(|y⟩) is the same as |y⟩ because |y⟩ is on the axis of reflection:

Figure 5.5 – A reflection of |y⟩
Figure 5.5 – A reflection of |y⟩

Now, look at the following diagram closely:

Figure 5.6 – A test for additivity
Figure 5.6 – A test for additivity

We moved the start point of |y⟩and R(|y⟩) to the end of |x⟩ and R(|x⟩), respectively, because Euclidean vectors are equal as long as they retain their length and magnitude, as we explained in Chapter 1, Superposition with Euclid. From the diagram, you should be able to make out that additivity holds for reflections as well. Therefore, our reflection transformation is a linear transformation.

An algebraic description
Let's look at another way you can describe a linear transformation. If you are dealing with n-tuples of numbers in ℝn, then you can say explicitly what the transform does to an n-tuple. Let's look at an example.

First, I need to define the domain and codomain of the transform, like so:


Then, I can define what the transform does:


We represent n-tuples as column vectors, so this can be rewritten as:


The preceding equations fully define the linear transformation for every vector in our domain, ℝ2. Here are a few instances of the transformation in action:


We should make sure this transformation is indeed linear as well. Let's do homogeneity first:


Let's see how our transformation does with this:


Alright, it passes! Let's try additivity:


Here's the test:


Again, it passes, so this transformation is linear. Now it's your turn – are the following transforms linear?

Exercise one

A basis vectors description
I'd like to show you one more way to describe a linear transformation. There are many more ways to describe a linear transformation, but I think these three are a good way to start.

Since any vector in a vector space can be expressed as a linear combination of a set of basis vectors, if you describe what the transform does to a set of basis vectors, you've described the complete transformation. Let's show this through an example.

We'll start with our computational basis vectors |0⟩ and |1⟩. I'll describe what my transform does to these two vectors:


I have now fully described the transformation for every vector in my domain ℝ2. Let's take a random vector, |x⟩ in ℝ2, and work out its transformation:


You'll notice that I've expressed the vector |x⟩ as a linear combination of our basis vectors. By definition of a basis, I can do this for any vector in ℝ2. Now, I will apply the transformation to the linear combination:


Through this example, I hope I've shown that you can describe a linear transformation by just stating what it does to a set of basis vectors. We'll move on now to matrices!

day-modeBookmark
Representing linear transformations with matrices
Now for the most common and important way of describing a linear transformation, the matrix. Through the magic of matrix-vector multiplication, a matrix is all you need to describe a linear transformation.

Again, let's start with an example. I'm going to describe the linear transformation we used in the An algebraic description section with a matrix. To jog your memory, here is the aforementioned linear transformation:


Now, here is how I can describe it with a matrix:


I don't even need to be that formal, other than telling you that we are using real numbers; I can just give you the matrix, and that describes everything. The dimension of the domain is the number of columns of the matrix, the dimension of the codomain is the number of rows of the matrix, and the actual transformation is the matrix itself. That is the power of a matrix!

Let's apply this transformation to the same example vectors we used in the An algebraic description section using matrix-vector multiplication:


We get the same exact answers!

Matrices depend on the bases chosen
Now, let's look to see how we can use a matrix to describe our reflection transformation from before. The crucial point of this example is that our matrix depends on the basis we choose to represent it. Look at the transformation and see whether you can determine any good basis to use it:

Figure 5.7 – A reflection transformation
Figure 5.7 – A reflection transformation

Let's use the basis set E of |e1⟩ and |e2⟩ in the following diagram:

Figure 5.8 – A reflection transformation with basis vectors
Figure 5.8 – A reflection transformation with basis vectors

Using this basis, we can see that:


We can use the scalars of this linear combination as coordinates, as we learned in Chapter 4, Vector Spaces. This gives us the following:


So now, for our transformation R, we need to find a matrix A that represents it. Here is what I'm trying to say mathematically:


If you look at the equation closely, you should be able to make out what the entries of the matrix should be. Here they are in all their glory!


This is great! We have now found a matrix that we can multiply any vector by in our 2D space to get its reflection using our basis vectors E. Let's do it for the vector |y⟩ in this diagram:

Figure 5.9 – A reflection of |y⟩ with basis vectors
Figure 5.9 – A reflection of |y⟩ with basis vectors

Since |y⟩ is on the axis of reflection, it is its own reflection. In terms of our basis vectors E, |y⟩ and its reflection have the following coordinates:


Alright, it's time for the moment of truth. Will our matrix A give us the right vector back? Let's check:


It does! I will go ahead and tell you that this matrix will work for any vector that is expressed in terms of our basis set E.

You should also be able to see that if we picked a different set of basis vectors, the matrix would be different as well. In our first example, we chose a matrix based implicitly on the canonical computational basis. This is called the standard matrix of the linear transformation. But if you change the basis, say to |+⟩ and |-⟩, the matrix will change as well. You can even get really complex and change the input and output bases of the transformation to affect a new matrix, but this is rarely done in practice. The takeaway point of this section is that a matrix can represent a linear transformation, but there are many matrices that can represent it based on the basis chosen. Finally, matrices that represent the same linear transformation are called similar.

Matrix multiplication and multiple transformations
The last superpower we will go over for matrices is the fact that not only can they represent transformations, but they can also represent multiple transformations through matrix multiplication!

Let's say that we wanted to do our reflection transformation twice. Intuitively, we should get back the same vector. Using matrix multiplication, we can show that algebraically:


And there you have it – we have just proven that for any vector in ℝ2, doing our reflection twice returns the same vector.

The commutator
You should remember from Chapter 1, Superposition with Euclid, that matrices do not, in general, commute. This also means that linear transformations do not commute in general. Physicists use something called the commutator to represent "how much" two transformations or matrices commute.

The commutator is defined to be:


for two n x n matrices. This holds for any matrices that represent a linear transformation. If the commutator is zero for two transformations, then they commute. If it is non-zero, the operators are said to be incompatible. In quantum mechanics, observables such as momentum are represented by linear transformations. All of this leads to the famous uncertainty principle that states that two observables that do not commute cannot be measured simultaneously.

Okay, let's move on to something a little less heady and talk about translations, rotations, and projections.

day-modeBookmark
Transformations inspired by Euclid
In linear algebra, there are many "special" types of linear transformations that have names that connote concepts we have in our real world, such as reflections and projections. These concepts have been generalized to apply to all types of vectors, but the geometric description of them with Euclidean vectors gives us an idea as to why they work the way they do. This intuition can then be taken and applied to all types of vectors and vector spaces.

Translation
The first transform we will look at is translation. It transforms all vectors in a vector space by a displacement vector. More precisely:


In the following graph, the vector |x⟩ is translated to the right by |d⟩ to form T(|x⟩):

Figure 5.10 – A graphical depiction of translation
Figure 5.10 – A graphical depiction of translation

What's interesting about this type of translation is that it turns out to be non-linear! I will quickly show you.

Let's start with additivity and work it out algebraically. First, we will transform two vectors and add them together:


This should equal the transformation of the two vectors added together:


Unfortunately, they are not equal. In other words:


Another quick way to prove that a transformation is not linear is to show that the transform of the zero vector does not return the zero vector:


Finally, if we draw out the vectors, we can see that the transformation is not linear. The following diagram is a test for homogeneity and, as you can see, the transform T(2|x⟩) does not equal 2T(|x⟩):

Figure 5.11 – A test for homogeneity
Figure 5.11 – A test for homogeneity

I could have left this transformation out of this section, but I thought it important to show you that even intuitive concepts such as translation can be non-linear. Now, let's look at the linear transformations of projection and rotation. No more trickery – all the remaining transformations are linear!

Rotation
Everyone has a concept of what a rotation is. We need to take that concept and express it mathematically. This section will rely a lot on trigonometry. If you need to brush up, please consult the Appendix chapter on trigonometry.

Okay, let's start with two-dimensional rotations. I will actually define them using the following graph:

Figure 5.12 – A graphical depiction of a rotation transformation
Figure 5.12 – A graphical depiction of a rotation transformation

Describing this in words, given a vector |v⟩ and an angle θ, R(θ) will rotate |v⟩ through an angle θ with respect to the x axis about the origin.

Let's see what this transformation does to our two computational basis vectors |0⟩ and |1⟩. First, |0⟩ – if I rotate |0⟩ by θ radians, what do I get? Let's look at a graph:

Figure 5.13 – The effect of rotation by Ѳ on |0⟩
Figure 5.13 – The effect of rotation by Ѳ on |0⟩

From the graph, we can tell that the new coordinates for |0⟩ will be:


Now, on to |1⟩. Let's look at its graph:

Figure 5.14 – The effect of rotation by Ѳ on |1⟩
Figure 5.14 – The effect of rotation by Ѳ on |1⟩

From the graph, we can tell that:


I have now fully described the transformation both geometrically and through the basis vectors. What if I want to come up with a matrix for this transformation? Well, there is a theorem in linear algebra that if I give you the results of a transformation according to the computational basis, I can then compute the matrix according to this formula:

(1)


In other words, I can use the results I found before of the transform's effect on the computational basis vectors. Taking those results as column vectors and putting them into a matrix gives me the standard matrix for the linear transformation! Without further ado, here is our result:


Based on this, I can give you the result of a rotation for any vector in ℝ2:


Note that Equation (1) works for any finite amount of computational basis vectors as well:


Now, on to another intuitive transformation, projection.

Projection
Projection is another linear transformation that it is good to be acquainted with in quantum computing, since it is used heavily in the measurement of qubits. A good way to conceptually look at it is the way we think about projection in the everyday world. Let's take the process of taking a picture with a camera. When you do this, you are projecting a 3D world onto a 2D surface.

Also, if you were to take a picture of the picture, you would get the same picture. Doing a projection twice does not yield a different result.

In this figure, I am projecting a 3D cube onto a two-dimensional plane:

Figure 5.15 – A projection of a cube on a 2-D plane
Figure 5.15 – A projection of a cube on a 2-D plane

In the following figure, I am projecting a two-dimensional circle onto a 1D line:

Figure 5.16 – A projection of a two-dimensional circle onto a one-dimensional line
Figure 5.16 – A projection of a two-dimensional circle onto a one-dimensional line

If I project the line again, I will get the same line. It is this feature of projection that mathematicians have generalized to create a definition for projections. If you have a linear transformation P, then if the following condition holds, it is a projection:


(2)

That's it! Not that bad, huh?

Okay, let's say that we want to come up with a projection matrix for the projection of the cube onto a plane in Figure 5.15. Let's say that the plane is the X-Y plane and all the points or vectors for the cube are in ℝ3. So, we need to keep the X-Y coordinates but set the Z coordinates to zero. We need a matrix that does this:


If we set P to the following matrix, that should do it:


Let's see if Equation (2) holds:


Indeed, it does. Now, you get to test it out.

Exercise two
What is the answer to this problem for a random three-dimensional vector?


Now, on to a special type of linear transformation.

day-modeBookmark
Linear operators
Linear operators are linear transformations that map vectors from and to the same vector space. Indeed, reflections, rotations, and projections are all linear operators. In quantum, we put a "hat" or caret on the top of the letter of the linear operator when we want to distinguish it from its representation as a matrix. For instance, all the following linear transformations are linear operators:







Most of the time, it is clear from the context that we are referring to a matrix or a linear operator, so the caret or "hat" is not used.

The following linear transformations are not linear operators:


You probably noticed that all linear operators are represented by square matrices. This leads to all types of special properties that they can have, such as determinants, eigenvalues, and invertibility. We will take up all these topics in later chapters, but I wanted to make sure that you knew this term. In quantum computing, you will rarely see the term linear transformation, but it is a common term used in mathematics. It will almost always be linear operator in quantum computing, and now you know that it is just a special type of linear transformation. Also, there is one other special type of linear transformation I would like to look at.

day-modeBookmark
Linear functionals
A linear functional is a special case of a linear transformation that takes in a vector and spits out a scalar:


For instance, I could define a linear functional for every vector in ℝ2:


So that:


There are many linear functionals that can be defined for a vector space. Here's another one:


The set of all linear functionals that can be defined on a vector space actually form their own vector space called the dual vector space. This concept is important to fully define a bra in bra-ket notation. Please see the Appendix section on bra-ket notation if you are interested in more information.

day-modeBookmark
A change of basis
We learned in Chapter 4, Vector Spaces, that a vector can have different coordinates depending on the basis that was chosen, but we didn't tell you how to go back and forth between bases. In this section, we will.

We want to come up with a matrix – let's call it B for a change of basis – that takes us from one basis to another. In other words, we want this mathematical formula to work:


This matrix B will convert the coordinates of a vector according to a basis C to the coordinates for the vector in the basis F. Now, how do we find this matrix?

Let's look at an example. We will define the basis C as the computational basis and the basis F this way:


Now, let's look at a random vector, |v⟩, defined in the computational basis C:

(3)


So, what we want to do is to find the coordinates of |v⟩ in the basis F. In other words, we want to find the variables a and b in the following equation:


What would happen if we took our basis vectors in C and multiplied them by our change of basis matrix B? We would get our basis vectors in C expressed as coordinates in the basis F, as shown in the following equation:

(4)


Let's take our original Equation (3), multiply it by our change of basis matrix B, and express it again based on our new-found knowledge from Equation (4):


We can express that very conveniently as matrix multiplication, like so:

(5)


The next step is to find our basis vectors in C, |0⟩ and |1⟩, expressed as coordinates in F. To do this, we have to find them expressed as a linear combination of the vectors in the basis F! We'll start with |0⟩:


Let's work it all out:


And here are the calculations to obtain the coordinates in F for |1⟩:


Now that we have that, let's plug these vectors back into Equation (5) and see what we get, using our change of basis matrix B on our random vector |v⟩:


So, there you have it – we have changed a vector expressed in C to a vector expressed in F using a matrix. Due to this, a change of basis is a linear transformation. With this change of basis matrix, we can change any vector expressed as coordinates in C to coordinates in F. But how do we know we're right? Well, the vector |v⟩ should be equal as a linear combination in either basis, so:




Okay, now that we've worked out an example, I'll give you the general formula for transforming a basis, and hence, you will be able to transform the coordinates for every vector in one basis to another:


This is basically saying that you have to express the basis vectors in the input basis as coordinates in the output basis.

day-modeBookmark
Summary
We have covered the breadth of linear transformations in this chapter. They are key to understanding the linear algebra that is pervasive in quantum computing. We've also seen how these transformations have been inspired by Euclidean geometry and considered special transformations such as linear operators and linear functionals. Finally, we saw how to do a change of basis, which is a linear transformation as well! Next up, we will go from real numbers into the field of complex numbers.