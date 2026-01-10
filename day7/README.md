# Advent of Code 2021 - Day 7

Problem: https://adventofcode.com/2021/day/7

## Part 1

We are given horizontal positions $ y = (y_1,\ldots, y_n) \in  \mathbb{N}^n$ and are asked to find $ b \in  \mathbb{N} $ such that

$$ f(b) := \sum \limits_{i \: = \:1}^{n} \; \lvert b-y_{i}\rvert = \left\| \textbf{1}b-y \right\|_1 \rightarrow min $$

Since 

$$ f^{\prime}(b) = \sum \limits_{i \: = \:1}^{n} \;  \mathrm{sgn}(b-y_{i}) \stackrel{!}{=} 0  $$


we need the same number of positive and negative terms among the $\mathrm{sgn}(b-y_{i})$, which means $b$ should be the [median](https://en.wikipedia.org/wiki/Median) of $y_i$.
The answer then is $f(y_{median})$


## Part 2

The loss function now reads 

$$ f(b) := \sum \limits_{i \: = \:1}^{n} \sum \limits_{k \: = \:1}^{\lvert b-y_{i}\rvert} \; k =
    \sum \limits_{i \: = \:1}^{n} \frac{\lvert b-y_{i}\rvert \left( \lvert b-y_{i}\rvert + 1 \right) }{2} =
    \sum \limits_{i \: = \:1}^{n} \frac{\left( b-y_i \right)^2 + \lvert b-y_{i}\rvert }{2} =
    \frac{1}{2} \left( \left\| \textbf{1}b-y \right\|^2_2 + \left\| \textbf{1}b-y \right\|_1 \right) \rightarrow min
$$

With

$$ b \in \mathbb{N} \land y_i \in  \mathbb{N} \implies \lvert b-y_i\rvert \notin \left( 0,1 \right) \implies  \lvert b-y_i\rvert \leq \left( b-y_i \right)^2 $$

we find upper and lower bounds for $f$:

$$
\frac{1}{2} \sum \limits_{i \: = \:1}^{n} \left( b-y_i \right)^2 \leq
\sum \limits_{i \: = \:1}^{n} \frac{\left( b-y_i \right)^2 + \lvert b-y_{i}\rvert }{2} \leq
 \sum \limits_{i \: = \:1}^{n} \left( b-y_i \right)^2

$$

Minimizing $ \sum \limits_{i \: = \:1}^{n} \left( b-y_i \right)^2 $ yields the [mean value](https://en.wikipedia.org/wiki/Least_squares) of $y_i$, which is 
$ \overline{y} = \frac{1}{n} \sum \limits_{i \: = \:1}^{n} y_i $ and we get

$$

\frac{1}{2} \overline{y} \leq b \leq \overline{y}

$$

The quadratic term in $f$ is dominating, so we expect $ b \approx \overline{y} $. Remember to round accordingly.

## Alternative

Since $ f^{\prime}(y_{min}) < 0 , f^{\prime}(y_{max}) > 0 $ one can find the root with bisection.
$f$ is convex and (convex) optimization can be applied.