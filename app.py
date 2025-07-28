import streamlit as st
import pandas as pd
import os
import json
import shutil
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Set page config for wide layout
st.set_page_config(page_title="YourCarbonFootprint", page_icon="🌍", layout="wide")

# Initialize session state variables if they don't exist
if "language" not in st.session_state:
    st.session_state.language = "English"
if "emissions_data" not in st.session_state:
    # Load data if exists, otherwise create empty dataframe
    if os.path.exists("data/emissions.json"):
        try:
            with open("data/emissions.json", "r") as f:
                data = f.read().strip()
                if data:  # Check if file is not empty
                    try:
                        st.session_state.emissions_data = pd.DataFrame(json.loads(data))
                    except json.JSONDecodeError:
                        # Create a backup of the corrupted file
                        backup_file = f"data/emissions_backup_{int(time.time())}.json"
                        shutil.copy("data/emissions.json", backup_file)
                        st.warning(
                            f"Corrupted emissions data file found. A backup has been created at {backup_file}"
                        )
                        # Create empty dataframe
                        st.session_state.emissions_data = pd.DataFrame(
                            columns=[
                                "date",
                                "scope",
                                "category",
                                "activity",
                                "quantity",
                                "unit",
                                "emission_factor",
                                "emissions_kgCO2e",
                                "notes",
                            ]
                        )
                else:
                    # Empty file, create new DataFrame
                    st.session_state.emissions_data = pd.DataFrame(
                        columns=[
                            "date",
                            "scope",
                            "category",
                            "activity",
                            "quantity",
                            "unit",
                            "emission_factor",
                            "emissions_kgCO2e",
                            "notes",
                        ]
                    )
        except Exception as e:
            st.error(f"Error loading emissions data: {str(e)}")
            # Create empty dataframe if loading fails
            st.session_state.emissions_data = pd.DataFrame(
                columns=[
                    "date",
                    "scope",
                    "category",
                    "activity",
                    "quantity",
                    "unit",
                    "emission_factor",
                    "emissions_kgCO2e",
                    "notes",
                ]
            )
            # Make sure data directory exists
            os.makedirs("data", exist_ok=True)
    else:
        st.session_state.emissions_data = pd.DataFrame(
            columns=[
                "date",
                "scope",
                "category",
                "activity",
                "quantity",
                "unit",
                "emission_factor",
                "emissions_kgCO2e",
                "notes",
            ]
        )
        # Make sure data directory exists
        os.makedirs("data", exist_ok=True)
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "active_page" not in st.session_state:
    st.session_state.active_page = "AI Insights"

# Translation dictionary
translations = {
    "English": {
        "title": "YourCarbonFootprint",
        "subtitle": "Carbon Accounting & Reporting Tool for SMEs",
        "dashboard": "Dashboard",
        "data_entry": "Data Entry",
        "reports": "Reports",
        "settings": "Settings",
        "about": "About",
        "scope1": "Scope 1 (Direct Emissions)",
        "scope2": "Scope 2 (Indirect Emissions - Purchased Energy)",
        "scope3": "Scope 3 (Other Indirect Emissions)",
        "date": "Date",
        "scope": "Scope",
        "category": "Category",
        "activity": "Activity",
        "quantity": "Quantity",
        "unit": "Unit",
        "emission_factor": "Emission Factor",
        "emissions": "Emissions (kgCO2e)",
        "notes": "Notes",
        "add_entry": "Add Entry",
        "upload_csv": "Upload CSV",
        "download_report": "Download Report",
        "total_emissions": "Total Emissions",
        "emissions_by_scope": "Emissions by Scope",
        "emissions_by_category": "Emissions by Category",
        "emissions_over_time": "Emissions Over Time",
        "language": "Language",
        "save": "Save",
        "cancel": "Cancel",
        "success": "Success!",
        "error": "Error!",
        "entry_added": "Entry added successfully!",
        "csv_uploaded": "CSV uploaded successfully!",
        "report_downloaded": "Report downloaded successfully!",
        "settings_saved": "Settings saved successfully!",
        "no_data": "No data available.",
        "welcome_message": "Welcome to YourCarbonFootprint! Start by adding your emissions data or uploading a CSV file.",
        "custom_category": "Custom Category",
        "custom_activity": "Custom Activity",
        "custom_unit": "Custom Unit",
        "entry_failed": "Failed to add entry.",
    },
    "Hindi": {
        "title": "आपका कार्बन फुटप्रिंट",
        "subtitle": "एसएमई के लिए कार्बन अकाउंटिंग और रिपोर्टिंग टूल",
        "dashboard": "डैशबोर्ड",
        "data_entry": "डेटा प्रविष्टि",
        "reports": "रिपोर्ट",
        "settings": "सेटिंग्स",
        "about": "के बारे में",
        "scope1": "स्कोप 1 (प्रत्यक्ष उत्सर्जन)",
        "scope2": "स्कोप 2 (अप्रत्यक्ष उत्सर्जन - खरीदी गई ऊर्जा)",
        "scope3": "स्कोप 3 (अन्य अप्रत्यक्ष उत्सर्जन)",
        "date": "तारीख",
        "scope": "स्कोप",
        "category": "श्रेणी",
        "activity": "गतिविधि",
        "quantity": "मात्रा",
        "unit": "इकाई",
        "emission_factor": "उत्सर्जन कारक",
        "emissions": "उत्सर्जन (kgCO2e)",
        "notes": "नोट्स",
        "add_entry": "प्रविष्टि जोड़ें",
        "upload_csv": "CSV अपलोड करें",
        "download_report": "रिपोर्ट डाउनलोड करें",
        "total_emissions": "कुल उत्सर्जन",
        "emissions_by_scope": "स्कोप द्वारा उत्सर्जन",
        "emissions_by_category": "श्रेणी द्वारा उत्सर्जन",
        "emissions_over_time": "समय के साथ उत्सर्जन",
        "language": "भाषा",
        "save": "सहेजें",
        "cancel": "रद्द करें",
        "success": "सफलता!",
        "error": "त्रुटि!",
        "entry_added": "प्रविष्टि सफलतापूर्वक जोड़ी गई!",
        "csv_uploaded": "CSV सफलतापूर्वक अपलोड की गई!",
        "report_downloaded": "रिपोर्ट सफलतापूर्वक डाउनलोड की गई!",
        "settings_saved": "सेटिंग्स सफलतापूर्वक सहेजी गईं!",
        "no_data": "कोई डेटा उपलब्ध नहीं है।",
        "welcome_message": "आपका कार्बन फुटप्रिंट में आपका स्वागत है! अपना उत्सर्जन डेटा जोड़कर या CSV फ़ाइल अपलोड करके प्रारंभ करें।",
        "custom_category": "कस्टम श्रेणी",
        "custom_activity": "कस्टम गतिविधि",
        "custom_unit": "कस्टम इकाई",
        "entry_failed": "प्रविष्टि जोड़ने में विफल रहा।",
    },
}


# Function to get translated text
def t(key):
    lang = st.session_state.language
    return translations.get(lang, {}).get(key, key)


# Function to save emissions data
def save_emissions_data():
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Create a backup of the existing file if it exists
        if os.path.exists("data/emissions.json"):
            backup_path = "data/emissions_backup.json"
            try:
                with (
                    open("data/emissions.json", "r") as src,
                    open(backup_path, "w") as dst,
                ):
                    dst.write(src.read())
            except Exception:
                # Continue even if backup fails
                pass

        # Save data to JSON file with proper formatting
        with open("data/emissions.json", "w") as f:
            if len(st.session_state.emissions_data) > 0:
                json.dump(
                    st.session_state.emissions_data.to_dict("records"), f, indent=2
                )
            else:
                # Write empty array if no data
                f.write("[]")

        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


