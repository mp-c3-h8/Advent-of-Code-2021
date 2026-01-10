# Advent of Code 2021 - Day 8

Problem: https://adventofcode.com/2021/day/8

## Part 2

Define sets as follows

$$
\begin{align*}

D_0 &:=  \left\{a,b,c,e,f,g\right\}  \\
D_1 &:=  \left\{c,f \right\}  \\
D_2 &:=  \left\{a,c,d,e,g \right\}  \\
D_3 &:=  \left\{a,c,d,f,g \right\}  \\
D_4 &:=  \left\{b,c,d,f \right\}  \\
D_5 &:=  \left\{a,b,d,f,g \right\}  \\
D_6 &:=  \left\{a,b,d,e,f,g \right\}  \\
D_7 &:=  \left\{a,c,f \right\}  \\
D_8 &:=  \left\{a,b,c,d,e,f,g \right\}  \\
D_9 &:=  \left\{a,b,c,d,f,g \right\}  \\

\end{align*}
$$

and the intersection of all sets with 5 or 6 elements, respectivly:

$$

I_5 := D_2 \cap D_3 \cap D_5 = \left\{ a,d,g \right\} \\
I_6 := D_0 \cap D_6 \cap D_9 = \left\{ a,b,f,g \right\}

$$

Now we use set operations (on sets with a unique number of elements) to express single elements. One way to do this is

$$
\begin{align*}
\left\{ a \right\} &= D_7 \setminus D_1 \\
\left\{ g \right\} &= I_6 \setminus ( D_3 \cup D_4 ) \\
\left\{ b \right\} &= I_6 \setminus (D_1 \cup \left\{ a,g \right\} ) \\
\left\{ d \right\} &= I_5  \setminus \left\{ a,g \right\} \\
\left\{ f \right\} &= I_6  \setminus \left\{ a,b,g \right\} \\
\left\{ c \right\} &= D_1 \setminus \left\{f \right\} \\
\left\{ e \right\} &= D_8 \setminus \left\{ a,b,c,d,f,g \right\} \\
\end{align*}

$$

Together with a bitmask and mapping we can rewire the cables.