import streamlit as st
import pandas as pd
import datetime as dt


# --- Data Prep  ---
def data_prep():  # when "df" in st.session_state
    if "df" in st.session_state:
        df = st.session_state["df"]
        df["Date"] = pd.to_datetime(df["Date"])
        if df["Amount"].dtype == "object":
            df["Amount"] = df["Amount"].str.replace(",", "")  # remove "," in amount, they can't convert to numbers
        df["Amount"] = pd.to_numeric(df["Amount"])  # change Amount from object to numberic
        df = df.dropna(subset=["Envelope", "Amount"])  # drop all NaN under Envelope column. also some NaN under Amount
        df["Amount"] = -df["Amount"]
        df["Envelope"] = df["Envelope"].str.strip()  # Remove leading and trailing whitespace
        # add columns for year and month
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        # this is cool. specifically for month by month for given years. "period" type
        df["year_month"] = df["Date"].dt.to_period("M")
        df["Date"] = df["Date"].dt.date  # date only, importmant for sliders
        st.session_state["df"] = df  # update session_state
    else:
        st.warning("Looks data is not available yet")


if "store_radio_index" not in st.session_state:
    st.session_state.store_radio_index = 0  # this is the default radio index, e.g. use demo data

if "uploaded_file_boolean" not in st.session_state:
    st.session_state.uploaded_file_boolean = False  # check previously uploaded file

# --- data selection: use demo data or import data ---
radio_labels = ["Use Demo Data", "Import Data"]
radio_captions = ["Default. Use built in demo data.", "Import your spending data below."]

st.title("Use demo data or import data")
select_data_source = st.radio(
    "Select demo data or upload your data",
    options=range(len(radio_labels)),  # use index numbers for radio output
    format_func=radio_labels.__getitem__,  # Use labels for display
    captions=radio_captions,
    key="key_radio_index",
    index=st.session_state.store_radio_index,
)
# store selected key_radio_index to store_radio_index
st.session_state.store_radio_index = st.session_state.key_radio_index


# --- use demo data ---
if st.session_state.store_radio_index == 0:  # default option: index=0, Demo Data
    df = pd.read_csv("data/spending_history_demo.csv")
    st.session_state["df"] = df
    data_prep()

# --- upload custom data ---
# elif st.session_state.store_radio_index == 1:  # not default option: index=1, Import Data
#     # df = None  # reset. remove df
#     if st.session_state.uploaded_file_boolean == False:  # if no previously uploaded file
#         if "df" in st.session_state:
#             del st.session_state["df"]  # remove "df" from session_state

file_uploader_disabled = [True, False]  # radio index 0: disabled=True, radio index 1: disabled=False
uploaded_file = st.file_uploader(
    "Upload csv data (Select 'Import Data' to enable the uploader. Once a new file is uploaded, it will overwrite existing data)",
    type="csv",
    disabled=file_uploader_disabled[st.session_state.store_radio_index],
)
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["df"] = df
    data_prep()
    st.session_state.uploaded_file_boolean = True

# --- Display if there is any file uploaded ---
if st.session_state.uploaded_file_boolean:
    st.caption("***File uploaded***", text_alignment="center")
else:
    st.caption("***No file uploaded yet***", text_alignment="center")

# --- Data Preview ---
with st.expander("Data Preview"):
    if "df" in st.session_state:
        st.subheader("A quick preview of a few top entries")
        df = st.session_state["df"]
        st.dataframe(df.head(), hide_index=True)  # type: ignore
    else:
        st.warning("Looks like the data is not imported yet. Please select the demo data or import data.")

with st.expander("Note for custom data"):
    url = "https://goodbudget.com/"
    st.markdown(
        """
        Custom data need to at least have the following columns with exact column names: **Date**, **Envelope**, **Amount**.  
        
        The data concept is inspired by [goodbudget](%s). If you download your goodbudget csv data, feel free test it here. % url
        """
    )
