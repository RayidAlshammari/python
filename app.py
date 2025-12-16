"""
Streamlit GUI for CSV Profiler.

This app provides a user-friendly interface for profiling CSV files:
- Upload CSV file
- Preview data
- Generate profile
- View results
- Download JSON and Markdown reports
"""

import sys
from pathlib import Path
from io import StringIO, BytesIO

import streamlit as st

# Add src to Python path to import csv_profiler
sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_profiler.io import read_csv
from csv_profiler.profiling import profile_csv
from csv_profiler.render import to_json, to_markdown


def main() -> None:
    """Main Streamlit application."""

    # Page configuration
    st.set_page_config(
        page_title="CSV Profiler",
        page_icon="📊",
        layout="wide",
    )

    # Title and description
    st.title("📊 CSV Profiler")
    st.markdown(
        "Generate detailed statistical profiles of your CSV files. "
        "Upload a file, preview the data, and download comprehensive reports."
    )

    # Sidebar for file upload
    st.sidebar.header("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file to profile",
    )

    # Initialize session state for profile persistence
    if "profile" not in st.session_state:
        st.session_state.profile = None

    if "csv_data" not in st.session_state:
        st.session_state.csv_data = None

    # Process uploaded file
    if uploaded_file is not None:
        try:
            # Read CSV file
            with st.spinner("Reading CSV file..."):
                # Convert uploaded file to string for read_csv
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                csv_content = stringio.getvalue()

                # Save to temporary file for read_csv function
                temp_path = Path("temp_upload.csv")
                temp_path.write_text(csv_content, encoding="utf-8")

                rows = read_csv(str(temp_path))

                # Clean up temp file
                temp_path.unlink()

            # Store data in session state
            st.session_state.csv_data = rows

            # Display file info
            st.sidebar.success(f"✓ Loaded {len(rows)} rows")

            # Data preview section
            st.header("📋 Data Preview")
            st.markdown("Preview of the first 10 rows of your CSV file:")

            # Convert rows to display format
            if rows:
                st.dataframe(
                    rows[:10],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.warning("The CSV file appears to be empty.")

            # Generate profile button
            st.header("🔍 Generate Profile")

            if st.button("Generate Profile", type="primary", use_container_width=True):
                with st.spinner("Profiling data..."):
                    # Generate profile
                    profile = profile_csv(rows)
                    st.session_state.profile = profile

                st.success("✓ Profile generated successfully!")

        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            st.session_state.csv_data = None
            st.session_state.profile = None

    # Display profile if available
    if st.session_state.profile is not None:
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

        # Create tabs for different views
        tab1, tab2 = st.tabs(["Overview Table", "Detailed View"])

        with tab1:
            # Overview table
            st.markdown("### Quick Overview")
            overview_data = []
            for col in profile["columns"]:
                overview_data.append({
                    "Column": col["name"],
                    "Type": col["type"],
                    "Count": col["count"],
                    "Missing": col["missing"],
                    "Unique": col["unique"],
                })
            st.dataframe(overview_data, use_container_width=True, hide_index=True)

        with tab2:
            # Detailed expandable sections
            st.markdown("### Detailed Statistics")
            for col in profile["columns"]:
                with st.expander(f"**{col['name']}** ({col['type']})"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Count", col["count"])
                        st.metric("Missing", col["missing"])

                    with col2:
                        st.metric("Unique", col["unique"])

                    if col["type"] == "number":
                        # Numeric statistics
                        with col3:
                            st.metric("Min", col.get("min", "N/A"))

                        col4, col5 = st.columns(2)
                        with col4:
                            st.metric("Max", col.get("max", "N/A"))
                        with col5:
                            st.metric("Mean", col.get("mean", "N/A"))

                    else:
                        # Text statistics - top values
                        st.markdown("**Top Values:**")
                        if col.get("top"):
                            top_data = []
                            for item in col["top"]:
                                top_data.append({
                                    "Value": item["value"],
                                    "Count": item["count"],
                                })
                            st.dataframe(top_data, use_container_width=True, hide_index=True)
                        else:
                            st.info("No top values available")

    else:
        # Instructions when no file is uploaded
        if uploaded_file is None:
            st.info("👈 Upload a CSV file using the sidebar to get started!")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**CSV Profiler v1.0.0**  \n"
        "SDAIA Academy Bootcamp Project"
    )


if __name__ == "__main__":
    main()
