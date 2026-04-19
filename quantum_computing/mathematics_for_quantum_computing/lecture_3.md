Chapter 3: Foundations
Up until this point, we have introduced our mathematics with as little rigor as possible. This chapter – and this part of the book – will change that. You may ask why? Well, this rigor and foundational material is needed when we get to much more complex concepts such as Hilbert spaces and tensor products. Without this chapter, these advanced concepts will not make sense, and you won't have the context to understand them.

This chapter goes through the field of abstract algebra. As you might expect, there will be some abstract concepts that will be explored. Abstract algebra takes a step back from all other forms of algebra, such as linear, Boolean, and elementary algebra, and it tries to see what can be generalized between them. Mathematicians have found that they can generalize a few foundational concepts that, when put together, allow us to go further in math than we have before and help us understand it at a more fundamental level. Within this chapter, our ultimate goal will be to define vector spaces rigorously.

So, without further ado, let's get into the material. We will cover the following topics:

Sets
Functions
Binary operations
Groups
Fields
Vector spaces
day-modeBookmark
Sets
Sets are very intuitive and are really about grouping things together. For example, all mammals – taken together – form a set. In this set, its members are things such as the fox, squirrel, and dog. Sets don't care about duplication – so, if we have 5,000 dogs in our first mammals set, this set is equal to a set of mammals that has only one dog. Let's make this more formal.

The definition of a set
A set is a collection of objects. This collection can be finite or infinite. Mathematical objects are abstract, have properties, and can be acted upon by operations. Examples of objects are numbers, functions, shapes, and matrices. Objects in a set are called elements or members.

Notation
There are multiple ways to denote a set. The easiest way is to just describe it, as I did with the set of mammals. Another example for doing this would be to describe a set S of all US States. Some examples of elements in this set would be Virginia and Alabama. Let's look at a more formal way to notate sets called set-builder notation.

Set-builder notation
Set-builder notation is definitely more formal, but with this formality, you gain preciseness (which mathematicians covet). The easiest way to denote a set in set-builder notation is just to enumerate all the members of a set. You do this by giving the variable name of the set, followed by an equals sign, and then the members of the set are put into curly brackets and separated by commas. Here is an example:



Any guesses on what this set is? Extra bonus points if you guessed the noble gases.

An ellipsis (…) is used to skip listing elements if a pattern is clear or to denote an infinite set, shown as follows:



The final way you can denote a set is to include conditions for the members of your set. Here is an annotated example to explain each part of the notation:


Figure 3.1 – An annotated description of set-builder notation
Figure 3.1 – An annotated description of set-builder notation

You can also describe what type of number you are dealing with by writing the type before the vertical bar, like so:



This is equivalent to the set {2, 3, 5, 7}.

Other set notation
An important symbol in set notation is ϵ, which denotes membership. If there is a slash through ϵ, it means the object is not a member of the set. For example, the following denotes that He (helium) is a member of the noble gases and O (oxygen) is not:



The next symbol to consider is used to denote subsets. If X and Y are sets, and every element of X is also an element of Y, then:

X is a subset of Y, denoted by X ⊆ Y.
Y is a superset of X, denoted by Y ⊇ X.
For example, the set N of the noble gases is a subset of the set E of all elements. Or, mammals are a subset of the animal kingdom and a superset of the primates.

Finally, it is important to define the empty set that has no members and is denoted by ∅ or {}. The empty set is a subset of all sets.

Important sets of numbers
Since mathematics is all about numbers, special attention should be given to certain sets of numbers that we will see in this book. Each one has a special double-struck capital letter to represent them. So, without further ado, here is the list:

