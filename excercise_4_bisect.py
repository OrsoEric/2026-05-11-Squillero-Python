import bisect

import bisect

class Cl_bisect_median:
    def __init__(self):
        # Always-sorted list maintained by bisect.insort
        self.data = []

    def add(self, value):
        # Insert while keeping the list sorted
        bisect.insort(self.data, value)

    def median(self):
        n = len(self.data)
        if n == 0:
            return None, [], []  # median, left, right

        mid = n // 2

        # Odd count → single middle element
        if n % 2 == 1:
            med = self.data[mid]
            left = len(self.data[:mid])
            right = len(self.data[mid+1:])
            return med, left, right

        # Even count → average of two middle elements
        med = (self.data[mid - 1] + self.data[mid]) / 2
        left = len(self.data[:mid])
        right = len(self.data[mid:])
        return med, left, right



if __name__ == "__main__":

    ln_test = [5, 1, 9, 3, 7]
    
    #ln_test = [2,1,1,1,1,1,1,1,1,1]


    # --- Example usage ---
    cl_bisect_median = Cl_bisect_median()

    for x in ln_test:
        cl_bisect_median.add(x)
        print(f"Added {x}, median now: {cl_bisect_median.median()}")


    median, left, right = cl_bisect_median.median()
    print("median:", median)
    print("left:", left)
    print("right:", right)