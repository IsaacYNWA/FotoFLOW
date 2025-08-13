# config.py DEFINITIVO

import sys
import os

def resource_path(relative_path):
    """ Obtiene la ruta absoluta a un recurso, funciona para desarrollo y para el .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Módulo de Video ---
# AHORA BUSCARÁ FFMPEG.EXE DENTRO DEL PAQUETE .EXE
FFMPEG_PATH = resource_path("ffmpeg.exe") 

CRF_VALUE = 28
VIDEO_CODEC = "libx265"
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv")

# --- Módulo de Renombrado ---
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic", ".avif"}

# --- Módulo de Gmail ---
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = resource_path('credentials.json')
TOKEN_FILE = 'token.json'
TEST_EMAIL_SENDER = 'isaacynwa03@gmail.com'
TEST_EMAIL_RECIPIENT = 'edgarzelada152@gmail.com'