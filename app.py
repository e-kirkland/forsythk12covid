# Third-party library imports
import pandas as pd

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html

# Local imports
from tools import scrape_data as sd, transform as tf
import plotly_tools as pt

# ------------------------------------------------------------------------------
# OBTAIN DATASET
# Read data
df = sd.data_download()

# # Import and clean data (importing csv into pandas)
# df = pd.read_csv("data/forsythk12_covid_data.csv")
print(df.tail())
print(df.columns)
print(df['8/25/20'])

# ------------------------------------------------------------------------------
# BUILD INDICATORS
# Daily positives for indicators
daily_totals = tf.get_daily_positives(df)

# Main indicator
fig_total = pt.get_main_indicator(daily_totals)

# Daily indicator
fig_daily = pt.get_daily_indicator(daily_totals)

# Grouped by type for indicator
type_grouped, type_grouped_yesterday = tf.school_type_totals(df)

# ------------------------------------------------------------------------------
# BUILD LINE CHART
# Aggregated totals for line chart
df_aggregated = tf.aggregated_totals(df)

# Line chart
fig_line = pt.get_line_chart(df_aggregated)

# ------------------------------------------------------------------------------
# BUILD BAR CHART
# Top schools for bar chart
top_schools = tf.top_schools(df)

# Bar chart
fig_bar = pt.get_bar_chart(top_schools)

# ------------------------------------------------------------------------------
# BUILD MAP
# Geo data for map
df_geo = tf.geo_data(df)

# Map
fig_map = pt.get_map(df_geo)

# ------------------------------------------------------------------------------
# APP LAYOUT
external_stylesheets = './dashstyle.css'
app = dash.Dash(__name__)
server = app.server

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)
plotly_figure = dict(data=[dict(x=[1,2,3], y=[2,4,8])])

app.layout = html.Div([
    html.Div([
            html.Div([
                html.H1(children='COVID-19 Dashboard - Forsyth Co. Public Schools',
                        className = "nine columns"),
                ]),
            html.Div([
                dcc.Markdown('''Source Data:
                Forsyth Co. Schools 
                                [Restart](https://www.forsyth.k12.ga.us/Page/52982)
                                [Open for Learning Week 7 onwards](https://www.forsyth.k12.ga.us/Page/53315)  
                                Dashboard Source Code: [GitHub](https://github.com/e-kirkland/forsythk12covid)/[Dataset](https://github.com/e-kirkland/forsythk12covid/blob/master/data/forsythk12_covid_data.csv)
                                ''',
                        className = "three columns"),
                ]),
        ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(style={'height': '350px'},id='g1', figure=fig_total,
                      config={
                          'displayModeBar': False
                      }
                      )
        ], className="three columns"),
        html.Div([
            dcc.Graph(style={'height': '350px'},id='g2', figure=fig_daily,
                      config={
                          'displayModeBar': False
                      }
                      )
        ], className="three columns"),
        html.Div([
            dcc.Graph(style={'height': '350px'}, id='g4', figure=fig_line,
                      config={
                          'displayModeBar': False
                      }
                      )
        ], className="six columns"),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(style={'height': '600px'}, id='g5', figure=fig_map,
                      config={
                          'displayModeBar': False
                      }
                      )
        ], className="six columns"),
        html.Div([
            html.Div([
                dcc.Graph(style={'height': '600px'}, id='g6', figure=fig_bar,
                          config={
                              'displayModeBar': False
                          }
                          )
            ], className="six columns"),
        ])
    ], className="row")
])


# ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components
# @app.callback(
#     [Output(component_id='output_container', component_property='children'),
#      Output(component_id='my_bee_map', component_property='figure')],
#     [Input(component_id='slct_year', component_property='value')]
# )
# def update_graph(option_slctd):
#     print(option_slctd)
#     print(type(option_slctd))
#
#     container = "The year chosen by user was: {}".format(option_slctd)
#
#     dff = df.copy()
#     dff = dff[dff["Year"] == option_slctd]
#     dff = dff[dff["Affected by"] == "Varroa_mites"]
#
#     # Plotly Express
#     fig = px.choropleth(
#         data_frame=dff,
#         locationmode='USA-states',
#         locations='state_code',
#         scope="usa",
#         color='Pct of Colonies Impacted',
#         hover_data=['State', 'Pct of Colonies Impacted'],
#         color_continuous_scale=px.colors.sequential.YlOrRd,
#         labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
#         template='plotly_dark'
#     )
#
#     # Plotly Graph Objects (GO)
#     # fig = go.Figure(
#     #     data=[go.Choropleth(
#     #         locationmode='USA-states',
#     #         locations=dff['state_code'],
#     #         z=dff["Pct of Colonies Impacted"].astype(float),
#     #         colorscale='Reds',
#     #     )]
#     # )
#     #
#     # fig.update_layout(
#     #     title_text="Bees Affected by Mites in the USA",
#     #     title_xanchor="center",
#     #     title_font=dict(size=24),
#     #     title_x=0.5,
#     #     geo=dict(scope='usa'),
#     # )
#
#     return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
