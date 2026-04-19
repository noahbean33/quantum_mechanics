Chapter 4: Vector Spaces
The entire last chapter led up to defining vector spaces. Now we will see how some vector spaces can be subsumed by other vector spaces. We'll revisit linear combinations to talk about linear independence. We will also learn new ways to define vector spaces with just a small set of vectors. Finally, while we used the word dimension previously to describe a vector space, we will attain a mathematical definition for it in this chapter.

In this chapter, we are going to cover the following main topics:

Subspaces
Linear independence
Span
Basis
Dimension
day-modeBookmark
Subspaces
Let's say you have a set, U, of vectors and it is a subset of a set, V, of vectors (U ⊆ V). This situation is shown in the following diagram:

Figure 4.1 – The set U as a subset of V
Figure 4.1 – The set U as a subset of V

Is it possible that U is a subspace of V? Well, yes. It has met the first condition for subspaces, namely, that the potential subspace has to be a subset of the bigger vector space's set of vectors. What's next? Well, U also has to be a vector space using the same field as the vector space V. This seems like it might be an exhaustive thing to do, but it has been proven that we only need to check for three small conditions to make sure U is a subspace of V, and two of them have to do with the closure property from Chapter 3, Foundations. As a reminder, here it is:

Closure: For every a,b ∈ A, a ֎ b produces an element, c, that is also in the set A. f: A × A → A
Armed with the concept of a subset and closure, we can now define a subspace.

Definition
For a subset, U, of a vector space, V, with an associated field, F, of scalars, U is a subspace if:

The 0 vector is included in the subset U. (0 ϵ U).
The subset U is closed for vector addition. If |u⟩ and |v⟩ ϵ U, then |u⟩ + |v⟩ ϵ U.
The subset U is closed for scalar multiplication. If |u⟩ ϵ U and s is a scalar, then s|u⟩ ϵ U.
We are basically trying to ensure that the following situation doesn't occur:


Figure 4.2 – Ensuring closure for a potential subspace
Figure 4.2 – Ensuring closure for a potential subspace

Alright, enough with formality! Let's look at concrete examples!

Examples
Let's use two-dimensional real space, ℝ2, as our overall vector space to keep things easy. As you know, ℝ2 is the complete Cartesian coordinate system. What if we picked a line on that X-Y plane to possibly be a subspace, shown as follows:


Figure 4.3 – The graph of y = x
Figure 4.3 – The graph of y = x

As you can see, we picked the line y = x. Let's call every vector on that line (for example, (1,1), (2,2), (-3, -3)) the set, W, of vectors. Let's represent the set in our set builder notation from Chapter 3, Foundations:



Equivalently, we could write:



Using our graph, we can see that our set, W, contains a subset of ℝ2 but is not equal to ℝ2 since vectors such as (1,3) and (2,3) are not in our set. Now, let's check whether W is a subspace of ℝ2.

The 0 vector is included in the subset U. (0 ϵ U).
Check! The 0 vector in ℝ2 is (0,0), and that meets the condition of our subset that the coordinates equal one another; so we're good here!

The subset U is closed for vector addition. If |u⟩ and |v⟩ ϵ U, then |u⟩ + |v⟩ ϵ U.
Hmmm, we'll have to work this one out:



It should be obvious that



so we're all good and we can check this condition off the list.

The subset U is closed for scalar multiplication. If |u⟩ ϵ U and s is a scalar, then s|u⟩ ϵ U. Alright, let's work this one out too:


Again, it should be obvious that



so, baa-ding! Check again!

So, all three conditions were true, and therefore W is a subspace of ℝ2.

Let's try another line on the X-Y plane like the one in the following diagram:

Figure 4.4 – The graph of y = x + 1
Figure 4.4 – The graph of y = x + 1

So, what do you think; is this one a subspace of ℝ2? I can tell you right now, the answer is no. It fails the very first condition: it does not contain the zero vector. Alrighty, now it's your turn.

Exercise 1
Test the following subsets of ℝ2 and determine which ones are subspaces and which are not. Assume all variables are real numbers.




day-modeBookmark
Linear independence
So, it ends up that these vectors got together and wrote a declaration of independence and that's what we'll cover here. Just joking! We do need humor every so often in a math book. To explain linear independence, we need to go back to the concept of a linear combination that we introduced earlier in this book.

Linear combination
We learned in Chapter 2, Superposition with Euclid, that linear combinations are the scaling and addition of vectors. I would like to give a more precise definition as we go beyond three-dimensional space.

