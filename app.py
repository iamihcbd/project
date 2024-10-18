import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the Ames Housing dataset
df = pd.read_csv('AmesHousing.csv')

# Data preparation
if 'LotFrontage' in df.columns:
    df['LotFrontage'].fillna(df['LotFrontage'].median(), inplace=True)

if 'MasVnrArea' in df.columns:
    df['MasVnrArea'].fillna(0, inplace=True)

if 'GarageYrBlt' in df.columns:
    df['GarageYrBlt'].fillna(df['YearBuilt'], inplace=True)

if 'PID' in df.columns:
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

    # Dropdown for neighborhood selection
    html.Label('Choose Neighborhood:'),
    dcc.Dropdown(
        id='neighborhood-dropdown',
        options=[{'label': neighborhood, 'value': neighborhood} for neighborhood in df['Neighborhood'].unique()],
        value='All',  # Default is All
        placeholder='Select a neighborhood'
    ),

    # Range slider for year selection
    html.Label('Select Year Range:'),
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year Built'].min(),
        max=df['Year Built'].max(),
        step=1,
        value=[df['Year Built'].min(), df['Year Built'].max()],
        marks={str(year): str(year) for year in range(df['Year Built'].min(), df['Year Built'].max() + 1, 5)}
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
from dash.dependencies import Input, Output

@app.callback(
    [Output('main-graph', 'figure'),
     Output('data-summary', 'children')],
    [Input('graph-type-dropdown', 'value'),
     Input('neighborhood-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(graph_type, neighborhood, year_range):
    # Filter based on neighborhood and year range
    filtered_df = df[(df['Year Built'] >= year_range[0]) & (df['Year Built'] <= year_range[1])]
    
    if neighborhood != 'All':
        filtered
