import ProcessTrips
import DataImport
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
<<<<<<< Updated upstream
=======
import matplotlib.lines as mlines
>>>>>>> Stashed changes

# Data processing
trips = ProcessTrips.transformTrips(DataImport.trips)
zones = DataImport.zones
<<<<<<< Updated upstream
=======
TripsWithZones = ProcessTrips.MergeZones(trips, zones)
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
import plotly.graph_objects as go
import plotly.express as px
=======
>>>>>>> Stashed changes

col5, col6, col7 = st.columns([1, 1, 2])  # Network chart column is wider

with col5:
<<<<<<< Updated upstream
    st.markdown("### Passenger Distribution")  # Adjusted font size for subheader
=======
    st.markdown("#### Passenger Distribution")  # Adjusted font size for subheader
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    st.markdown("### Payment Type Distribution")  # Adjusted font size for subheader
=======
    st.markdown("#### Payment Type Distribution")  # Adjusted font size for subheader
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
# Kol kas neveikia (memory error) - reiks pamastyt ka daryt vietoj jo
with col7:
    st.markdown("### Popular Destinations (Network Chart)")  # Adjusted font size for subheader
    st.text("Placeholder for Network Chart")
    # Replace with actual network chart code
=======

with col7:
    st.markdown("#### Popular Destinations (Network Chart)", unsafe_allow_html=True)

    # Identify the most frequent routes by grouping pickup and dropoff zones
    top_routes = TripsWithZones.groupby(['pickup_zone', 'Zone_dropoff_zone'], as_index=False) \
        .size() \
        .rename(columns={'size': 'trip_count'}) \
        .sort_values('trip_count', ascending=False) \
        .head(20)

    # Generate a gradient color list dynamically
    cmap = plt.cm.RdYlGn  # Red to Yellow to Green
    colors = [cmap(i / (len(top_routes) - 1)) for i in range(len(top_routes))]
    top_routes['color'] = colors

    # Extract the unique pick-up and drop-off zones
    pickup_zones = list(top_routes['pickup_zone'].unique())
    dropoff_zones = list(top_routes['Zone_dropoff_zone'].unique())

    # Create the visualization with a black background
    fig, ax = plt.subplots(figsize=(15, 8), facecolor='none')  # Set figure background color to dark grey like streamlit

    # Set the background color of the plot to black
    ax.set_facecolor('none')

    # Add vertical dotted lines to separate the pick-up and drop-off zones
    ax.vlines(x=1, ymin=-1, ymax=len(pickup_zones), color='white', alpha=0.7, linewidth=1, linestyles='dotted')
    ax.vlines(x=3, ymin=-1, ymax=len(dropoff_zones), color='white', alpha=0.7, linewidth=1, linestyles='dotted')

    # Label the pick-up zones with white color
    for idx, zone in enumerate(pickup_zones):
        ax.text(0.8, idx, zone, horizontalalignment='right', verticalalignment='center', fontsize=14, color='white')

    # Label the drop-off zones with white color
    for idx, zone in enumerate(dropoff_zones):
        ax.text(3.2, idx, zone, horizontalalignment='left', verticalalignment='center', fontsize=14, color='white')

    # Draw lines connecting popular pick-up and drop-off zones
    for idx, pickup_zone in enumerate(pickup_zones):
        matching_routes = top_routes[top_routes['pickup_zone'] == pickup_zone].index
        for route_idx in matching_routes:
            dropoff_zone = top_routes.loc[route_idx, 'Zone_dropoff_zone']
            dropoff_idx = dropoff_zones.index(dropoff_zone)
            line_color = top_routes.loc[route_idx, 'color']
            line = mlines.Line2D([1, 3], [idx, dropoff_idx], marker='o', markersize=6, color=line_color)
            ax.add_line(line)

    # Adjust the plot settings and remove axes
    ax.set(xlim=(0, 4), ylim=(-1, max(len(pickup_zones), len(dropoff_zones))), ylabel='')
    ax.set_xticks([1, 3])
    ax.set_xticklabels(['Pick-up Zone', 'Drop-off Zone'], fontsize=15, color='white')
    ax.tick_params(axis='both', which='both', left=False, bottom=False, labelleft=False, labelcolor='white')

    # Hide all spines to keep the plot clean
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(False)

    # Display the plot in Streamlit
    st.pyplot(fig, bbox_inches='tight', pad_inches=0.1)  # Ensure no whitespace around the plot
>>>>>>> Stashed changes


# --------

<<<<<<< Updated upstream
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
=======
col8, col9 = st.columns([1, 1])  # Equal widths

with col8:
    st.markdown("#### Trip Distance Distribution", unsafe_allow_html=True)  # Make text white
    
    # Plot the histogram - trip distance distribution
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='none')  # Adjust figure size
    trips['trip_distance'].plot(
        kind='hist',
        bins=20,  # Adjust number of bins if more data is available
        color='blue',
        edgecolor='black',
        ax=ax
    )
    ax.set_facecolor('none')
    ax.set_xlabel('Trip Distance (miles)', fontsize=12, color='white')  # White text for axis labels
    ax.set_ylabel('Frequency', fontsize=12, color='white')  # White text for axis labels
    ax.tick_params(axis='both', labelsize=10, colors='white')  # White tick labels

    st.pyplot(fig)

with col9:
    st.markdown("#### Trips Heatmap (Hour vs Weekday)", unsafe_allow_html=True)  # Make text white

    # Aggregate data to get counts for each hour-weekday pair
    heatmap_data = trips.groupby(['pickup_weekday', 'pickup_hour']).size().reset_index(name='trip_count')

    # Pivot the data for heatmap
    heatmap_pivot = heatmap_data.pivot(index="pickup_weekday", columns="pickup_hour", values="trip_count")

    # Reorder weekdays to start from Monday
    weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(weekdays_order).fillna(0)

    # Ensure X-axis includes all hours (0-23)
    hour_range = list(range(24))
    heatmap_pivot = heatmap_pivot.reindex(columns=hour_range, fill_value=0)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='none')  # Adjust figure size
    sns.heatmap(
        heatmap_pivot, 
        cmap="YlGnBu", 
        linewidths=.5, 
        annot=True,  # Annotate the heatmap values
        fmt='d', 
        cbar_kws={'label': 'Trip Count'}, 
        ax=ax
    )
    ax.set_xlabel("Hour of Day", fontsize=12, color='white')  # White text for x-axis label
    ax.set_ylabel("Weekday", fontsize=12, color='white')  # White text for y-axis label
    ax.set_xticks(range(24))
    ax.set_xticklabels(hour_range, rotation=45, fontsize=10, color='white')  # White text for tick labels
    ax.tick_params(axis='y', labelsize=10, colors='white')  # White text for y-axis tick labels

    # Update annotations (values in the heatmap) to white
    for text in ax.texts:
        text.set_color('white')

    ax.set_facecolor('none')

    # Set the colorbar legend text to white
    colorbar = ax.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=10, labelcolor='white')  # Change color of colorbar ticks to white
    colorbar.set_label('Trip Count', fontsize=12, color='white')  # Change color of colorbar label to white

    plt.tight_layout()
    st.pyplot(fig)
>>>>>>> Stashed changes
