Chapter 6: Complex Numbers
"What is unpleasant here, and indeed directly to be objected to, is the use of complex numbers. Ψ is surely fundamentally a real function."

– Letter from Schrödinger to Lorentz. June 6, 1926.

Even the great physicist Erwin Schrödinger was perplexed by the occurrence of complex numbers in quantum mechanics. Yet, complex numbers have been found to be inherent to quantum mechanics and, hence, quantum computing. Up until now, we have concentrated on the real numbers to make concepts easier to get across. It is time now to cross the Rubicon and make our way into the complex plane. You have probably come across complex numbers before, but we will go into great depths about them in this chapter. I think it is unfortunate that René Descartes named i an imaginary number, as it makes it seem that this topic should be otherworldly. But so was the number 0 when it was introduced, and the same with negative numbers. No one gives them a second thought today and you should treat complex numbers the same way. They are just another set of numbers.

In this chapter, we are going to cover the following main topics:

Three forms, one number
Cartesian form
Polar form
The most beautiful equation in mathematics
Exponential form
Bloch sphere
day-modeBookmark
Three forms, one number
There are three main ways of representing a complex number:

Cartesian form (aka the general form)
Polar form
Exponential form
Each one has its advantages and disadvantages, depending on what we are trying to do. These will become evident as we go through them.

Definition of complex numbers
A complex number is a number that can be expressed in the following way:


(1)

where a and b are real numbers and i is the imaginary unit. The imaginary unit is defined as:



It follows from this that there are two square roots of -1, i and -i.

The real part of a complex number is denoted by Re(z) and the imaginary part is denoted by Im(z). For our complex number, z, defined in Equation (1), Re(z) = a and Im(z) = b. Two complex numbers, z and w, are equal if, and only if, Re(z) = Re(w) and Im(z) = Im(w).

It is important to remember that the set of real numbers ℝ is a subset of ℂ. Hence, if Im(z) = 0 for a complex number z, then z is also a real number.

Let's quickly look at some examples of complex numbers:









Now, let's move on to describing the three forms of complex numbers.

day-modeBookmark
Cartesian form
We used the Cartesian form to define a complex number. To see why it is called Cartesian, notice we can also use an ordered pair of real numbers to represent the complex number z. The first number of the ordered pair will be the real part of the complex number, and the second number will be the imaginary part:



Given this, we can represent complex numbers on a Cartesian coordinate system since a and b are just real numbers. We will need to make a couple of modifications though.

We will replace the x axis with an axis for the real part of a complex number ( Re(z) ), and the y axis with an axis for the imaginary part of a complex number ( Im(z) ), like so:


Figure 6.1 – The complex plane
Figure 6.1 – The complex plane

This is called the complex plane. Here is an example involving actual complex numbers:


Figure 6.2 – Complex numbers on the complex plane
Figure 6.2 – Complex numbers on the complex plane

Keep this in mind as we go through the basic operations of complex numbers as we can think of them both algebraically and geometrically, as we did in Chapter 2, Superposition with Euclid.

Addition
Addition is rather easy for complex numbers; just add Re(z) and Im(z) of the two numbers together to get the sum. We will be using the following two complex numbers in our following definitions:





Here is the definition:



Subtraction is defined as:



Here are some examples:



Remember that you can view complex numbers as vectors on the complex plane, so addition, scalar multiplication, and subtraction can be viewed graphically as well, as in the following:

Figure 6.3 – Vector addition and scalar multiplication [1]
Figure 6.3 – Vector addition and scalar multiplication [1]

Alright, let's move on to multiplication.

Multiplication
I will show you another way to do complex multiplication later in this chapter, but you should know how to do it with the Cartesian form of a complex number. Hopefully, you remember the FOIL method from high school algebra. If you do, you can skip the next section. If not, here's a quick refresher:

FOIL method (optional)
The FOIL method is used to multiply two binomials together. It stands for:

First terms
Outer terms
Inner terms
Last terms
You add these all up, and there you are! This figure should jog your memory:

