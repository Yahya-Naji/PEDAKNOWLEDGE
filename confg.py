import mysql.connector
from mysql.connector import Error
import streamlit as st

# Retrieve database credentials from Streamlit Secrets
DB_HOST = st.secrets["DB_HOST"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_NAME = st.secrets["DB_NAME"]

# Function to create a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@yd@1996',
            database='PedaKnowledge'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")  # This will show the error in the app
        return None


# Function to add content to the database
def add_content(chapter_name, grade, learning_objective, sample_questions):
    connection = create_connection()
    if connection is None:
        return {"error": "Failed to connect to the database"}

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO learning_content (chapter_name, grade, learning_objective, sample_questions)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (chapter_name, grade, learning_objective, sample_questions))
        connection.commit()
        return {"success": True}
    except Error as e:
        return {"error": f"Failed to add content: {e}"}
    finally:
        cursor.close()
        connection.close()

# Function to retrieve content from the database
def get_content():
    connection = create_connection()
    if connection is None:
        return {"error": "Failed to connect to the database"}

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM learning_content"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        return {"error": f"Failed to retrieve content: {e}"}
    finally:
        cursor.close()
        connection.close()
