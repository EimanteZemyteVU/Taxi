import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set a fixed page width
st.set_page_config(layout="wide", page_title="Enhanced Streamlit Dashboard")

# Dashboard title
st.title("Enhanced Streamlit Dashboard")

# Sample DataFrame
np.random.seed(0)  # For reproducible data
df = pd.DataFrame({
    'Category': np.random.choice(['A', 'B', 'C'], 100),
    'Values': np.random.randint(1, 100, 100),
    'Dates': pd.date_range('2023-01-01', periods=100, freq='D')
})

# Header: KPI cards at the top
st.subheader("Key Metrics")

# Use columns to place KPIs side-by-side
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total Values", value=int(df['Values'].sum()))
with kpi2:
    st.metric(label="Average Value", value=f"{df['Values'].mean():.2f}")
with kpi3:
    st.metric(label="Unique Categories", value=df['Category'].nunique())

# Filter section
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox("Select Category", options=df['Category'].unique())
selected_date_range = st.sidebar.date_input("Select Date Range", 
                                            [df['Dates'].min(), df['Dates'].max()])

# Filter data based on sidebar inputs
filtered_data = df[(df['Category'] == selected_category) & 
                   (df['Dates'] >= pd.to_datetime(selected_date_range[0])) & 
                   (df['Dates'] <= pd.to_datetime(selected_date_range[1]))]

# Visualizations section
st.subheader("Visualizations")

# Create three columns for charts
col1, col2, col3 = st.columns(3)

# Line chart
with col1:
    st.write("Line Chart of Values Over Time")
    line_fig = px.line(filtered_data, x="Dates", y="Values", title="Values Over Time")
    st.plotly_chart(line_fig, use_container_width=True)

# Bar chart
with col2:
    st.write("Category Distribution (Bar Chart)")
    category_counts = df['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']  # Rename columns for clarity
    bar_fig = px.bar(category_counts, 
                     x='Category', y='Count', 
                     title="Category Counts")
    st.plotly_chart(bar_fig, use_container_width=True)


# Pie chart
with col3:
    st.write("Category Proportion (Pie Chart)")
    pie_fig = px.pie(df, names='Category', title="Category Proportion")
    st.plotly_chart(pie_fig, use_container_width=True)

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data)


# import streamlit as st
# import pandas as pd
# import numpy as np

# # Set title
# st.title("My Streamlit Dashboard")

# # Add a sample DataFrame
# st.write("Here is a sample DataFrame:")
# df = pd.DataFrame(np.random.randn(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
# st.write(df)

# # Add a chart
# st.line_chart(df)

# # Add an interactive widget
# st.write("Select a number to filter the data:")
# num = st.slider("Choose a number", 0, 10, 5)
# st.write(df.head(num))