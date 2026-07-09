import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Project Alpha",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("📈 Project Alpha")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Run Analysis",
        "Top Stocks",
        "Portfolio",
        "Backtesting",
        "Settings"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if page == "Dashboard":

    st.title("📈 PROJECT ALPHA")

    st.subheader("AI Institutional Investment Committee")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Market Status",
            "Waiting..."
        )

    with col2:
        st.metric(
            "AI Confidence",
            "--"
        )

    with col3:
        st.metric(
            "Stocks Analysed",
            "--"
        )

    st.markdown("---")

    st.header("Today's Summary")

    st.info(
        "Run today's analysis to generate recommendations."
    )

# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------
elif page == "Run Analysis":

    st.title("Run Today's Analysis")

    st.write(
        "Click the button below to run Project Alpha."
    )

    if st.button("🚀 Run Project Alpha"):

        st.success("Analysis Started")

        st.info(
            "Later we will connect this button to your Python engine."
        )

# --------------------------------------------------
# TOP STOCKS
# --------------------------------------------------
elif page == "Top Stocks":

    st.title("Top Ranked Stocks")

    st.info(
        "Stock rankings will appear here."
    )

# --------------------------------------------------
# PORTFOLIO
# --------------------------------------------------
elif page == "Portfolio":

    st.title("Recommended Portfolio")

    st.info(
        "Portfolio allocation will appear here."
    )

# --------------------------------------------------
# BACKTESTING
# --------------------------------------------------
elif page == "Backtesting":

    st.title("Backtesting")

    st.info(
        "Historical performance will appear here."
    )

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------
elif page == "Settings":

    st.title("Settings")

    st.info(
        "Project settings will appear here."
    )
