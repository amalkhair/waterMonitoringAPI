import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import bcrypt
import mysql.connector
import mysql

# Gmail login credentials
sender_email = "amal.indarto@gmail.com"
gmail_password = os.environ.get("GMAIL_PASSWORD")

print(f"------Ini password GMAIL dari ENVIRONEMENT: {gmail_password}")

# Hash password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Verify password
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))




if not gmail_password:
    print("App password not set. Please set the APP_PASSWORD environment variable.")
    exit(1)

# send email function
def send_mail(subject: str, body: str, receiver_email: str):
    try:
        # Compose email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, gmail_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# save tds data to database
def save_to_database(data):
    print(f"Saving data to database: {data}")
    cursor = None  # Initialize cursor to None
    try:
        # Create a new connection for this operation
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="water_monitoring"
        )
        cursor = db.cursor(dictionary=True)
        query = """
                INSERT INTO tds_data (tds_value, time_registration, temperature, cycle)
                VALUES (%s, %s, %s, %s)
            """
        values = (
            data.get("TDS"),
            data.get("time"),
            data.get("temperature"),
            data.get("cycle"),
        )
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        print(f"Error saving user data: {e}")
        if db.is_connected():
            db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db.is_connected():
            db.close()


# save user data to database (signup)
def save_user_to_database(userdata):
    print(f"Saving user data to database: {userdata}")
    success = False
    cursor = None  # Initialize cursor to None
    try:
        # Create a new connection for this operation
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="water_monitoring"
        )
        cursor = db.cursor(dictionary=True)
        query = """
            INSERT INTO user (email_address, username, password)
            VALUES (%s, %s, %s)
        """
        values = (
            userdata.get("email_address"),
            userdata.get("username"),
            userdata.get("password"),
        )
        cursor.execute(query, values)
        db.commit()
        success = True
    except Exception as e:
        print(f"Error saving user data: {e}")
        if db.is_connected():
            db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db.is_connected():
            db.close()

    return success

# get user data from database (login)
def get_user_from_database(username):
    user = None
    cursor = None
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="water_monitoring"
        )
        cursor = db.cursor(dictionary=True)
        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        print(user)
    except Exception as e:
        print(f"Error retrieving user: {e}")
    finally:
        if cursor:
            cursor.close()
        if db.is_connected():
            db.close()
    return user


# get tds data from database to the frontend
def read_from_database():
    # Placeholder function to simulate reading data from a database
    print("Reading data from database")
    # Implement actual database reading logic here
    cursor = None  # Initialize cursor to None
    try:
        # Create a new connection for this operation
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="water_monitoring"
        )
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM tds_data"
        cursor.execute(query)
        items = cursor.fetchall()
        print(items)
        return items
    except Exception as e:
        print(f"Error reading data from database: {e}")
        return []

