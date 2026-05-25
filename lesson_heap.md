# HEAP

an heap is a tree that is complete

mmeaning children fills up from up to down, from left to right, with two children per leaf

It can be indexed as an array

A

B C

E F G H

Arrat

0 | 1 | 2  ...
A | B | C  ...

## PUSH 

add as last element

bubble up exchange with father until father is smaller

complexity log2

## POP

remove father and replace with largest leaf

#

https://en.wikipedia.org/wiki/Heap_(data_structure)

## MAX HEAP

for any given node C, if P is the parent node of C, then the key (the value) of P is greater than or equal to the key of C.

## MIN HEAP

the key of P is less than or equal to the key of C.[1] The node at the "top" of the heap (with no parents) is called the root node. 

# heapq library

