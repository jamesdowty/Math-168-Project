import networkx as nx
from import_test import *
import matplotlib.pyplot as plt
import numpy as np

metrolink = TransitSystem("../NYC GTFS")

G = nx.Graph()
positions = {}
label = {}

for stop in metrolink.stops:
    G.add_node(metrolink.stops[stop].stop_id)
    positions.update({stop: np.array([float(metrolink.stops[stop].stop_lon), float(metrolink.stops[stop].stop_lat)])})
    label.update({stop: metrolink.stops[stop].stop_name})

for trip in metrolink.trips:
    for i in range(1, len(metrolink.trips[trip].sequence)):
        travel_time = 0
        from_time = metrolink.trips[trip].sequence[i-1].departure_time.split(':')
        to_time = metrolink.trips[trip].sequence[i].arrival_time.split(':')
        travel_time += (int(to_time[0]) - int(from_time[0]))*60
        travel_time += (int(to_time[1]) - int(from_time[1]))
        travel_time += (int(to_time[2]) - int(from_time[2]))/60
        G.add_edge(metrolink.trips[trip].sequence[i-1].stop_id, metrolink.trips[trip].sequence[i].stop_id, weight=travel_time)
edge_weights = nx.get_edge_attributes(G, 'weight')

component_count = 0
total_time = 0
total_pairs=0

for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
    total_time += nx.average_shortest_path_length(C, weight='weight')*C.number_of_nodes()*(C.number_of_nodes()-1)
    component_count += 1
    total_pairs += C.number_of_nodes()*(C.number_of_nodes()-1)
average_shortest_path = total_time/total_pairs

print(average_shortest_path)
print(component_count)
nx.draw_networkx(G, pos=positions, labels=label, font_size=6)
nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_weights, font_size=6)
plt.show()
