import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
file_path = 'Group2_Sample.xlsx'
data = pd.read_excel(file_path)

# Select the year and country (for example, 2020 and Sri Lanka)
selected_year = 2020
selected_country = 'Sri Lanka'
filtered_data = data[(data['Year'] == selected_year) & (data['Partner Country (Importer)'] == selected_country)]

# Assuming the US coordinates as the starting point
us_lat, us_lon = 37.0902, -95.7129

# Taking the mean of the coordinates for Sri Lanka from the filtered data
sl_lat = filtered_data['Importer_lat'].mean()
sl_lon = filtered_data['Importer_lon'].mean()

fig = go.Figure()

# Add line between the US and Sri Lanka
fig.add_trace(go.Scattergeo(
    lat = [us_lat, sl_lat], 
    lon = [us_lon, sl_lon],
    mode = 'lines',
    line = dict(width = 2, color = 'blue'),
))

# Adding the arrow to the end of the line
l = 1.1  # arrow length, adjust as needed
widh = 0.035  # 2*widh is the width of the arrow base as a triangle

# Calculate vector from US to Sri Lanka
A = np.array([us_lon, us_lat])
B = np.array([sl_lon, sl_lat])
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
    title = f'Trade Flow from US to {selected_country} in {selected_year}',
    width = 900,
    height = 750,
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