ℕ, which is the set of natural numbers defined as {0, 1, 2, 3, …}. This is the first set of numbers you learn as a child, and they are used for counting.
ℤ, which is the set of integers defined as {…, -3, -2, -1, 0, 1, 2, 3, …}. This is a superset of ℕ. The letter Z comes from the German word Zahlen, which means numbers.
ℚ, which is the set of rational numbers, where a rational number is defined as any number that can be expressed as a ratio or quotient of two integers. Since all integers are divisible by 1, ℤ is a subset of ℚ.
ℝ, which is the set of real numbers. The real numbers are composed of ℚ and all the irrational numbers. Irrational numbers, when represented as a decimal, do not terminate, nor do they end with a repeating sequence. For example, the rational number 1/3 is represented as 0.33333… in decimal, but the irrational number π starts with 3.14159, but it never terminates nor repeats a sequence. Some other examples of irrational numbers are as follows: all square roots of natural numbers that are not perfect squares; the golden ratio, ϕ; Euler's number, e.
ℂ, which is the set of complex numbers. We will go in-depth into complex numbers in a later chapter, but for now, we will just say that a complex number is represented by:


If we set b = 0, then we have the set of all real numbers, so ℝ ⊆ ℂ.

To sum up:



The following diagram shows this very well graphically:

Figure 3.2 – A diagram showing all the sets of numbers [1]
Figure 3.2 – A diagram showing all the sets of numbers [1]

Alright, let's move on to tuples!

Tuples
It is important to note that sets do not care about order. So, if set A = {1, 2, 3} and set B = {2, 3, 1}, A and B are equal. Sets also do not care about duplication. So, if set C = {1, 2, 3, 3, 3} and set D = {1, 2, 3}, C and D are also equal. A mathematical object that does care about these things is called a tuple.

A tuple is a finite, ordered list of elements, which is denoted with open and close parentheses, as shown here:



Since order and duplication matters to tuples, none of the preceding examples are equal to each other. The number of elements in a tuple is defined as n, and we use this number to refer to a tuple as an n-tuple. For example, in the preceding example, E is a 4-tuple and F is a 3-tuple. Some n-tuples have special names; for example, a 2-tuple is also known as an ordered pair.

The Cartesian product
The Cartesian product may not be as familiar to you as sets, but it is still important. The Cartesian product takes two sets and creates a third set of ordered pairs (that is, 2-tuples) from those two sets. It is denoted by the × symbol. The following figure shows an example for the Cartesian product of two sets A={x, y, z} and B={1, 2, 3}.

Figure 3.3 – An example of the Cartesian product of A × B [2]
Figure 3.3 – An example of the Cartesian product of A × B [2]

Here's another example: if I have a set A = {1, 2} and a set B = {6, 7, 8, 9}, then A × B is equal to {(1, 6), (1, 7), (1, 8), (1, 9), (2, 6), (2, 7), (2, 8), (2, 9)}. It should be noted that the Cartesian product is not commutative, so in general, A × B ≠ B × A.

The greatest example of this operation is from Rene Descartes (who the Cartesian product is named after). You have probably heard of the Cartesian plane, as shown in the following diagram. Well, this is the Cartesian product of the set X of the real numbers ℝ and the set Y of the real numbers ℝ, and it is denoted by ℝ × ℝ = ℝ2.

Figure 3.4 – A Cartesian plane with Cartesian coordinates [3]
Figure 3.4 – A Cartesian plane with Cartesian coordinates [3]

The Cartesian product can be done multiple times, so if you have three sets, for example, X, Y, and Z, then X × Y × Z is the set of all 3-tuples for every combination of elements of X, Y, and Z. Again, an example is helpful: let's say ℝ × ℝ × ℝ produces ℝ3, which is the set of all 3-tuples of real numbers or three-dimensional space. In general:



So, for shorthand, we write ℝn to denote all of the n-tuples of real numbers.

Now that we have covered everything to do with sets and tuples, let's look at another fundamental object: functions.

day-modeBookmark
Functions
Functions are fundamental to mathematics, and there is no doubt that you have been exposed to them before. However, I want to go over certain aspects of them in depth, as we will define things such as matrices as representations of functions later in the book.

The definition of a function
A function, for example, y = f(x), maps every element x in a set A to another element y in set B. Each element y is called the image of x under the function f(x). Set A is called the domain of the function and set B is called the codomain of the function. The domain and codomain of a function are denoted by f: A → B . The following mapping diagram shows the function f: X → Y.

