from flask import Flask, render_template, request
import smtplib
import ssl
import os

app = Flask(__name__)

# Static email credentials (Note: Keep these secure in production environments)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Brevo SMTP key
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form["message"]

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp-relay.sendinblue.com", 465, context=context) as server:
                server.login(SMTP_USERNAME, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, f"Subject: New Message\n\n{message}")
            return "✅ Message sent successfully!"
        except Exception as e:
            return f"❌ Error sending email: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    # Use the environment variable for the port (Render sets it automatically)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
