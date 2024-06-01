import os
from flask import Flask, render_template, request, flash
import oauth

MY_EMAIL = "nikos.lyberidis@gmail.com"
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)

service = oauth.get_g_service()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template("contact.html", msg_sent=False)
    else:
        data = request.form
        try:
            send_email(data)
            flash("Message sent successfully!", category="success")
        except Exception as e:  # Catch any errors during email sending
            flash("An error occurred while sending the message. Please try again later.", category="error")
        return render_template("contact.html", msg_sent=True)


def send_email(info):
    import smtplib
    text = (f'Subject: Contact from site\n\n'
            f'Name: {info['name']}\n'
            f'Email: {info['email']}\n'
            f'Phone: {info["phone"] if "phone" in info else "N/A"}\n'  # Handle missing phone number
            f'Message: {info['message']}\n'
            )
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # TLS makes the connection secure
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=text.encode("utf-8")
        )


if __name__ == "__main__":
    app.run(debug=True, port=5003)
