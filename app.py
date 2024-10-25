# Generated with Calude 3.5 Sonnet ;-)
import streamlit as st
from streamlit_folium import st_folium

from src.plots import (
    create_customer_map,
    create_plot,
    generate_customer_data,
    generate_random_timeseries,
)

# Initialize session state for data persistence
if "customer_data" not in st.session_state:
    st.session_state.customer_data = generate_customer_data(seed=42)
if "timeseries_data" not in st.session_state:
    st.session_state.timeseries_data = {
        "data1": generate_random_timeseries(volatility=0.5, seed=42),
        "data2": generate_random_timeseries(volatility=0.8, seed=43),
        "data3": generate_random_timeseries(volatility=0.3, seed=44),
        "data4": generate_random_timeseries(volatility=0.4, seed=45),
    }

# Set up the Streamlit page
st.set_page_config(layout="wide", page_title="Dashboard")

# Add title
st.title("Dashboard")

# Add sidebar
with st.sidebar:
    st.title("Menu")
    st.button("Home", type="primary")
    st.button("Warehouse")
    st.button("Query Optimization and Processing")
    st.button("Storage")
    st.button("Contact Us")

# Create tabs
tab1, tab2 = st.tabs(["📊 Analytics", "🗺️ Customer Map"])

# Tab 1: Analytics
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_plot(
                st.session_state.timeseries_data["data1"],
                "C1",
                plot_type="area",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            create_plot(st.session_state.timeseries_data["data3"], "C3"),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            create_plot(
                st.session_state.timeseries_data["data2"],
                "C2",
                plot_type="bar",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            create_plot(st.session_state.timeseries_data["data4"], "C4"),
            use_container_width=True,
        )

# Tab 2: Customer Map
with tab2:
    # Add filters in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_segments = st.multiselect(
            "Customer Segments",
            options=["Premium", "Standard", "Basic"],
            default=["Premium", "Standard", "Basic"],
            key="segments",
        )

    with col2:
        min_value = st.number_input(
            "Min Lifetime Value (€)",
            min_value=0,
            max_value=int(
                st.session_state.customer_data["lifetime_value"].max()
            ),
            value=0,
            key="min_value",
        )

    with col3:
        min_purchases = st.number_input(
            "Min Total Purchases",
            min_value=0,
            max_value=int(
                st.session_state.customer_data["total_purchases"].max()
            ),
            value=0,
            key="min_purchases",
        )

    # Filter data based on selections
    filtered_df = st.session_state.customer_data[
        (st.session_state.customer_data["segment"].isin(selected_segments))
        & (st.session_state.customer_data["lifetime_value"] >= min_value)
        & (st.session_state.customer_data["total_purchases"] >= min_purchases)
    ]

    # Create and display map
    st.write("### Customer Locations")
    customer_map = create_customer_map(filtered_df)
    st_folium(customer_map, width=1400, height=600, key="map")

    # Display customer metrics
    st.write("### Customer Details")

    # Summary metrics
    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        st.metric("Total Customers", len(filtered_df))
    with metric2:
        st.metric(
            "Avg Lifetime Value",
            f"€{filtered_df['lifetime_value'].mean():,.2f}",
        )
    with metric3:
        st.metric(
            "Avg Purchases", f"{filtered_df['total_purchases'].mean():.1f}"
        )
    with metric4:
        st.metric(
            "Avg Order Value", f"€{filtered_df['avg_order_value'].mean():,.2f}"
        )

    # Detailed table
    st.dataframe(
        filtered_df.drop(["lat", "lon"], axis=1),
        hide_index=True,
        use_container_width=True,
    )