Figure 3.5 – An example function [4]
Figure 3.5 – An example function [4]

All the images of f(x) form a set called the range. The range is a subset of the codomain. In the previous diagram of our function f: X → Y, the codomain was the set Y, but the range was the set {D, C}. The image of the element 1 in the domain was the element D in the range.

I could define another function, f:ℝ → ℝ, where f(x) = 2x. Here, the domain and codomain are the real numbers, as well as the range. The image of 3 under f(x) is f (3)=6.

There are two rules that functions must follow:

Every member of the domain must be mapped.
Every member of the domain cannot be mapped to more than one element in the codomain.
The mapping shown in the following figure is illegal because it doesn't follow these two rules. It breaks the first rule by not mapping the elements 3 and 4 in the domain. Can you spot how it breaks the second rule?

Figure 3.6 – An example of an illegal function [5]
Figure 3.6 – An example of an illegal function [5]

I'm sure you pointed out that it breaks the second rule by mapping the element 2 to B and C.

Let's say I have a set C = {1, 2, 3} and a set D = {4, 5, 6}. One of the many ways I can define a function is with a table. This table defines a function, f:C → D.

Figure 3.7 – A function table
Figure 3.7 – A function table

Now, imagine I delete the last row from the table. Is it still a function? No, because I do not have a mapping for every element of the domain set A, namely, the number 3.

Exercise 1
For the sets E = {a, b, c} and F = {4, 5, 6, 7, 8}, and a function, f:E → F, which of the following tables do not represent a function?

Figure 3.8 – The Exercise 1 tables
Figure 3.8 – The Exercise 1 tables

Invertible functions
Invertible functions are key in quantum computing because the laws of quantum mechanics only allow these types of functions in certain situations. Before going into invertibility, I'd like to look at three other properties of functions.

Injective functions
An injective function, also known as a one-to-one function, is a function where each element in the range is the image of only one element in the domain. It is important to note that not every element in the codomain needs to be in the range, so a function is still injective if there are members of the codomain that are not mapped. Let's look at an example.

Figure 3.9 – The function on the left is injective and the function on the right is not
Figure 3.9 – The function on the left is injective and the function on the right is not

The function on the left in Figure 3.9 is injective because A, B, and C are the image of only one element in the domain X. The function on the right is not injective because B is the image of both the numbers 2 and 3 in the domain X.

Surjective functions
A surjective function, also known as an onto function, is a function where the range of the domain of the function is equal to its codomain. Another way to say this is that every element in the codomain is mapped to by at least one element in the domain.

Neither of the functions from Figure 3.9 is surjective because they leave elements in the codomain unmapped. However, the following functions are surjective:

Figure 3.10 – Two surjective functions
Figure 3.10 – Two surjective functions

The function f:ℝ →ℝ, where f(x) = x2, is not surjective because not all of the elements in the codomain (namely, all negative real numbers) are mapped to, as the square of a number (that is, x2) can only be non-negative. The negative real numbers are left out.

Bijective functions
Now that we know what injective and surjective functions are, defining a bijective function is quite easy! A bijective function is one that is both injective and surjective. And guess what else we get in this deal!? A function is invertible if it is bijective!

Now, did you notice any bijective functions in our preceding examples? Extra, extra bonus points if you pointed to the function on the right in Figure 3.10, which is reproduced in the following figure:

Figure 3.11 – A bijective, invertible function
Figure 3.11 – A bijective, invertible function

The inverse of a function, such as, f(x) is usually denoted by f -1 (x). It makes sense that an invertible function has to be bijective. The only way I can make f -1 (x) a function is to make it follow the two rules for functions that we described before, namely:

Every member of the domain must be mapped.
Every member of the domain cannot be mapped to more than one element in the codomain.
For f -1 (x), the domain and codomain are flipped. For it to follow the first rule, every element of the codomain for f(x) must be mapped (that is, f(x) has to be surjective). And for it to follow the second rule, every member of the range of f(x) cannot be mapped to more than one element in its domain (that is, f(x) is injective). The following figure shows f -1 (x) graphically:

