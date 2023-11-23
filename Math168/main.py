import csv

# A class to hold each stop in the transit system class
class Stop:
    def __init__(self, stop_id, stop_name, stop_lat, stop_lon, zone_id, stop_url, to_from, stop_alias):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.zone_id = zone_id
        self.stop_url = stop_url
        self.to_from = to_from
        self.stop_alias = stop_alias

# A class to hold all the information for a transit system
class transitSystem:
    stops = [] # Array for all stops in system

    def __init__(self, folderPath): # Need to specify a folder path containing GTFS files
        with open(folderPath + "/stops.txt") as stops_file:
            reader = csv.reader(stops_file)
            for row in reader:
                self.stops.append(Stop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]));
            stops_file.close()
            self.stops.pop() # First element is headings



metrolink = transitSystem("../Metrolink GTFS")