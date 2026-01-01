import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt


st.title("Deep Dive With Custom Filters")


# ---- Function for filter form ----
def filter_form():
    st.subheader("Selected filters below")
    with st.form("filter_form"):
        # select envelopes
        selected_envelope_list = st.pills(
            "Select one or multiple envelopes",
            df["Envelope"].unique(),
            selection_mode="multi",
            default=df["Envelope"].unique()[0:2],
        )
        # select dates
        min_date_val = df["Date"].min()  #### somehow .date() used in data prep. necessary for slides.
        max_date_val = df["Date"].max()

        selected_date = st.slider(
            f"Select a range of dates (available dates from **{min_date_val:%Y/%m/%d}** to **{max_date_val:%Y/%m/%d}**)",
            min_value=min_date_val,
            max_value=max_date_val,
            value=(min_date_val, max_date_val),
            format="YYYY/MM/DD",
        )
        # submit_button
        st.caption("Click button below to apply the filters above.")
        submit_button = st.form_submit_button("Apply Filters")
        if submit_button:
            if not selected_envelope_list:
                st.error("Please select at least one envelope.")
                st.stop()
    # create filtered data
    df_filtered = filtered_data(df, selected_envelope_list, selected_date[0], selected_date[1])
    # tabs for show graphs and data
    st.write("")
    st.caption("> Graphs and table below are based on the filtered data.")
    tab1, tab2 = st.tabs(["Graphs for filtered data", "Table for filtered data"])
    with tab2:
        st.subheader("Review filtered data below")
        df_filtered_show = df_filtered[["Date", "Envelope", "Name", "Amount", "Account"]]
        st.dataframe(df_filtered_show, hide_index=True)
    with tab1:
        st.subheader("Monthly Trend & Envelope Pie Chart")
        show_monthly_chart_by_envelope(df_filtered)


# ---- Function to create filtered data ----
def filtered_data(dataframe, envelope_list, start_date, end_date):
    df_filtered = dataframe.query("Date >= @start_date and Date <= @end_date and Envelope in @envelope_list")
    return df_filtered


# ---- Function to create filtered data ----
def show_monthly_chart_by_envelope(dataframe):
    df_mon = dataframe.groupby(["year_month", "Envelope"])["Amount"].sum().reset_index()
    df_mon["month_start"] = df_mon[
        "year_month"
    ].dt.to_timestamp()  # important: add column convert back to datetime for Plotly x-axis
    fig1 = px.bar(
        df_mon,
        x="month_start",
        y="Amount",
        #        text="Amount",
        color="Envelope",
        template="plotly_dark",
        labels={"month_start": "Date", "Amount": "Spending"},
    )
    fig1.update_layout(
        # title=f"Monthly Trend Chart",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.00,
        ),
    )
    fig2 = px.pie(df_mon, values="Amount", names="Envelope", color="Envelope", title="Spending by Envelope")
    col1, col2 = st.columns((1.2, 1), border=True)
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.plotly_chart(fig2)


# ---- Display filter form and graph ----
if "df" in st.session_state:
    df = st.session_state["df"]
    filter_form()

else:
    st.warning("Please upload data first")