Figure 3.12 – The inverse of f(x)
Figure 3.12 – The inverse of f(x)

Alright, that concludes our discussion of functions. Let's move on to binary operations.

day-modeBookmark
Binary operations
You are probably familiar with some binary operations, for example, addition and multiplication, but we are going to look at binary operations in more depth.

The definition of a binary operation
A binary operation is simply a function that takes two input values and outputs one value. More precisely, it takes an ordered pair (known as an operand) from the Cartesian product of two sets and produces an element in another set. Using our notation:



An operation can be anything! For example, sexual reproduction within the set of mammals can be considered a binary operation. It takes an ordered pair from the subsets of males and females and produces another member of the set of mammals. More formally:



Within the number systems, addition is a good example of a binary operation. Let's define it for the real numbers:





You'll notice that with binary operations, we don't use the usual function notation of f(x, y), but instead, we use a symbol with the first element on the left side and the second element on the right side. I want to remind you that binary operations are a general concept – that is, they can be anything – so I will use the unusual ֎ symbol when I want to talk about operations in general.

Properties
Operations can have several properties, most of which are probably familiar to you from grade school. But again, it's important to spell these out to understand abstract algebra. Here are the properties for a set S:

Identity: There exists an identity element, e ∈ S, such that for all x ∈ S, a ֎ e = e ֎ a = a. This element, e, is unique, and it is called the identity element of the group.
Associativity: If a, b, c ∈ S, then a ֎ (b ֎ c) = (a ֎ b) ֎ c.
Invertibility: For every a ∈ S, there exists an a-1, such that a ֎ a-1 = a-1 ֎ a = e, where e is the identity element identified in rule one.
Closure: For every a, b ∈ A, a ֎ b produces an element c that is also in the set A. f: A × A → A.
Commutativity: If a, b ∈ S, then a ֎ b = b ֎ a.
Okay, now that we defined binary operations and their properties, we can move on to discuss important algebraic structures.

day-modeBookmark
Groups
A group builds upon the concept of a set by adding a binary operation to it. We denote a group by putting the set and the operation in angle brackets (⟨⟩). For example, ⟨A, ֎⟩ for set A and operation ֎. The operation has to follow certain rules to be considered a group, namely, the rules of identity, associativity, invertibility, and closure. If the operation ֎ also has the property of commutativity, then it is called an Abelian group (also known as a commutative group).

In our example set of mammals, the operation of sexual reproduction would not make it a group because the only property it has is commutativity.

Now, let's look at a mathematical example. What if we define ֎ to be addition over the natural numbers ℕ denoted ⟨ℕ, ֎⟩ – is this a group? Well, let's go through the properties and see if it fulfills each one.

Identity: Does there exist an identity element e, such that a + e = e + a = a? Well, yes, if we define e = 0!
Associativity: Does a + (b + c) = (a + b) + c? Yes!
Invertibility: For every a ∈ ℕ, is there an a-1, such that a + a-1 = a-1 + a = e, where e is the identity element identified in rule one (e = 0)? Hmmm, this is a tough one. So, ℕ starts at zero and goes to positive infinity, but it does not include the negative numbers. Without negative numbers, there is no way to define an inverse of a that when added to a, will always equal zero.
Closure: If we take two numbers, a and b, in ℕ, then does a + b produce a natural number, c? Well, zero is taken care of because it is our identity element for rule one. 1 + 2 = 3, and 3 is also in ℕ. How about 100,000 + 200,000? Well, that equals 300,000, and that is also in ℕ. So, no matter how large we pick two numbers in ℕ, they will always produce another number in ℕ, as it goes to positive infinity!
So, there you have it. It ends up that addition with the set ℕ is not a group. Is there a set that would work? Why yes! The set of all integers, ℤ! We can then define a-1 to be –a, and suddenly, invertibility is fulfilled because a + (-a) = 0! Therefore, the set ℤ with the operation of addition qualifies as a group! Since addition is commutative as well, the group is also an Abelian group.

