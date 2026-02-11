import osmnx as ox
import networkx as nx
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# 1. Load trained risk model
# Use absolute path relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "models", "risk_model.pkl")

if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    print("Please ensure the model is trained and saved.")
    exit(1)

print(f"Loading risk model from {model_path}...")
try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# 2. Get road graph from OpenStreetMap
place = "Chicago, Illinois, USA"
print(f"Downloading graph for {place} (this may take a moment)...")
try:
    # Configure osmnx with a custom User-Agent to avoid blocking
    ox.settings.user_agent = "Protego-AI-Safety-System/1.0 (vaibhav@example.com)"
    G = ox.graph_from_place(place, network_type="drive")
except Exception as e:
    print(f"Error downloading graph from OSM: {e}")
    exit(1)

# 3. Add risk weight to each edge (Vectorized implementation)
print("Calculating risk scores for all road segments...")

now = datetime.now()
hour = now.hour
day = now.weekday()

# Collect all edge data first
edges_data = []
edge_keys = []

for u, v, k, data in G.edges(keys=True, data=True):
    # Get coordinates of the starting node of the edge
    lat = G.nodes[u]['y']
    lon = G.nodes[u]['x']
    
    edges_data.append({
        'Latitude': lat,
        'Longitude': lon,
        'hour': hour,
        'day': day,
        'crime_enc': 1, # Dummy value (Assault/Battery etc)
        'loc_enc': 1,   # Dummy value (Street)
        'Arrest': 0,    # Dummy value
        'Domestic': 0   # Dummy value
    })
    edge_keys.append((u, v, k))

if not edges_data:
    print("Error: No edges found in the graph.")
    exit(1)

# Create DataFrame
df_edges = pd.DataFrame(edges_data)

# Feature columns expected by the model
feature_cols = ['Latitude', 'Longitude', 'hour', 'day', 'crime_enc', 'loc_enc', 'Arrest', 'Domestic']

# Batch predict
try:
    risk_scores = model.predict(df_edges[feature_cols])
except Exception as e:
    print(f"Error during risk prediction: {e}")
    exit(1)

# Update graph edges with risk weights
print("Updating graph weights...")
for (u, v, k), risk in zip(edge_keys, risk_scores):
    # Risk is 0-1. We use it as a weight.
    # Higher risk = Higher weight (cost)
    # Add small epsilon to ensure non-zero and positive
    G[u][v][k]['risk_weight'] = float(risk) + 0.01

# 4. Get start & end nodes
print("Finding nearest nodes for origin and destination...")
try:
    orig = ox.nearest_nodes(G, -87.7068, 41.8640)
    dest = ox.nearest_nodes(G, -87.6043, 41.7829)
except Exception as e:
    print(f"Error finding nearest nodes: {e}")
    exit(1)

# 5. Calculate paths
print("Calculating routes...")
try:
    # Safest path (minimize risk)
    safest_route = nx.shortest_path(G, orig, dest, weight='risk_weight')
    print(f"Safest Route found: {len(safest_route)} nodes")
    
    # Fastest path (minimize length)
    fastest_route = nx.shortest_path(G, orig, dest, weight='length')
    print(f"Fastest Route found: {len(fastest_route)} nodes")

    # 6. Plotting
    print("Attempting to generate route map...")
    try:
        if hasattr(ox, 'plot_graph_routes'):
            ox.plot_graph_routes(G, [safest_route, fastest_route],
                                route_colors=['green','red'],
                                route_linewidth=4, show=False)
            print("Route map generated.")
        else:
            # OSMnx 2.0+ alternative
            print("OSMnx 2.0+ detected. Falling back to plot_graph_route (if available) or skipping.")
            # Simple fallback: just plot the graph with the route if possible, or just skip
            # For now, explicit skip is safer than guessing the API in a headless env
            print("Visualization skipped (OSMnx v2+ API requires different plotting calls).")
            print("Routes are valid.")
            
    except Exception as plot_err:
        print(f"Warning: Plotting failed: {plot_err}")
        print("Note: This does not affect the route calculations.")

except nx.NetworkXNoPath:
    print("Error: No path found between origin and destination.")
except Exception as e:
    print(f"Error calculating routes: {e}")
