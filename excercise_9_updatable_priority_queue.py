"""
make me an updatable priority queue class Cl_updatable_priority_queue implemented as a binary tree max heap, using an array as underlying data structure

elements are a s_value, n_priority pair

n_priority is what the queue is sorted for,

it has push( i_s_value, i_n_priority) that inserts an element of given value with a given priority

pop(i_n_value)removes the element of given value 

update() forces the structure to update and make the priority sorted

make me a test bench __main__ with events opf a nuclear power plant

core_meltdown high priority

control_rod_up and control_rod down medium priority

turn_on_light low priority


"""


class Cl_updatable_priority_queue_llm:
    """
    Max-heap priority queue with lazy updates.

    Elements are stored as:
        (s_value, n_priority)

    Higher n_priority means higher priority.
    """

    def __init__(self):
        self.a_heap = []
        self.d_index = {}  # maps s_value -> index in heap

    # =========================================================
    # Internal helpers
    # =========================================================

    def _swap(self, i, j):
        self.a_heap[i], self.a_heap[j] = self.a_heap[j], self.a_heap[i]

        s_val_i = self.a_heap[i][0]
        s_val_j = self.a_heap[j][0]

        self.d_index[s_val_i] = i
        self.d_index[s_val_j] = j

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.a_heap[index][1] > self.a_heap[parent][1]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _heapify_down(self, index):
        size = len(self.a_heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if (
                left < size
                and self.a_heap[left][1] > self.a_heap[largest][1]
            ):
                largest = left

            if (
                right < size
                and self.a_heap[right][1] > self.a_heap[largest][1]
            ):
                largest = right

            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break

    # =========================================================
    # Public API
    # =========================================================

    def push(self, i_s_value, i_n_priority):
        """
        Insert or update an element.
        """

        if i_s_value in self.d_index:
            # Update existing priority
            index = self.d_index[i_s_value]
            old_priority = self.a_heap[index][1]

            self.a_heap[index] = (i_s_value, i_n_priority)

            if i_n_priority > old_priority:
                self._heapify_up(index)
            else:
                self._heapify_down(index)

            return

        self.a_heap.append((i_s_value, i_n_priority))

        index = len(self.a_heap) - 1
        self.d_index[i_s_value] = index

        self._heapify_up(index)

    def pop(self, i_s_value):
        """
        Remove the element with given value.
        """

        if i_s_value not in self.d_index:
            return False

        index = self.d_index[i_s_value]
        last_index = len(self.a_heap) - 1

        # Swap with last
        self._swap(index, last_index)

        removed = self.a_heap.pop()
        del self.d_index[removed[0]]

        # Restore heap if not removing last element
        if index < len(self.a_heap):
            self._heapify_down(index)
            self._heapify_up(index)

        return True

    def update(self):
        """
        Rebuild heap from scratch.
        Useful if priorities were externally modified.
        """

        for i in reversed(range(len(self.a_heap) // 2)):
            self._heapify_down(i)

    def peek(self):
        """
        Return highest-priority element without removing it.
        """

        if not self.a_heap:
            return None

        return self.a_heap[0]

    def pop_max(self):
        """
        Remove and return highest-priority element.
        """

        if not self.a_heap:
            return None

        top_value = self.a_heap[0][0]
        top_item = self.a_heap[0]

        self.pop(top_value)

        return top_item

    def is_empty(self):
        return len(self.a_heap) == 0

    def __len__(self):
        return len(self.a_heap)

    def __str__(self):
        return str(self.a_heap)

    def display_array(self):
        print("\n=== Heap Array View ===")
        print(f"{'Index':<6} {'Item':<20} {'Priority':<10}")
        print("-" * 45)

        for i, (item, prio) in enumerate(self.a_heap):
            print(f"{i:<6} {item:<20} {prio:<10}")

    def display_tree(self):
        print("\n=== Heap Tree View ===")

        if not self.a_heap:
            print("<empty>")
            return

        level = 0
        i = 0
        n = len(self.a_heap)

        while i < n:
            level_count = 2 ** level
            line = []

            for _ in range(level_count):
                if i >= n:
                    break
                item, prio = self.a_heap[i]
                line.append(f"({item},{prio})")
                i += 1

            indent = " " * (2 ** (max(0, 4 - level)))
            print(indent + "   ".join(line))
            level += 1





# =============================================================
# Test Bench
# =============================================================

if __name__ == "__main__":

    print("=== Nuclear Power Plant Event Queue ===")

    cl_queue = Cl_updatable_priority_queue_llm()

    # Low priority
    cl_queue.push("turn_on_light", 10)
    cl_queue.display_array()


    # Medium priority
    cl_queue.push("control_rod_up", 50)
    cl_queue.display_array()

    cl_queue.push("control_rod_down", 50)
    cl_queue.display_array()

    # High priority
    cl_queue.push("core_meltdown", 100)
    cl_queue.display_array()

    print("\nInitial heap:")
    print(cl_queue)

    print("\nProcessing events by priority:\n")

    while not cl_queue.is_empty():
        s_event, n_priority = cl_queue.pop_max()

        print(
            f"EVENT: {s_event:<20} "
            f"PRIORITY: {n_priority}"
        )

    print("\n=== Reinserting events ===")

    cl_queue.push("turn_on_light", 10)
    cl_queue.push("control_rod_up", 50)

    print("\nBefore emergency:")
    print(cl_queue)

    print("\n!!! Reactor instability detected !!!")

    # Escalate event
    cl_queue.push("core_meltdown", 100)

    print("\nAfter emergency insertion:")
    print(cl_queue)

    print("\nTop priority event:")
    print(cl_queue.peek())
