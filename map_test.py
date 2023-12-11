import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Function to interpolate points between two coordinates
def interpolate_points(lon1, lat1, lon2, lat2, num_points):
    lons = np.linspace(lon1, lon2, num_points)
    lats = np.linspace(lat1, lat2, num_points)
    return lons, lats

# Load the dataset
file_path = 'Group2_Sample.xlsx'
data = pd.read_excel(file_path)

print(data)
# Select the year for the analysis
selected_year = 2020
data = data[data['Year'] == selected_year]


# Initialize figure
fig = go.Figure()

# Define mapbox style and token
mapbox_style = "open-street-map" 

# Get unique list of exporters and importers
exporters = data['Reporting Country (Exporter)'].unique()
importers = data['Partner Country (Importer)'].unique()

# Iterate over each exporter-importer pair
for exporter in exporters:
    for importer in importers:
        # Filter data for the current exporter-importer pair
        exporter_data = data[data['Reporting Country (Exporter)'] == exporter]
        importer_data = data[data['Partner Country (Importer)'] == importer]
        
        # Calculate mean coordinates for exporter and importer
        exporter_mean = exporter_data[['Exporter_lon', 'Exporter_lat']].mean()
        importer_mean = importer_data[['Importer_lon', 'Importer_lat']].mean()
        
        # Add straight line between exporter and importer using Scattermapbox
        fig.add_trace(go.Scattermapbox(
            lon = [exporter_mean['Exporter_lon'], importer_mean['Importer_lon']],
            lat = [exporter_mean['Exporter_lat'], importer_mean['Importer_lat']],
            mode = 'lines',
            line = dict(width = 2, color = 'blue'),
        ))

         # Add direction marker at the end of the line
        fig.add_trace(go.Scattermapbox(
            lon = [exporter_mean['Exporter_lon'], importer_mean['Importer_lon']],
            lat = [exporter_mean['Exporter_lat'], importer_mean['Importer_lat']],
            mode = 'lines',
            line = dict(width = 2, color = 'blue'),
        ))

        # Calculate the arrowhead for the line
        l = 1.1  # arrow length
        widh = 0.010  # half the width of the arrow base
        A = np.array([exporter_mean['Exporter_lon'], exporter_mean['Exporter_lat']])
        B = np.array([importer_mean['Importer_lon'], importer_mean['Importer_lat']])
        v = B - A
        w = v / np.linalg.norm(v)
        u = np.array([-v[1], v[0]])  # orthogonal to w
        
        # Calculate points for the arrowhead
        P = B - l * w
        S = P - widh * u
        T = P + widh * u
        
        # Add the arrowhead as a filled triangle
        fig.add_trace(go.Scattermapbox(
            lon = [S[0], T[0], B[0], S[0]],
            lat = [S[1], T[1], B[1], S[1]],
            mode = 'lines',
            fill = 'toself',
            fillcolor = 'blue',
            line_color = 'blue'
        ))

# Update the layout to adjust the appearance and set the mapbox style
fig.update_layout(
    title = f'Trade Flows in {selected_year}',
    showlegend = False,
    mapbox = dict(
        style = mapbox_style,
        center = go.layout.mapbox.Center(
            lat = 30,  # Center latitude for the initial map view
            lon = 0    # Center longitude for the initial map view
        ),
        zoom = 1.2  # Initial zoom level
    )
)

fig.show()
