"""CSV Profiler - Streamlit Web Interface"""

from pathlib import Path
from io import StringIO
import streamlit as st

from csv_profiler.io import read_csv
from csv_profiler.profiling import profile_csv

# Page config
st.set_page_config(page_title="CSV Profiler", page_icon="📊", layout="wide")

# Header
st.title("📊 CSV Profiler")
st.markdown("Generate detailed statistical profiles of your CSV files.")

# Session state
if "profile" not in st.session_state:
    st.session_state.profile = None
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

# Sidebar - File upload
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Process uploaded file
if uploaded_file:
    try:
        with st.spinner("Reading CSV file..."):
            temp_path = Path("temp_upload.csv")
            temp_path.write_text(StringIO(uploaded_file.getvalue().decode("utf-8")).getvalue(), encoding="utf-8")
            rows = read_csv(str(temp_path))
            temp_path.unlink()

        st.session_state.csv_data = rows
        st.sidebar.success(f"✓ Loaded {len(rows)} rows")

        # Data preview
        st.header("📋 Data Preview")
        st.markdown("Preview of the first 10 rows:")
        if rows:
            st.dataframe(rows[:10], use_container_width=True, hide_index=True)
        else:
            st.warning("The CSV file appears to be empty.")

        # Generate profile button
        st.header("🔍 Generate Profile")
        if st.button("Generate Profile", type="primary", use_container_width=True):
            with st.spinner("Profiling data..."):
                st.session_state.profile = profile_csv(rows)
            st.success("✓ Profile generated successfully!")

    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.csv_data = None
        st.session_state.profile = None

# Display profile
if st.session_state.profile:
    profile = st.session_state.profile

    # Summary metrics
    st.header("📈 Summary Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", profile["n_rows"])
    with col2:
        st.metric("Total Columns", profile["n_cols"])

    # Column details
    st.header("📊 Column Details")
    tab1, tab2 = st.tabs(["Overview Table", "Detailed View"])

    with tab1:
        st.markdown("### Quick Overview")
        overview_data = [{"Column": col["name"], "Type": col["type"], "Count": col["count"], "Missing": col["missing"], "Unique": col["unique"]} for col in profile["columns"]]
        st.dataframe(overview_data, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Detailed Statistics")
        for col in profile["columns"]:
            with st.expander(f"**{col['name']}** ({col['type']})"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Count", col["count"])
                    st.metric("Missing", col["missing"])
                with c2:
                    st.metric("Unique", col["unique"])
                if col["type"] == "number":
                    with c3:
                        st.metric("Min", col.get("min", "N/A"))
                    c4, c5 = st.columns(2)
                    with c4:
                        st.metric("Max", col.get("max", "N/A"))
                    with c5:
                        st.metric("Mean", col.get("mean", "N/A"))
                else:
                    st.markdown("**Top Values:**")
                    if col.get("top"):
                        st.dataframe([{"Value": item["value"], "Count": item["count"]} for item in col["top"]], use_container_width=True, hide_index=True)
                    else:
                        st.info("No top values available")
else:
    if not uploaded_file:
        st.info("👈 Upload a CSV file to get started!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**CSV Profiler v1.0.0**  \nSDAIA Academy Bootcamp Project")
