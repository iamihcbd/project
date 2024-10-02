import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the Ames Housing dataset
df = pd.read_csv('AmesHousing.csv')

# Data preparation based on ibrahim-project-dashapp.py
# Check if 'LotFrontage' exists in the DataFrame
if 'LotFrontage' in df.columns:
    df['LotFrontage'].fillna(df['LotFrontage'].median(), inplace=True)

df['MasVnrArea'].fillna(0, inplace=True)
df['GarageYrBlt'].fillna(df['YearBuilt'], inplace=True)
df.drop(['PID'], axis=1, inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Graph 1: Scatter plot of Living Area vs Sale Price
scatter_fig = px.scatter(df, x='Gr Liv Area', y='SalePrice', color='Overall Qual',
                         title="Living Area vs Sale Price",
                         labels={'Gr Liv Area': 'Above Grade Living Area (sq ft)', 'SalePrice': 'Sale Price'},
                         hover_data=['Neighborhood'])

# Graph 2: Histogram of SalePrice
histogram_fig = px.histogram(df, x='SalePrice', nbins=50, title="Distribution of Sale Prices")

# Graph 3: Box plot of Lot Area by Neighborhood
box_plot_fig = px.box(df, x='Neighborhood', y='Lot Area', title="Lot Area by Neighborhood")

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children='Ames Housing Dataset Dashboard'),

    # Dropdown for selecting which graph to show
    html.Label('Choose Graph Type:'),
    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[
            {'label': 'Scatter: Living Area vs Sale Price', 'value': 'scatter'},
            {'label': 'Histogram: Sale Price Distribution', 'value': 'histogram'},
            {'label': 'Box Plot: Lot Area by Neighborhood', 'value': 'boxplot'}
        ],
        value='scatter'
    ),

    dcc.Graph(id='main-graph'),

    html.H2(children='Summary of Analysis'),
    html.Div(id='data-summary'),

    html.Div(children=[
        html.H4("Student Name: Ibrahim Haque Choudhury"),
        html.H4("Student ID: 1221400091")
    ])
])

# Callback for interactivity
@app.callback(
    [dash.dependencies.Output('main-graph', 'figure'),
     dash.dependencies.Output('data-summary', 'children')],
    [dash.dependencies.Input('graph-type-dropdown', 'value')]
)
def update_graph(graph_type):
    if graph_type == 'scatter':
        fig = scatter_fig
        summary = "The scatter plot shows a relationship between living area and sale price."
    elif graph_type == 'histogram':
        fig = histogram_fig
        summary = "The histogram shows that most homes have sale prices below $300,000."
    elif graph_type == 'boxplot':
        fig = box_plot_fig
        summary = "The box plot reveals differences in lot sizes across neighborhoods."
    
    return fig, summary

# Expose the Flask server to be run by gunicorn
server = app.server

# Run the app locally for development
if __name__ == '__main__':
    app.run_server(debug=True)
