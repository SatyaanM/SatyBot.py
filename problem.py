import imaplib
import email
from dotenv import load_dotenv
import os


def get_problem():
    load_dotenv('/.env')

    username = os.getenv('USER')
    password = os.getenv('PASS')

    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    mail.login(username, password)
    mail.select('"Daily Coding Problem"')

    result, data = mail.uid('search', None, "ALL")

    msgs = data[0].split()
    most_recent = msgs[-1]

    result, data = mail.uid('fetch', most_recent, '(RFC822)')

    raw = data[0][1]
    emailMsg = email.message_from_bytes(raw)
    emailBody = str(emailMsg.get_payload(0))

    sep = "printable"
    stripped = emailBody.split(sep, 1)[1]
    sep = "---"
    stripped = stripped.split(sep, 1)[0]

    problem = stripped.strip()
    return problem
