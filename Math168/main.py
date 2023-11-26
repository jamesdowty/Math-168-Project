import csv
import networkx as nx
from import_test import *
import matplotlib.pyplot as plt
import numpy as np

metrolink = transitSystem("../Metrolink GTFS")

G = nx.Graph()
positions = {}
label = {}

for stop in metrolink.stops:
    G.add_node(metrolink.stops[stop].stop_id)
    positions.update({stop: np.array([float(metrolink.stops[stop].stop_lat), float(metrolink.stops[stop].stop_lon)])})
    label.update({stop: metrolink.stops[stop].stop_name})

for trip in metrolink.trips:
    for i in range(1, len(metrolink.trips[trip].sequence)):
        G.add_edge(metrolink.trips[trip].sequence[i-1].stop_id, metrolink.trips[trip].sequence[i].stop_id)

nx.draw_networkx(G, pos=positions, labels=label, font_size=5)
plt.show()

