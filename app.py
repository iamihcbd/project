import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the Ames Housing dataset
df = pd.read_csv('AmesHousing.csv')

# Data preparation based on ibrahim-project-dashapp.py
df['LotFrontage'].fillna(df['LotFrontage'].median(), inplace=True)  # Fill missing 'LotFrontage' with median
df['MasVnrArea'].fillna(0, inplace=True)  # Fill missing values in 'MasVnrArea' with 0
df['GarageYrBlt'].fillna(df['YearBuilt'], inplace=True)  # Replace missing 'GarageYrBlt' with 'YearBuilt'
df.drop(['PID'], axis=1, inplace=True)  # Drop the 'PID' column as it's not needed

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

# Interactivity: Dropdown for Graph Selection
graph_options = [
    {'label': 'Scatter: Living Area vs Sale Price', 'value': 'scatter'},
    {'label': 'Histogram: Sale Price Distribution', 'value': 'histogram'},
    {'label': 'Box Plot: Lot Area by Neighborhood', 'value': 'boxplot'}
]

# Interactivity: Slider for Year Built Filter
year_slider = dcc.Slider(
    min=df['Year Built'].min(),
    max=df['Year Built'].max(),
    value=df['Year Built'].max(),
    marks={str(year): str(year) for year in range(df['Year Built'].min(), df['Year Built'].max(), 10)},
    step=None,
    id='year-slider'
)

# Interactivity: Neighborhood Checklist Filter
neighborhood_options = [{'label': neighborhood, 'value': neighborhood} for neighborhood in df['Neighborhood'].unique()]
neighborhood_checklist = dcc.Checklist(
    options=neighborhood_options,
    value=df['Neighborhood'].unique(),
    id='neighborhood-checklist'
)

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children='Ames Housing Dataset Dashboard'),

    # Dropdown for selecting which graph to show
    html.Label('Choose Graph Type:'),
    dcc.Dropdown(
        id='graph-type-dropdown',
        options=graph_options,
        value='scatter'
    ),

    # Slider for filtering by year built
    html.Label('Filter by Year Built:'),
    year_slider,

    # Checklist for filtering by neighborhood
    html.Label('Filter by Neighborhood:'),
    neighborhood_checklist,

    # Graph output
    dcc.Graph(id='main-graph'),

    # Summary/analysis of the graphs and data
    html.H2(children='Summary of Analysis'),
    html.Div(id='data-summary', style={'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px'}),

    # Adding student name and ID
    html.Div(children=[
        html.H4("Student Name: Ibrahim Haque Choudhury"),
        html.H4("Student ID: 1221400091")
    ], style={'margin-top': '30px', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px'})
])

# Callback for interactivity
@app.callback(
    [dash.dependencies.Output('main-graph', 'figure'),
     dash.dependencies.Output('data-summary', 'children')],
    [
        dash.dependencies.Input('graph-type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('neighborhood-checklist', 'value')
    ]
)
def update_graph_and_summary(graph_type, selected_year, selected_neighborhoods):
    # Filter the data based on year and neighborhood
    filtered_df = df[(df['Year Built'] <= selected_year) & (df['Neighborhood'].isin(selected_neighborhoods))]

    # Generate the figure based on the selected graph type
    if graph_type == 'scatter':
        fig = px.scatter(filtered_df, x='Gr Liv Area', y='SalePrice', color='Overall Qual',
                         title="Living Area vs Sale Price",
                         labels={'Gr Liv Area': 'Above Grade Living Area (sq ft)', 'SalePrice': 'Sale Price'},
                         hover_data=['Neighborhood'])
        summary = "The scatter plot shows the relationship between living area and sale price, with homes in better condition (Overall Qual) generally having higher sale prices."

    elif graph_type == 'histogram':
        fig = px.histogram(filtered_df, x='SalePrice', nbins=50, title="Distribution of Sale Prices")
        summary = "The histogram shows that most homes have sale prices below $300,000, with some expensive homes creating a long tail in the distribution."

    elif graph_type == 'boxplot':
        fig = px.box(filtered_df, x='Neighborhood', y='Lot Area', title="Lot Area by Neighborhood")
        summary = "The box plot reveals differences in lot sizes across neighborhoods. Some neighborhoods have consistently larger lots, while others are more varied."

    # Return the updated figure and summary text
    return fig, summary

# Expose the Flask server to be run by gunicorn
server = app.server

# Run the app locally for development
if __name__ == '__main__':
    app.run_server(debug=True)
