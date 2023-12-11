import pandas as pd

# Load your data
data = pd.read_excel('Group2_Sample.xlsx')

# Aggregate your data by the necessary fields. This will depend on the specific details of your dataset.
# For example, if you need to aggregate by year and partner country:
aggregated_data = data.groupby(['Year', 'Partner Country (Importer)']).agg({
    'Quantity': 'sum',
    'Value': 'sum',
    'Importer_lat': 'mean',  # Assuming that lat/lon are the same for all entries of a country
    'Importer_lon': 'mean',
}).reset_index()


import plotly.graph_objects as go

def create_trade_flow_map(data, year):
    fig = go.Figure()

    # Assuming the United States is the exporter
    us_lat, us_lon = 37.0902, -95.7129

    # Filter data for the selected year and the specific trade partner
    year_data = data[(data['Year'] == year) & (data['Partner Country (Importer)'] == 'Sri Lanka')]

    # Add lines for each partner country
    for i, row in year_data.iterrows():
        # Here we plot the line
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[us_lon, row['Importer_lon']],
            lat=[us_lat, row['Importer_lat']],
            mode='lines',
            line=dict(width=row['Quantity'] / max(year_data['Quantity']) * 10, color='blue'),
            opacity=0.6,
        ))

        # Here we add the arrowhead
        fig.add_annotation(
            x=row['Importer_lon'],
            y=row['Importer_lat'],
            showarrow=True,
            arrowhead=8,
            arrowsize=7,
            arrowwidth=8,
            arrowcolor='red',
            ax=0,
            ay=0,
            standoff=10
        )

    # Update layout properties
    fig.update_layout(
        title=f'Trade Flow Map for {year}',
        geo=dict(
            scope='world',
            projection_type='equirectangular',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(200, 200, 200)',
        ),
    )

    return fig

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Initialize your Dash app
app = Dash(__name__)

# Define the layout of your app
app.layout = html.Div([
    # Dropdown menu for selecting the year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in data['Year'].unique()],
        value=data['Year'].min()  # Default value
    ),
    # The Plotly graph
    dcc.Graph(id='trade-flow-map')
])

# Define the callback to update the graph
@app.callback(
    Output('trade-flow-map', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_figure(selected_year):
    return create_trade_flow_map(aggregated_data, selected_year)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
