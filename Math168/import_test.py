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


class TransitSystem:
    stops = {}  # Map for all stops in system
    trips = {}  # Map for all trips in system

    def __init__(self, folder_path):  # Need to specify a folder path containing GTFS files
        with open(folder_path + "/stops.txt") as stops_file:
            reader = csv.reader(stops_file)
            stop_id_index = -1
            stop_name_index = -1
            stop_lat_index = -1
            stop_lon_index = -1
            for i, row in enumerate(reader):
                if i == 0:
                    for n in range(0, len(row)):
                        if row[n] == "stop_id":
                            stop_id_index = n
                        elif row[n] == "stop_name":
                            stop_name_index = n
                        elif row[n] == "stop_lat":
                            stop_lat_index = n
                        elif row[n] == "stop_lon":
                            stop_lon_index = n
                else:
                    self.stops.update({row[stop_id_index]: Stop(row[stop_id_index], row[stop_name_index], row[stop_lat_index], row[stop_lon_index])})
            stops_file.close()

        with open(folder_path + "/trips.txt") as trips_file:
            reader = csv.reader(trips_file)
            route_id_index = -1
            service_id_index = -1
            trip_id_index = -1
            for i, row in enumerate(reader):
                if i == 0:
                    for n in range(0, len(row)):
                        if row[n] == "route_id":
                            route_id_index = n
                        elif row[n] == "service_id":
                            service_id_index = n
                        elif row[n] == "trip_id":
                            trip_id_index = n
                else:
                    self.trips.update({row[trip_id_index]: Trip(row[route_id_index], row[service_id_index], row[trip_id_index])})
            trips_file.close()

        with open(folder_path + "/stop_times.txt") as stop_times_file:
            reader = csv.reader(stop_times_file)
            trip_id_index = -1
            arrival_time_index = -1
            departure_time_index = -1
            stop_id_index = -1
            stop_sequence_index = -1
            for i, row in enumerate(reader):
                if i == 0:
                    for n in range(0, len(row)):
                        if row[n] == "trip_id":
                            trip_id_index = n
                        elif row[n] == "arrival_time":
                            arrival_time_index = n
                        elif row[n] == "departure_time":
                            departure_time_index = n
                        elif row[n] == "stop_id":
                            stop_id_index = n
                        elif row[n] == "stop_sequence":
                            stop_sequence_index = n
                else:
                    self.trips[row[trip_id_index]].sequence.append(StopTime(row[trip_id_index], row[arrival_time_index], row[departure_time_index], row[stop_id_index], row[stop_sequence_index]))
            stop_times_file.close()

        for trip in self.trips:
            self.trips[trip].sequence.sort(key=lambda x: x.stop_sequence)


def to_minutes(time_string):
    minutes = 0
    separate = time_string.split(':')
    minutes += int(separate[0]) * 60
    minutes += int(separate[1])
    minutes += int(separate[2]) / 60
    return minutes
