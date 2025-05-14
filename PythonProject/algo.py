# imports
import pandas as pd
import requests
import numpy as np
import osmnx as ox
import networkx as nx
import random
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

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
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
    data['time_of_day'] = timestamp.hour
    data['weekday'] = timestamp.weekday()
    data['season'] = (timestamp.month % 12 + 3) // 3
    data['lat'] = data['lat'] / 90.0
    data['lon'] = data['lon'] / 180.0
    return data

# Function to visualize dataset on a map
def visualize_dataset(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['lon'], df['lat'], c='blue', marker='o', label='Locations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Locations in Dataset')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to analyze dataset
def analyze_dataset(df):
    print("\nDataset Analysis:")
    print(f"Total Locations: {len(df)}")
    print(f"Average Latitude: {df['lat'].mean()}")
    print(f"Average Longitude: {df['lon'].mean()}")
    print(f"Time of Day Distribution:\n{df['time_of_day'].value_counts()}")
    print(f"Weekday Distribution:\n{df['weekday'].value_counts()}")
    print(f"Season Distribution:\n{df['season'].value_counts()}")

# Function to train a machine learning model
def train_model(df):
    # Features and target
    X = df[['lat', 'lon', 'time_of_day', 'weekday', 'season']]
    y = df['time_of_day']  # Example target: predict time of day

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"\nModel Performance:")
    print(f"Mean Squared Error: {mse}")

    return model

# Fetch road network with error handling
def fetch_road_network(coords, distance=5000, network_type='drive'):
    try:
        return ox.graph_from_point(coords, dist=distance, network_type=network_type)
    except ox._errors.InsufficientResponseError:
        print("Error: No road network found for the given coordinates.")
        return None

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


def main():
    places = pd.DataFrame()

    for i in range(4):  # Collect data for 10 places
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


    data = {'lat': places['lat'], 'lon': places['lon']}
    processed_data = preprocess_data(data)
    save_to_csv(processed_data, filename="dataset.csv")


    dataset = pd.read_csv("dataset.csv")


    visualize_dataset(dataset)


    analyze_dataset(dataset)

    # Train a machine learning model
    model = train_model(dataset)

    # Print all collected locations
    print("\nCollected Locations:")
    for i, row in places.iterrows():
        print(f"{i + 1}: Latitude = {row['lat']}, Longitude = {row['lon']}")


    while True:
        try:
            source_index = int(input("Choose source location (1-10): ")) - 1
            dest_index = int(input("Choose destination location (1-10): ")) - 1
            if source_index < 0 or source_index >= len(places) or dest_index < 0 or dest_index >= len(places):
                print("Invalid input! Please enter numbers between 1 and 10.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter valid numbers.")

    # Set source and destination coordinates
    SOURCE_COORDS = (places['lat'][source_index], places['lon'][source_index])
    DEST_COORDS = (places['lat'][dest_index], places['lon'][dest_index])

    print("\nFetching graph...")
    graph = fetch_road_network(SOURCE_COORDS)
    if graph is None:
        print("Exiting due to road network fetch error.")
        return

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