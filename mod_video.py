import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# ===== CONFIGURACIÓN =====
# Ruta completa a ffmpeg.exe (ajusta según tu instalación)
FFMPEG_PATH = r"C:\Users\Isaac\Desktop\ffmpeg-2025-08-11-git-3542260376-essentials_build\bin\ffmpeg.exe"

# CRF: calidad vs peso (menor valor = más calidad, más peso)
CRF_VALUE = 28  
# Codec recomendado: H.265 para mejor compresión
VIDEO_CODEC = "libx265"  
# Extensiones de video a procesar
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv")  

def seleccionar_carpeta(mensaje):
    carpeta = filedialog.askdirectory(title=mensaje)
    return carpeta

def _comprimir_video(ruta_entrada, ruta_salida):
    comando = [
        FFMPEG_PATH, "-i", ruta_entrada,
        "-vcodec", VIDEO_CODEC,
        "-crf", str(CRF_VALUE),
        "-preset", "medium",  # velocidad de compresión
        "-y",
        ruta_salida
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8')

    #Si el codigo de retorno no es 0, significa que FFMPEG encontró un error.
    if resultado.returncode != 0:
        print(f"Error al procesar: {os.path.basename(ruta_entrada)}.")
        print("  Este video podría estar corrupto o usar un formato no soportado.")
        #Imprimir el error
        print(f"   Detalle del error de FFMPEG: {resultado.stderr.strip()}")
        return False
    return True


def iniciar_conversion_masiva():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    print("Por favor, seleccione la carpeta que contiene los videos a comprimir...")
    carpeta_origen = filedialog.askdirectory(title="Selecciona la carpeta de Origen de los Videos")
    if not carpeta_origen:
        print("Operación cancelada por el usuario.")
        return "El usuario canceló la selección de la carpeta de origen."
    
    print("Ahora, seleccione la carpeta donde se guardarán los videos comprimidos...")
    carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta de Destino para los Videos")
    if not carpeta_destino:
        print("Operación cancelada por el usuario.")
        return "El usuario canceló la selección de la carpeta de destino."
    
    informe_lineas = [
        "Informe de Conversión de Video",
        "==============================",
        f"Carpeta de Origen: {carpeta_origen}",
        f"Carpeta de Destino: {carpeta_destino}"
        f"Configuración: Codec={VIDEO_CODEC}, CRF={CRF_VALUE}",
        "" #Para separar.
    ]

    videos_a_procesar = [
        f for f in os.listdir(carpeta_origen)
        if os.path.isfile(os.path.join(carpeta_origen, f)) and f.lower().endswith(VIDEO_EXTENSIONS)
    ]

    if not videos_a_procesar:
        mensaje = "No se encontraron videos con las extensiones compatibles en la carpeta de origen."
        print(mensaje)
        informe_lineas.append(mensaje)
        return "\n".join(informe_lineas)
    
    print(f"\nSe encontraron {len(videos_a_procesar)} videos. Iniciando proceso de conversión...")
    informe_lineas.append(f"Se encontraron {len(videos_a_procesar)} videos para procesar: ")

    exitosos = 0
    fallidos = 0

    for archivo in videos_a_procesar:
        ruta_entrada = os.path.join(carpeta_origen, archivo)
        # Aseguramos que el archivo de salida tenga la extensión .mp4 para consistencia
        nombre_base, _ = os.path.splitext(archivo)
        ruta_salida = os.path.join(carpeta_destino, f"{nombre_base}.mp4")

        print(f"🔄 Comprimiendo: {archivo} ...")
        
        if _comprimir_video(ruta_entrada, ruta_salida):
            print(f"✅ Conversión exitosa: {os.path.basename(ruta_salida)}")
            informe_lineas.append(f"✅ ÉXITO: '{archivo}' -> '{os.path.basename(ruta_salida)}'")
            exitosos += 1
        else:
            # La función _comprimir_video ya imprimió el error detallado
            informe_lineas.append(f"❌ FALLO: '{archivo}' no pudo ser convertido.")
            fallidos += 1

    print("\n🎯 Proceso de conversión completado.")
    
    # Agregamos el resumen final al informe
    informe_lineas.append("\n--- RESUMEN DE LA OPERACIÓN ---")
    informe_lineas.append(f"Videos procesados exitosamente: {exitosos}")
    informe_lineas.append(f"Videos que fallaron: {fallidos}")
    informe_lineas.append(f"Total de videos analizados: {len(videos_a_procesar)}")
    
    # Unimos todas las líneas del informe en un solo string y lo devolvemos
    return "\n".join(informe_lineas)