Figure 6.4 – FOIL method illustrated [2]
Figure 6.4 – FOIL method illustrated [2]

Now that we've jogged your memory, on to the defintion of multiplication for complex numbers.

Definition
Here is the definition of the multiplication of two complex numbers in Cartesian form. It is:



As always, here is an example for your viewing pleasure:



Now it's your turn.

Exercise 1
What is:







Now for a new concept that doesn't exist for real numbers.

Complex conjugate
While the definition of the complex conjugate is very simple, store it somewhere safe in your brain as it will become very important to us as we move forward. The complex conjugate of a complex number a + bi is a – bi. That's it! It is written as z* for a complex number z. Here it is again, just to drill it into your skull :)



It is interesting to view complex conjugation on the complex plane as it is just a reflection of the real axis, as you can see in the following figure:


Figure 6.5 – Complex vector reflected on the real axis
Figure 6.5 – Complex vector reflected on the real axis

Now we'll use the complex conjugate to get the absolute value of a complex number.

Absolute value or modulus
Again, simple, but very important. The absolute value or modulus of a complex number z, denoted |z|, is the square root of z multiplied by its conjugate, z*:



It can also be defined thus for a complex number z = x+ iy:



Here's an example:







Exercise 2
Compute the following absolute values:







Division
The way to compute the division of two complex numbers is unfortunately much harder than multiplication. However, there is a process named "rationalizing the denominator," which makes it easier.

Let's define our two complex numbers as:



where both a and b ≠ 0. First, we multiply the numerator and denominator by the complex conjugate of the denominator:



Then we use the FOIL method:



Finally, we substitute the terms that have i2 with -1:



Hopefully, that wasn't too bad. Let's look at an example for this quotient:



From there, let's solve it together:



As you can see, it's a little more than division in the real numbers.

Powers of i
I wanted to make sure that you could calculate the powers of i in your complex number toolkit. The positive powers of i follow this pattern:



The negative powers of i follow a very similar pattern:



Hopefully, you see the patterns here and can derive any power of i. Alright, off to the next form of complex numbers – polar!

day-modeBookmark
Polar form
The polar form is based on polar coordinates, which you may or may not be used to. If not, the next section goes through these, otherwise, you can skip it. Also, the rest of the chapter is heavy on trigonometry and we use radians for all angles. If you require a quick refresher on these, please consult the Appendix.

Polar coordinates
Polar coordinates are another way of representing points in ℝ2. We are very familiar with the Cartesian coordinate system and its points, such as (x,y). Now we will represent a point with two coordinates called r and θ. The following diagram is very helpful in terms of putting this all together:

Figure 6.6 – Polar coordinates on a graph
Figure 6.6 – Polar coordinates on a graph

As you can see, r is the hypotenuse of a right triangle with the other two sides being the Cartesian coordinates x and y. Because of this, it is easy to derive the equation to find r given the Cartesian coordinates using the Pythagorean theorem:


(2)

We can use the trigonometric function tangent to derive θ:




(3)

Let's look at an example. Let's say we have the point (3,4), as shown in the following figure:


Figure 6.7 – The point (3,4)
Figure 6.7 – The point (3,4)

Now we need to convert from Cartesian coordinates to polar coordinates using our formulas. So, using Equation (2), r would be:



Now that we've found r, we need θ. Again, we'll use our formula from Equation (3):





There you go! We have found that (3, 4) in Cartesian coordinates is (5, .9273) in polar coordinates. Now it is your turn.

Exercise 3
Convert the following into polar coordinates:

(-3,3)

(4, 1)

(-2, π)

Defining complex numbers in polar form
Since we can use Cartesian coordinates with complex numbers, we can also use polar coordinates with complex numbers. Here is Figure 6.6 from the last section again, but this time using the complex plane:


Figure 6.8 – Polar coordinates of the complex number z
Figure 6.8 – Polar coordinates of the complex number z

Several things have changed in the graph. The real and imaginary axes have replaced the x and y axes, along with the x coordinate being Re(z) and the y coordinate being Im(z) now.

