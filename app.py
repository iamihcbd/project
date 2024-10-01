import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the Ames Housing dataset
df = pd.read_csv('AmesHousing.csv')

# Data preparation based on insights from `ibrahim-project-dashapp.py`
# Example: Dropping irrelevant columns and handling missing values
df.drop(['PID'], axis=1, inplace=True)  # Dropping 'PID' as it may not be useful
df.dropna(axis=1, inplace=True)  # Dropping columns with missing values

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a scatter plot using Plotly Express
fig = px.scatter(df, x='Gr Liv Area', y='SalePrice', color='Overall Qual',
                 title="Living Area vs Sale Price",
                 labels={'Gr Liv Area': 'Above Grade Living Area (sq ft)', 'SalePrice': 'Sale Price'},
                 hover_data=['Neighborhood'])

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children='Ames Housing Dataset Dashboard'),

    html.Div(children='''
        Visualizing relationships between housing attributes and sale prices.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Expose the Flask server to be run by gunicorn
server = app.server

# Run the app locally for development
if __name__ == '__main__':
    app.run_server(debug=True)
