import csv

# A class to hold each stop in the transit system class
class Stop:
    def __init__(self, stop_id, stop_name, stop_lat, stop_lon):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

class Trip:
    def __init__(self, route_id, service_id, trip_id):
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id
        self.sequence = []

class StopTime:
    def __init__(self, trip_id, arrival_time, departure_time, stop_id, stop_sequence):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = int(stop_sequence)

# A class to hold all the information for a transit system
class transitSystem:
    stops = {} # Map for all stops in system
    trips = {} # Map for all trips in system

    def __init__(self, folder_path):  # Need to specify a folder path containing GTFS files
        with open(folder_path + "/stops.txt") as stops_file:
            reader = csv.reader(stops_file)
            for row in reader:
                self.stops.update({row[0]: Stop(row[0], row[1], row[2], row[3])});
            stops_file.close()
            del self.stops["stop_id"]  # First element is headings

        with open(folder_path + "/trips.txt") as trips_file:
            reader = csv.reader(trips_file)
            for row in reader:
                self.trips.update({row[2]: Trip(row[0], row[1], row[2])})
            trips_file.close()
            del self.trips["trip_id"]  # First element is headings

        with open(folder_path + "/stop_times.txt") as stop_times_file:
            reader = csv.reader(stop_times_file)
            for row in reader:
                if row[0] != "trip_id":
                    self.trips[row[0]].sequence.append(StopTime(row[0], row[1], row[2], row[3], row[4]))
            stop_times_file.close()

        for trip in self.trips:
            self.trips[trip].sequence.sort(key=lambda x: x.stop_sequence)