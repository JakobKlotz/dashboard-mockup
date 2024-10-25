# Generated with Calude 3.5 Sonnet ;-)
from datetime import datetime, timedelta

import folium
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def generate_random_timeseries(
    n_points=20, n_series=3, volatility=1.0, seed=None
):
    """Generate random time series data similar to the screenshot."""
    if seed is not None:
        np.random.seed(seed)

    time = np.arange(n_points)
    series = {}

    for i in range(n_series):
        random_walk = np.random.normal(0, volatility, n_points).cumsum()
        seasonality = 0.5 * np.sin(2 * np.pi * time / 12)
        series[chr(97 + i)] = random_walk + seasonality

    return pd.DataFrame(series, index=time)


def create_plot(data, title, plot_type="area"):
    """Create a Plotly figure with the specified data and style."""
    fig = go.Figure()

    colors = ["rgb(53, 162, 235)", "rgb(249, 115, 115)", "rgb(147, 147, 147)"]

    for idx, col in enumerate(data.columns):
        if plot_type == "area":
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[col],
                    name=col.upper(),
                    fill="tonexty" if idx > 0 else None,
                    line=dict(color=colors[idx]),
                )
            )
        else:  # bar
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data[col],
                    name=col.upper(),
                    marker_color=colors[idx],
                )
            )

    fig.update_layout(
        title=title,
        template="plotly_dark",
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
        ),
        height=300,
        margin=dict(t=30, l=0, r=0, b=20),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="rgba(128, 128, 128, 0.2)"
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="rgba(128, 128, 128, 0.2)"
    )

    return fig


def generate_customer_data(n_customers=100, seed=None):
    """Generate random customer data in Tyrol region."""
    if seed is not None:
        np.random.seed(seed)

    # Tyrol approximate boundaries
    tyrol_bounds = {"lat": (46.8, 47.7), "lon": (10.0, 12.9)}

    segments = ["Premium", "Standard", "Basic"]

    # Generate random dates within last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    customers = []
    for i in range(n_customers):
        customer_id = f"CUST_{str(i+1).zfill(4)}"
        segment = np.random.choice(segments, p=[0.2, 0.5, 0.3])

        # Location - create clusters around major cities
        if np.random.random() < 0.6:  # 60% chance to be near Innsbruck
            lat = 47.2692 + np.random.normal(0, 0.1)
            lon = 11.4041 + np.random.normal(0, 0.1)
        else:
            lat = np.random.uniform(
                tyrol_bounds["lat"][0], tyrol_bounds["lat"][1]
            )
            lon = np.random.uniform(
                tyrol_bounds["lon"][0], tyrol_bounds["lon"][1]
            )

        registration_date = start_date + timedelta(
            days=np.random.randint(0, 730)
        )
        days_as_customer = (end_date - registration_date).days

        if segment == "Premium":
            purchases = np.random.randint(20, 50)
            avg_order_value = np.random.uniform(200, 500)
        elif segment == "Standard":
            purchases = np.random.randint(10, 30)
            avg_order_value = np.random.uniform(100, 300)
        else:  # Basic
            purchases = np.random.randint(1, 15)
            avg_order_value = np.random.uniform(50, 200)

        lifetime_value = purchases * avg_order_value

        customers.append(
            {
                "customer_id": customer_id,
                "segment": segment,
                "lat": lat,
                "lon": lon,
                "registration_date": registration_date.strftime("%Y-%m-%d"),
                "days_as_customer": days_as_customer,
                "total_purchases": purchases,
                "avg_order_value": round(avg_order_value, 2),
                "lifetime_value": round(lifetime_value, 2),
            }
        )

    return pd.DataFrame(customers)


def create_customer_map(customers_df):
    """Create a Folium map centered on Tyrol with customer locations."""
    tyrol_center = [47.2692, 11.4041]

    m = folium.Map(
        location=tyrol_center, zoom_start=8, tiles="cartodbdark_matter"
    )

    segment_colors = {"Premium": "red", "Standard": "blue", "Basic": "gray"}

    for _, customer in customers_df.iterrows():
        popup_content = f"""
        <div style='font-family: Arial'>
            <b>Customer ID: {customer['customer_id']}</b><br>
            Segment: {customer['segment']}<br>
            Customer Since: {customer['registration_date']}<br>
            Total Purchases: {customer['total_purchases']}<br>
            Avg Order Value: €{customer['avg_order_value']:,.2f}<br>
            Lifetime Value: €{customer['lifetime_value']:,.2f}
        </div>
        """

        folium.CircleMarker(
            location=[customer["lat"], customer["lon"]],
            radius=6,
            popup=popup_content,
            color=segment_colors[customer["segment"]],
            fill=True,
            fill_color=segment_colors[customer["segment"]],
            fill_opacity=0.7,
            weight=1,
        ).add_to(m)

    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px; border-radius: 5px; font-family: Arial">
        <h4>Customer Segments</h4>
        <div><span style="color: red">●</span> Premium</div>
        <div><span style="color: blue">●</span> Standard</div>
        <div><span style="color: gray">●</span> Basic</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m
