from heapq import heapify, heappop
import random

# generate 10 random integers from 1 to 1000
ln_data = [random.randint(1, 1000) for _ in range(10)]
print("Original:", ln_data)

# turn list into a heap
heapify(ln_data)

# pop elements in sorted order
ln_sorted = [heappop(ln_data) for _ in range(len(ln_data))]
print("Sorted:", ln_sorted)
