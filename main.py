import os
from flask import Flask, render_template, request, flash
import oauth_local
from email.mime.text import MIMEText
import base64

MY_EMAIL = "nikos.lyberidis@gmail.com"
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

service = oauth.get_g_service()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


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


def send_email(info, user_id='me'):
    message = MIMEText(f'Subject: Contact from site\n\n'
                       f'Name: {info["name"]}\n'
                       f'Email: {info["email"]}\n'
                       f'Phone: {info["phone"] if "phone" in info else "N/A"}\n'  # Handle missing phone number
                       f'Message: {info["message"]}\n'
                       )
    message['to'] = MY_EMAIL
    message['from'] = MY_EMAIL
    message['subject'] = 'Contact from site'
    msg = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    try:
        service = oauth.get_g_service()
        message = (service.users().messages().send(userId=user_id, body=msg)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except ValueError as e:
        print('An error occurred: %s' % e)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
