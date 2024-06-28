import streamlit as st
import pandas as pd
import numpy as np

# Function to apply CSS styling for full window length
def set_full_window_length():
    st.markdown(
        """
        <style>
        .dataframe {
            height: calc(100vh - 80px) !important;
            overflow-y: scroll !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app
st.set_page_config(layout="wide")  # Use the wide layout

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
    ecco_subtypes = ['All'] + list(summary_trades.index.get_level_values('ECCO_SUBTYPE').unique())

    # Sidebar filters
    st.sidebar.header('Filters')
    selected_ecco_subtype = st.sidebar.selectbox('Select ECCO_SUBTYPE', ecco_subtypes)

    if selected_ecco_subtype == 'All':
        complex_symbol_ids = ['All'] + list(summary_trades.index.get_level_values('COMPLEX_SYMBOL_ID').unique())
    else:
        complex_symbol_ids = ['All'] + list(summary_trades.xs(selected_ecco_subtype, level='ECCO_SUBTYPE').index.get_level_values('COMPLEX_SYMBOL_ID').unique())

    selected_complex_symbol_id = st.sidebar.selectbox('Select COMPLEX_SYMBOL_ID (optional)', complex_symbol_ids)

    # Filter data based on sidebar input
    def filter_data(df, ecco_subtype, complex_symbol_id):
        if ecco_subtype == 'All':
            filtered = df
        else:
            filtered = df.xs(ecco_subtype, level='ECCO_SUBTYPE')

        if complex_symbol_id != 'All':
            filtered = filtered.xs(complex_symbol_id, level='COMPLEX_SYMBOL_ID')

        return filtered

    filtered_summary_trades = filter_data(summary_trades, selected_ecco_subtype, selected_complex_symbol_id)
    filtered_volume_summary = filter_data(volume_summary, selected_ecco_subtype, selected_complex_symbol_id)
    filtered_volume_per_mm = filter_data(volume_per_mm, selected_ecco_subtype, selected_complex_symbol_id)

    # Apply CSS styling for full window length
    set_full_window_length()

    # Display the filtered data
    st.subheader('Summary Trades')
    st.dataframe(filtered_summary_trades, height=600)

    st.subheader('Total Summary Trades by Trading Date')
    st.dataframe(total_summary_trades, height=600)

    st.subheader('Volume Summary')
    st.dataframe(filtered_volume_summary, height=600)

    st.subheader('Total Volume Summary by Trading Date')
    st.dataframe(total_volume_summary, height=600)

    st.subheader('Volume per Market Maker')
    st.dataframe(filtered_volume_per_mm, height=600)
else:
    st.info("Please upload an Excel file to proceed.")