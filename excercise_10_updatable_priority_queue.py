from lib.cl_priority_binary_tree import Cl_priority_binary_tree


# ============================================================
# TEST BENCH: Nuclear Power Plant Event Queue
# ============================================================

def test_bench():
    cl_queue = Cl_priority_binary_tree()

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
    cl_queue.pop_highest()
    cl_queue.show_tree()

    cl_queue.pop_highest()
    cl_queue.show_tree()

    cl_queue.pop_highest()
    cl_queue.show_tree()

    print("\n=== FINAL STATS ===")
    cl_queue.show_stats()


if __name__ == "__main__":
    test_bench()
