import base64
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import qrcode

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]
global service
def send_email_with_qrcode(service, to_email, qr_data):
    """
    Send an email with a QR Code image attached.

    Args:
        service: An authorized Gmail API service instance.
        to_email (str): The recipient's email address.
        qr_data (str): The data to be encoded in the QR Code.
    """

    img = qrcode.make(qr_data)
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    msg = MIMEMultipart()
    text = MIMEText('Please Scan the QR Code to connect')
    msg.attach(text)

    image = MIMEImage(img_buffer.read())
    image.add_header('Content-Disposition', 'attachment', filename='qrcode.png')
    msg.attach(image)

    msg['to'] = to_email
    msg['subject'] = 'MSPR-Cafe QRCode Validation'
    create_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        message = None


def init_mail_sender():
    """
    Authenticate the user, create a Gmail API service instance, and return the created service
    """

    flow = InstalledAppFlow.from_client_secrets_file('ressource/GoogleAuth/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)

    return service

def get_mail_sender():
    """
    Get the service if created, generate it otherwise
    Returns:service
    """

    if service == None :
        service = init_mail_sender()
        return service
    else:
        return service