import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import Prophet_bristor

# Create the Dash app
app = Dash(__name__)

# Sample data preparation
data1 = {
    "date": ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05"],
    "value": [10, 15, 20, 25, 30],
}

pastdf = Prophet_bristor.get_past_df()

df = Prophet_bristor.fc()

dfs = [df]

# Define the limits based on the date
limits = df["ds"]
future_dates = df["ds"]


app.layout = html.Div([

    # Title Section
    html.Div([
        html.H1("Volumes Prediction and Event Forecasting", style={'color': '#fff', 'fontSize': '32px', 'textAlign': 'center'}),
        html.P("Use the sliders and dropdowns below to control the displayed data.",
               style={'color': '#bbb', 'textAlign': 'center'}),
    ], style={'padding': '20px'}),

    # Graph Section
    dcc.Graph(id="graph", style={'backgroundColor': '#1e1e1e'}),  # Set graph background color to dark

    html.Div([  # Date-based Slider
        html.Label("Recorded and Forecast Data Slider", style={'color': '#bbb', 'fontSize': '14px'}),
        dcc.Slider(
            id="slider",
            min=0,
            max=len(limits) - 1,
            step=1,
            value=0,  # Initial slider position
            marks={i: {"label": limits.iloc[i].strftime('%m-%y'), "style": {"transform": "rotate(45deg)"}} for i in range(len(limits))},
            updatemode='drag',
        ),
    ], style={'width': '96%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([  # Event Slider
        html.Label("Event Slider", style={'color': '#bbb', 'fontSize': '14px'}),
        dcc.Slider(
            id="event-slider",
            min=0,
            max=len(future_dates) - 1,
            step=1,
            value=0,  # Default value
            marks={i: {"label": future_dates.iloc[i].strftime('%m-%y'), "style": {"transform": "rotate(45deg)"}} for i in range(len(future_dates))},
        ),
    ], style={'width': '96%', 'display': 'inline-block', 'padding': '10px'}),

    # Controls Section (Sliders, Dropdowns, Input Box)
    html.Div([

        # Product Dropdown
        html.Div([
            html.Label("Product", style={'color': '#bbb'}),
            dcc.Dropdown(
                id="product",
                options=[
                    {"label": "Bristor", "value": "bristor"},
                    {"label": "Yrex", "value": "yrex"},
                    {"label": "Competitors", "value": "competitors"},
                ],
                value="bristor",  # Default selection
                style={'backgroundColor': '#777', 'color': '#111', 'border': '1px solid #444'}
            ),
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'}),

        # Variable Dropdown
        html.Div([
            html.Label("Factor of Influence", style={'color': '#bbb'}),
            dcc.Dropdown(
                id="content",
                options=[
                    {"label": "Competitors new patients", "value": "competitors_new_patients"},
                    {"label": "Emails", "value": "emails"},
                    {"label": "Calls", "value": "calls"},
                    {"label": "Competitors share of voice", "value": "competitors_share_of_voice"},
                    {"label": "Share of voice", "value": "share_of_voice"},
                    {"label": "Factory volumes", "value": "factory_volumes"},
                    {"label": "New patients", "value": "new_patients"},
                    {"label": "Competitors demand volumes", "value": "competitors_demand_volumes"},
                ],
                value="activity",  # Default selection
                style={
                'backgroundColor': '#777',  # Dark background for the dropdown
                'color': '#111',  # White text for dropdown labels
                'border': '1px solid #444',  # Dark border
                'width': '100%'
            },
            ),
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'}),

        # Factor Numeric Input
        html.Div([
            html.Label("Multiplier", style={'color': '#bbb'}),
            dcc.Input(
                id="numeric-input",
                type="number",
                min=0,
                value=100,  # Default numeric input
                style={'width': '100%', 'backgroundColor': '#777', 'color': '#111', 'border': '1px solid #444', 'fontFamily': 'monospace'}
            ),
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '10px'}),

    ], style={'padding': '20px', 'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),


], style={'padding': '20px', 'backgroundColor': '#121212', 'minHeight': '100vh', 'fontFamily': 'monospace'})  # Set main background to a very dark color

previous_event_date = ""
previous_num_value = -1
previous_content = ''

# Callback to update the graph
@app.callback(
    Output("graph", "figure"),
    Input("slider", "value"),
    Input("event-slider", "value"),
    Input("product", "value"),
    Input("content", "value"),
    Input("numeric-input", "value"),
)


def update_graph(slider_value, event_date, product, content, numeric_value):
    global previous_event_date
    global previous_content
    global previous_num_value
    global df
    global dfs

    if (previous_event_date != event_date or previous_num_value != numeric_value or previous_content != content):
        df = Prophet_bristor.fc(future_dates.iloc[event_date], (numeric_value / 100.0 if numeric_value is not None else 0), content)
        dfs = [df]
    previous_event_date = event_date
    previous_num_value = numeric_value
    previous_content = content

    # Get the current limit from the slider (the date corresponding to the slider value)
    limit = limits.iloc[slider_value]

    # Initialize the figure
    fig = go.Figure()

    # Dataframe 1 on the left of the limit
    fig.add_trace(
        go.Scatter(
            x=pastdf[pastdf["ds"] <= limit]["ds"],
            y=pastdf[pastdf["ds"] <= limit]["y"],
            mode="markers+lines",
            name=f"Dataset 1 (Limit: {limit.strftime('%Y-%m-%d')})",
            line=dict(color="blue"),
        )
    )

    # Dataframes on the right of the limit
    for i, df in enumerate(dfs):
        lower_error = df["yhat"] - df["yhat_lower"]
        upper_error = df["yhat_upper"] - df["yhat"]

        fig.add_trace(
            go.Scatter(
                x=df[df["ds"] >= limit]["ds"],
                y=df[df["ds"] >= limit]["yhat"],
                error_y=dict(
                    type="data",
                    array=upper_error[df["ds"] >= limit],  # Upper error range
                    symmetric=False,  # Indicating asymmetric error bars
                    arrayminus=lower_error[df["ds"] >= limit]  # Lower error range
                ),
                mode="markers+lines",
                name=f"Dataset {i + 2}",
                line=dict(color=f"rgba({255 - i * 100},{100 + i * 50},{150 - i * 50},0.8)"),  # Different colors
            )
        )

    # Use custom slider, dropdown, and numeric input to update the title dynamically
    fig.update_layout(
        title=(
            f"Two Dataframes with Movable Limit: {limit.strftime('%Y-%m-%d')}<br>"
            f"Custom Slider: {event_date}, Dropdown: {product}, dd: {content}, Numeric: {numeric_value}"
        ),
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_dark",
        font_family="Monospace",
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