day-modeBookmark
Fields
Fields extend the concept of groups to include another operation. Now, mathematicians end up defining fields with the familiar symbols of ⋅ and +, and they even call them multiplication and addition, but hopefully by now, you can see that in abstract algebra, these are just general terms that can mean anything. So, without further ado, let's define a field.

A field is a set (denoted by S) and two operations (+ and ⋅) that we will notate as {S, +, ⋅}, which follows these rules:

⟨S, +⟩ is an Abelian group with the identity element e = 0.
If you exclude the number 0 from the set S to produce a new set S', then ⟨S', ⋅ ⟩ is an Abelian group with the identity element e = 1.
For the rule of distributivity, let a, b, c ∈ S. Then, a ⋅ (b + c) = a ⋅ b + a ⋅ c.
The set of real numbers ℝ, with the operations of addition and multiplication, is the most obvious example of a field, but there are plenty of others.

Exercise 2
Is the set ℝ, with the operations of subtraction and division {ℝ, −, ÷}, a field?

day-modeBookmark
Vector space
Now that we have covered all of the abstract concepts we need to understand, we can give a formal definition of a vector space, before looking at the implications of these in the following chapters.

A vector space is defined as having the following mathematical objects:

An Abelian group ⟨V,+⟩ with an identity element e. We call members of the set V vectors. We define the identity element to be the zero vector, and we denote this by 0. The operation + is called vector addition.
A field {F, +, ⋅}. We say that V is a vector space over the field F, and we call the members of F scalars.
The Zero Vector Is Not Denoted by |0⟩

It is important to note that we denote the zero vector with a bold zero – 0 – and it is totally different from the vector |0⟩ we defined earlier in the book. This is the convention in quantum computing.

We can define an additional operation as scalar multiplication, which is an operation between a scalar and a vector defined as follows:

Let a scalar s ∈ F and the vector |v⟩ ∈ V. Scalar multiplication is a binary operation, f: F × V → V. The multiplicative identity element of the field F of scalars is 1: |v⟩ ⋅ 1 = 1 ⋅ |v⟩ = |v⟩ .
This new operation – scalar multiplication – must also be compatible or work with addition and multiplication from our field F of scalars in rule two. It also has to be compatible with the operation of the vector addition defined in rule one. More formally, let α, β ∈ F and |u⟩, |v⟩ ∈ V. Or in other words, α and β are scalars and |u⟩ and |v⟩ are vectors:

Scalar multiplication is compatible with field multiplication:


Distributivity of scalar multiplication with respect to vector addition:


Distributivity of scalar multiplication with respect to field addition:


These two mathematical objects – an Abelian group ⟨V, +⟩ of vectors and a field {F, +, ⋅} of scalars along with the operation of scalar multiplication – are all we need to define a vector space! That's it! That wasn't too bad, was it?

Any guesses which field our vector spaces in quantum computing are concerned with? If you answered the field of complex numbers, ℂ, give yourself three extra bonus points! However, for the next few chapters, I will stick to the field of real numbers, ℝ, as this makes it easier to get the concepts across without getting caught up in the extraneous complexities inherent in ℂ. Don't worry, there will be a whole chapter on complex numbers, and the latter half of the book will use this field almost exclusively.

Also, since vectors are the name we give to members of the set V, they can be any mathematical object. In quantum computing, they are n-tuples, but in mathematics and quantum mechanics, they can be anything, including functions, matrices, and polynomials. You do not need to worry about this for quantum computing, but you should know about it, as it will clarify why definitions are given in a generalized way to accommodate all of these possible things being vectors in a vector space.

day-modeBookmark
Summary
In this chapter, we have built a solid foundation that will carry us through the rest of this book. We started with two fundamental mathematical concepts: sets and functions. From there, we defined a binary operation as being a function with two input values from sets. We combined all of these concepts to create groups, fields, and our ultimate goal, vector spaces. In the next chapter, we will look at all the great things we can do with these vectors that live in vector spaces!

day-modeBookmark
Answers to Exercises
Exercise 1
Parts B and D are not functions.

Exercise 2
No, this is not a field. ⟨ℝ, −⟩ is not an Abelian group; subtraction is not commutative.