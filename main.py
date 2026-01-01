import streamlit as st

# --- Page Setup ---
page_upload = st.Page(
    page="pages/1_upload_data.py",
    title="Upload Data",
    icon=":material/upload:",
    default=True,
)

page_2 = st.Page(
    page="pages/2_monthly_trend.py",
    title="Monthly Trend",
    icon=":material/bar_chart:",
)

page_3 = st.Page(
    page="pages/3_per_envelope.py",
    title="Trend Per Envelope",
    icon=":material/account_balance_wallet:",
)

page_4 = st.Page(
    page="pages/4_data_table.py",
    title="Data Table Deep Dive",
    icon=":material/data_table:",
)

# --- Navigation Setup (without sections) ---
# pg = st.navigation(pages=[home_page, page_1, page_2])
# pg.run()

# --- Navigation Setup (with sections) ---
pg = st.navigation({"Import Data": [page_upload], "Spending Analysis": [page_2, page_3, page_4]})


# --- Shared on all pages ---
st.logo("assets/logo-grey-200px.png")

pg.run()

# --- show df state on the sidebar --- ### need to put this after pg.run() to the get the latest df state
# st.sidebar.markdown("***")
# st.sidebar.text("")
if "df" in st.session_state:
    st.sidebar.success("Data imported")
else:
    st.sidebar.warning("Select or import data")

st.sidebar.caption("> New Groundstate")  # show this in the end
