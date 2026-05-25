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


from typing import List, Tuple


class Cl_updatable_priority_queue:
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


# ============================================================
# TEST BENCH: Nuclear Power Plant Event Queue
# ============================================================

def test_bench():
    cl_queue = Cl_updatable_priority_queue()

    print("\n=== INITIAL STATS ===")
    cl_queue.show_stats()

    print(">>> Adding low‑priority event: turn_on_light")
    cl_queue.push("turn_on_light", 10)
    cl_queue.show_tree()

    print(">>> Adding medium‑priority event: control_rod_up")
    cl_queue.push("control_rod_up", 50)
    cl_queue.show_tree()

    print(">>> Adding medium‑priority event: control_rod_down")
    cl_queue.push("control_rod_down", 50)
    cl_queue.show_tree()

    print(">>> Adding HIGH‑priority event: core_meltdown")
    cl_queue.push("core_meltdown", 100)
    cl_queue.show_tree()

    print("\n=== FINAL STATS ===")
    cl_queue.show_stats()

    print("\n=== POPPING EVENTS ===")

    print(">>> Removing low‑priority event: turn_on_light")
    cl_queue.pop("turn_on_light")
    cl_queue.show_tree()

    print(">>> Removing medium‑priority event: control_rod_up")
    cl_queue.pop("control_rod_up")
    cl_queue.show_tree()

    print(">>> Removing HIGH‑priority event: core_meltdown")
    cl_queue.pop("core_meltdown")
    cl_queue.show_tree()

    print("\n=== FINAL STATS ===")
    cl_queue.show_stats()


if __name__ == "__main__":
    test_bench()
