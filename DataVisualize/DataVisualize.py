import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import chardet

# Detect the encoding of the CSV file
with open('Popular_Spotify_Songs.csv', 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

# Read the dataset with the detected encoding
df = pd.read_csv('Popular_Spotify_Songs.csv', encoding=encoding)

# Convert 'treams' column to numeric
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

# Inisialisasi aplikasi Dash
app = dash.Dash(__name__)

# Layout aplikasi
app.layout = html.Div([
    html.H1("Dashboard Visualisasi Data dengan Plotly dan Dash"),
    html.Div (id= 'dummy', style={'display' : 'none'}), # Menambahkan komponen dummy
    dcc.Tabs([
        dcc.Tab(label='Line Chart', children=[
            dcc.Graph(id='line-chart')
        ]),
        dcc.Tab(label='Bar Chart', children=[
            dcc.Graph(id='bar-chart')
        ]),
        dcc.Tab(label='Pie Chart', children=[
            dcc.Graph(id='pie-chart')
        ]),
        dcc.Tab(label='Scatter Plot', children=[
            dcc.Graph(id='scatter-plot')
        ]),
        dcc.Tab(label='Histogram', children=[
            dcc.Graph(id='histogram')
        ]),
        dcc.Tab(label='Box Plot', children=[
            dcc.Graph(id='box-plot')
        ]),
        dcc.Tab(label='Heatmap', children=[
            dcc.Graph(id='heatmap')
        ])
    ])
])

# Callbacks
@app.callback(
    Output('line-chart', 'figure'),
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('scatter-plot', 'figure'),
    Output('histogram', 'figure'),
    Output('box-plot', 'figure'),
    Output('heatmap', 'figure'),
    Input('dummy', 'children')  # Dummy input untuk trigger callback saat aplikasi dimulai
)

def update_graphs(dummy):
    # Line Chart
    line_fig = px.line(df.groupby('released_year')['streams'].mean().reset_index(),
                       x='released_year', y='streams',
                       title='Rata-rata Jumlah Stream per Tahun Rilis')

    # Bar Chart
    bar_fig = px.bar(df.groupby('artist(s)_name')['track_name'].count().reset_index().sort_values(by='track_name', ascending=False).head(10),
                     x='artist(s)_name', y='track_name',
                     title='Jumlah Lagu per Artis (Top 10)')

    # Pie Chart
    pie_fig = px.pie(df, values='track_name', names='in_spotify_playlists',
                     title='Proporsi Jumlah Lagu di Spotify Playlists')

    # Scatter Plot
    scatter_fig = px.scatter(df, x='streams', y='danceability_%',
                             color='artist(s)_name',
                             title='Sebaran Streams dan Danceability berdasarkan Artis')

    # Histogram
    hist_fig = px.histogram(df, x='released_year',
                            title='Distribusi Tahun Rilis')

    # Box Plot
    box_fig = px.box(df, y='streams', color='released_year',
                     title='Distribusi Streams per Tahun Rilis')

    # Heatmap
    heatmap_data = df.pivot_table(values='streams', index='artist(s)_name', columns='released_year', aggfunc='sum').fillna(0)
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis'
    ))
    heatmap_fig.update_layout(title='Peta Panas Streams per Artis dan Tahun Rilis')

    return line_fig, bar_fig, pie_fig, scatter_fig, hist_fig, box_fig, heatmap_fig

# Menjalankan aplikasi
if __name__ == '__main__':
    app.run_server(debug=True)