# Function to add new emission entry
def add_emission_entry(
    date,
    business_unit,
    project,
    scope,
    category,
    activity,
    country,
    facility,
    responsible_person,
    quantity,
    unit,
    emission_factor,
    data_quality,
    verification_status,
    notes,
):
    """Add a new emission entry to the emissions data."""
    try:
        # Calculate emissions
        emissions_kgCO2e = float(quantity) * float(emission_factor)

        # Create new entry
        new_entry = pd.DataFrame(
            [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "business_unit": business_unit,
                    "project": project,
                    "scope": scope,
                    "category": category,
                    "activity": activity,
                    "country": country,
                    "facility": facility,
                    "responsible_person": responsible_person,
                    "quantity": float(quantity),
                    "unit": unit,
                    "emission_factor": float(emission_factor),
                    "emissions_kgCO2e": emissions_kgCO2e,
                    "data_quality": data_quality,
                    "verification_status": verification_status,
                    "notes": notes,
                }
            ]
        )

        # Add to existing data
        st.session_state.emissions_data = pd.concat(
            [st.session_state.emissions_data, new_entry], ignore_index=True
        )

        # Save data and return success/failure
        return save_emissions_data()
    except Exception as e:
        st.error(f"Error adding entry: {str(e)}")
        return False


def delete_emission_entry(index):
    try:
        # Make a copy of the current data
        if len(st.session_state.emissions_data) > index:
            # Drop the row at the specified index
            st.session_state.emissions_data = st.session_state.emissions_data.drop(
                index
            ).reset_index(drop=True)

            # Save data and return success/failure
            return save_emissions_data()
        else:
            st.error("Invalid index for deletion")
            return False
    except Exception as e:
        st.error(f"Error deleting entry: {str(e)}")
        return False


# Function to process uploaded CSV
def process_csv(uploaded_file):
    """Process uploaded CSV file and add to emissions data."""
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        required_columns = [
            "date",
            "scope",
            "category",
            "activity",
            "quantity",
            "unit",
            "emission_factor",
        ]

        # Check if all required columns exist
        if not all(col in df.columns for col in required_columns):
            st.error(
                f"CSV must contain all required columns: {', '.join(required_columns)}"
            )
            return False

        # Validate data types
        try:
            # Convert quantity and emission_factor to float
            df["quantity"] = df["quantity"].astype(float)
            df["emission_factor"] = df["emission_factor"].astype(float)

            # Validate dates
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        except Exception as e:
            st.error(f"Data validation error: {str(e)}")
            return False

        # Calculate emissions if not provided
        if "emissions_kgCO2e" not in df.columns:
            df["emissions_kgCO2e"] = df["quantity"] * df["emission_factor"]

        # Add enterprise fields if not present
        enterprise_fields = {
            "business_unit": "Corporate",
            "project": "Not Applicable",
            "country": "India",
            "facility": "",
            "responsible_person": "",
            "data_quality": "Medium",
            "verification_status": "Unverified",
            "notes": "",
        }

        # Add missing columns with default values
        for field, default_value in enterprise_fields.items():
            if field not in df.columns:
                df[field] = default_value

        # Append to existing data
        st.session_state.emissions_data = pd.concat(
            [st.session_state.emissions_data, df], ignore_index=True
        )

        # Save data
        if save_emissions_data():
            st.success(f"Successfully added {len(df)} entries")
            return True
        else:
            st.error("Failed to save data")
            return False
    except Exception as e:
        st.error(f"Error processing CSV: {str(e)}")
        return False


# Function to generate PDF report
def generate_report():
    # Create a BytesIO object
    buffer = BytesIO()

    # Create a simple CSV report for now
    st.session_state.emissions_data.to_csv(buffer, index=False)
    buffer.seek(0)

    return buffer


