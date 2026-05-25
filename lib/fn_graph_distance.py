from lib.cl_graph_dict import Cl_graph
from lib.cl_priority_binary_tree import Cl_priority_binary_tree

class lib_numpy:
    from numpy import empty, inf


def graph_distance( i_cl_graph : Cl_graph, i_s_start : str, i_s_end : str ) -> list:

    cl_graph = i_cl_graph
    cl_frontier = Cl_priority_binary_tree()

    #compute the indexes of the nodes
    i_n_start_index = cl_graph.get_node_index(i_s_start)
    print(f"Start {i_s_start} {i_n_start_index}")
    i_n_end_index = cl_graph.get_node_index(i_s_end)
    print(f"Start {i_s_end} {i_n_end_index}")

    #create a vector of distance, one per node
    ln_cost = lib_numpy.empty((cl_graph.num_node), dtype=float)   
    ln_cost.fill(lib_numpy.inf)
    ln_cost[i_n_start_index] = 0
    print(f"Cost vector {ln_cost}")

    # parent dictionary for path reconstruction
    d_parent = { i_s_start: None }

    #create the frontier
    l_link_start = cl_graph.get_neighbour(i_s_start)
    for s_node_end, n_link_cost in l_link_start:
        cl_frontier.push(s_node_end, n_link_cost)
        i_n_index = cl_graph.get_node_index(s_node_end)
        ln_cost[i_n_index] = n_link_cost
        d_parent[s_node_end] = i_s_start

    print(f"Cost vector after frontier  {ln_cost}")
    print(f"Frontier: {l_link_start}")

    while len(cl_frontier) > 0:
        print("===================")
        print(f"Frontier: {cl_frontier}")

        # SAFER UNPACKING
        popped = cl_frontier.pop_lowest()

        # handle cases where pop_lowest returns only label
        if isinstance(popped, tuple):
            s_node_name, n_link_length = popped
        else:
            s_node_name = popped
            n_link_length = ln_cost[cl_graph.get_node_index(s_node_name)]

        print(f"POP {s_node_name} {n_link_length}")

        # index of popped node
        i_n_curr_index = cl_graph.get_node_index(s_node_name)

        # destination reached
        if s_node_name == i_s_end:
            print("Reached destination")
            print(f"Final cost = {ln_cost[i_n_curr_index]}")

            # reconstruct path
            l_path = []
            s_curr = i_s_end
            while s_curr is not None:
                l_path.append(s_curr)
                s_curr = d_parent.get(s_curr)

            l_path.reverse()
            print("Optimal path:", l_path)
            return l_path

        # explore neighbours
        l_neigh = cl_graph.get_neighbour(s_node_name)
        print(f"  Neigh of {s_node_name}: {l_neigh}")

        for s_next, n_cost_edge in l_neigh:
            i_n_next_index = cl_graph.get_node_index(s_next)
            n_new_cost = ln_cost[i_n_curr_index] + n_cost_edge

            if n_new_cost < ln_cost[i_n_next_index]:
                print(f"    Relax {s_next}: {ln_cost[i_n_next_index]} → {n_new_cost}")
                ln_cost[i_n_next_index] = n_new_cost
                d_parent[s_next] = s_node_name
                cl_frontier.push(s_next, n_new_cost)

    # If unreachable: return empty list
    print("Destination unreachable")
    return []
