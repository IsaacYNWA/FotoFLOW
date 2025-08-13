import os
import sys
import re  # Módulo de Expresiones Regulares para validar el formato del email

# --- Importaciones de nuestros Módulos ---
# Importamos solo las funciones principales que necesitamos de cada módulo.
# Esto mantiene el código limpio y claro sobre sus dependencias.
from mod_video import iniciar_conversion_masiva
from mod_renombrar import iniciar_renombrado
from mod_limpieza import iniciar_menu_limpieza
from mod_gmail import enviar_correo

# --- Importaciones de la Configuración ---
# Necesitamos saber quién es el remitente del correo.
from config import TEST_EMAIL_SENDER

# --- Funciones de Utilidad ---

def limpiar_pantalla():
    """Limpia la ventana de la terminal (compatible con Windows, macOS, Linux)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def es_email_valido(email):
    """
    Valida si una cadena de texto tiene un formato de email válido.
    
    Args:
        email (str): La cadena a validar.
        
    Returns:
        bool: True si el formato es válido, False en caso contrario.
    """
    # Expresión regular común para validar la mayoría de los formatos de email.
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def obtener_email_usuario():
    """
    Pide al usuario su correo electrónico y no continúa hasta que se ingrese
    uno con un formato válido.
    
    Returns:
        str: La dirección de correo electrónico validada.
    """
    while True:
        email = input("Por favor, introduce tu dirección de correo para recibir los informes: ").strip()
        if es_email_valido(email):
            print(f"✅ Correo '{email}' registrado. Los informes de las tareas se enviarán aquí.")
            return email
        else:
            print("❌ Formato de correo no válido. Por favor, inténtalo de nuevo (ej: usuario@dominio.com).")

def mostrar_menu(email_registrado):
    """Imprime el menú principal de la aplicación en la consola."""
    limpiar_pantalla()
    print("========================================")
    print("   APLICACIÓN DE AUTOMATIZACIÓN PYTHON  ")
    print("========================================")
    print(f"  Informes se enviarán a: {email_registrado}")
    print("----------------------------------------")
    print("1. Comprimir videos en una carpeta")
    print("2. Renombrar imágenes por fecha")
    print("3. Utilidades de limpieza de Windows")
    print("4. Enviar correo de prueba")
    print("5. Salir")
    print("----------------------------------------")

# --- Función Principal de la Aplicación ---

def main():
    """
    Bucle principal de la aplicación. Gestiona el menú, la ejecución de tareas
    y el envío de informes por correo electrónico.
    """
    limpiar_pantalla()
    print("========================================")
    print("   BIENVENIDO A LA APP DE AUTOMATIZACIÓN  ")
    print("========================================")
    email_usuario = obtener_email_usuario()
    input("\nPresiona Enter para continuar al menú principal...")

    while True:
        mostrar_menu(email_usuario)
        opcion = input("Seleccione una opción y presione Enter: ")

        limpiar_pantalla()
        print(f"--- Ejecutando Opción {opcion} ---")
        
        informe_resultado = None
        asunto_correo = "Informe de Tarea de Automatización"

        try:
            if opcion == '1':
                asunto_correo = "Informe de Conversión de Videos"
                informe_resultado = iniciar_conversion_masiva()
            elif opcion == '2':
                asunto_correo = "Informe de Renombrado de Imágenes"
                informe_resultado = iniciar_renombrado()
            elif opcion == '3':
                asunto_correo = "Informe de Limpieza del Sistema"
                informe_resultado = iniciar_menu_limpieza()
            elif opcion == '4':
                asunto_correo = "Correo de Prueba desde la App"
                informe_resultado = (
                    f"Hola,\n\nEste es un correo de prueba para verificar que la configuración de envío "
                    f"a tu dirección ('{email_usuario}') funciona correctamente.\n\n"
                    "¡La prueba ha sido un éxito!"
                )
                print("Enviando correo de prueba...")
            elif opcion == '5':
                print("Gracias por usar la aplicación. ¡Hasta luego!")
                sys.exit(0)
            else:
                print("❌ Opción no válida. Por favor, elija un número del menú.")

            # ---- LÓGICA CENTRAL DE ENVÍO DE INFORMES ----
            # Si la función del módulo devolvió un informe (no es None)...
            if informe_resultado:
                print("\n--- Tarea finalizada. Preparando informe para envío por correo... ---")
                enviar_correo(
                    destinatario=email_usuario,
                    remitente=TEST_EMAIL_SENDER,
                    asunto=asunto_correo,
                    cuerpo=informe_resultado
                )
            else:
                print("\n--- Tarea finalizada o cancelada. No se generó ningún informe para enviar. ---")
        
        except Exception as e:
            # Capturador de errores general. Si algo falla en un módulo, la app no se cierra.
            print(f"\n🔥🔥🔥 ¡HA OCURRIDO UN ERROR INESPERADO! 🔥🔥🔥")
            print(f"La aplicación ha encontrado un problema durante la ejecución.")
            print(f"Detalle del error: {e}")
            
            # Intentamos notificar al usuario del error por correo.
            print("\nIntentando enviar un correo de notificación de error...")
            cuerpo_error = (
                f"La aplicación encontró un error grave mientras se ejecutaba la opción '{opcion}'.\n\n"
                f"El programa no pudo completar la tarea.\n\n"
                f"Detalle técnico del error:\n{type(e).__name__}: {e}"
            )
            enviar_correo(email_usuario, TEST_EMAIL_SENDER, "¡ERROR CRÍTICO! en la App de Automatización", cuerpo_error)

        input("\nPresione Enter para volver al menú principal...")

# --- Punto de Ejecución ---
if __name__ == "__main__":
    # Esta línea asegura que la función main() solo se ejecute
    # cuando el script es llamado directamente.
    main()