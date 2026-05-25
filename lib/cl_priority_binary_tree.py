"""
Cl_updatable_priority_queue implemented as a binary tree max heap, using an array as underlying data structure

elements are a s_value, n_priority pair

elements are stored into two lists, index in the list is directly associated with a tree element
0 root, 1 root left child, 2 right child, ...

n_priority is what the queue is sorted for,

it has push( i_s_value, i_n_priority) that inserts an element of given value with a given priority

pop(i_n_value)removes the element of given value 

update() forces the structure to update and make the priority sorted

show_tree() will show the tree structure with root and leafs correctly indented

make me a test bench __main__ with events opf a nuclear power plant

core_meltdown high priority

control_rod_up and control_rod down medium priority

turn_on_light low priority
"""

"""
python excercise_10_updatable_priority_queue.py 

=== INITIAL STATS ===
Queue size: 0
Elements:

>>> Adding low‑priority event: turn_on_light

--- TREE ---
> turn_on_light(10)
------------

>>> Adding medium‑priority event: control_rod_up

--- TREE ---
> control_rod_up(50)
    > turn_on_light(10)
------------

>>> Adding medium‑priority event: control_rod_down

--- TREE ---
> control_rod_up(50)
    > turn_on_light(10)
    > control_rod_down(50)
------------

>>> Adding HIGH‑priority event: core_meltdown

--- TREE ---
> core_meltdown(100)
    > control_rod_up(50)
        > turn_on_light(10)
    > control_rod_down(50)
------------


=== FINAL STATS ===
Queue size: 4
Elements:
  core_meltdown: 100
  control_rod_up: 50
  control_rod_down: 50
  turn_on_light: 10


=== POPPING EVENTS ===
>>> Removing low‑priority event: turn_on_light

--- TREE ---
> core_meltdown(100)
    > control_rod_up(50)
    > control_rod_down(50)
------------

>>> Removing medium‑priority event: control_rod_up

--- TREE ---
> core_meltdown(100)
    > control_rod_down(50)
------------

>>> Removing HIGH‑priority event: core_meltdown

--- TREE ---
> control_rod_down(50)
------------


=== FINAL STATS ===
Queue size: 1
Elements:
  control_rod_down: 50
"""


from typing import List, Tuple


class Cl_priority_binary_tree:
    """
    Max‑heap priority queue with updatable priorities.
    Elements stored in two parallel arrays:
    - g_ls_label:   element labels (string)
    - g_ln_priority: priorities (int, higher = more urgent)
    """

    def __init__(self):
        self.g_ls_label: List[str] = []
        self.g_ln_priority: List[int] = []

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _swap(self, i, j):
        self.g_ls_label[i], self.g_ls_label[j] = self.g_ls_label[j], self.g_ls_label[i]
        self.g_ln_priority[i], self.g_ln_priority[j] = self.g_ln_priority[j], self.g_ln_priority[i]

    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.g_ln_priority[idx] > self.g_ln_priority[parent]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _bubble_down(self, idx):
        n = len(self.g_ls_label)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx

            if left < n and self.g_ln_priority[left] > self.g_ln_priority[largest]:
                largest = left
            if right < n and self.g_ln_priority[right] > self.g_ln_priority[largest]:
                largest = right

            if largest != idx:
                self._swap(idx, largest)
                idx = largest
            else:
                break

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def push(self, i_s_value: str, i_n_priority: int):
        """Insert new element."""
        self.g_ls_label.append(i_s_value)
        self.g_ln_priority.append(i_n_priority)
        self._bubble_up(len(self.g_ls_label) - 1)

    def pop(self, i_s_value: str):
        """Remove element by label."""
        if i_s_value not in self.g_ls_label:
            return

        idx = self.g_ls_label.index(i_s_value)
        last = len(self.g_ls_label) - 1

        # swap with last and remove
        self._swap(idx, last)
        self.g_ls_label.pop()
        self.g_ln_priority.pop()

        # restore heap
        if idx < len(self.g_ls_label):
            self._bubble_up(idx)
            self._bubble_down(idx)

    def pop_highest(self):
        """Remove and return the element with the highest priority (the root)."""
        if not self.g_ls_label:
            return None

        # root element
        top_label = self.g_ls_label[0]
        top_priority = self.g_ln_priority[0]

        last = len(self.g_ls_label) - 1

        # move last element to root and remove last
        self._swap(0, last)
        self.g_ls_label.pop()
        self.g_ln_priority.pop()

        # restore heap property
        if self.g_ls_label:
            self._bubble_down(0)

        return top_label, top_priority


    def update(self):
        """Rebuild heap from scratch."""
        n = len(self.g_ls_label)
        for i in reversed(range(n // 2)):
            self._bubble_down(i)

    def show_tree(self):
        """Pretty-print the heap as an indented binary tree."""
        print("\n--- TREE ---")
        self._show_tree_rec(0, 0)
        print("------------\n")

    def _show_tree_rec(self, idx: int, indent: int):
        n = len(self.g_ls_label)
        if idx >= n:
            return

        # current node
        print(" " * indent + f"> {self.g_ls_label[idx]}({self.g_ln_priority[idx]})")

        left = 2 * idx + 1
        right = 2 * idx + 2

        # left child
        if left < n:
            self._show_tree_rec(left, indent + 4)

        # right child
        if right < n:
            self._show_tree_rec(right, indent + 4)


    def show_stats(self):
        print("Queue size:", len(self.g_ls_label))
        print("Elements:")
        for lbl, pr in zip(self.g_ls_label, self.g_ln_priority):
            print(f"  {lbl}: {pr}")
        print()