The r in the hypotenuse represents the modulus of our complex number, z. This makes sense if we remember that for a complex number, z = a + bi:



The Greek letter Θ (pronounced "theta") is called the argument of the complex number z by mathematicians, but in quantum computing, it is often called the "phase." We denote this in math as follows:



From the graph, we can derive the following:



Putting this all together, we can say that for a complex number, z, it can be represented in polar form as:





Let's explore some more concepts of complex numbers in polar form.

Example
Okay, let's put this into an example. Let's find the polar form of z = -4 + 4i. First, we need to find the value of r:





Now we have to find θ:



Now that we have r and θ, we can express z in polar form:



Let's now explore some more concepts of complex numbers in polar form.

Multiplication and division in polar form
While the polar form is not recommended for addition and subtraction, it is recommended for multiplication and division. It is much easier to perform these operations, as you will quickly realize.

Given the two complex numbers below:



The product of these two numbers is:


(4)

Notice that all we had to do was add the angles and multiply the moduli. Pretty easy, right!?!

Dividing the two complex numbers is similarly easy. It is defined as:



Here, all you have to do is subtract the angles and divide the moduli.

Example
Say we have two complex numbers:





Converting to polar form, we have:



Applying our formula to the product of the two complex numbers in Equation (4), we get the following for the product:



De Moivre's theorem
If we use Equation (4) to repeatedly multiply one complex number by itself, we get:



You should see a pattern whereby, in order to get a power of a complex number, we take the power of the modulus and multiply the angles by the power. This is known as de Moivre's theorem. It states that:



Make sure to tuck this away somewhere. Let's now move on to the most beautiful equation in mathematics!

day-modeBookmark
The most beautiful equation in mathematics
In 1748, Leonhard Euler (pronounced "oy-lr") published his most famous formula, aptly called Euler's Formula:



This is true for any real number θ. Substituting θ = π into this equation gives the most beautiful equation in math, called Euler's identity:



It is hard to overstate the beauty of this equation. It combines in one equation what are arguably the most important symbols and operations in mathematics. Along with the operations of addition, multiplication, and exponentiation, you have 0, the additive identity, 1, the multiplicative identity, i, the imaginary unit, and two of the most important mathematical constants, e and π. This equation is also integral to quantum computing. You will see eiθ all over the place in quantum computing, so you better get used to it!

So, how does this equation help us in quantum computing? You're about to find out, but first, we need to use it to express complex numbers in exponential form.

day-modeBookmark
Exponential form
Complex numbers written in terms of eiθ are said to be in the exponential form, as opposed to the polar or Cartesian form we have seen earlier. Using Euler's formula, we can express a complex number, z, as:



So



As you can see, the exponential form is very close to polar form, but now you have θ in one place instead of two!

Exercise 4
Express the following complex numbers in exponential form:







Conjugation
As we have seen, the conjugation of a complex number is represented as a reflection around the real axis. For complex numbers in exponential form, this means we just change the sign of the angle to get the complex conjugate:







Multiplication
Multiplication and division are even easier in exponential form and are one of the reasons why it is so preferred to work with. We can take our steps for multiplication from the polar form and easily restate them in exponential form.

Given the two complex numbers below:



In exponential form, they are represented as:



The product of these two numbers in polar form is then:



Their product in exponential form is then:



Without going through all that, I will simply state that for division:



Example
Let's reuse our example from the section on the polar form, but do it in the exponential form!





Going from the Cartesian form to the polar form and then the exponential form, we get:



Finally, using our definition of multiplication in the exponential form from before, we get:



day-modeBookmark
Conjugate transpose of a matrix
Since we now have the definition of the complex conjugate of a number, I'd like to quickly go over the conjugate transpose of a matrix as we will use this later in the book. The conjugate transpose is exactly as it sounds. It combines the notions of complex conjugates and the transposition of a matrix into one operation. If you remember from Chapter 2, The Matrix, we defined the transpose to be:



This is where we essentially convert the rows into columns and the columns into rows.

