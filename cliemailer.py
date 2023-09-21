#!usr/bin/env python3

"""
Command line interface for sending emails.
"""

import sys
import smtplib
from getpass import getpass
from email.message import EmailMessage


USERNAME = ""
PASSWORD = ""
SMTP_HOST = ""
SMTP_PORT = ""


class Emailer:
    def __init__(self):
        """Instantiate the Emailer class."""

        if USERNAME and PASSWORD:
            self.username = USERNAME
            self.password = PASSWORD

        else:
            self.username, self.password = self._get_login()

        if SMTP_HOST and SMTP_PORT:
            self.smtp_host = SMTP_HOST
            self.smtp_port = SMTP_PORT

        else:
            self.smtp_host, self.smtp_port = self._get_smtp()

        self.smtp_connection = self._connection()

    def _get_login(self):
        """Get login credentials for email server if none are provided."""
        
        username = input(">>> Please enter your username: ")
        password = getpass(prompt=">>> Please enter your password: ")
        return (username, password)

    def _get_smtp(self):
        """Get SMTP server information if none are provided."""
        
        server_name = input(">>> Please enter the SMTP server address: ")
        port = input(">>> Please enter the SMTP port: ")
        return (server_name, int(port))

    def _connection(self):
        """Connect to SMTP server."""
        
        try:
            smtp_connection = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp_connection.ehlo()
            smtp_connection.starttls()
            smtp_connection.login(self.username, self.password)
            print(f">>> Connected to {self.smtp_host}.")
            return smtp_connection
        except Exception as e:
            print(">>> Couldn't make SMTP connection. Here's the error:\n")
            print(e)
            sys.exit(1)

    def send_email(self):
        '''Create and send email.'''
        
        msg = EmailMessage()
        msg["From"] = self.username
        while True:
            msg["To"] = input(">>> Please enter the recipient: ")
            decision = input(f">>> Is this correct? (Y/n) {msg['To']} ")
            if decision.lower() not in ("yes", "y"):
                del msg["To"]  # need to completely clear the field in order to redo it
                continue
            else:
                break
        while True:
            msg["Subject"] = input(f">>> Please enter your subject: ")
            decision = input(f">>> Is this correct? (Y/n) {msg['Subject']} ")
            if decision.lower() not in ("yes", "y"):
                del msg["Subject"]
                continue
            else:
                break
        while True:
            message_body = input(">>> Please enter your message: ")
            msg.set_content(message_body)
            decision = input(f"Here is your message: {message_body}. Okay? (Y/n)")
            if decision.lower() not in ("yes", "y"):
                continue
            else:
                connection = self.smtp_connection
                connection.send_message(msg)
                print(">>> Message sent.")
                break


def main():
    mailer = Emailer()

    while True:
        mailer.send_email()
        decision = input(">>> Would you like to send another? (Y/n) ")
        if decision.lower() in ("yes", "y"):
            continue
        elif decision.lower() in ("no", "n"):
            break


if __name__ == "__main__":
    main()
