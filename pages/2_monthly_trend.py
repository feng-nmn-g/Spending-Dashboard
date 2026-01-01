import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# st.set_page_config(page_title="title of page1")
st.title("Monthly Trend Analysis")


# ---- Function of showing 3 KPI box ----
def show_date_range_count(dataframe):
    date_min = dataframe["Date"].min()
    date_max = dataframe["Date"].max()
    count = dataframe["Amount"].count()
    ### use 3 columns to show
    col1, col2, col3 = st.columns(3, border=True)
    with col1:
        st.metric(
            label="Start date",
            value=f"{date_min:%Y-%m-%d}",
        )
    with col2:
        st.metric(
            label="End date",
            value=f"{date_max:%Y-%m-%d}",
        )
    with col3:
        st.metric(
            label="Number of entries",
            value=f"{count:,}",
        )


# ---- Function: convert to monthly data and plot monthly chart ----
def show_monthly_chart(dataframe):
    df_mon = dataframe.groupby(["year_month", "Envelope"])["Amount"].sum().reset_index()
    df_mon["month_start"] = df_mon[
        "year_month"
    ].dt.to_timestamp()  # important: add column convert back to datetime for Plotly x-axis
    fig = px.bar(
        df_mon,
        x="month_start",
        y="Amount",
        #        text="Amount",
        color="Envelope",
        template="plotly_dark",
        labels={"month_start": "Date", "Amount": "Spending"},
    )
    fig.update_layout(
        # title=f"Monthly Trend Chart",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.00,
        ),
    )
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


# ---- Function: use monthly data and plot monthly chart ----
def show_monthly_percentage(dataframe):
    df_mon = dataframe.groupby(["year_month", "Envelope"])["Amount"].sum().reset_index()
    df_mon["Monthly_Total"] = df_mon.groupby("year_month")["Amount"].transform(
        "sum"
    )  # transform doesn't change dataframe shape
    df_mon["Amount_pct"] = df_mon["Amount"] / df_mon["Monthly_Total"] * 100
    df_mon["month_start"] = df_mon[
        "year_month"
    ].dt.to_timestamp()  # important: add column convert back to datetime for Plotly x-axis
    fig = px.bar(
        df_mon,
        x="month_start",
        y="Amount_pct",
        color="Envelope",
        template="plotly_dark",
        opacity=0.9,
        labels={"month_start": "Date", "Amount_pct": "Spending in %"},
    )
    fig.update_layout(
        # title=f"Monthly Trend Chart",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.00,
        ),
    )
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


# ---- Display Stats and Charts ----
if "df" in st.session_state:
    df = st.session_state["df"]
    # quick stats card section
    st.subheader("Quick Stats")
    show_date_range_count(df)
    # monthly chart section
    show_percentage_toggle = st.toggle("Show percentage by envelopes")
    if show_percentage_toggle:
        st.subheader("Monthly Trend By Envelope Percentage")
        show_monthly_percentage(df)
    else:
        st.subheader("Monthly Trend Chart")
        show_monthly_chart(df)

else:
    st.warning("Please upload data first")