A linear combination for vectors |x1⟩,|x2⟩, … |xn⟩ and scalars c1, c2, … cn in a vector space, V, is a vector of the form:

 (1)

Basically, it is still scaling and addition, but now we can do it for vectors of any dimension and with as many finite numbers of vectors as we wish.

Let's look at an example:



So now that we have defined linear combinations, let's look at the antonym of linear independence – linear dependence.

Linear dependence
If you have a set of vectors and you can create a linear combination of one of the vectors from a subset of the other vectors, then all of those vectors are linearly dependent. Let's look at some examples.

The following vectors are linearly dependent:



This is because we can create |f⟩ from a linear combination of |d⟩ and |e⟩ using the scalars 3 and 2, as shown here:



Are |0⟩ and |1⟩ linearly dependent? No, because there are no scalars that you can multiply |0⟩ by to get |1⟩ and vice-versa. You should quickly verify this.

How about these vectors?



These are not linearly dependent as there are no scalars that you can use to create one out of a subset of all three. Now, you might rightly ask, how do you know? That is a very good question and there are whole branches of computational linear algebra dedicated to just this problem. The short answer is that there are several methods, some easier than others. However, I'm going to give you a pass. The methods are not needed for quantum computing, just the concept. You can use a very nice calculator to do the computation for you, such as Wolfram Alpha (https://www.wolframalpha.com/). Here is a screenshot from there asking about those three vectors we just defined:

Figure 4.5 – Screenshot from Wolfram Alpha
Figure 4.5 – Screenshot from Wolfram Alpha

If you read the screenshot carefully, it gives you a hint to this next part. A set of vectors is either linearly dependent or linearly independent! They cannot be both and they have to be one or the other. In fact, that is how we will define linear independence:

A set of vectors is linearly independent if they are not linearly dependent.

So, there you have it, you now know what linear independence is. Be sure not to forget this concept as it will be important later on.

day-modeBookmark
Span
In the section on subspaces, we used set builder notation to define possible candidates for subspaces. There is a better way to do this, however, using something called the span. The span uses a set of distinct, indexed vectors to generate a vector space. How does it do this? It uses every possible linear combination of the set of vectors. As you hopefully see by now, linear combinations are at the heart of linear algebra.

So, let's start with a set, S, of vectors with just one vector, like the following:



Let's look at our one vector graphically:

Figure 4.6 – Graph of the one vector in S
Figure 4.6 – Graph of the one vector in S

Okay, what would be its span? Or, in other words, what are all the vectors that are linear combinations of this one vector? Well, we can't add because all we have is one vector. So all we can do is scale this vector. If we scale it for all real numbers, it becomes a ….. line! We would say that S spans the space, or span(S) generates the space. So, our subspace would look like the following:


Figure 4.7 – Graph of the span of S
Figure 4.7 – Graph of the span of S

Hopefully, this line looks familiar, it is the line y = x from the previous section. So, we have just created a subspace of ℝ2 with one vector using the span operator.

Let's add a vector and see whether we can generate a more interesting subspace:



Let's look at these vectors graphically:


Figure 4.8 – Graph of the two vectors in set T
Figure 4.8 – Graph of the two vectors in set T

As you can see, they lie on the same line. Now, the big question is, what are all their linear combinations? The answer ends up being disappointing. Yes, we do have another vector to add now, but since the two vectors are linearly dependent, it buys us nothing. All their linear combinations end up being the same line we had before, y = x. So, span(S) = span(T).

To really get something, we need to add vectors that are linearly independent to the vectors already in our spanning set. Let's go ahead and do that:



The third vector is not a linear combination of the first two. Let's draw them on a graph:


Figure 4.9 – Graph of the three vectors in set U
Figure 4.9 – Graph of the three vectors in set U

Alright, now we can do something! What are all the linear combinations of the three vectors in our set U? I've drawn a few as follows:


Figure 4.10 – Graph of the linear combinations of vectors in the set U
Figure 4.10 – Graph of the linear combinations of vectors in the set U

If we continued to draw all the vectors that are linear combinations of the set U, we would end up filling the entire vector space of ℝ2! That's right; we just defined ℝ2 with only three vectors:



Can we find a set with fewer vectors that spans ℝ2? It just so happens that we can! The following set will do the job:



