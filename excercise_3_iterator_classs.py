from heapq import heapify, heappop

class Cl_iterator:
    def __init__(self, i_ln_data):
        # make a shallow copy so original list is untouched
        self._heap = list(i_ln_data)
        heapify(self._heap)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._heap:
            raise StopIteration
        return heappop(self._heap)
    

# -------------------------

if __name__ == "__main__":
    
    cl_data = Cl_iterator([5, 1, 9, 3, 7])

    for n_data in cl_data:
        print(n_data)