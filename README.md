![quickmail logo](https://raw.githubusercontent.com/loganjameshart/quickmail/main/.quickmail.svg)

Command line interface for sending emails.

## Overview

This Python script provides a command line interface (CLI) for sending emails using the Simple Mail Transfer Protocol (SMTP). It allows users to send emails with a specified recipient, subject, and message directly from the command line.

## Prerequisites

Before using this CLI tool, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- Internet access to connect to the SMTP server.
- Valid email credentials (username and password) and SMTP server information (host and port).

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/loganjameshart/quickmail.git
   ```

2. Change to the project directory:

   ```bash
   cd quickmail
   ```

## Usage

1. Run the script by executing the following command:

   ```bash
   python3 quickmail.py
   ```

2. Follow the on-screen prompts to provide the necessary information for sending an email:

   - Enter your email username and password or SMTP server information if not provided in the script.
   - Specify the recipient's email address or addresses (if multiple recipients, separate by a comma or semicolon).
   - Enter the email subject.
   - Compose the email message, pressing Enter twice to finish.
   - Review the email details and confirm before sending.

3. The script will connect to the SMTP server and send the email.

4. You will receive a confirmation message once the email is sent.

## Note

- This script supports sending emails through an SMTP server. Make sure you have the correct SMTP server host and port information if it's not hardcoded in the script.

- Ensure that your email account allows "less secure apps" or generate an "app password" if you encounter authentication issues.

- The script uses the `getpass` module to securely input your password.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/)
