import base64
import os
from email.message import EmailMessage

# --- Importaciones de Google ---
# Es crucial tener estas librerías instaladas (están en requirements.txt)
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Importación de la Configuración Centralizada ---
from config import GMAIL_SCOPES, TOKEN_FILE, CREDENTIALS_FILE, TEST_EMAIL_SENDER, TEST_EMAIL_RECIPIENT

def _obtener_credenciales():
    """
    Gestiona la autenticación del usuario con la API de Gmail.
    
    Busca un token.json válido. Si no existe o ha caducado, inicia el flujo
    de autenticación para crear o refrescar uno.
    
    Raises:
        FileNotFoundError: Si el archivo 'credentials.json' no se encuentra.

    Returns:
        google.oauth2.credentials.Credentials: Las credenciales válidas para usar el servicio.
    """
    creds = None
    # El archivo token.json almacena los tokens de acceso y de refresco del usuario.
    # Se crea automáticamente durante el primer flujo de autorización.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, GMAIL_SCOPES)
        
    # Si no hay credenciales (válidas), se permite al usuario que inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Si las credenciales han expirado pero tenemos un refresh token, lo usamos.
            print("Refrescando token de autenticación...")
            creds.refresh(Request())
        else:
            # Si es la primera vez o el refresh token no funciona, iniciamos el flujo de login.
            print("Iniciando autenticación de Google por primera vez...")
            if not os.path.exists(CREDENTIALS_FILE):
                # Este es un punto de fallo común. El mensaje de error debe ser claro.
                raise FileNotFoundError(
                    f"Error: El archivo de credenciales '{CREDENTIALS_FILE}' no se encontró. "
                    "Asegúrate de haberlo descargado desde tu Google Cloud Console y "
                    "de que se encuentra en la misma carpeta que el script."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Guardamos las credenciales para la próxima ejecución.
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"Credenciales guardadas en '{TOKEN_FILE}'.")
        
    return creds

def enviar_correo(destinatario, remitente, asunto, cuerpo):
    """
    Construye y envía un correo electrónico usando la API de Gmail.

    Args:
        destinatario (str): La dirección de email del receptor.
        remitente (str): La dirección de email del emisor (debe coincidir con la cuenta autenticada).
        asunto (str): El asunto del correo.
        cuerpo (str): El contenido de texto del correo.
    """
    try:
        # 1. Obtener las credenciales
        creds = _obtener_credenciales()
        
        # 2. Construir el servicio de la API
        service = build('gmail', 'v1', credentials=creds)

        # 3. Crear el mensaje
        message = EmailMessage()
        message.set_content(cuerpo)
        message['To'] = destinatario
        message['From'] = remitente
        message['Subject'] = asunto

        # 4. Codificar el mensaje en el formato que requiere la API (base64 url-safe)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # 5. Enviar el mensaje usando el servicio
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"✅ Correo enviado exitosamente a '{destinatario}'. ID del Mensaje: {send_message['id']}")

    except FileNotFoundError as e:
        # Captura el error de credentials.json no encontrado.
        print(f"❌ ERROR DE CONFIGURACIÓN: {e}")
    except HttpError as error:
        # Captura errores específicos de la API de Google.
        print(f"❌ Ocurrió un error con la API de Gmail: {error}")
    except Exception as e:
        # Captura cualquier otro error (ej: problemas de red).
        print(f"❌ Ocurrió un error inesperado al intentar enviar el correo: {e}")

# --- Bloque de Prueba ---
if __name__ == '__main__':
    """
    Este bloque se ejecuta solo cuando se corre el script directamente
    (ej: `python mod_gmail.py`). Sirve para probar el módulo de forma aislada.
    """
    print("--- MODO DE PRUEBA DEL MÓDULO GMAIL ---")
    print("Intentando enviar un correo de prueba...")
    
    asunto_prueba = "Prueba de Módulo Gmail"
    cuerpo_prueba = (
        "Este es un mensaje de prueba automático.\n\n"
        "Si lo has recibido, el módulo 'mod_gmail.py' y la autenticación con "
        "Google funcionan correctamente."
    )
    
    # Usamos los datos de prueba definidos en config.py
    enviar_correo(TEST_EMAIL_RECIPIENT, TEST_EMAIL_SENDER, asunto_prueba, cuerpo_prueba)
    print("\n--- FIN DE LA PRUEBA ---")