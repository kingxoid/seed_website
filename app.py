from flask import Flask, render_template, request
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
import requests
import json

app = Flask(__name__)

# Static email credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Brevo SMTP key
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")



@app.route("/wallets")
def wallets():
    return render_template("wallets.html")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/connect", methods=["GET", "POST"])
def connect():
    if request.method == "POST":
        message = request.form["message"]

        try:
            # Create the email content
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg['Subject'] = "New Message from Flask App"

            body = f"Message: {message}"
            msg.attach(MIMEText(body, 'plain'))

            # Set up SSL context
            context = ssl.create_default_context()

            # Connect to the SMTP server and send the email

            with smtplib.SMTP("smtp-relay.sendinblue.com", 587) as server:
                server.starttls()  # Use TLS encryption
                server.login(SMTP_USERNAME, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

            return "✅ Message sent successfully!"
        except Exception as e:
            return f"❌ Error sending email: {e}"

    return render_template("connect.html")

if __name__ == "__main__":
    # Use the environment variable for the port (Render sets it automatically)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)