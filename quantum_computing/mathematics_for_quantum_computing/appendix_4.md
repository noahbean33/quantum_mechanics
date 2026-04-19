Appendix 4: Probability
The study of gambling, specifically the throwing of dice, led to the mathematical field of probability. Probability is the study of how likely an event is to occur given a number of possible outcomes. A real number between 0 and 1 is assigned to each event where 0 signifies the event has no chance of happening and 1 signifies the event will always happen. You can also multiply these numbers by 100 to get a percentage that the event will happen. All the probabilities for all possible outcomes must sum to 1. For instance, the probability of a coin flip landing on heads is 0.5 or 50%. For tails, it is also 0.5 or 50%. Both of these numbers add up to 1. From these basics, this chapter will go over the probability needed in the study of quantum computing.

In this chapter, we are going to cover the following main topics:

Definitions
Random variables
day-modeBookmark
Definitions
Let's start by getting some basic definitions out of the way. The word experiment is used in probability theory to denote the execution of a procedure that produces a random outcome. Examples of experiments are flipping a coin or rolling dice. In quantum computing, an experiment is measuring a qubit.

A sample space is the set of all possible outcomes of an experiment. It is usually denoted by Ω (the upper case Greek letter omega). The set Ω for a fair coin is {Heads, Tails}. The set Ω for one die is {1, 2, 3, 4, 5, 6}. The set Ω for a qubit when measured in the Z basis is {|0⟩, |1⟩}.

An event (E) is a subset of Ω. Every outcome is a subset of size 1 – for example, {Heads} and {Tails} are events for a fair coin. But as we saw in Chapter 3, Foundations, subsets also include the empty set ∅ and the whole set itself, which is Ω in this case. The set of all events is called an event space and is usually denoted with a ℱ. Here is the event space for a fair coin:

∅
{Heads}
{Tails}
{Heads, Tails} = Ω
Because of the definition of an event, you can also group outcomes together. For instance, {1 ,2, 3} is the event that a die is 3 or below after a roll (aka experiment).

Finally, there is a probability function (P) that maps each event to a real number between 0 and 1:


The probability function has these properties:


Here is an example for a flip of a coin using these definitions, where H stands for Heads and T stands for Tails:


Let's move on to to see how we can analyze these events further.

day-modeBookmark
Random variables
An important concept in probability is a random variable. Oftentimes, we are not interested in the actual outcome of an experiment but some function of the outcome. For instance, let's define the function S to be the number of tails when flipping two coins. We know that Ω is {(H,H), (H,T), (T,H), (T,T)} where H stands for heads and T stands for tails. We also know that the probability of each of these outcomes is 1/4th. However, I want to know the amount of tails in my outcomes, which I define as this:


If I define S to be a random variable, then:


In general, random variables are written with capital letters such as X, Y, and Z. Random variables are functions from the sample space Ω to a measurable space, which is not a trivial thing. Fortunately for us, for most of our random variables, the measurable space will be the real numbers.

Discrete random variables
There are continuous and discrete random variables. Most random variables in quantum computing are discrete, and hence, we will only deal with this type. Discrete random variables have distinct values, and their sample spaces are finite or countably infinite. Instead of writing P(X = z) all the time, we define a new function called the Probability Mass Function (PMF) this way:



Two properties of the PMF are:


Histograms are often used to show the PMF graphically for a random variable. Here is a nice histogram showing the PMF for a random variable S, defined as the sum of two dice being rolled:

Figure 13.1 – The PMF of S, the sum of two dice rolled
Figure 13.1 – The PMF of S, the sum of two dice rolled

Let's look at how we can describe our random variables.

The measures of a random variable
There are a few measures that are important to know for random variables. The first is the expected value of a random variable denoted as E[X] where X is the random variable. Let's start with an example first and look at the roll of a single die. The expected value takes each possible outcome and multiplies it by the PMF for that value. So, if we let X represent the value of the outcome of a die roll, then the expected value will be:


You should note that the expected value is not actually a possible value of the PMF. This will often be true. Intuitively, this should also look like the average or mean, and it is if all outcomes have the same PMF value. Let's define this mathematically. The expected value for a random variable X is defined as:


The other important measure of a random variable is its variance, which measures the spread of possible PMF values. It is defined as:



Let's calculate the variance for our roll of one die example. We already know the expected value of X, but we also need the expected value of X2. Here's the calculation:


Now, we can calculate the variance of our roll of one die:


The last measure to consider is called the standard deviation of a random variable, and it is quite easy once you have the variance. It is just the square root of the variance.

And there you go – you now know the three most important measures of a random variable: the expected value, the variance, and the standard deviation.

day-modeBookmark
Summary
The field of probability is vast, but you now have the necessary tools to understand it as it applies to quantum computing. The foundation for understanding probability is the definitions we went through, and in quantum computing, it all revolves around random variables.

day-modeBookmark
Works cited