from .emails import Emails
from .render_html import render_html
import os
# from dotenv import load_dotenv
#
# # Variable environment should be loaded from app.py
# dotenv_path = os.path.join(os.path.dirname(__file__), './../../.env')
# load_dotenv(dotenv_path)


def send_welcome_email(receiver_email: str, receiver_name):
    """

    :param receiver_email: Email
    :param receiver_name:
    :return:
    """
    email_cli = Emails(sender_email=os.getenv("SENDER_EMAIL"),
                       app_password=os.getenv("GMAIL_APP_PASSWORD"))

    return email_cli.send_email(
        receiver=receiver_email,
        subject="Welcome to Flask rest API",
        body=render_html(
            html_file="email/welcome.html",
            username=receiver_name
        )
    )

