import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector

import mysql

# Gmail login credentials
sender_email = "amal.indarto@gmail.com"
app_password = os.environ.get("APP_PASSWORD")
print(f"App Password: {app_password}")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="water_monitoring"
)
cursor = db.cursor(dictionary=True)

if not app_password:
    exit(1)

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
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def save_to_database(data):
    # Placeholder function to simulate saving data to a database
    print(f"Saving data to database: {data}")
    # Implement actual database saving logic here

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

def read_from_database():
    # Placeholder function to simulate reading data from a database
    print("Reading data from database")
    # Implement actual database reading logic here

    query = "SELECT * FROM tds_data"
    cursor.execute(query)
    items = cursor.fetchall()
    print(items)
    return items

