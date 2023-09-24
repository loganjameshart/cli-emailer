#!usr/bin/env python3

"""
Command line interface for sending emails.
Author: Logan Hart
"""

import sys
import re
import smtplib
import getpass
import time
from configparser import ConfigParser
from email.message import EmailMessage

parser = ConfigParser()
parser.read("config.ini")

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

USERNAME = parser["Login"]["Username"]
PASSWORD = parser["Login"]["Password"]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587  # make sure this is an int if you hardcode it


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

        while True:
            username = input(">>> Please enter your username: ")
            if self._is_valid_email(username):
                break
            else:
                print(">>> Please use a valid email address.")
                continue
        password = getpass.getpass(prompt=">>> Please enter your password: ")
        return (username, password)

    def _get_smtp(self):
        """Get SMTP server information if it is not provided."""

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

    def _is_valid_email(self, email_address):
        """Check email address's validity against regex."""

        email_re = re.compile(EMAIL_REGEX)
        if not email_re.match(email_address):
            return False
        else:
            return True

    def _get_valid_recipient(self):
        """Get and validate inputted recipient email address(es)."""

        while True:
            recipient = input(">>> Please enter the recipient: ")
            if self._is_valid_email(recipient):
                return recipient
            else:
                print(">>> Invalid email address. Please try again.")
                continue

    def _get_valid_subject(self):
        """Get and validate subject line."""

        while True:
            subject = input(">>> Please enter your subject: ")
            if subject:
                return subject
            else:
                print(">>> Please enter a valid subject.")
                continue

    def _parse_recipient_input(self, recipient_input):
        """Parse inputted recipients into sender list."""

        if ";" in recipient_input:
            recipient_list = recipient_input.split(";")
            return recipient_list
        elif "," in recipient_input:
            recipient_list = recipient_input.split(",")
            return recipient_list
        else:
            recipient_list = [recipient_input]
            return recipient_list

    def _get_message(self):
        """Get a multi-line message."""

        print(">>> Please enter your message (press Enter twice to finish):")
        message_lines = []
        while True:
            line = input()
            if not line:
                break
            message_lines.append(line)

        message_body = "\n".join(message_lines)
        return message_body

    def send_email(self):
        """Create and send email."""

        msg = EmailMessage()
        msg["From"] = self.username

        while True:
            recipient_input = self._get_valid_recipient()
            recipient_list = self._parse_recipient_input(recipient_input)
            msg["To"] = ", ".join(recipient_list)
            decision = input(f">>> Is this correct? (Y/n) {msg['To']} ")
            if decision.lower() not in ("yes", "y"):
                del msg["To"]  # need to completely clear the field in order to redo it
                continue
            else:
                break

        while True:
            msg["Subject"] = self._get_valid_subject()
            decision = input(f">>> Is this correct? (Y/n) {msg['Subject']} ")
            if decision.lower() not in ("yes", "y"):
                del msg["Subject"]
                continue
            else:
                break

        while True:
            message_body = self._get_message()
            msg.set_content(message_body)
            decision = input(f">>> Here is your message: {message_body}. Okay? (Y/n)")
            if decision.lower() not in ("yes", "y"):
                continue
            else:
                break

        while True:
            decision = input(
                f">>> Here is your message:\n {msg.as_string()}\nIs this okay? (Y/n) "
            )
            if decision.lower() not in ("yes", "y"):
                continue
            else:
                connection = self.smtp_connection
                connection.send_message(msg)
                print(">>> Message sent.")
                break


def main():
    print(USERNAME, PASSWORD)
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
