import streamlit as st
import pandas as pd
import numpy as np

# Set title
st.title("My Streamlit Dashboard")

# Add a sample DataFrame
st.write("Here is a sample DataFrame:")
df = pd.DataFrame(np.random.randn(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
st.write(df)

# Add a chart
st.line_chart(df)

# Add an interactive widget
st.write("Select a number to filter the data:")
num = st.slider("Choose a number", 0, 10, 5)
st.write(df.head(num))