This set of vectors is linearly independent. This condition of linear independence for a spanning set ends up being so important that we give spanning sets of linearly independent vectors a special name – a basis.

day-modeBookmark
Basis
The word basis is used often in English speech and its colloquial definition is actually a good way to look at the word basis in linear algebra:

Basis, ba·sis \ ˈbā-səs \ plural bases\ ˈbā-ˌsēz \ Noun

Something on which something else is established or based. Example 1: Stories with little basis in reality. Example 2: No legal basis for a new trial.

The reason for this is that you can choose different bases for a vector space. While the vector space itself does not change when you choose a different basis, the way things are described with numbers does.

Let's look at an example in ℝ2. Consider the vector |u⟩, given as follows:

Figure 4.11 – Graph of the vector |u⟩ 
Figure 4.11 – Graph of the vector |u⟩

Clearly, its coordinates are (3,3). What if I told you I could describe the same vector with the coordinates (3,0)? Wait a minute; that should disturb you. We never talk about the basis in most math classes because we implicitly use the standard basis. What is the standard basis, you may ask? It is the set of vectors whose components are all zeros, except one component that has the number one. For ℝ2, they are:



You will notice that these vectors are our familiar zero- and one-state vectors. This is no accident. In quantum computing, we call the standard basis the computational basis, and that is the term we will use in this book.

Okay, now remember when I said you could write any vector as a linear combination of a spanning set? Well, since a basis is a spanning set, this is true for a basis as well. But what's special about a basis is that there is a unique linear combination to describe each vector and the scalars used in this unique linear combination are called coordinates.

Let's look at this for our example vector |u⟩. The unique linear combination to describe |u⟩ using the standard basis is:



I purposely named the scalars x and y because they correspond to the x and y coordinates according to the computational basis.

Now, I am going to describe ℝ2 with a different basis, F, shown as follows:



Let's look at |f1⟩ and |f2⟩ on our standard coordinate system:

Figure 4.12 – Graph of the vectors in set F
Figure 4.12 – Graph of the vectors in set F

This basis is just as valid as the computational basis from before because every vector in ℝ2 can be uniquely defined by a linear combination of these two vectors. So, the next question is: What is the linear combination that describes |u⟩? You can probably make out geometrically what the unique linear combination is that describes |u⟩, but let's write it out algebraically as well:



So, the scalars for this linear combination are (3,0) and these are the coordinates of |u⟩ according to our basis, F. Let's look at |u⟩ in our new coordinate system:

Figure 4.13 – Graph of |u⟩ in the F basis
Figure 4.13 – Graph of |u⟩ in the F basis

Notice that |u⟩ is still the same vector according to our very first definition of a vector as being a line segment with a length and direction. But with a new basis, we just use different coordinates to describe it. As Shakespeare wrote in Romeo and Juliet:

What's in a name? That which we call a rose

By any other name would smell as sweet;

Or, in other words:

What's in coordinates? That which we call a vector

By any other coordinates would still be the same vector;

So, I have now shown you how I can describe the same vector with different components or coordinates. To denote the basis we are writing a vector in, we use a subscript like so, where C denotes the computational basis:



If no basis is given, then we assume we are using the computational basis. It should be noted that the basis has to be indexed and ordered so that our coordinates do not get mixed up (for example, (0,3) does not equal (3,0) in the computational basis).

I know all of this may be a little confusing, but I need to blow your mind a little to prepare you for what lies ahead. In the next chapter, I will show you how to use matrices to travel between bases easily.

day-modeBookmark
Dimension
The dimension of a vector space ends up being very easy to define once you know what a basis is. One thing we didn't talk about in our previous section is that the basis is the minimum set of vectors needed to span a space, and that the number of vectors in a basis for a particular vector space is always the same.

From this, we define the dimension of a vector space to be equal to the number of vectors it takes as a basis to describe a vector space. Equivalently, we could say that it is the number of coordinates it takes to describe a vector in the vector space. It follows that the dimension of ℝ2 is two, ℝ3 is three, and ℝn is n.

day-modeBookmark
Summary
We have covered a bit of ground around describing vector spaces in this chapter. We've seen how a vector space has subspaces and how to test whether a set of vectors is a subspace. We've rigorously defined linear combinations and derived the concept of linear independence from it. We've also learned multiple ways to describe a vector space through the span and basis. From this, we've learned the true meaning of coordinates and put all that together to define the dimension of a vector space. In the next chapter, we will look at how to transform vectors in these vector spaces using matrices!