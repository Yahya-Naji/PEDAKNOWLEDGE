import streamlit as st
import pandas as pd
import mysql.connector
import confg  # Importing the backend functions from confg.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the stored username and password from .env
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

# Function to validate the inputs
def validate_inputs(chapter_name, grade, learning_objective, sample_questions):
    if not chapter_name:
        st.error("Chapter name is required")
        return False
    if not isinstance(grade, int) or grade < 1 or grade > 12:
        st.error("Grade must be an integer between 1 and 12")
        return False
    if not learning_objective:
        st.error("Learning objective is required")
        return False
    if not sample_questions:
        st.error("Sample questions are required")
        return False
    return True

# Function for login verification
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.success("Login successful!")
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

# Main app logic with authentication
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # If logged in, show the app content
    st.title("Learning Content Management")

    # Choose between adding new content and retrieving existing content
    action = st.selectbox("Choose Action", ["Add New Content", "Retrieve Existing Content"])

    if action == "Add New Content":
        # Prompt for content details
        st.subheader("Add New Learning Content")
        
        chapter_name = st.text_input("Chapter Name")
        grade = st.number_input("Grade", min_value=1, max_value=12, step=1)
        learning_objective = st.text_area("Learning Objective")
        sample_questions = st.text_area("Sample Questions")

        if st.button("Submit"):
            # Validate input before sending to the database
            if validate_inputs(chapter_name, grade, learning_objective, sample_questions):
                result = confg.add_content(chapter_name, grade, learning_objective, sample_questions)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Content added successfully!")

    elif action == "Retrieve Existing Content":
        st.subheader("Existing Learning Content")

        if st.button("Retrieve Content"):
            content = confg.get_content()
            if "error" in content:
                st.error(content["error"])
            else:
                # Display the content in a table using Pandas
                df = pd.DataFrame(content)
                st.dataframe(df)
