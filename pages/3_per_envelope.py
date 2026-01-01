import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("Trend Per Envelope")
st.caption(
    "Evelope is the category or bucket for the spending data. Here is we focus on the monly trend for individual evelopes."
)


def show_per_envelope_chart(dataframe):
    df_mon = dataframe.groupby(["year_month", "Envelope"])["Amount"].sum().reset_index()
    # important: add column convert back to datetime for Plotly x-axis
    df_mon["month_start"] = df_mon["year_month"].dt.to_timestamp()
    df_mon = df_mon[["month_start", "Envelope", "Amount"]].sort_values("month_start", ascending=True)
    mon_number_for_avg = 12  # average over how many months
    df_mon["Moving_Avg"] = df_mon["Amount"].rolling(window=mon_number_for_avg).mean()
    # Plotly part
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_mon["month_start"],
            y=df_mon["Amount"],
            name=f"Monthly Spending for Selected Envelope",
            opacity=0.6,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_mon["month_start"],
            y=df_mon["Moving_Avg"],
            mode="lines+markers",
            marker=dict(
                symbol="circle",
                size=8,
                color="red",
                opacity=1,
                line=dict(
                    color="#1A1A1A",  # Set the outline color
                    width=2,
                ),
            ),
            name=f"Moving Average {mon_number_for_avg} months",
        )
    )
    fig.update_layout(
        # title='Simple Scatter Plot Example',
        xaxis_title="Date",
        yaxis_title="Spending",
        width=800,
        height=450,
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0.1),
    )
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


if "df" in st.session_state:
    df = st.session_state["df"]
    selected_envelope = st.pills(
        "Select one envelope", df["Envelope"].unique(), selection_mode="single", default=df["Envelope"].unique()[1]
    )
    if selected_envelope is not None:
        st.subheader(f"Trend Chart: {selected_envelope}")
        show_per_envelope_chart(df[df["Envelope"] == selected_envelope])
    else:
        st.warning("Please select one evenlope above to generate the graph.")
else:
    st.warning("Please upload data first")