# Custom CSS
def local_css():
    st.markdown(
        """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #059669;
        --primary-dark: #047857;
        --primary-light: #10b981;
        --secondary-color: #3b82f6;
        --accent-color: #f59e0b;
        --success-color: #22c55e;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --text-light: #9ca3af;
        --background-primary: #ffffff;
        --background-secondary: #f9fafb;
        --background-tertiary: #f3f4f6;
        --border-color: #e5e7eb;
        --border-light: #f3f4f6;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
    }
    
    /* Base styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Main container improvements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Enhanced Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%) !important;
        border-right: none !important;
        min-height: 100vh;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        padding: 2rem 1.5rem;
    }
    
    /* Sidebar brand */
    [data-testid="stSidebar"] h1 {
        color: white !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 14px !important;
        font-weight: 400;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar navigation buttons */
    [data-testid="stSidebar"] .stButton>button {
        width: 100% !important;
        text-align: left !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        padding: 1rem 1.25rem !important;
        margin-bottom: 0.75rem !important;
        border-radius: var(--radius-md) !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255,255,255,0.2) !important;
        border-color: rgba(255,255,255,0.4) !important;
        transform: translateX(4px);
        box-shadow: var(--shadow-md);
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: var(--radius-md) !important;
        color: white !important;
    }
    
    /* Main content headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.875rem !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        color: var(--text-primary) !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        color: var(--text-primary) !important;
    }
    
    /* Enhanced Card styling */
    .stCard, div.stCard {
        background: var(--background-primary) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: var(--shadow-md) !important;
        border: 1px solid var(--border-light) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stCard:hover {
        box-shadow: var(--shadow-lg) !important;
        transform: translateY(-2px);
    }
    
    .stCard::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    /* AI Insights card styling */
    .stCard p {
        margin-bottom: 1rem;
        line-height: 1.7;
        color: var(--text-primary);
    }
    
    .stCard h1, .stCard h2, .stCard h3, .stCard h4 {
        color: var(--primary-color) !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stCard ul, .stCard ol {
        margin-left: 1.5rem;
        margin-bottom: 1.5rem;
        color: var(--text-primary);
    }
    
    .stCard li {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    .stCard table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1.5rem;
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    .stCard th, .stCard td {
        border: none;
        padding: 1rem;
        text-align: left;
    }
    
    .stCard th {
        background: var(--background-secondary);
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .stCard td {
        border-bottom: 1px solid var(--border-light);
    }
    
    /* Enhanced Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--background-primary) 0%, var(--background-secondary) 100%);
        border-radius: var(--radius-xl);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-light);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        opacity: 0.8;
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white !important;
        border-radius: var(--radius-md);
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-md);
        text-transform: none;
        letter-spacing: 0.025em;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-md);
    }
    
    .stButton>button:focus {
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.3);
        outline: none;
    }
    
    /* Secondary buttons */
    .stButton>button[kind="secondary"] {
        background: var(--background-primary);
        color: var(--primary-color) !important;
        border: 2px solid var(--primary-color);
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: var(--primary-color);
        color: white !important;
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--background-secondary);
        padding: 0.5rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--radius-md);
        padding: 0.875rem 1.5rem;
        font-weight: 500;
        color: var(--text-secondary);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.8);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
    }
    
    /* Enhanced Info boxes */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
        border-left: 4px solid var(--secondary-color);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid var(--warning-color);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .success-box {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid var(--success-color);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    /* Enhanced Form fields */
    [data-baseweb="input"], [data-baseweb="textarea"] {
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--border-color) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    [data-baseweb="input"]:focus, [data-baseweb="textarea"]:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1) !important;
    }
    
    /* Enhanced Selectbox */
    [data-baseweb="select"] {
        border-radius: var(--radius-md) !important;
    }
    
    /* Enhanced Dataframe styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
        margin: 2rem 0;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        font-weight: 600;
        text-align: left;
        padding: 1rem;
        border: none;
    }
    
    .dataframe td {
        padding: 1rem;
        border-bottom: 1px solid var(--border-light);
        background: var(--background-primary);
    }
    
    .dataframe tr:hover td {
        background: var(--background-secondary);
    }
    
    .dataframe tr:last-child td {
        border-bottom: none;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* Progress bars */
    .stProgress .st-bo {
        background-color: var(--primary-color) !important;
    }
    
    /* Enhanced alerts */
    .stAlert {
        border-radius: var(--radius-lg) !important;
        border: none !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Enhanced Responsive design improvements */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.25rem !important;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .stCard {
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Mobile navigation adjustments */
        [data-testid="stSidebar"] .stButton>button {
            padding: 0.75rem 1rem !important;
            font-size: 14px !important;
        }
        
        /* Form improvements on mobile */
        [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
        
        /* Chart height adjustments */
        .js-plotly-plot {
            height: 300px !important;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.75rem;
        }
        
        .stCard {
            padding: 1rem !important;
        }
        
        /* Stack columns on very small screens */
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem;
            font-size: 14px;
        }
    }
    
    /* Footer enhancement */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: rgba(255,255,255,0.8);
        font-size: 12px;
        margin-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.2);
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: var(--radius-md);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--text-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .slide-in {
        animation: slideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# Navigation component
def render_navigation():
    nav_items = [
        {"icon": "🤖", "label": "AI Insights", "id": "AI Insights"},
        {"icon": "📝", "label": "Data Entry", "id": "Data Entry"},
        {"icon": "📊", "label": "Dashboard", "id": "Dashboard"},
        {"icon": "⚙️", "label": "Settings", "id": "Settings"},
    ]

    st.markdown("### Navigation")

    for item in nav_items:
        active_class = "active" if st.session_state.active_page == item["id"] else ""
        if st.sidebar.button(
            f"{item['icon']} {item['label']}",
            key=f"nav_{item['id']}",
            help=f"Go to {item['label']}",
            use_container_width=True,
        ):
            st.session_state.active_page = item["id"]
            st.rerun()


# Enhanced metric card component
def metric_card(
    title,
    value,
    description=None,
    icon=None,
    prefix="",
    suffix="",
    trend=None,
    color_scheme="primary",
):
    """Enhanced metric card with animations and trend indicators."""
    trend_html = ""
    if trend:
        trend_icon = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
        trend_color = "#22c55e" if trend > 0 else "#ef4444" if trend < 0 else "#6b7280"
        trend_html = f'<div style="font-size: 12px; color: {trend_color}; margin-top: 0.5rem;">{trend_icon} {abs(trend):.1f}% vs last period</div>'

    color_schemes = {
        "primary": "var(--primary-color)",
        "secondary": "var(--secondary-color)",
        "success": "var(--success-color)",
        "warning": "var(--warning-color)",
        "accent": "var(--accent-color)",
    }

    border_color = color_schemes.get(color_scheme, color_schemes["primary"])

    st.markdown(
        f"""
    <div class="metric-card fade-in" style="border-left: 4px solid {border_color};">
        {f'<div class="metric-icon">{icon}</div>' if icon else ''}
        <div class="metric-label">{title}</div>
        <div class="metric-value">{prefix}{value}{suffix}</div>
        {f'<div style="color: var(--text-secondary); font-size: 13px; margin-top: 0.5rem;">{description}</div>' if description else ''}
        {trend_html}
    </div>
    """,
        unsafe_allow_html=True,
    )


# Card component
def card(content, title=None):
    if title:
        st.markdown(
            f"<div class='stCard'><h3>{title}</h3>{content}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"<div class='stCard'>{content}</div>", unsafe_allow_html=True)


# Apply custom CSS
local_css()

# Sidebar
with st.sidebar:
    st.markdown(
        f"<h1 style='margin-bottom: 0; font-size: 24px;'>{t('title')}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='margin-top: 0; color: #aaa; font-size: 12px;'>{t('subtitle')}</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # Language selector
    language = st.selectbox(t("language"), ["English", "Hindi"])
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

    st.divider()

    # Navigation
    render_navigation()

    st.divider()

    # Footer
    st.markdown(
        "<div class='footer' style='color: #555555;'> 2025 YourCarbonFootprint<br>Product Owner: Sonu Kumar<br>sonu@aianytime.net</div>",
        unsafe_allow_html=True,
    )

# Main content
if st.session_state.active_page == "Dashboard":
    st.markdown(f"<h1 class='fade-in'>🌍 {t('dashboard')}</h1>", unsafe_allow_html=True)

    if len(st.session_state.emissions_data) == 0:
        st.markdown(
            f"""
            <div class='info-box fade-in'>
                <h3 style='margin-top: 0; color: var(--secondary-color);'>🚀 Welcome to YourCarbonFootprint!</h3>
                <p>{t('welcome_message')}</p>
                <p>Ready to start tracking your carbon emissions? Use the navigation menu to:</p>
                <ul>
                    <li><strong>Data Entry</strong> - Add your first emission record</li>
                    <li><strong>AI Insights</strong> - Get help from our AI assistant</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show sample data visualization even with no data
        st.markdown(
            "<h2 class='fade-in'>📈 Sample Dashboard Preview</h2>",
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card(
                title="Total Emissions",
                value="0.00",
                suffix=" kgCO2e",
                icon="🌍",
                description="Start adding data to see your footprint",
                color_scheme="primary",
            )
        with col2:
            metric_card(
                title="Latest Entry",
                value="No data",
                icon="📅",
                description="Add your first emission record",
                color_scheme="secondary",
            )
        with col3:
            metric_card(
                title="Total Entries",
                value="0",
                icon="📊",
                description="Number of emission records",
                color_scheme="accent",
            )
        with col4:
            metric_card(
                title="Reduction Target",
                value="Set Goal",
                icon="🎯",
                description="Define your reduction target",
                color_scheme="success",
            )
    else:
        # Calculate metrics
        # Ensure emissions_kgCO2e is numeric
        st.session_state.emissions_data["emissions_kgCO2e"] = pd.to_numeric(
            st.session_state.emissions_data["emissions_kgCO2e"], errors="coerce"
        )

        # Replace NaN with 0
        st.session_state.emissions_data["emissions_kgCO2e"].fillna(0, inplace=True)

        total_emissions = st.session_state.emissions_data["emissions_kgCO2e"].sum()

        # Calculate additional metrics
        df = st.session_state.emissions_data.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Current month emissions
        current_month = datetime.now().replace(day=1)
        current_month_data = df[df["date"] >= current_month]
        current_month_emissions = (
            current_month_data["emissions_kgCO2e"].sum()
            if len(current_month_data) > 0
            else 0
        )

        # Previous month for comparison
        previous_month = current_month - pd.DateOffset(months=1)
        previous_month_data = df[
            (df["date"] >= previous_month) & (df["date"] < current_month)
        ]
        previous_month_emissions = (
            previous_month_data["emissions_kgCO2e"].sum()
            if len(previous_month_data) > 0
            else 0
        )

        # Calculate trend
        trend = None
        if previous_month_emissions > 0:
            trend = (
                (current_month_emissions - previous_month_emissions)
                / previous_month_emissions
            ) * 100

        # Average monthly emissions
        if len(df) > 0:
            df["month"] = df["date"].dt.to_period("M")
            monthly_avg = df.groupby("month")["emissions_kgCO2e"].sum().mean()
        else:
            monthly_avg = 0

        # Display enhanced metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card(
                title=t("total_emissions"),
                value=f"{total_emissions:.2f}",
                suffix=" kgCO2e",
                icon="🌍",
                description="Lifetime carbon footprint",
                color_scheme="primary",
            )
        with col2:
            metric_card(
                title="This Month",
                value=f"{current_month_emissions:.2f}",
                suffix=" kgCO2e",
                icon="📅",
                description="Current month emissions",
                trend=trend,
                color_scheme="secondary",
            )
        with col3:
            metric_card(
                title="Monthly Average",
                value=f"{monthly_avg:.2f}",
                suffix=" kgCO2e",
                icon="📊",
                description="Average per month",
                color_scheme="accent",
            )
        with col4:
            entry_count = len(st.session_state.emissions_data)
            # Calculate carbon intensity (emissions per entry)
            intensity = total_emissions / entry_count if entry_count > 0 else 0
            metric_card(
                title="Carbon Intensity",
                value=f"{intensity:.2f}",
                suffix=" kgCO2e",
                icon="⚡",
                description=f"Per entry ({entry_count} total)",
                color_scheme="warning",
            )

        # Enhanced Charts Section
        st.markdown(
            f"<h2 class='fade-in'>📊 {t('emissions_by_scope')}</h2>",
            unsafe_allow_html=True,
        )

        # Check if there are any non-zero emissions before creating charts
        if total_emissions > 0:
            # Create scope data for pie chart
            scope_data = (
                st.session_state.emissions_data.groupby("scope")["emissions_kgCO2e"]
                .sum()
                .reset_index()
            )

            # Only create chart if we have data with emissions
            if not scope_data.empty and scope_data["emissions_kgCO2e"].sum() > 0:
                col_chart, col_summary = st.columns([2, 1])

                with col_chart:
                    fig1 = px.pie(
                        scope_data,
                        values="emissions_kgCO2e",
                        names="scope",
                        color="scope",
                        color_discrete_map={
                            "Scope 1": "#059669",
                            "Scope 2": "#3b82f6",
                            "Scope 3": "#f59e0b",
                        },
                        hole=0.5,
                        title="Emissions Distribution by Scope",
                    )
                    fig1.update_traces(
                        textposition="auto",
                        textinfo="percent+label",
                        hovertemplate="<b>%{label}</b><br>Emissions: %{value:.2f} kgCO2e<br>Percentage: %{percent}<extra></extra>",
                        textfont_size=12,
                        marker=dict(line=dict(color="#ffffff", width=2)),
                    )
                    fig1.update_layout(
                        margin=dict(t=60, b=40, l=40, r=40),
                        legend=dict(
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.05,
                        ),
                        height=450,
                        font=dict(family="Inter, sans-serif", size=12),
                        title=dict(font=dict(size=16, color="#111827"), x=0.5),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(
                        fig1, use_container_width=True, config={"displayModeBar": False}
                    )

                with col_summary:
                    st.markdown("#### Scope Breakdown")
                    for _, row in scope_data.iterrows():
                        percentage = (row["emissions_kgCO2e"] / total_emissions) * 100
                        color = {
                            "Scope 1": "#059669",
                            "Scope 2": "#3b82f6",
                            "Scope 3": "#f59e0b",
                        }.get(row["scope"], "#6b7280")
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 1rem; padding: 1rem; background: var(--background-secondary); border-radius: var(--radius-md); border-left: 4px solid {color};">
                                <div style="font-weight: 600; color: var(--text-primary);">{row["scope"]}</div>
                                <div style="font-size: 1.25rem; font-weight: 700; color: {color};">{row["emissions_kgCO2e"]:.2f} kgCO2e</div>
                                <div style="font-size: 0.875rem; color: var(--text-secondary);">{percentage:.1f}% of total</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.markdown(
                    """
                    <div class='info-box'>
                        <h4 style='margin-top: 0;'>📊 No Scope Data Available</h4>
                        <p>Add emission entries to see scope breakdown visualization.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class='info-box'>
                    <h4 style='margin-top: 0;'>📊 No Emissions Data</h4>
                    <p>Start adding emission data to see your scope breakdown!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Enhanced Category and Time Series Charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"<h3 class='slide-in'>📈 {t('emissions_by_category')}</h3>",
                unsafe_allow_html=True,
            )

            if total_emissions > 0:
                # Create category data for bar chart
                category_data = (
                    st.session_state.emissions_data.groupby("category")[
                        "emissions_kgCO2e"
                    ]
                    .sum()
                    .reset_index()
                )
                category_data = category_data.sort_values(
                    "emissions_kgCO2e", ascending=False
                )

                # Only create chart if we have data with emissions
                if (
                    not category_data.empty
                    and category_data["emissions_kgCO2e"].sum() > 0
                ):
                    # Take top 8 categories to avoid clutter
                    top_categories = category_data.head(8)

                    fig2 = px.bar(
                        top_categories,
                        x="emissions_kgCO2e",
                        y="category",
                        orientation="h",
                        color="emissions_kgCO2e",
                        color_continuous_scale="Viridis",
                        labels={
                            "emissions_kgCO2e": "Emissions (kgCO2e)",
                            "category": "Category",
                        },
                        title="Top Emission Categories",
                    )
                    fig2.update_traces(
                        hovertemplate="<b>%{y}</b><br>Emissions: %{x:.2f} kgCO2e<extra></extra>",
                        texttemplate="%{x:.1f}",
                        textposition="outside",
                    )
                    fig2.update_layout(
                        showlegend=False,
                        margin=dict(t=60, b=40, l=40, r=40),
                        height=450,
                        font=dict(family="Inter, sans-serif", size=12),
                        title=dict(font=dict(size=16, color="#111827"), x=0.5),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
                        yaxis=dict(showgrid=False),
                        coloraxis_colorbar=dict(title="kgCO2e"),
                    )
                    st.plotly_chart(
                        fig2, use_container_width=True, config={"displayModeBar": False}
                    )
                else:
                    st.markdown(
                        """
                        <div class='info-box'>
                            <h5 style='margin-top: 0;'>📊 No Category Data</h5>
                            <p>Add emission entries to see category breakdown.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    """
                    <div class='info-box'>
                        <h5 style='margin-top: 0;'>📊 No Category Data</h5>
                        <p>Start adding data to see category breakdown!</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown(
                f"<h3 class='slide-in'>📅 {t('emissions_over_time')}</h3>",
                unsafe_allow_html=True,
            )

            if (
                total_emissions > 0
                and "date" in st.session_state.emissions_data.columns
            ):
                # Convert date column to datetime
                time_data = st.session_state.emissions_data.copy()
                time_data["date"] = pd.to_datetime(time_data["date"], errors="coerce")

                # Filter out rows with invalid dates
                time_data = time_data.dropna(subset=["date"])

                if not time_data.empty:
                    # Create month column for aggregation
                    time_data["month"] = time_data["date"].dt.strftime("%Y-%m")

                    # Group by month and scope
                    monthly_data = (
                        time_data.groupby(["month", "scope"])["emissions_kgCO2e"]
                        .sum()
                        .reset_index()
                    )

                    if len(monthly_data["month"].unique()) > 0:
                        # Create enhanced line chart
                        fig3 = px.line(
                            monthly_data,
                            x="month",
                            y="emissions_kgCO2e",
                            color="scope",
                            markers=True,
                            color_discrete_map={
                                "Scope 1": "#059669",
                                "Scope 2": "#3b82f6",
                                "Scope 3": "#f59e0b",
                            },
                            labels={
                                "emissions_kgCO2e": "Emissions (kgCO2e)",
                                "month": "Month",
                                "scope": "Scope",
                            },
                            title="Monthly Emissions Trend",
                        )
                        fig3.update_traces(
                            line=dict(width=3),
                            marker=dict(size=8, line=dict(width=2, color="white")),
                            hovertemplate="<b>%{fullData.name}</b><br>Month: %{x}<br>Emissions: %{y:.2f} kgCO2e<extra></extra>",
                        )
                        fig3.update_layout(
                            margin=dict(t=60, b=40, l=40, r=40),
                            xaxis_title="Month",
                            yaxis_title="Emissions (kgCO2e)",
                            legend_title="Scope",
                            height=450,
                            font=dict(family="Inter, sans-serif", size=12),
                            title=dict(font=dict(size=16, color="#111827"), x=0.5),
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
                            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="center",
                                x=0.5,
                            ),
                        )
                        st.plotly_chart(
                            fig3,
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    else:
                        st.markdown(
                            """
                            <div class='info-box'>
                                <h5 style='margin-top: 0;'>📈 Limited Time Data</h5>
                                <p>Add more entries over time to see trends.</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        """
                        <div class='info-box'>
                            <h5 style='margin-top: 0;'>📅 No Date Data</h5>
                            <p>Ensure your entries have valid dates.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    """
                    <div class='info-box'>
                        <h5 style='margin-top: 0;'>📅 No Time Series Data</h5>
                        <p>Add emission data to see trends over time!</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

elif st.session_state.active_page == "Data Entry":
    st.markdown(
        f"<h1 class='fade-in'>📝 {t('data_entry')}</h1>", unsafe_allow_html=True
    )

    # Enhanced introduction
    st.markdown(
        """
        <div class='success-box slide-in'>
            <h4 style='margin-top: 0; color: var(--success-color);'>✨ Smart Data Entry</h4>
            <p>Our intelligent form helps you accurately categorize emissions with AI-powered suggestions and validation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["🖊️ Manual Entry", "📁 CSV Upload"])

    with tabs[0]:
        st.markdown(
            """
            <div class='stCard fade-in'>
                <h3 style='margin-top: 0; color: var(--primary-color);'>🌟 Add New Emission Entry</h3>
                <p style='color: var(--text-secondary); margin-bottom: 2rem;'>Fill in the details below to add a new emission record. Required fields are marked with *</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("emission_form", border=False, clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input(
                    t("date"), datetime.now(), help="Date when the emission occurred"
                )

                # Add business unit field for enterprise tracking with tooltip
                business_unit = st.selectbox(
                    "Business Unit",
                    [
                        "Corporate",
                        "Manufacturing",
                        "Sales",
                        "R&D",
                        "Logistics",
                        "IT",
                        "Other",
                    ],
                    help="The business unit responsible for this emission",
                )
                if business_unit == "Other":
                    business_unit = st.text_input(
                        "Custom Business Unit", placeholder="Enter business unit name"
                    )

                # Add project field for better categorization with tooltip
                project = st.selectbox(
                    "Project",
                    [
                        "Not Applicable",
                        "Carbon Reduction Initiative",
                        "Sustainability Program",
                        "Operational",
                        "Other",
                    ],
                    help="The project or initiative associated with this emission",
                )
                if project == "Other":
                    project = st.text_input(
                        "Custom Project", placeholder="Enter project name"
                    )

                # Add scope selection with tooltip explaining each scope
                scope = st.selectbox(
                    t("scope"),
                    ["Scope 1", "Scope 2", "Scope 3"],
                    help="Scope 1: Direct emissions from owned sources\nScope 2: Indirect emissions from purchased energy\nScope 3: All other indirect emissions in value chain",
                )
                category_options = {
                    "Scope 1": [
                        "Stationary Combustion",
                        "Mobile Combustion",
                        "Fugitive Emissions",
                        "Process Emissions",
                        "Other",
                    ],
                    "Scope 2": ["Electricity", "Steam", "Heating", "Cooling", "Other"],
                    "Scope 3": [
                        "Purchased Goods and Services",
                        "Capital Goods",
                        "Fuel- and Energy-Related Activities",
                        "Upstream Transportation and Distribution",
                        "Waste Generated in Operations",
                        "Business Travel",
                        "Employee Commuting",
                        "Upstream Leased Assets",
                        "Downstream Transportation and Distribution",
                        "Processing of Sold Products",
                        "Use of Sold Products",
                        "End-of-Life Treatment of Sold Products",
                        "Downstream Leased Assets",
                        "Franchises",
                        "Investments",
                        "Other",
                    ],
                }
                category = st.selectbox(
                    t("category"),
                    category_options[scope],
                    help="The category of emission source",
                )
                if category == "Other":
                    category = st.text_input(
                        t("custom_category"), placeholder="Enter custom category"
                    )

                # Enhanced location tracking with facility details and tooltips
                country_options = [
                    "India",
                    "United States",
                    "United Kingdom",
                    "Japan",
                    "Indonesia",
                    "Other",
                ]
                country = st.selectbox(
                    "Country",
                    country_options,
                    help="Country where the emission occurred",
                )
                if country == "Other":
                    country = st.text_input(
                        "Custom Country", placeholder="Enter country name"
                    )

                # Add facility/location field with tooltip
                facility = st.text_input(
                    "Facility/Location",
                    placeholder="e.g., Mumbai HQ, Jakarta Plant 2, etc.",
                    help="Specific facility or location where the emission occurred",
                )

                # Add responsible person field with tooltip
                responsible_person = st.text_input(
                    "Responsible Person",
                    placeholder="Person responsible for this emission source",
                    help="Name of the person accountable for managing this emission source",
                )
            with col2:
                activity_options = {
                    "Stationary Combustion": [
                        "Boiler",
                        "Furnace",
                        "Generator",
                        "Other",
                    ],
                    "Mobile Combustion": [
                        "Company Vehicle",
                        "Fleet Vehicle",
                        "Machinery",
                        "Other",
                    ],
                    "Fugitive Emissions": [
                        "Refrigerant Leak",
                        "SF6 Emissions",
                        "Other",
                    ],
                    "Process Emissions": [
                        "Cement Production",
                        "Chemical Production",
                        "Other",
                    ],
                    "Electricity": [
                        "Office Electricity",
                        "Manufacturing Electricity",
                        "Other",
                    ],
                    "Steam": ["Industrial Steam", "Heating Steam", "Other"],
                    "Heating": ["Office Heating", "Industrial Heating", "Other"],
                    "Cooling": ["Office Cooling", "Industrial Cooling", "Other"],
                    "Purchased Goods and Services": [
                        "Raw Materials",
                        "Office Supplies",
                        "Other",
                    ],
                    "Capital Goods": [
                        "Equipment Purchase",
                        "Vehicle Purchase",
                        "Other",
                    ],
                    "Fuel- and Energy-Related Activities": [
                        "Upstream Fuel Production",
                        "Transmission Losses",
                        "Other",
                    ],
                    "Upstream Transportation and Distribution": [
                        "Supplier Transport",
                        "Inbound Logistics",
                        "Other",
                    ],
                    "Waste Generated in Operations": [
                        "Solid Waste",
                        "Wastewater",
                        "Other",
                    ],
                    "Business Travel": [
                        "Air Travel",
                        "Ground Travel",
                        "Hotel Stays",
                        "Other",
                    ],
                    "Employee Commuting": [
                        "Private Vehicle",
                        "Public Transport",
                        "Other",
                    ],
                    "Upstream Leased Assets": [
                        "Leased Equipment",
                        "Leased Vehicles",
                        "Other",
                    ],
                    "Downstream Transportation and Distribution": [
                        "Outbound Logistics",
                        "Customer Transport",
                        "Other",
                    ],
                    "Processing of Sold Products": [
                        "Intermediate Processing",
                        "Final Assembly",
                        "Other",
                    ],
                    "Use of Sold Products": [
                        "Product Operation",
                        "Energy Consumption",
                        "Other",
                    ],
                    "End-of-Life Treatment of Sold Products": [
                        "Recycling",
                        "Landfill",
                        "Other",
                    ],
                    "Downstream Leased Assets": [
                        "Leased Equipment",
                        "Leased Property",
                        "Other",
                    ],
                    "Franchises": [
                        "Franchise Operations",
                        "Franchise Energy Use",
                        "Other",
                    ],
                    "Investments": [
                        "Investment Emissions",
                        "Financed Emissions",
                        "Other",
                    ],
                    "Other": ["Custom Activity", "Other"],
                }
                activity_key = category if category != "Other" else "Other"
                activity_list = activity_options.get(
                    activity_key, ["Custom Activity", "Other"]
                )
                activity = st.selectbox(
                    "Activity",
                    activity_options.get(category, ["Other"]),
                    help="Specific activity that generated the emissions",
                )
                if activity == "Other":
                    activity = st.text_input(
                        "Custom Activity", placeholder="Enter custom activity"
                    )

                # Add validation for quantity with tooltip
                quantity = st.number_input(
                    t("quantity"),
                    min_value=0.0,
                    format="%.2f",
                    help="The amount of activity (e.g., kWh used, liters consumed, etc.)",
                )

                # Enhanced unit selection with tooltip
                unit_options = [
                    "kWh",
                    "MWh",
                    "GJ",
                    "liter",
                    "gallon",
                    "kg",
                    "tonne",
                    "km",
                    "mile",
                    "hour",
                    "day",
                    "piece",
                    "USD",
                    "Other",
                ]
                unit = st.selectbox(
                    t("unit"),
                    unit_options,
                    help="The unit of measurement for the quantity",
                )
                if unit == "Other":
                    unit = st.text_input(
                        t("custom_unit"), placeholder="Enter custom unit"
                    )

                # Emission factor auto-population based on country and category
                emission_factors = {
                    "India": {
                        "Electricity": 0.82,
                        "Mobile Combustion": 2.31,
                        "Stationary Combustion": 1.85,
                        "Other": 0.0,
                    },
                    "United States": {
                        "Electricity": 0.42,
                        "Mobile Combustion": 2.32,
                        "Stationary Combustion": 2.01,
                        "Business Travel": 0.12,
                        "Employee Commuting": 0.15,
                    },
                }
                default_factor = (
                    emission_factors.get(country, {}).get(category, 0.0)
                    if country != "Other"
                    else 0.0
                )

                # Now that default_factor is defined, show AI suggestion
                st.info(
                    f"💡 AI Suggestion: Based on your selections, a typical emission factor for {category} in {country} would be around {default_factor:.4f} kgCO2e per unit."
                )

                emission_factor = st.number_input(
                    t("emission_factor"),
                    min_value=0.0,
                    value=default_factor,
                    format="%.4f",
                    help=f"Emission factor in kgCO2e per unit. Typical range: {max(0.1, default_factor*0.8):.4f} to {default_factor*1.2:.4f}",
                )

                # Add data quality indicator with color-coded help
                data_quality = st.select_slider(
                    "Data Quality",
                    options=["Low", "Medium", "High"],
                    value="Medium",
                    help="🔴 Low: Estimated or proxy data\n🟡 Medium: Calculated from bills or invoices\n🟢 High: Directly measured or metered data",
                )

                # Add verification status with detailed help
                verification_status = st.selectbox(
                    "Verification Status",
                    ["Unverified", "Internally Verified", "Third-Party Verified"],
                    help="Unverified: No verification process applied\nInternally Verified: Checked by internal team\nThird-Party Verified: Validated by external auditor",
                )

                # Enhanced notes field with better guidance
                notes = st.text_area(
                    t("notes"),
                    placeholder="Additional information, data sources, calculation methods, etc.",
                    help="Include information about data sources, calculation methodology, assumptions made, and any other relevant context",
                )

                # Add cost field for financial impact tracking (optional)
                cost = st.number_input(
                    "Cost (Optional)",
                    min_value=0.0,
                    value=0.0,
                    format="%.2f",
                    help="Optional: Associated cost in your local currency",
                )

                # Add cost currency if cost is entered
                if cost > 0:
                    currency = st.selectbox(
                        "Currency",
                        ["USD", "EUR", "INR", "GBP", "JPY", "Other"],
                        help="Currency for the entered cost",
                    )

            # Enhanced form submission section
            st.markdown(
                "<hr style='margin: 2rem 0; border: 1px solid var(--border-light);'>",
                unsafe_allow_html=True,
            )

            # Form validation preview
            emissions_preview = (
                quantity * emission_factor
                if quantity > 0 and emission_factor > 0
                else 0
            )
            if emissions_preview > 0:
                st.markdown(
                    f"""
                    <div style='background: var(--background-secondary); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1rem;'>
                        <h4 style='margin: 0; color: var(--primary-color);'>📊 Emission Preview</h4>
                        <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'><strong>{emissions_preview:.2f} kgCO2e</strong> will be added to your footprint</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                submitted = st.form_submit_button(
                    "🚀 " + t("add_entry"), type="primary", use_container_width=True
                )
            with col2:
                clear = st.form_submit_button(
                    "🔄 Clear Form", type="secondary", use_container_width=True
                )
            with col3:
                save_draft = st.form_submit_button(
                    "💾 Save Draft", use_container_width=True
                )

            if submitted:
                # Enhanced validation with progress indicator
                validation_errors = []

                if quantity <= 0:
                    validation_errors.append("⚠️ Quantity must be greater than zero")
                if emission_factor <= 0:
                    validation_errors.append(
                        "⚠️ Emission factor must be greater than zero"
                    )
                if not activity or not activity.strip():
                    validation_errors.append("⚠️ Activity description is required")

                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        status_text.text("🔍 Validating data...")
                        progress_bar.progress(25)

                        status_text.text("💾 Saving entry...")
                        progress_bar.progress(50)

                        # Include cost in the entry if provided
                        cost_value = cost if "cost" in locals() and cost > 0 else 0.0
                        currency_value = (
                            currency if "currency" in locals() and cost > 0 else ""
                        )

                        progress_bar.progress(75)

                        success = add_emission_entry(
                            date,
                            business_unit,
                            project,
                            scope,
                            category,
                            activity,
                            country,
                            facility,
                            responsible_person,
                            quantity,
                            unit,
                            emission_factor,
                            data_quality,
                            verification_status,
                            notes,
                        )

                        progress_bar.progress(100)
                        status_text.text("✅ Entry added successfully!")

                        if success:
                            st.success(
                                f"""
                                🎉 **{t('entry_added')}**
                                
                                **{emissions_preview:.2f} kgCO2e** has been added to your carbon footprint.
                                """
                            )

                            # Auto-redirect after delay
                            import time

                            time.sleep(2)
                            st.session_state.active_page = "Dashboard"
                            st.rerun()
                        else:
                            st.error("❌ Failed to save entry. Please try again.")

                    except Exception as e:
                        progress_bar.progress(0)
                        status_text.text("")
                        st.error(f"❌ {t('entry_failed')} {str(e)}")

            elif save_draft:
                # Save form data to session state for later
                st.session_state.draft_entry = {
                    "date": date,
                    "business_unit": business_unit,
                    "project": project,
                    "scope": scope,
                    "category": category,
                    "activity": activity,
                    "country": country,
                    "facility": facility,
                    "responsible_person": responsible_person,
                    "quantity": quantity,
                    "unit": unit,
                    "emission_factor": emission_factor,
                    "data_quality": data_quality,
                    "verification_status": verification_status,
                    "notes": notes,
                }
                st.info("💾 Draft saved! You can return to complete this entry later.")

    # Show existing data table
    if len(st.session_state.emissions_data) > 0:
        st.markdown("<h3>Existing Emissions Data</h3>", unsafe_allow_html=True)

        # Create a copy of the dataframe with an action column
        display_df = st.session_state.emissions_data.copy()

        # Add a column for the delete action
        col1, col2 = st.columns([3, 1])

        with col1:
            # Display the dataframe
            st.dataframe(
                display_df,
                column_config={
                    "date": st.column_config.DateColumn("Date"),
                    "business_unit": st.column_config.TextColumn("Business Unit"),
                    "project": st.column_config.TextColumn("Project"),
                    "scope": st.column_config.TextColumn("Scope"),
                    "category": st.column_config.TextColumn("Category"),
                    "activity": st.column_config.TextColumn("Activity"),
                    "country": st.column_config.TextColumn("Country"),
                    "facility": st.column_config.TextColumn("Facility"),
                    "responsible_person": st.column_config.TextColumn(
                        "Responsible Person"
                    ),
                    "quantity": st.column_config.NumberColumn(
                        "Quantity", format="%.2f"
                    ),
                    "unit": st.column_config.TextColumn("Unit"),
                    "emission_factor": st.column_config.NumberColumn(
                        "Emission Factor", format="%.4f"
                    ),
                    "emissions_kgCO2e": st.column_config.NumberColumn(
                        "Emissions (kgCO2e)", format="%.2f"
                    ),
                    "data_quality": st.column_config.TextColumn("Data Quality"),
                    "verification_status": st.column_config.TextColumn("Verification"),
                    "notes": st.column_config.TextColumn("Notes"),
                },
                use_container_width=True,
                hide_index=False,
            )

        with col2:
            # Add delete functionality
            st.markdown("### Delete Entry")
            entry_to_delete = st.number_input(
                "Select entry number to delete",
                min_value=0,
                max_value=len(display_df) - 1 if len(display_df) > 0 else 0,
                step=1,
                help="Enter the index number of the entry you want to delete",
            )

            if st.button("🗑️ Delete Selected Entry", type="primary"):
                if delete_emission_entry(entry_to_delete):
                    st.success(f"Entry {entry_to_delete} deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to delete entry {entry_to_delete}")

    with tabs[1]:
        st.markdown("<h3>Upload CSV File</h3>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(t("upload_csv"), type="csv")
        if uploaded_file is not None:
            if process_csv(uploaded_file):
                st.success(t("csv_uploaded"))
                # Redirect to Dashboard after successful upload
                st.session_state.active_page = "Dashboard"
                st.rerun()
            else:
                st.error("Failed to process CSV file. Please check the format.")

        # Sample CSV download with enterprise-grade fields
        sample_data = {
            "date": ["2025-01-15", "2025-01-20"],
            "business_unit": ["Corporate", "Logistics"],
            "project": ["Carbon Reduction Initiative", "Operational"],
            "scope": ["Scope 2", "Scope 1"],
            "category": ["Electricity", "Mobile Combustion"],
            "activity": ["Office Electricity", "Company Vehicle"],
            "country": ["India", "United States"],
            "facility": ["Mumbai HQ", "Chicago Distribution Center"],
            "responsible_person": ["Rahul Sharma", "John Smith"],
            "quantity": [1000, 50],
            "unit": ["kWh", "liter"],
            "emission_factor": [0.82, 2.31495],
            "data_quality": ["High", "Medium"],
            "verification_status": ["Internally Verified", "Unverified"],
            "notes": ["Monthly electricity bill", "Fleet vehicle fuel consumption"],
        }
        sample_df = pd.DataFrame(sample_data)
        csv = sample_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Sample CSV",
            data=csv,
            file_name="sample_emissions.csv",
            mime="text/csv",
        )

# Reports page removed - focusing on AI features only

elif st.session_state.active_page == "Settings":
    st.markdown(f"<h1> {t('settings')}</h1>", unsafe_allow_html=True)

    st.markdown("<h3>Company Information</h3>", unsafe_allow_html=True)

    # Company info form
    with st.form("company_info_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            industry = st.text_input("Industry")
            location = st.text_input("Location")
        with col2:
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

        st.markdown("<h4>Export Markets</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            eu_market = st.checkbox("European Union")
        with col2:
            japan_market = st.checkbox("Japan")
        with col3:
            indonesia_market = st.checkbox("Indonesia")

        submitted = st.form_submit_button("Save Settings")
        if submitted:
            st.success("Settings saved successfully!")

elif st.session_state.active_page == "AI Insights":
    st.markdown(f"<h1 class='fade-in'>🤖 AI Insights</h1>", unsafe_allow_html=True)

    # Enhanced introduction for AI features
    st.markdown(
        """
        <div class='stCard fade-in'>
            <h3 style='margin-top: 0; color: var(--secondary-color);'>🚀 AI-Powered Carbon Intelligence</h3>
            <p style='color: var(--text-secondary); margin-bottom: 1rem;'>
                Get personalized insights, recommendations, and guidance from our advanced AI agents specialized in carbon accounting and sustainability.
            </p>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;'>
                <div style='background: var(--background-secondary); padding: 1rem; border-radius: var(--radius-md);'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🔍</div>
                    <strong>Smart Classification</strong><br>
                    <small>AI helps categorize emissions accurately</small>
                </div>
                <div style='background: var(--background-secondary); padding: 1rem; border-radius: var(--radius-md);'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📊</div>
                    <strong>Automated Reports</strong><br>
                    <small>Generate comprehensive summaries</small>
                </div>
                <div style='background: var(--background-secondary); padding: 1rem; border-radius: var(--radius-md);'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🌱</div>
                    <strong>Offset Guidance</strong><br>
                    <small>Find verified carbon offset projects</small>
                </div>
                <div style='background: var(--background-secondary); padding: 1rem; border-radius: var(--radius-md);'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>⚖️</div>
                    <strong>Regulation Tracking</strong><br>
                    <small>Stay compliant with latest rules</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Import AI agents
    from ai_agents import CarbonFootprintAgents

    # Initialize AI agents
    if "ai_agents" not in st.session_state:
        st.session_state.ai_agents = CarbonFootprintAgents()

    # Create enhanced tabs for different AI insights
    ai_tabs = st.tabs(
        [
            "🔍 Data Assistant",
            "📋 Report Summary",
            "🌱 Offset Advisor",
            "⚖️ Regulation Radar",
            "⚡ Emission Optimizer",
        ]
    )

    with ai_tabs[0]:
        st.markdown(
            """
            <div class='stCard'>
                <h3 style='margin-top: 0; color: var(--primary-color);'>🔍 Data Entry Assistant</h3>
                <p style='color: var(--text-secondary);'>
                    Get intelligent help with classifying emissions and mapping them to the correct scope and category. 
                    Our AI understands complex emission scenarios and provides accurate categorization.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Enhanced input with examples
        col1, col2 = st.columns([2, 1])

        with col1:
            data_description = st.text_area(
                "🔍 Describe your emission activity",
                placeholder="Example: We use diesel generators for backup power at our office in Mumbai. How should I categorize this?",
                height=120,
                help="Provide as much detail as possible for accurate classification",
            )

        with col2:
            st.markdown("#### 💡 Example Queries")
            example_queries = [
                "Company vehicle fuel consumption",
                "Office electricity usage",
                "Business travel flights",
                "Employee commuting",
                "Waste disposal",
                "Purchased goods",
            ]

            for i, example in enumerate(example_queries):
                if st.button(
                    f"📝 {example}", key=f"example_{i}", use_container_width=True
                ):
                    st.session_state.example_query = f"How should I categorize {example.lower()}? What scope does this belong to?"

        # Use example query if selected
        if "example_query" in st.session_state:
            data_description = st.session_state.example_query
            del st.session_state.example_query

        col1, col2 = st.columns([1, 3])
        with col1:
            get_help = st.button(
                "🚀 Get AI Assistance",
                key="data_assistant_btn",
                type="primary",
                use_container_width=True,
            )

        if get_help:
            if data_description and data_description.strip():
                with st.spinner("🤖 AI assistant is analyzing your request..."):
                    try:
                        result = st.session_state.ai_agents.run_data_entry_crew(
                            data_description
                        )
                        # Handle CrewOutput object by converting it to string
                        result_str = str(result)

                        st.markdown(
                            f"""
                            <div class='stCard' style='margin-top: 1.5rem; border-left: 4px solid var(--success-color);'>
                                <h4 style='color: var(--success-color); margin-top: 0;'>🎯 AI Recommendation</h4>
                                {result_str}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Add quick action button
                        if st.button(
                            "📝 Use This Classification in Data Entry",
                            key="use_classification",
                        ):
                            st.session_state.active_page = "Data Entry"
                            st.rerun()

                    except Exception as e:
                        st.error(
                            f"""
                            ❌ **AI Service Error**
                            
                            {str(e)}
                            
                            💡 **Tips:**
                            - Check your internet connection
                            - Verify your Groq API key is set correctly
                            - Try again in a few moments
                            """
                        )
            else:
                st.warning(
                    "⚠️ Please describe your emission activity first to get AI assistance."
                )

    with ai_tabs[1]:
        st.markdown("<h3>Report Summary Generator</h3>", unsafe_allow_html=True)
        st.markdown("Generate a human-readable summary of your emissions data.")

        if len(st.session_state.emissions_data) == 0:
            st.warning("No emissions data available. Please add data first.")
        else:
            if st.button("Generate Summary", key="report_summary_btn"):
                with st.spinner("Generating report summary..."):
                    try:
                        # Convert DataFrame to string representation for the AI
                        emissions_str = st.session_state.emissions_data.to_string()
                        result = st.session_state.ai_agents.run_report_summary_crew(
                            emissions_str
                        )
                        # Handle CrewOutput object by converting it to string
                        result_str = str(result)
                        st.markdown(
                            f"<div class='stCard'>{result_str}</div>",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.error(
                            f"Error: {str(e)}. Please check your API key and try again."
                        )

    with ai_tabs[2]:
        st.markdown("<h3>Carbon Offset Advisor</h3>", unsafe_allow_html=True)
        st.markdown(
            "Get recommendations for verified carbon offset options based on your profile."
        )

        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location", placeholder="e.g., Mumbai, India")
            industry = st.selectbox(
                "Industry",
                [
                    "Manufacturing",
                    "Technology",
                    "Agriculture",
                    "Transportation",
                    "Energy",
                    "Services",
                    "Other",
                ],
            )

        if len(st.session_state.emissions_data) == 0:
            st.warning("No emissions data available. Please add data first.")
        else:
            total_emissions = st.session_state.emissions_data["emissions_kgCO2e"].sum()
            st.markdown(
                f"<p>Total emissions to offset: <strong>{total_emissions:.2f} kgCO2e</strong></p>",
                unsafe_allow_html=True,
            )

            if st.button("Get Offset Recommendations", key="offset_advisor_btn"):
                if location:
                    with st.spinner("Finding offset options..."):
                        try:
                            result = st.session_state.ai_agents.run_offset_advice_crew(
                                total_emissions, location, industry
                            )
                            # Handle CrewOutput object by converting it to string
                            result_str = str(result)
                            st.markdown(
                                f"<div class='stCard'>{result_str}</div>",
                                unsafe_allow_html=True,
                            )
                        except Exception as e:
                            st.error(
                                f"Error: {str(e)}. Please check your API key and try again."
                            )
                else:
                    st.warning("Please enter your location.")

    with ai_tabs[3]:
        st.markdown("<h3>Regulation Radar</h3>", unsafe_allow_html=True)
        st.markdown(
            "Get insights on current and upcoming carbon regulations relevant to your business."
        )

        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input(
                "Company Location",
                placeholder="e.g., Jakarta, Indonesia",
                key="reg_location",
            )
            industry = st.selectbox(
                "Industry Sector",
                [
                    "Manufacturing",
                    "Technology",
                    "Agriculture",
                    "Transportation",
                    "Energy",
                    "Services",
                    "Other",
                ],
                key="reg_industry",
            )
        with col2:
            export_markets = st.multiselect(
                "Export Markets",
                [
                    "European Union",
                    "Japan",
                    "United States",
                    "China",
                    "Indonesia",
                    "India",
                    "Other",
                ],
            )

        if st.button("Check Regulations", key="regulation_radar_btn"):
            if location and len(export_markets) > 0:
                with st.spinner("Analyzing regulatory requirements..."):
                    try:
                        result = st.session_state.ai_agents.run_regulation_check_crew(
                            location, industry, ", ".join(export_markets)
                        )
                        # Handle CrewOutput object by converting it to string
                        result_str = str(result)
                        st.markdown(
                            f"<div class='stCard'>{result_str}</div>",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.error(
                            f"Error: {str(e)}. Please check your API key and try again."
                        )
            else:
                st.warning(
                    "Please enter your location and select at least one export market."
                )

    with ai_tabs[4]:
        st.markdown("<h3>Emission Optimizer</h3>", unsafe_allow_html=True)
        st.markdown("Get AI-powered recommendations to reduce your carbon footprint.")

        if len(st.session_state.emissions_data) == 0:
            st.warning("No emissions data available. Please add data first.")
        else:
            if st.button(
                "Generate Optimization Recommendations", key="emission_optimizer_btn"
            ):
                with st.spinner("Analyzing your emissions data..."):
                    try:
                        # Convert DataFrame to string representation for the AI
                        emissions_str = st.session_state.emissions_data.to_string()
                        result = st.session_state.ai_agents.run_optimization_crew(
                            emissions_str
                        )
                        # Handle CrewOutput object by converting it to string
                        result_str = str(result)
                        st.markdown(
                            f"<div class='stCard'>{result_str}</div>",
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.error(
                            f"Error: {str(e)}. Please check your API key and try again."
                        )

# About page removed - focusing on AI features only
