#inputs = list of starting nodes, list of ending nodes, and directed weighted graph
#loops through all combination of connected nodes [a,b] and finds the avg shortest
#path between a_start and b_end
import networkx as nx

def avg_min_travel_time(start, end, G):
    avgs = {}
    n = G.number_of_nodes()
    nodes = []
    for s in start:
        for e in end:
            nodes.append(s)
            nodes.append(e)
            avgs[[s, e]] = float(-inf)
            if nx.algorithms.has_path(G, s ,e):
                length, path = nx.algorithms.single_source_dijkstra(G, s, e)
                sum_of_paths = 0              
                for l in lengths:
                    sum_of_paths += l
                avg[[s, e]] = (1 / (n * (n-1)))(sum_of_paths)

    return avgs
