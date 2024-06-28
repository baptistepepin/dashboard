import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app
st.title('QSB Summary Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the uploaded Excel file
    summary_trades = pd.read_excel(uploaded_file, sheet_name="Trades_Summary", index_col=[0,1,2,3])
    total_summary_trades = pd.read_excel(uploaded_file, sheet_name="Total_Trades_Summary", index_col=[0])
    volume_summary = pd.read_excel(uploaded_file, sheet_name="Volume_Summary", index_col=[0,1,2,3])
    total_volume_summary = pd.read_excel(uploaded_file, sheet_name="Total_Volume_Summary", index_col=[0])
    volume_per_mm = pd.read_excel(uploaded_file, sheet_name="Volume_Per_MM_Summary", index_col=[0,1,2,3,4])

    # Extract unique values for filters
    ecco_subtypes = summary_trades.index.get_level_values('ECCO_SUBTYPE').unique()
    complex_symbol_ids = summary_trades.index.get_level_values('COMPLEX_SYMBOL_ID').unique()

    # Sidebar filters
    st.sidebar.header('Filters')
    ecco_subtype = st.sidebar.selectbox('Select ECCO_SUBTYPE', sorted(ecco_subtypes))
    complex_symbol_id = st.sidebar.selectbox('Select COMPLEX_SYMBOL_ID (optional)', ['All'] + sorted(complex_symbol_ids))

    # Filter data based on sidebar input
    filtered_data = summary_trades.loc[(slice(None), ecco_subtype), :]

    if complex_symbol_id != 'All':
        filtered_data = filtered_data.loc[(slice(None), ecco_subtype, complex_symbol_id), :]

    # Display the filtered data
    st.subheader('Summary Trades')
    st.dataframe(filtered_data)

    st.subheader('Total Summary Trades by Trading Date')
    st.dataframe(total_summary_trades)

    st.subheader('Volume Summary')
    st.dataframe(volume_summary)

    st.subheader('Total Volume Summary by Trading Date')
    st.dataframe(total_volume_summary)

    st.subheader('Volume per Market Maker')
    st.dataframe(volume_per_mm)
else:
    st.info("Please upload an Excel file to proceed.")