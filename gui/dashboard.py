import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from path_finder import find_path
from path_finder.border_locations import locations
from streamlit.components.v1 import html

st.title("AI Border Security System")

zone = st.selectbox("Select Border Zone", list(locations.keys()))
mission = st.selectbox("Mission Type", ["stealth", "speed", "safety"])
end_input = st.text_input("Destination (lat, lon)", "26.9050, 70.9200")

if st.button("Run Pathfinding"):
    try:
        start = locations[zone]
        end = tuple(map(float, end_input.split(',')))
        find_path.find_path(start, end, mission)
        with open("data/terrain_maps/route_map.html", "r", encoding="utf-8") as f:
            map_html = f.read()
        html(map_html, height=500)
    except Exception as e:
        st.error(f"⚠️ Error running pathfinding: {e}")

if st.button("Start Threat Detection"):
    st.write("Launching detection...")
    import subprocess
    subprocess.Popen(["python", "object_detection/detect.py"])