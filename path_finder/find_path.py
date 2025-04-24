import osmnx as ox
import networkx as nx
import folium
import os

def find_path(start_coords, end_coords, mode='stealth'):
    """
    Find the optimal path between two coordinates based on the specified mode.
    
    Args:
        start_coords (tuple): (latitude, longitude) of start point
        end_coords (tuple): (latitude, longitude) of end point
        mode (str): 'stealth' (shortest), 'speed' (fastest), or 'safety' (safest)
    
    Returns:
        None (saves HTML map with route)
    """
    try:
        # Calculate a bounding box that includes both points
        min_lat = min(start_coords[0], end_coords[0])
        max_lat = max(start_coords[0], end_coords[0])
        min_lon = min(start_coords[1], end_coords[1])
        max_lon = max(start_coords[1], end_coords[1])
        
        # Add buffer (~5km)
        buffer = 0.05  
        bbox = (
            max_lat + buffer,  # north
            min_lat - buffer,  # south
            max_lon + buffer,  # east
            min_lon - buffer   # west
        )

        # Correct OSMnx 2.0+ syntax - pass the bbox tuple directly
        G = ox.graph_from_bbox(bbox, network_type="all")

        if G is None or len(G.nodes) == 0:
            raise ValueError("Could not retrieve OSM data for this location.")

        # Find nearest nodes (OSMnx 2.0+ syntax)
        orig_node = ox.nearest_nodes(G, X=[start_coords[1]], Y=[start_coords[0]])[0]
        dest_node = ox.nearest_nodes(G, X=[end_coords[1]], Y=[end_coords[0]])[0]

        # Set weight based on mode
        if mode == 'speed':
            G = ox.add_edge_speeds(G)  # Adds 'speed_kph' attribute
            G = ox.add_edge_travel_times(G)  # Adds 'travel_time' attribute
            weight = 'travel_time'
        elif mode == 'safety':
            # Placeholder: If you have safety data, apply it here
            weight = 'length'  # Default to shortest path
        else:  # 'stealth' (shortest path)
            weight = 'length'

        # Find the shortest path
        route = nx.shortest_path(G, orig_node, dest_node, weight=weight)

        # Create a Folium map
        m = folium.Map(location=start_coords, zoom_start=13)
        
        # Extract route coordinates
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(m)
        
        # Add markers
        folium.Marker(start_coords, popup='Start', icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(end_coords, popup='End', icon=folium.Icon(color='red')).add_to(m)
        
        # Save the map
        os.makedirs("data/terrain_maps", exist_ok=True)
        m.save("data/terrain_maps/route_map.html")

    except Exception as e:
        raise RuntimeError(f"Error in pathfinding: {str(e)}")

# Example usage:
# find_path((37.7749, -122.4194), (37.7849, -122.4294), mode='speed')