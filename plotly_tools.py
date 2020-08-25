# Third-party library imports
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

def get_main_indicator(daily_totals):

    fig_total = go.Figure()

    fig_total.add_trace(go.Indicator(
        mode="number+delta",
        value=int(daily_totals.sum()),
        title={
            "text": f"Total Cases<br>({daily_totals.index[-1]})<br><span style='font-size:0.6em;color:gray'>Daily change</span>"},
        delta={'reference': int(daily_totals[:-1].sum()), 'relative': True, 'position': "bottom"},
    ))
    fig_total.update_layout(autosize=True
                            )

    return fig_total


def get_daily_indicator(daily_totals):
    # Daily indicator
    fig_daily = go.Figure()

    fig_daily.add_trace(go.Indicator(
        mode="number+delta",
        value=int(daily_totals[-1]),
        title={
            "text": f"Daily Cases<br>({daily_totals.index[-1]})<br><span style='font-size:0.6em;color:gray'>Daily change</span>"},
        delta={'reference': int(daily_totals[-2]), 'relative': True, 'position': "bottom"}))

    fig_daily.update_layout(autosize=True
                            )

    return fig_daily

def get_type_totals(type_grouped, type_grouped_yesterday):
    # Type indicators
    fig_type_totals = go.Figure()

    fig_type_totals.add_trace(go.Indicator(
        mode="number+delta",
        value=int(type_grouped[0]),
        #     title = {"text": f"Elementary School Total"},
        domain={'x': [0, 0.1], 'y': [0, 0.25]},
        align="left",
        delta={'reference': int(type_grouped_yesterday[0]), 'relative': True, 'position': "right"}))

    fig_type_totals.add_trace(go.Indicator(
        mode="number+delta",
        value=int(type_grouped[2]),
        #     title = {"text": f"Middle School Total"},
        domain={'x': [0, 0.1], 'y': [0.36, 0.62]},
        align="left",
        delta={'reference': int(type_grouped_yesterday[2]), 'relative': True, 'position': "right"}))

    fig_type_totals.add_trace(go.Indicator(
        mode="number+delta",
        value=int(type_grouped[1]),
        #     title = {"text": f"High School Total"},
        domain={'x': [0, 0.1], 'y': [0.75, 1]},
        align="left",
        delta={'reference': int(type_grouped_yesterday[1]), 'relative': True, 'position': "right"}))

    fig_type_totals.update_layout(
        title={"text": "<span style='font-size:1em;color:black'>Total Cases</span>",
               "yanchor": "middle",
               "xanchor": "center",
               "x": 0.4,
               "y": 0.85})

    fig_type_totals.update_layout(
        annotations=[
            dict(text="<span style='font-size:2em;color:black'>High School</span>",
                 align="right",
                 showarrow=False,
                 x=0.9,
                 y=0.95, ),
            dict(text="<span style='font-size:2em;color:black'>Middle School</span>",
                 align="right",
                 showarrow=False,
                 x=0.9,
                 y=0.48, ),
            dict(text="<span style='font-size:2em;color:black'>Elementary</span>",
                 align="right",
                 showarrow=False,
                 x=0.9,
                 y=0.05, )])

    return fig_type_totals

def get_line_chart(df_aggregated):
    title = 'Total Cases by Date'
    colors = ['rgb(83,190,171)']

    mode_size = [8]
    line_size = [2]

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_aggregated.index, y=df_aggregated, mode='lines',
                                  line=dict(color=colors[0], width=2),
                                  connectgaps=True,
                                  ))

    # endpoints
    fig_line.add_trace(go.Scatter(
        x=[df_aggregated.index[-1]],
        y=[df_aggregated[-1]],
        mode='markers',
        marker=dict(color=colors[0], size=6)
    ))

    fig_line.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)')
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=20,
            r=20,
            t=20,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    fig_line.update_layout(annotations=[dict(xref='paper', yref='paper', x=0.5, y=0.9,
                                             xanchor='center', yanchor='bottom',
                                             text=title,
                                             font=dict(size=26,
                                                       color='rgb(82, 82, 82)'),
                                             showarrow=False)])

    return fig_line


def get_bar_chart(top_schools):
    bar_title = "Schools with Most Positive Cases"

    fig_bar = go.Figure(go.Bar(
        x=top_schools,
        y=top_schools.index,
        orientation='h',
        marker=dict(
            color='rgb(83,190,171)')))

    fig_bar.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)')
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            # l=100,
            # r=20,
            # t=100,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    fig_bar.update_layout(margin=dict(autoexpand=True),
                          annotations=[dict(xref='paper', yref='paper', x=0.43, y=1,
                                            xanchor='center', yanchor='bottom',
                                            text=bar_title,
                                            font=dict(size=26,
                                                      color='rgb(82, 82, 82)'),
                                            showarrow=False)])

    return fig_bar

def get_map(df_geo):
    # Map
    fig_map = px.scatter_mapbox(df_geo,
                                lat="latitude",
                                lon="longitude",
                                animation_frame='date',
                                animation_group='school',
                                color="Category",
                                size="total",
                                color_discrete_sequence=px.colors.qualitative.Prism,
                                center={"lat": 34.221749,
                                        "lon": -84.135526},
                                zoom=10,
                                # height=00,
                                # width=700,
                                hover_name='school',
                                hover_data=['school', 'total', 'F2F Students & Staff'])
    fig_map.update_layout(mapbox_style="carto-positron")
    fig_map.update_layout(margin={},
                          autosize=True,
                          title=dict(
                              text='Reported Positive Cases',
                              font=dict(
                                  color='black',
                                  size=26),
                              xanchor="center",
                              x=0.5))

    # fig_map['layout']['sliders'][0]['y'] = 1.2
    # fig_map['layout']['updatemenus'][0]['y'] = 1.2

    return fig_map
