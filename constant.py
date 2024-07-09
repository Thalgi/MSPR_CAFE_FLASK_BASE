# Chemins des fichiers
SSL_CERT_PATH = "path/to/server.crt"
SSL_KEY_PATH = "path/to/server.key"
GOOGLE_CREDENTIALS_PATH = 'ressource/GoogleAuth/credentials.json'

# Configuration de l'application
SECRET_KEY = 'TVNQUl9DYWZlOmVwc2kyMDIz'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# URLs
BASE_URL = "https://7695-2a01-cb19-d81-c600-dd62-6606-ee27-e4bb.ngrok-free.app"
CONFIRM_USER_URL = f"{BASE_URL}/confirm_user"

# Paramètres de sécurité
TOKEN_LENGTH = 32

# Scopes pour l'API Gmail
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]