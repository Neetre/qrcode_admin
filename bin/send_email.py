import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import ssl
import os


EMAIL = os.environ.get('EMAIL')
print(EMAIL)
PASSWORD_EMAIL = os.environ.get('PASSWORD_EMAIL')
SMTP_PORT = 465

DEF_EMAIL = "{}@studenti.marconiverona.edu.it"


def smtp_server(email):
    domain = email.split("@")[1]
    domain = "smtp." + "gmail.com" #domain
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
        server.login(EMAIL, PASSWORD_EMAIL)
        server.sendmail(EMAIL, to_email, msg.as_string())


def get_files(path):
    qr_codes_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            qr_codes_paths.append(os.path.join(path, file))
            
    sorted_files = sorted(qr_codes_paths)
    return sorted_files


def get_emails(path):
    emails = []
    with open(path, 'r') as file:
        reader = file.readlines()
        
        for row in reader[1:]:
            matricola, classe = row.split(";")
            if classe in ["1DI", "2EI"] or classe.startswith("5"):
                emails.append(matricola)
                
    return emails


def concatenate_data(files, emails):
    conc = [(file, email) for file in files for email in emails]
    return conc


def email_sender():
    files = get_files('../data/qr_codes/')
    print("File read...")
    
    # import sys; sys.exit(0)
    # emails = get_emails("../data/matricola-classe.csv")
    emails = ["19746@studenti.marconiverona.edu.it"]
    print("Emails read ...")
    data = concatenate_data(files, emails)
    print("Data Created...")
    print(data[0])

    try:
        for file, email in data:
            print(file, email)
            send_email(email, 'Qr Code per Cori', 'Ecco il tuo qrcode. Ricorda, è soltanto tuo. Se lo userai con un altro cellulare esso verrà segnato come usato', file)
            print(f"Email sent to {email} with file {file}")
            break
    except Exception as e:
        print(f"Exception cought while sending email: {e}")
    print("All emails sent")


if __name__ == '__main__':
    email_sender()
