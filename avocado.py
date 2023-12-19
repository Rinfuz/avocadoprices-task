import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Dataset Avocado Price - Kelompok B TUBES PYTHON
url = "https://raw.githubusercontent.com/hananlu/basicPython/master/Dataset/avocadoPrice.csv"
df = pd.read_csv(url)

df['Date'] = pd.to_datetime(df['Date'])
# Filter data tahun 2017 & 2018
df_selected_years = df[df['Date'].dt.year.isin([2016, 2017, 2018])]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("Avocado Prices Data", className="display-4", style={'color': '#4CAF50'}),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df_selected_years['region'].unique()],
            value='Albany',  # Daerah awal
            multi=False,
            className="custom-dropdown"
        ),
    ], className="jumbotron text-center", style={'background-color': '#f8f9fa', 'padding': '20px'}),

    html.Div([
        dcc.RangeSlider(
            id='date-range-slider',
            min=df_selected_years['Date'].min().replace(day=1, hour=0, minute=0, second=0).timestamp(),
            max=df_selected_years['Date'].max().replace(day=1, hour=0, minute=0, second=0).timestamp(),
            marks={timestamp: pd.to_datetime(timestamp, unit='s').strftime('%Y-%m') for timestamp in range(
                int(df_selected_years['Date'].min().replace(day=1, hour=0, minute=0, second=0).timestamp()),
                int(df_selected_years['Date'].max().replace(day=1, hour=0, minute=0, second=0).timestamp()) + 60*60*24*30,
                60*60*24*30
            )},
            value=[
                df_selected_years['Date'].min().replace(day=1, hour=0, minute=0, second=0).timestamp(),
                df_selected_years['Date'].max().replace(day=1, hour=0, minute=0, second=0).timestamp()
            ],
        ),
    ], className="container mt-4", style={'background-color': '#f8f9fa', 'padding': '20px', 'border-radius': '10px'}),

    html.Div([
        dcc.Graph(id='line-chart'),
    ], className="container mt-4", style={'background-color': '#f8f9fa', 'padding': '20px', 'border-radius': '10px'}),

    html.Div([
        dcc.Graph(id='bar-chart'),
    ], className="container mt-4", style={'background-color': '#f8f9fa', 'padding': '20px', 'border-radius': '10px'}),

    html.Div([
        dcc.Graph(id='scatter-chart'),
    ], className="container mt-4", style={'background-color': '#f8f9fa', 'padding': '20px', 'border-radius': '10px'}),
], className="container-fluid", style={'font-family': 'Arial, sans-serif'})

@app.callback(
    Output('line-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('date-range-slider', 'value')]
)
def update_line_chart(selected_region, date_range):
    filtered_df = df_selected_years[(df_selected_years['region'] == selected_region) & (df_selected_years['Date'] >= pd.to_datetime(date_range[0], unit='s')) & (df_selected_years['Date'] <= pd.to_datetime(date_range[1], unit='s'))]
    fig = px.line(filtered_df, x='Date', y='AveragePrice', title=f'Average Price Over Time ({selected_region})')
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('date-range-slider', 'value')]
)
def update_bar_chart(selected_region, date_range):
    filtered_df = df_selected_years[(df_selected_years['region'] == selected_region) & (df_selected_years['Date'] >= pd.to_datetime(date_range[0], unit='s')) & (df_selected_years['Date'] <= pd.to_datetime(date_range[1], unit='s'))]
    year_volume = filtered_df.groupby(filtered_df['Date'].dt.year)['Total Volume'].sum().reset_index()
    fig = px.bar(year_volume, x='Date', y='Total Volume', title=f'Total Volume Per Year ({selected_region})')
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=2017, dtick=1))

    return fig

@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('date-range-slider', 'value')]
)
def update_scatter_chart(selected_region, date_range):
    filtered_df = df_selected_years[(df_selected_years['region'] == selected_region) & (df_selected_years['Date'] >= pd.to_datetime(date_range[0], unit='s')) & (df_selected_years['Date'] <= pd.to_datetime(date_range[1], unit='s'))]
    fig = px.scatter(filtered_df, x='Date', y='AveragePrice', size='Total Volume', title=f'Average Price Over Time ({selected_region})')
    return fig

# CSS dikit
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/slate/bootstrap.min.css']
app.css.external_stylesheets = external_stylesheets

# jalankeun
if __name__ == '__main__':
    app.run_server(debug=True)
