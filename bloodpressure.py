import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
def get_sheet():
    # Define the scope and authorize the client.
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    
    # Replace with your spreadsheet ID (found in the URL of your Google Sheet)
    #spreadsheet_id = "YOUR_SPREADSHEET_ID"
    spreadsheet_id = "1s9Jhw5hKC7eNabxXkmQExqafNgL15Tt4NRlp1nsByq8"    
    sheet = client.open_by_key(spreadsheet_id).sheet1

    # Initialize header row if the sheet is empty.
    if len(sheet.get_all_values()) == 0:
        sheet.append_row(["timestamp", "systolic", "diastolic", "pulse"])
    return sheet

# --- App Navigation ---
st.sidebar.title("Blood Pressure Tracker")
page = st.sidebar.radio("Go to", ["Enter Data", "View Data"])

# --- Page 1: Data Entry ---
if page == "Enter Data":
    st.title("Enter Your Blood Pressure and Pulse Reading")
    
    # Input fields for readings.
    systolic = st.number_input("Systolic", min_value=0, step=1)
    diastolic = st.number_input("Diastolic", min_value=0, step=1)
    pulse = st.number_input("Pulse", min_value=0, step=1)
    
    if st.button("Submit"):
        # Record the current timestamp.
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = [now, systolic, diastolic, pulse]
        
        try:
            sheet = get_sheet()
            sheet.append_row(new_data)
            st.success("Data submitted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Page 2: View Data ---
elif page == "View Data":
    st.title("View All Entered Data")
    try:
        sheet = get_sheet()
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No data found.")
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
