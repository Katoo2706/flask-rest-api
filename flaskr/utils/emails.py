import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emails:
    def __init__(self, sender_email, app_password) -> None:
        """

        :param sender_email: Sender email
        :param app_password: App password
        """
        self.sender_email = sender_email
        self.app_password = app_password
        pass

    def send_email(self, receiver: str, subject: str, body: str):
        # Create MIMEMultipart object
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.sender_email

        part = MIMEText(body, "html")
        msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.app_password)
            print("Logged in...")
            server.sendmail(
                self.sender_email, receiver, msg.as_string()
            )
            print("Email has been sent!")

