from flask import Flask, render_template, request
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
app = Flask(__name__)

# Static email credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Brevo SMTP key
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")

@app.route("/", methods=["GET", "POST"])
def index():
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
            with smtplib.SMTP_SSL("smtp-relay.sendinblue.com", 465, context=context) as server:
                server.login(SMTP_USERNAME, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

            return "✅ Message sent successfully!"
        except Exception as e:
            return f"❌ Error sending email: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
