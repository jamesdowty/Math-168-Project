import networkx as nx
from import_test import *
import matplotlib.pyplot as plt
import numpy as np

metrolink = TransitSystem("../Metrolink GTFS")

# Directed Graph that takes schedule into account
S = nx.DiGraph()  # Graph that takes schedule into account
begin_nodes = []  # Begin with these nodes when doing graph traversal. Format is *stop_id*_begin
end_nodes = []  # These are the target nodes when doing graph traversal. Format is *stop_id*_end
for stop in metrolink.stops:
    S.add_node(metrolink.stops[stop].stop_id + "_begin", id=metrolink.stops[stop].stop_id + "_begin", depart=100000, arrive=100000)
    S.add_node(metrolink.stops[stop].stop_id + "_end", id=metrolink.stops[stop].stop_id + "_end", depart=100000, arrive=100000)
    begin_nodes.append(metrolink.stops[stop].stop_id + "_begin")
    end_nodes.append(metrolink.stops[stop].stop_id + "_end")

tripCounter = 1
for currTrip in metrolink.trips:
    print("Processing trip", tripCounter, "out of", len(metrolink.trips))
    tripCounter += 1
    trip = metrolink.trips[currTrip]
    for i in range(0, len(trip.sequence)):
        newNode = trip.sequence[i].stop_id + "_" + trip.trip_id
        prevNode = (trip.sequence[i - 1].stop_id + "_" + trip.trip_id) if i > 0 else ""
        beginNode = trip.sequence[i].stop_id + "_begin"
        endNode = trip.sequence[i].stop_id + "_end"
        arrival = to_minutes(trip.sequence[i].arrival_time)
        departure = to_minutes(trip.sequence[i].departure_time)
        S.add_node(newNode, arrive=arrival, depart=departure, id=trip.sequence[i].stop_id)
        S.add_edge(beginNode, newNode, time=0)
        S.add_edge(newNode, endNode, time=arrival - departure)
        if i > 0:
            travelTime = departure - S.nodes[prevNode]['depart']
            S.add_edge(prevNode, newNode, time=travelTime)

        possibleTransfers = [x for x, y in S.nodes(data=True) if y['id'] == trip.sequence[i].stop_id]
        for stop in possibleTransfers:
            if stop != newNode and S.nodes[stop]['arrive'] < departure:
                S.add_edge(stop, newNode, time=departure - S.nodes[stop]['depart'])

print(nx.shortest_path(S, source='113_begin', target='141_end', weight='time'))
print(nx.shortest_path_length(S, source='113_begin', target='141_end', weight='time'))

"""
print("Drawing graph...")
label = nx.get_node_attributes(S, 'id')
positions = nx.shell_layout(S)
nx.draw_networkx(S, with_labels=True, font_size=6, pos=positions)
edge_weights = nx.get_edge_attributes(S, 'time')
nx.draw_networkx_edge_labels(S, edge_labels=edge_weights, font_size=6, pos=positions)
plt.show()
"""
# Undirected graph (doesn't take schedule into account)
"""
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
"""
