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
        
        # Add line between exporter and importer
        fig.add_trace(go.Scattergeo(
            lon = [exporter_mean['Exporter_lon'], importer_mean['Importer_lon']],
            lat = [exporter_mean['Exporter_lat'], importer_mean['Importer_lat']],
            mode = 'lines',
            line = dict(width = 2, color = 'blue'),
        ))

        
        # Calculate the arrowhead for the line
        l = 1.1  # arrow length, adjust as needed
        widh = 0.010  # 2*widh is the width of the arrow base as a triangle
        A = np.array(exporter_mean)
        B = np.array(importer_mean)
        v = B - A
        w = v / np.linalg.norm(v)
        u = np.array([-v[1], v[0]])  # u orthogonal to w
        
        # Calculate points for the arrowhead
        P = B - l * w
        S = P - widh * u
        T = P + widh * u
        
        # Add the arrowhead as a filled triangle
        fig.add_trace(go.Scattergeo(
            lon = [S[0], T[0], B[0], S[0]],
            lat = [S[1], T[1], B[1], S[1]],
            mode = 'lines',
            fill = 'toself',
            fillcolor = 'blue',
            line_color = 'blue'
        ))

# Update the layout to adjust the appearance
fig.update_layout(
    title = f'Trade Flows in {selected_year}',
    showlegend = False,
    geo = dict(
        projection_type = 'equirectangular',
        showland = True,
        landcolor = 'rgb(217, 217, 217)',
        countrycolor = 'rgb(200, 200, 200)',
        showcountries = True,
        countrywidth = 1
    )
)

fig.show()
