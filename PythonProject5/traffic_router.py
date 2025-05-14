import pandas as pd
import numpy as np
import networkx as nx
import streamlit as st

# Load the dataset
data = pd.read_csv('traffic_dataset.csv')  # Make sure to have your dataset in the same directory

# Clean the dataset
data.dropna(inplace=True)
data['speed'] = data['speed'].astype(float)
data['volume'] = data['volume'].astype(float)
data['location'] = data['location'].astype(str)

# Create a graph
G = nx.Graph()

# Add edges to the graph based on the dataset
for index, row in data.iterrows():
    G.add_node(row['location'])
    if index < len(data) - 1:
        G.add_edge(row['location'], data.iloc[index + 1]['location'], weight=row['speed'])

# Print available locations for debugging
print("Available locations:", G.nodes)


def heuristic(a, b):
    # Return a constant value as a heuristic
    return 1  # This will make the A* algorithm behave like Dijkstra's algorithm


def a_star(graph, start, goal):
    open_set = {start}
    came_from = {}

    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = g_score[start] + heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)  # Add the start node to the path
            return path[::-1]  # Return reversed path

        open_set.remove(current)

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None  # No path found


# Streamlit UI
st.title("Route Optimization App")

# Create a list of locations for dropdowns
locations = list(G.nodes)

# Dropdown for source and destination
source = st.selectbox("Select Source Location:", locations)
destination = st.selectbox("Select Destination Location:", locations)

if st.button("Find Shortest Path"):
    if source == destination:
        st.error("Source and destination cannot be the same.")
    else:
        path = a_star(G, source, destination)
        if path:
            st.success(f"Shortest path from {source} to {destination}: {' -> '.join(path)}")
        else:
            st.error("No path found.")