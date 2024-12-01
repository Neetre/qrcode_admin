import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl
import os


EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
SMTP_PORT = 465


def smtp_server(email):
    domain = email.split("@")[1]
    domain = "smtp." + domain
    return domain


def send_email(to_email, subject, body, filepath: str = None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        elif not os.path.isfile(filepath):
            raise ValueError(f"Path is not a file: {filepath}")
        elif filepath is not None:
            filepath = filepath
            filename = os.path.basename(filepath)
            attachment = open(filepath, 'rb')

            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())

            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)
    except Exception as e:
        print(f"Exception cought while reading filepath: {e}")

    context = ssl.create_default_context()
    SMTP_SERVER = smtp_server(EMAIL)
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())


def get_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


def get_emails(path):
    with open(path, 'r') as file:
        for line in file:
            yield line.strip()


def concatenate_data(files, emails):
    conc = [(file, email) for file in files for email in emails]
    return conc


def main():
    files = get_files('../data/qr_codes/')
    emails = get_emails("../data/emails.txt")
    data = concatenate_data(files, emails)

    for file, email in data:
        send_email(email, 'Qr Code per Cori', 'Ecco il tuo qrcode. Ricorda, è soltanto tuo. Se lo userai con un altro cellulare esso verrà segnato come usato', file)
        print(f"Email sent to {email} with file {file}")
    print("All emails sent")


if __name__ == '__main__':
    main()
