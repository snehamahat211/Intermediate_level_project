# imports
import pandas as pd
import requests
import numpy as np
import osmnx as ox
import networkx as nx
import random
from datetime import datetime


# Function to fetch place details from Baato API
def fetch_place_details(search):
    url1 = "https://api.baato.io/api/v1/search"
    params1 = {
        'key': 'bpk.uMsAWg9AUcMHeEq4ygkiyZ49K3KqGUsD6ea5J5WFGyha',
        'q': search,
        'limit': 10
    }
    response = requests.get(url1, params1)
    data = response.json()['data']
    df = pd.DataFrame(data)[['name', 'address', 'type', 'placeId']]
    return df


# Function to get coordinates from placeId
def get_coordinates(placeId):
    url2 = "https://api.baato.io/api/v1/places"
    params2 = {
        "key": "bpk.uMsAWg9AUcMHeEq4ygkiyZ49K3KqGUsD6ea5J5WFGyha",
        "placeId": placeId
    }
    response2 = requests.get(url2, params=params2)
    data2 = response2.json()['data']
    df2 = pd.DataFrame(data2)['centroid']
    destination = df2[0]
    return destination['lat'], destination['lon']


# Function to save data to a CSV file
def save_to_csv(data, filename="places_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


# Function to preprocess data
def preprocess_data(data):
    # Add a timestamp
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert timestamp to time of day, weekday, and season
    timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
    data['time_of_day'] = timestamp.hour
    data['weekday'] = timestamp.weekday()  # Monday=0, Sunday=6
    data['season'] = (timestamp.month % 12 + 3) // 3  # 1=Winter, 2=Spring, 3=Summer, 4=Fall

    # Normalize latitude and longitude (if needed)
    data['lat'] = data['lat'] / 90.0
    data['lon'] = data['lon'] / 180.0

    return data


# Fetch road network
def fetch_road_network(coords, distance=2000, network_type='drive'):
    return ox.graph_from_point(coords, dist=distance, network_type=network_type)


# Find nearest nodes
def find_nearest_nodes(graph, source_coords, dest_coords):
    source_node = ox.distance.nearest_nodes(graph, X=source_coords[1], Y=source_coords[0])
    dest_node = ox.distance.nearest_nodes(graph, X=dest_coords[1], Y=dest_coords[0])
    return source_node, dest_node


# D* class for dynamic path planning
class DStar:
    def __init__(self, graph):
        self.graph = graph
        self.obstacles = []

    def add_obstacle(self, u, v):
        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)
            self.obstacles.append((u, v))
        if self.graph.has_edge(v, u):
            self.graph.remove_edge(v, u)
            self.obstacles.append((v, u))

    def replan(self, source_node, dest_node):
        try:
            return nx.shortest_path(self.graph, source=source_node, target=dest_node, weight='length')
        except nx.NetworkXNoPath:
            print("No path found after obstacle!")
            return []


# Main function
def main():
    places = pd.DataFrame()

    for i in range(2):
        search = input(f"Place {i + 1}? ")
        df = fetch_place_details(search)
        print(df)

        while True:
            try:
                choice = int(input("Make your choice (1-10): "))
                if choice < 1 or choice > len(df):
                    print(f"Please enter a number between 1 and {len(df)}.")
                else:
                    break
            except ValueError:
                print("Invalid input! Please enter a valid number.")

        option = np.int64(df['placeId'][choice - 1])
        option_value = option.item()
        dest_lat, dest_long = get_coordinates(option_value)

        temp_df = pd.DataFrame({'lat': [dest_lat], 'lon': [dest_long]})
        places = pd.concat([places, temp_df], ignore_index=True)

    # Save and preprocess data
    data = {'lat': places['lat'], 'lon': places['lon']}
    processed_data = preprocess_data(data)
    save_to_csv(processed_data)

    print(f"Points: {places['lat'][0]},{places['lon'][0]};{places['lat'][1]},{places['lon'][1]}")

    SOURCE_COORDS = (places['lat'][0], places['lon'][0])
    DEST_COORDS = (places['lat'][1], places['lon'][1])

    print("Fetching graph...")
    graph = fetch_road_network(SOURCE_COORDS)
    print("Graph fetched.")

    print("Finding nearest nodes...")
    source_node, dest_node = find_nearest_nodes(graph, SOURCE_COORDS, DEST_COORDS)
    print(f"Source Node: {source_node}, Destination Node: {dest_node}")

    dstar = DStar(graph)

    print("\nFinding initial path using A*...")
    initial_path = nx.shortest_path(graph, source=source_node, target=dest_node, weight='length')
    print(f"Initial Path Found: {initial_path}")

    print("\nAdding a roadblock...")
    blocked_edge = random.choice(list(zip(initial_path[:-1], initial_path[1:])))
    dstar.add_obstacle(*blocked_edge)
    print(f"Blocked Edge: {blocked_edge}")

    print("\nRecalculating path with D*...")
    new_path = dstar.replan(source_node, dest_node)

    if new_path:
        print(f"New Path Found: {new_path}")
    else:
        print("No alternative path found!")


if __name__ == "__main__":
    main()