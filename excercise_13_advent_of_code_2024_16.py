"""
===================
Frontier: [13,1:28.0, 13,9:28.0, 3,7:28.0, 11,8:27.0, 11,7:28.0]
POP 11,8 27.0
  Neigh of 11,8: [('11,7', 1), ('11,9', 1)]
===================
Frontier: [13,1:28.0, 13,9:28.0, 3,7:28.0, 11,7:28.0]
POP 13,1 28.0
Reached destination
Final cost = 28.0
Final Distance: True
"""


from pathlib import Path

from lib.cl_graph_dict import Cl_graph



from lib.fn_graph_distance import graph_distance

def load_maze_from_file(i_s_filename: Path, i_cl_graph: Cl_graph) -> list:
    """
    Load an ASCII maze and convert it into a graph.
    Walkable tiles: 'S', '.', 'E'
    Walls: '#'
    Each walkable tile becomes a node named "r,c".
    Adjacent walkable tiles get a link of cost 1.
    """

    # Read all lines
    ls_lines = i_s_filename.read_text().splitlines()

    n_rows = len(ls_lines)
    n_cols = len(ls_lines[0])

    ln_special : List = list()

    # Helper to check walkability
    def is_walkable(ch: str) -> bool:
        return ch in ("S", ".", "E")

    # First pass: add nodes
    for r in range(n_rows):
        for c in range(n_cols):
            ch = ls_lines[r][c]
            if ch=="S":
                ln_special.append((r,c))
            if ch=="E":
                ln_special.append((r,c))
            if is_walkable(ch):
                node_name = f"{r},{c}"
                i_cl_graph.add_node(node_name)

    # Second pass: add edges between adjacent walkable cells
    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # down, up, right, left

    for r in range(n_rows):
        for c in range(n_cols):
            ch = ls_lines[r][c]
            if not is_walkable(ch):
                continue

            node_a = f"{r},{c}"

            for dr, dc in directions:
                rr = r + dr
                cc = c + dc

                if 0 <= rr < n_rows and 0 <= cc < n_cols:
                    ch2 = ls_lines[rr][cc]
                    if is_walkable(ch2):
                        node_b = f"{rr},{cc}"
                        # undirected link, cost = 1
                        i_cl_graph.add_link_two_way(node_a, node_b, 1)

    return ln_special

def save_maze(i_s_filename: Path, i_cl_graph: Cl_graph ) -> bool:
    """
    Save a graph back into ASCII maze form.
    - i_s_start and i_s_end are node names like "13,1"
    - All nodes in the graph are walkable ('.'), except:
        start -> 'S'
        end   -> 'E'
    - Everything else becomes '#'
    """

    # --- determine maze bounds ---
    ls_nodes = list(i_cl_graph.iter_node())
    coords = []

    for node in ls_nodes:
        r, c = map(int, node.s_label.split(","))
        coords.append((r, c))

    max_r = max(r for r, _ in coords)
    max_c = max(c for _, c in coords)

    # --- initialize maze with walls ---
    maze = [["#" for _ in range(max_c + 1)] for _ in range(max_r + 1)]

    # --- fill walkable cells ---
    for node in ls_nodes:
        r, c = map(int, node.s_label.split(","))
        maze[r][c] = "."

    # --- write to file ---
    with i_s_filename.open("w") as f:
        for row in maze:
            f.write("".join(row) + "\n")

    return True



def dummy_graph( i_cl_graph ):
     # Rail distances (approximate, km)
    i_cl_graph.add_link_two_way("London", "Paris", 450)
    i_cl_graph.add_link_two_way("London", "Brussels", 320)
    i_cl_graph.add_link_two_way("Paris", "Brussels", 300)
    i_cl_graph.add_link_two_way("Brussels", "Amsterdam", 200)
    i_cl_graph.add_link_two_way("Amsterdam", "Berlin", 650)
    i_cl_graph.add_link_two_way("Paris", "Berlin", 1050)
    return False


def test_bench():
    print("shaka")

    cl_graph = Cl_graph()

    lnn_start_end = load_maze_from_file( Path("data","aoc_2024_16.map"), cl_graph )
    #lnn_start_end = load_maze_from_file( Path("data","maze_4x4.map"), cl_graph )

    print(f"Start and End: {lnn_start_end}")

    save_maze(Path("data","excercise13.out"), cl_graph )
   
    cl_graph.show()

    i_s_node_start = f"{lnn_start_end[0][0]},{lnn_start_end[0][1]}"
    i_s_node_end = f"{lnn_start_end[1][0]},{lnn_start_end[1][1]}"

    n_distance = graph_distance( cl_graph, i_s_node_start, i_s_node_end )

    #dijkstra(cl_graph, "London", "Berlin")
    print(f"Final Distance: {n_distance}")


if __name__ == "__main__":
    test_bench()