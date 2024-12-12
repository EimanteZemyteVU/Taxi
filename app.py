import ProcessTrips
import DataImport
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines

# Data processing
trips = ProcessTrips.transformTrips(DataImport.trips)
zones = DataImport.zones
trips = ProcessTrips.MergeZones(trips, zones)


# Set a fixed page width
st.set_page_config(layout="wide", page_title="Taxi Dashboard")

# Sidebar for page selection
with st.sidebar:
    page_option = st.selectbox("Select Page", ["Explanatory Data Analysis", "Modeling"], help="Choose a page to view")

# Page for Explanatory Data Analysis
if page_option == "Explanatory Data Analysis":
   
    st.title("Taxi Data Preview")

    # Sidebar for filters 
    with st.sidebar:

        #----- Vendors filter
        vendor_map = {
            1: "Creative Mobile Technologies",
            2: "VeriFone Inc."
        }
        unique_vendor_ids = trips['VendorID'].unique()
        vendor_options = ["All"] + [vendor_map.get(vendor_id, f"Unknown Vendor {vendor_id}") for vendor_id in unique_vendor_ids]

        vendor_option = st.selectbox("Vendor", vendor_options, help="Select the taxi vendor")

        # Filter trips based on the selected vendor
        if vendor_option != "All":
            # Reverse the mapping to get VendorID from the vendor name
            vendor_id = [vendor_id for vendor_id, name in vendor_map.items() if name == vendor_option][0]
            trips = trips[trips['VendorID'] == vendor_id]  # Filter trips by the selected vendor

        #----- Date range filter
        min_date = trips['pickup_date'].min()
        max_date = trips['pickup_date'].max()

        selected_start_date, selected_end_date = st.date_input(
            "Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date,
            help="Choose the start and end date for the data"
        )

        # Filter trips by the selected date range
        trips = trips[(trips['pickup_date'] >= pd.to_datetime(selected_start_date)) & 
                    (trips['pickup_date'] <= pd.to_datetime(selected_end_date))]
        
        #------ Payment type filter
        payment_type_map = {
            1: 'Credit card',
            2: 'Cash',
            3: 'No charge',
            4: 'Dispute',
            5: 'Unknown',
            6: 'Voided trip'
        }
        unique_payment_types = trips['payment_type'].unique()
        payment_type_options = ['All'] + [payment_type_map.get(pt, f"Unknown Payment Type {pt}") for pt in unique_payment_types]  # Map numeric payment types
        payment_type = st.selectbox("Payment Type", payment_type_options, help="Choose the payment method")
        
        # Filter trips 
        if payment_type != "All":
            # Reverse the mapping to get the numeric payment type from the description
            payment_type_id = [key for key, value in payment_type_map.items() if value == payment_type][0]
            trips = trips[trips['payment_type'] == payment_type_id] 

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


    col5, col6, col7 = st.columns([1, 1, 2])  # Network chart column is wider

    with col5:
        st.markdown("#### Passenger Distribution") 

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
                font=dict(color="white"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.markdown("#### Payment Type Distribution") 

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
                font=dict(color="white"), 
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown("#### Popular Destinations (Network Chart)", unsafe_allow_html=True)

        # Identify the most frequent routes by grouping pickup and dropoff zones
        top_routes = trips.groupby(['pickup_zone', 'Zone_dropoff_zone'], as_index=False) \
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

    col8, col9 = st.columns([1, 1])  # Equal widths

    with col8:
        st.markdown("#### Trip Distance Distribution") 
        
        # Plot the histogram 
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='none')  # Adjust figure size
        trips['trip_distance'].plot(
            kind='hist',
            bins=20,  # Adjust number of bins if more data is available
            color="#66C5CC",
            edgecolor='black',
            ax=ax
        )
        ax.set_facecolor('none')
        ax.set_xlabel('Trip Distance (miles)', fontsize=12, color='white')
        ax.set_ylabel('Frequency', fontsize=12, color='white')
        ax.tick_params(axis='both', labelsize=10, colors='white')
        st.pyplot(fig)

    with col9:
        st.markdown("#### Trips Heatmap (Hour vs Weekday)") 

        # Check if there are at least 7 days in the filtered trips DataFrame
        unique_dates = trips['pickup_date'].nunique()  # Get the number of unique dates in the filtered data
        if unique_dates < 7:
            st.write("Please select at least 7 days in the date filter to get the visual.")
        else:
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

            # Create the heatmap plot
            fig, ax = plt.subplots(figsize=(14, 7), facecolor='none')

            # Plot the heatmap with a color scale from red (most popular) to green (least popular)
            cmap = plt.cm.RdYlGn_r  # Reversed Red to Yellow to Green colormap
            sns.heatmap(
                heatmap_pivot, 
                cmap=cmap,  # Use the reversed red-yellow-green colormap
                linewidths=0.5, 
                annot=True,  # Annotate the heatmap values
                fmt='d', 
                cbar_kws={'label': 'Trip Count'}, 
                ax=ax
            )
            ax.set_xlabel("Hour of Day", fontsize=12, color='white')
            ax.set_ylabel("Weekday", fontsize=12, color='white')
            ax.set_xticks(range(24))
            ax.set_xticklabels(hour_range, rotation=45, fontsize=10, color='white')
            ax.tick_params(axis='y', labelsize=10, colors='white')

            # Update annotations (values in the heatmap) to white
            for text in ax.texts:
                text.set_color('white')

            # Update colorbar text to white
            colorbar = ax.collections[0].colorbar
            colorbar.ax.tick_params(labelsize=10, labelcolor='white')  # Change color of colorbar ticks to white
            colorbar.set_label('Trip Count', fontsize=12, color='white')  # Change color of colorbar label to white

            ax.set_facecolor('none')
            plt.tight_layout()
            st.pyplot(fig)

elif page_option == "Modeling":

    # Placeholder for Modeling page content (mockup)
    st.title("Modeling Page - Coming Soon!")
    st.markdown("""
        This page will contain machine learning models and predictions.
        Here you can visualize model performance, select algorithms, 
        and evaluate metrics like accuracy, precision, recall, etc.
        
        ### Select your model and parameters here:
        - Random Forest
        - XGBoost
        - Linear Regression
        - etc.
        
        ### Model Evaluation:
        - Confusion Matrix
        - ROC Curve
        - Precision-Recall Curve
        - etc.
        
        Please stay tuned for further updates on this page!
    """)