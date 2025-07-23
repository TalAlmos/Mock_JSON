import streamlit as st
import sys
import os
import json

# Set Streamlit theme and page config
st.set_page_config(
    page_title="Mock JSON Data Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to sys.path for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from insurance_schemas import get_available_insurance_types
from config import Config
from commands.generate_command import GenerateCommand
from commands.generator_context import GeneratorContext
from factories.generator_factory import GeneratorFactory
from example_analyzer import analyze_examples

# Custom CSS for consistent spacing and modern look
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stButton>button, .stDownloadButton>button {
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-size: 1.1rem;
    }
    .stTextInput>div>input, .stSelectbox>div>div>div {
        border-radius: 6px;
        font-size: 1.05rem;
    }
    .stTable, .stDataFrame {
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mock JSON Data Generator GUI")
st.write("Welcome to the Streamlit interface for generating and analyzing mock insurance data.")

# Sidebar navigation
menu_options = [
    "Generate Data",
    "List Types",
    "Preserve Fields",
    "Analyze Data",
    "Settings",
    "About"
]

st.sidebar.title("Navigation")
selected_menu = st.sidebar.radio("Go to", menu_options)

# Panel display logic
if selected_menu == "Generate Data":
    st.header("Generate Data Panel")
    # Fetch available insurance types from backend
    try:
        insurance_types = get_available_insurance_types()
        selected_type = st.selectbox("Select insurance type", insurance_types)
        num_records = st.number_input("Number of records", min_value=1, max_value=1000, value=10)
        save_separately = st.checkbox("Save each record as a separate file", value=False)
        output_path = st.text_input("Output file or directory", value="data/mock_output/")
        generate_btn = st.button("Generate")
        if generate_btn:
            try:
                # Load config
                config = Config.from_yaml_file("config.yaml") if os.path.exists("config.yaml") else Config()
                # Analyze examples for field profiles
                field_profiles = analyze_examples("data/examples/")
                # Set up factory and context
                factory = GeneratorFactory(config, field_profiles)
                context = GeneratorContext(config)
                context.factory = factory
                # Generate records
                command = GenerateCommand(selected_type, num_records)
                records = command.execute(context)
                # Save output
                if save_separately:
                    base_dir = os.path.join("data", "mock_output", selected_type)
                    os.makedirs(base_dir, exist_ok=True)
                    filenames = []
                    for record in records:
                        file_id = str(st.session_state.get('file_id', 100000000) + len(filenames))
                        file_path = os.path.join(base_dir, f"{file_id}.json")
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(record, f, ensure_ascii=False, indent=2)
                        filenames.append(file_path)
                    st.success(f"Saved {len(filenames)} records to {base_dir}/ as separate files.")
                    st.write("Files:")
                    for fname in filenames:
                        st.write(fname)
                else:
                    # Determine output file path
                    if os.path.isdir(output_path):
                        out_file = os.path.join(output_path, selected_type, "mock.json")
                        os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    else:
                        out_file = output_path
                        os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    with open(out_file, "w", encoding="utf-8") as f:
                        json.dump(records, f, ensure_ascii=False, indent=2)
                    st.success(f"Generated records saved to {out_file}")
                    st.download_button("Download JSON", data=json.dumps(records, ensure_ascii=False, indent=2), file_name=os.path.basename(out_file), mime="application/json")
            except Exception as e:
                st.error(f"Error generating data: {e}")
    except Exception as e:
        st.error(f"Failed to fetch insurance types: {e}")
    st.info("Panel for generating mock insurance data.")
elif selected_menu == "List Types":
    st.header("List Types Panel")
    try:
        # Load config and set up context/factory
        config = Config.from_yaml_file("config.yaml") if os.path.exists("config.yaml") else Config()
        field_profiles = analyze_examples("data/examples/")
        factory = GeneratorFactory(config, field_profiles)
        context = GeneratorContext(config)
        context.factory = factory
        # Fetch types
        from commands.list_types_command import ListTypesCommand
        list_cmd = ListTypesCommand()
        types = list_cmd.execute(context)
        if types:
            st.table([{k: v for k, v in t.items() if k != 'module'} for t in types])
        else:
            st.info("No insurance types found.")
    except Exception as e:
        st.error(f"Failed to fetch insurance types: {e}")
    st.info("Panel for listing supported insurance types.")
elif selected_menu == "Preserve Fields":
    st.header("Preserve Fields Panel")
    try:
        config_path = "config.yaml"
        config = Config.from_yaml_file(config_path) if os.path.exists(config_path) else Config()
        preserve_fields = sorted(config.list_preserve_fields())
        st.subheader("Current Preserve Fields")
        if preserve_fields:
            st.write(preserve_fields)
        else:
            st.info("No preserve fields found in config.")
        # Add new field UI
        new_field = st.text_input("Add a new preserve field", key="add_preserve_field")
        if st.button("Add Field"):
            if new_field:
                if new_field in preserve_fields:
                    st.warning(f"Field '{new_field}' is already in the preserve list.")
                else:
                    try:
                        config.add_preserve_field(new_field)
                        # Save to YAML
                        import yaml
                        with open(config_path, "w", encoding="utf-8") as f:
                            yaml.safe_dump(config.to_dict(), f, allow_unicode=True, sort_keys=False)
                        st.success(f"Added '{new_field}' to preserve fields.")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Failed to add field: {e}")
            else:
                st.warning("Please enter a field name to add.")
        # Remove field UI
        remove_field = st.selectbox("Select a field to remove", preserve_fields, key="remove_preserve_field") if preserve_fields else None
        if preserve_fields and st.button("Remove Field"):
            try:
                config.remove_preserve_field(remove_field)
                # Save to YAML
                import yaml
                with open(config_path, "w", encoding="utf-8") as f:
                    yaml.safe_dump(config.to_dict(), f, allow_unicode=True, sort_keys=False)
                st.success(f"Removed '{remove_field}' from preserve fields.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to remove field: {e}")
    except Exception as e:
        st.error(f"Failed to fetch preserve fields: {e}")
    st.info("Panel for managing preserve fields in config.")
elif selected_menu == "Analyze Data":
    st.header("Analyze Data Panel")
    try:
        if 'analysis_summary' not in st.session_state:
            st.session_state['analysis_summary'] = None
        if st.button("Run Example Data Analysis"):
            from example_analyzer import summarize_examples
            try:
                summary = summarize_examples("data/examples/")
                st.session_state['analysis_summary'] = summary
                st.subheader("Insurance Types Found")
                st.write(summary.get("insurance_types", []))
                st.subheader("Unique Fields")
                st.write(summary.get("fields", []))
                st.subheader("Value Distributions (Top 10)")
                value_distributions = summary.get("value_distributions", {})
                if value_distributions:
                    for field, values in list(value_distributions.items())[:10]:
                        st.write(f"{field}: {values}")
                else:
                    st.info("No value distributions found.")
            except Exception as e:
                st.error(f"Failed to analyze example data: {e}")
        # Export and download button
        if st.session_state.get('analysis_summary'):
            analysis_json = json.dumps(st.session_state['analysis_summary'], ensure_ascii=False, indent=2)
            st.download_button("Download Analysis Report (JSON)", data=analysis_json, file_name="analysis_report.json", mime="application/json")
    except Exception as e:
        st.error(f"Failed to load analysis panel: {e}")
    st.info("Panel for analyzing mock data.")
elif selected_menu == "Settings":
    st.header("Settings Panel")
    try:
        config_path = "config.yaml"
        config = Config.from_yaml_file(config_path) if os.path.exists(config_path) else Config()
        st.subheader("Current Paths and Config")
        st.write({
            "Swagger Path": str(config.swagger_path),
            "Examples Path": str(config.examples_path),
            "Output Path": str(config.output_path),
            "Preserve Fields": sorted(config.list_preserve_fields())
        })
        # Editable inputs
        st.subheader("Edit Settings")
        swagger_path = st.text_input("Swagger Path", value=str(config.swagger_path))
        examples_path = st.text_input("Examples Path", value=str(config.examples_path))
        output_path = st.text_input("Output Path", value=str(config.output_path))
        uploaded_config = st.file_uploader("Upload config.yaml (optional)", type=["yaml"])
        if st.button("Save Settings"):
            try:
                import yaml
                if uploaded_config:
                    # Overwrite config.yaml with uploaded file
                    with open(config_path, "wb") as f:
                        f.write(uploaded_config.read())
                    config = Config.from_yaml_file(config_path)
                else:
                    config.swagger_path = swagger_path
                    config.examples_path = examples_path
                    config.output_path = output_path
                    with open(config_path, "w", encoding="utf-8") as f:
                        yaml.safe_dump(config.to_dict(), f, allow_unicode=True, sort_keys=False)
                # Validate config
                config.validate()
                st.success("Settings saved and validated successfully.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to save or validate settings: {e}")
    except Exception as e:
        st.error(f"Failed to load settings: {e}")
    st.info("Panel for configuring paths and settings.")
elif selected_menu == "About":
    st.header("About Panel")
    st.subheader("Mock JSON Data Generator GUI")
    st.markdown("""
**Version:** 1.0.0  
**Author:** Talal Mosleh  
**GitHub:** [Mock_JSON on GitHub](https://github.com/talalmos/Mock_JSON)  

A modern Streamlit interface for generating, analyzing, and managing mock insurance data for development and testing. Easily create, inspect, and export mock data for a variety of insurance types, with full backend integration and configuration management.
""")
    st.info("Information about the project.")
