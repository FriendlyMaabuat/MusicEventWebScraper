import time
from email.mime.text import MIMEText
import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "myudemycourses47@gmail.com"
    password = "irjhfowavapmbhuk"

    message = MIMEText(message, "plain")
    message["Subject"] = "MusicEventWebScraper Subject Test Email"
    message["From"] = username

    receiver = "myudemycourses47@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message.as_string())
    print("Email was sent!")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE date=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                message = """
                If you see this, then the email was successfully sent!
                """
                send_email(message)
        time.sleep(2)  # Checking for new tours every 2 seconds



