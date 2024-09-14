import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


# Function to create a connection to the MySQL database
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,  # replace with your MySQL username
            password=DB_PASSWORD,  # replace with your MySQL password
            database=DB_NAME  # replace with your MySQL database
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
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
