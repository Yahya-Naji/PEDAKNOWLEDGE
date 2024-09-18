import streamlit as st
import pandas as pd
import mysql.connector
import confg  # Importing the backend functions from confg.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the stored username and password from .env
APP_USERNAME="test"
APP_PASSWORD="test"


# Debug: Check if environment variables are loaded properly


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
    username = st.text_input("Username").strip()  # Stripping extra spaces
    password = st.text_input("Password", type="password").strip()  # Stripping extra spaces
    
    if st.button("Login"):   
        if username == USERNAME and password == PASSWORD:
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username  # Store username in session state for future use
        else:
            st.error("Invalid username or password")

# Main app logic with authentication
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # Debug: Display logged-in username
    st.write(f"Debug: Logged in as {st.session_state['username']}")

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
            
            # Debug: Show the result of the content retrieval
            st.write(f"Debug: Result from get_content: {content}")
            
            if "error" in content:
                st.error(content["error"])
            else:
                # Display the content in a table using Pandas
                df = pd.DataFrame(content)
                st.dataframe(df)
