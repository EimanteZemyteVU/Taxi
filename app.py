import ProcessTrips
import DataImport
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Data processing
trips = ProcessTrips.transformTrips(DataImport.trips)
zones = DataImport.zones

# Set a fixed page width
st.set_page_config(layout="wide", page_title="Taxi Explanatory Data Analysis")

# Dashboard title
st.title("Taxi Data Preview")

# Sidebar for filters (not working yet) - MOCKUP
with st.sidebar:
    # st.image("taxi_image.png", use_column_width=True)  # Replace with your taxi image
    st.header("Filters")
    st.selectbox("Vendor", ["Vendor 1", "Vendor 2"], help="Select the taxi vendor")
    st.date_input("Date Range", [], help="Choose the start and end date for the data")
    st.text_input("Pick-up Location", help="Enter the pick-up location")
    st.text_input("Drop-off Location", help="Enter the drop-off location")
    st.selectbox("Payment Type", ["Cash", "Card", "Other"], help="Choose the payment method")
    st.selectbox("Rate Code", ["Standard", "Other"], help="Select the rate code")

# -------------
# Cards visuals: 
# Calculate the required metrics
total_trips = len(trips)
average_trip_distance = trips["trip_distance"].mean()
average_fare_amount = trips["fare_amount"].mean()
average_passenger_count = trips["passenger_count"].mean()

# Top Row: Metric Cards
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Equal widths for metric cards
col1.metric("Total Trips", f"{total_trips:,}", help="The total number of trips.")
col2.metric("Avg. Trip Distance", f"{average_trip_distance:,.2f} miles", help="The average distance per trip.")
col3.metric("Avg. Fare Amount", f"${average_fare_amount:,.2f}", help="The average fare collected per trip.")
col4.metric("Avg. Passenger Count", f"{average_passenger_count:,.1f}", help="The average number of passengers per trip.")

# -------------

import plotly.graph_objects as go
import plotly.express as px

col5, col6, col7 = st.columns([1, 1, 2])  # Network chart column is wider

with col5:
    st.markdown("### Passenger Distribution")  # Adjusted font size for subheader

    # Calculate the passenger count distribution
    passenger_distribution = trips['passenger_count'].value_counts().sort_index()

    # Create the interactive Plotly donut chart
    fig = go.Figure(
        go.Pie(
            labels=[str(label) for label in passenger_distribution.index],
            values=passenger_distribution.values,
            hole=0.6,  # Creates the donut
            textinfo="label+percent",  # Show both labels and percentages on the chart
            hoverinfo="label+value",  # Show labels and values on hover
            marker=dict(colors=px.colors.qualitative.Pastel),  # Add color palette for a dark theme
        )
    )
    fig.update_layout(
        margin=dict(t=20, b=40, l=10, r=10),  # Added space for legend
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background for dark theme
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Position below the chart
            x=0.5,
            xanchor="center",
            font=dict(color="white"),  # White font for dark theme
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown("### Payment Type Distribution")  # Adjusted font size for subheader

    # Define the mapping of numeric codes to payment descriptions
    payment_type_map = {
        1: 'Credit card',
        2: 'Cash',
        3: 'No charge',
        4: 'Dispute',
        5: 'Unknown',
        6: 'Voided trip'
    }

    # Calculate the payment type distribution
    payment_distribution = trips['payment_type'].value_counts().sort_index()

    # Calculate the total number of trips for percentage calculation
    total_trips = sum(payment_distribution)

    # Group payment types with a percentage below 10% into 'Other'
    threshold = 0.1  # 10% threshold
    payment_distribution_grouped = payment_distribution[payment_distribution / total_trips >= threshold]
    payment_distribution_other = payment_distribution[payment_distribution / total_trips < threshold]

    # Combine the small categories into 'Other'
    if not payment_distribution_other.empty:
        payment_distribution_grouped['Other'] = payment_distribution_other.sum()

    # Create the interactive Plotly donut chart
    fig = go.Figure(
        go.Pie(
            labels=[
                payment_type_map.get(label, 'Other')
                for label in payment_distribution_grouped.index
            ],
            values=payment_distribution_grouped.values,
            hole=0.6,  # Creates the donut
            textinfo="label+percent",  # Show both labels and percentages on the chart
            hoverinfo="label+value",  # Show labels and values on hover
            marker=dict(colors=px.colors.qualitative.Pastel),  # Add color palette for a dark theme
        )
    )
    fig.update_layout(
        margin=dict(t=20, b=40, l=10, r=10),  # Added space for legend
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background for dark theme
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Position below the chart
            x=0.5,
            xanchor="center",
            font=dict(color="white"),  # White font for dark theme
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

# Kol kas neveikia (memory error) - reiks pamastyt ka daryt vietoj jo
with col7:
    st.markdown("### Popular Destinations (Network Chart)")  # Adjusted font size for subheader
    st.text("Placeholder for Network Chart")
    # Replace with actual network chart code


# --------

# col8, col9 = st.columns([1, 1])  # Equal widths

# with col8:
#     st.subheader("Trip Distance Distribution")
    
#     # Plot the histogram - trip distance distribution
#     fig, ax = plt.subplots(figsize=(10, 5))  # Adjust figure size
#     trips['trip_distance'].plot(
#         kind='hist',
#         bins=20,  # Adjust number of bins if more data is available
#         color='blue',
#         edgecolor='black',
#         ax=ax,
#         title='Trip Distance Distribution'
#     )
#     ax.set_xlabel('Trip Distance (miles)', fontsize=12)
#     ax.set_ylabel('Frequency', fontsize=12)
#     ax.tick_params(axis='both', labelsize=10)
#     st.pyplot(fig)

# with col9:
#     st.subheader("Trips Heatmap (Hour vs Weekday)")

#     # Aggregate data to get counts for each hour-weekday pair
#     heatmap_data = trips.groupby(['pickup_weekday', 'pickup_hour']).size().reset_index(name='trip_count')

#     # Pivot the data for heatmap
#     heatmap_pivot = heatmap_data.pivot(index="pickup_weekday", columns="pickup_hour", values="trip_count")

#     # Reorder weekdays to start from Monday
#     weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     heatmap_pivot = heatmap_pivot.reindex(weekdays_order).fillna(0)

#     # Ensure X-axis includes all hours (0-23)
#     hour_range = list(range(24))
#     heatmap_pivot = heatmap_pivot.reindex(columns=hour_range, fill_value=0)

#     # Plot heatmap
#     fig, ax = plt.subplots(figsize=(14, 7))  # Adjust figure size
#     sns.heatmap(
#         heatmap_pivot, 
#         cmap="YlGnBu", 
#         linewidths=.5, 
#         annot=False, 
#         fmt='d', 
#         cbar_kws={'label': 'Trip Count'}, 
#         ax=ax
#     )
#     ax.set_title("Trips Heatmap (Hour vs Weekday)", fontsize=14)
#     ax.set_xlabel("Hour of Day", fontsize=12)
#     ax.set_ylabel("Weekday", fontsize=12)
#     ax.set_xticks(range(24))
#     ax.set_xticklabels(hour_range, rotation=45, fontsize=10)
#     ax.tick_params(axis='y', labelsize=10)
#     plt.tight_layout()
#     st.pyplot(fig)