The conjugate of a matrix is just the conjugation of every entry:



For example, if the matrix M equals

,

then M* equals

.

So here is the big payoff. The conjugate transpose of a matrix A is defined to be:



The cross symbol at the top right of A is pronounced "dagger," and therefore when you hear "A dagger," the conjugate transpose of A is being referred to.

A quick example should get this all sorted. Let's use our matrix M from before. The conjugate transpose of M would be:



Please note that the conjugate transpose of a matrix also goes under the names Hermitian conjugate and adjoint matrix.

Okay, with all that squared away, we can get to some cool quantum computing stuff called the Bloch sphere!

day-modeBookmark
Bloch sphere
This is the big payoff of the chapter, understanding the Bloch sphere! The Bloch sphere, named after Felix Bloch, is a way to visualize a single qubit. From Chapter 1, Superposition with Euclid, we know that a qubit can be represented in the following way:



We did not say this before, but now that we have introduced complex numbers, we can say that α and β are actually complex numbers.

Now we know that complex numbers take two real numbers to represent, it looks as though we will need four real numbers to characterize a qubit state. This is very hard to graph as we cannot visualize 4D space. Let's see whether we can decrease the number of real numbers required to represent a qubit state.

First, let's replace α and β with their exponential form to get:



Now, let's rearrange the right side of the equation by taking out  and distributing it. Notice that I need to subtract the phase of  from the second term:


(5)

It ends up that quantum mechanics (QM) calls  the "global phase" in Equation (5) and that it has no measurable effect on the qubit state. Therefore, QM lets us drop it. So now we have:



The (φβ - φα) in the second term is called the "relative phase." We will replace it with just one φ and also restrict it to go from 0 to 2π radians. Here is the new equation:



Okay, hopefully, you're keeping up. If you're keeping score at home, with all this mathematical contortion, we are now down from four dimensions to three dimensions to describe the qubit state. Can we get down to two dimensions? Let's try!

Another constraint we know is that α and β represent probability measurements and all probabilities must add up to one, so:



Because of this, the following must also be true:



We can represent this on the first quarter of a unit circle like so:

Figure 6.9 – Unit circle with a right triangle showing the parameters of our qubit
Figure 6.9 – Unit circle with a right triangle showing the parameters of our qubit

You may have noticed that we use θ/2 rather than just θ. The reason for this goes into very deep physics and math that are beyond the scope of this book. If you are very interested in why this is the case, please consult https://physics.stackexchange.com/questions/174562/why-is-theta-over-2-used-for-a-bloch-sphere-instead-of-theta.

Now we can represent our two coefficients for r as:







Okay, here's the big payoff!



We're down to only two dimensions (θ and φ). Using these two angles, we can represent the qubit state on a unit sphere like so:

Figure 6.10 – Bloch sphere [3]
Figure 6.10 – Bloch sphere [3]

Θ is like the latitude on a map, but it goes from zero on the north pole, represented by the zero state, to π/2 on the equator and π on the south pole, which represents the one state. I was only able to show you how to get to the sphere mathematically, which is still a lot! For more information on why we need the Bloch sphere, please consult Packt's other great book, Dancing with Qubits, by Robert Sutor. For a cool, interactive visualization of the Bloch sphere, please go to https://www.st-andrews.ac.uk/physics/quvis/simulations_html5/sims/blochsphere/blochsphere.html.

day-modeBookmark
Summary
Well, we've come a long way in a few pages. We've now seen how complex numbers can be expressed in the three forms of Cartesian, polar, and exponential. We've also seen which forms are better for different operations. You've learned how to multiply, divide, add, and subtract complex numbers. Finally, we've put it all together to mathematically derive the Bloch sphere. Bravo!

In the next chapter, we will explore the world of eigenvalues, eigenvectors, and all kinds of eigenstuff. Get ready!

day-modeBookmark
Exercises
Exercise 1






Exercise 2






Exercise 3
(-3,3)



(4, 1)



(-2, π)





Exercise 4




