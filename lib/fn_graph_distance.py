from lib.cl_graph_dict import Cl_graph

from lib.cl_priority_binary_tree import Cl_priority_binary_tree

class lib_numpy:
    from numpy import empty, inf

def graph_distance( i_cl_graph : Cl_graph, i_s_start : str, i_s_end : str ) -> float:

    cl_graph = i_cl_graph

    cl_frontier = Cl_priority_binary_tree()

    #compute the indexes of the nodes
    i_n_start_index = cl_graph.get_node_index(i_s_start)
    print(f"Start {i_s_start} {i_n_start_index}")
    i_n_end_index = cl_graph.get_node_index(i_s_end)
    print(f"Start {i_s_end} {i_n_end_index}")

    #create a vector of distance, one per node
    ln_cost = lib_numpy.empty((cl_graph.num_node), dtype=float)   
    #distance is infinite to all nodes
    ln_cost.fill(lib_numpy.inf)
    #distance to itself is zero
    ln_cost[i_n_start_index] = 0
    print(f"Cost vector {ln_cost}")

    #create the frontier
    l_link_start= cl_graph.get_neighbour(i_s_start)
    for s_node_end, n_link_cost in l_link_start:
        
        #append right
        cl_frontier.push( s_node_end, n_link_cost) 
        #index of the destination of this link
        i_n_index = cl_graph.get_node_index(s_node_end)
        ln_cost[i_n_index] = n_link_cost

    print(f"Cost vector after frontier  {ln_cost}")

    print(f"Frontier: {l_link_start}")

    n_cost = lib_numpy.inf

    while len(cl_frontier) > 0:
        print(f"===================")
        print(f"Frontier: {cl_frontier}")
        s_node_name, n_link_length = cl_frontier.pop_lowest()
        print(f"POP {s_node_name} {n_link_length}")

        # index of popped node
        i_n_curr_index = cl_graph.get_node_index(s_node_name)

        # if this is the destination, we can stop
        if s_node_name == i_s_end:
            n_cost = ln_cost[i_n_curr_index]
            print("Reached destination")
            print(f"Final cost = {n_cost}")
            return True

        # explore neighbours of the popped node
        l_neigh = cl_graph.get_neighbour(s_node_name)
        print(f"  Neigh of {s_node_name}: {l_neigh}")

        for s_next, n_cost_edge in l_neigh:
            i_n_next_index = cl_graph.get_node_index(s_next)

            # new candidate cost
            n_new_cost = ln_cost[i_n_curr_index] + n_cost_edge

            # relax
            if n_new_cost < ln_cost[i_n_next_index]:
                print(f"    Relax {s_next}: {ln_cost[i_n_next_index]} → {n_new_cost}")
                ln_cost[i_n_next_index] = n_new_cost

                # push into frontier
                cl_frontier.push(s_next, n_new_cost)

    return n_cost