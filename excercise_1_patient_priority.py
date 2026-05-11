
"""
patient come

patient have a priority

with same priority arrival order

use dataclass

heapq has partial ordering
insterting has cost log(n)
it's a way to sort arrays with n logn

"""

from dataclasses import dataclass
from datetime import datetime

from heapq import heapify, heappop

@dataclass
class St_patient:
    priority: int
    timestamp: datetime
    name: str

    def __init__(self, priority: int, timestamp: datetime, name: str):
        self.priority = priority
        self.timestamp = timestamp
        self.name = name

    # heapq will use this
    def __lt__(self, other):
        # Lower priority value = higher priority in the heap
        if self.priority != other.priority:
            return self.priority < other.priority
        
        # If priorities tie, earlier timestamp wins
        return self.timestamp < other.timestamp


# -------------------------
# Test bench
# -------------------------

def test_bench_patients():
    lst_patients = list()
    lst_patients.append(
        St_patient(1, datetime(2024, 5, 1, 9, 30), "Alice")
    )
    lst_patients.append(
        St_patient(3, datetime(2024, 5, 1, 9, 45), "Bob")
    )
    lst_patients.append(
        St_patient(2, datetime(2024, 5, 1, 9, 50), "Charlie")
    )
    lst_patients.append(
        St_patient(5, datetime(2024, 5, 1, 10, 10), "Diana")
    )
    lst_patients.append(
        St_patient(4, datetime(2024, 5, 1, 10, 20), "Ethan")
    )

    print(lst_patients)
    return lst_patients




# -------------------------
# Test bench using system timestamps
# -------------------------

def test_bench_patients_now():
    lst_patients = list()
    lst_patients.append( St_patient(1, datetime.now(), "Poo") ) 
    lst_patients.append(
        St_patient(3, datetime.now(), "Foo")
    )
    lst_patients.append(
        St_patient(2, datetime.now(), "Bee")
    )
    lst_patients.append(
        St_patient(2, datetime.now(), "Rii")
    )
    lst_patients.append(
        St_patient(2, datetime.now(), "Naa")
    )

    
    return lst_patients



if __name__ == "__main__":
    test_bench_patients()


if __name__ == "__main__":
    #test_bench_patients()
    
    lst_patients = test_bench_patients_now()
    
    print("============================")
    print("RAW")
    print(lst_patients)
    
    #this does not sort the list, it just rearranges it to satisfy the heap property

    heapify(lst_patients)
    print("============================")
    print("HEAPQ")
    print(lst_patients)

    #this will pop the patients in order of priority and timestamp

    print("ORDERED POPS")
    while lst_patients:
        print(heappop(lst_patients))