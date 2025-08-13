import os
import shutil

# Importamos la configuración desde nuestro archivo central
from config import IMAGE_EXTENSIONS

def iniciar_renombrado():
    """
    Pide al usuario una carpeta y un prefijo para renombrar imágenes secuencialmente
    basándose en su fecha de creación. Devuelve un informe detallado de la operación.

    Returns:
        str: Un informe multi-línea del resultado del proceso.
    """
    # 1. OBTENER Y VALIDAR LA CARPETA DE ORIGEN
    # Usamos .strip('"') por si el usuario arrastra la carpeta y la ruta queda entre comillas.
    carpeta = input("Arrastra una carpeta con imágenes aquí y presiona Enter: ").strip().strip('"')
    if not carpeta or not os.path.isdir(carpeta):
        error_msg = "❌ Error: La ruta proporcionada no es una carpeta válida o está vacía. Operación cancelada."
        print(error_msg)
        return "Operación cancelada: La ruta proporcionada no era una carpeta válida."

    # 2. OBTENER Y VALIDAR EL PREFIJO
    nombre_prefijo = input("Escribe el prefijo para los nuevos nombres (ej: Vacaciones_2023): ").strip()
    if not nombre_prefijo:
        error_msg = "❌ Error: El prefijo no puede estar vacío. Operación cancelada."
        print(error_msg)
        return "Operación cancelada: No se proporcionó un prefijo."

    # 3. PREPARAR EL INFORME Y EL DESTINO
    # Creamos la carpeta de destino dentro de la carpeta original.
    destino = os.path.join(carpeta, nombre_prefijo)
    os.makedirs(destino, exist_ok=True)

    # Inicializamos la lista que contendrá las líneas del informe para el email
    informe_lineas = [
        "Informe de Renombrado de Imágenes",
        "=================================",
        f"Carpeta Analizada: {carpeta}",
        f"Prefijo Utilizado: '{nombre_prefijo}'",
        f"Carpeta de Destino: {destino}",
        "" # Línea en blanco para espaciar
    ]

    # 4. BUSCAR Y ORDENAR LAS IMÁGENES
    try:
        # Usamos una expresión generadora para eficiencia.
        # os.path.getctime ordena por fecha de creación (en Windows) o de último cambio de metadatos (en Unix).
        imgs = sorted(
            (f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f)) and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS),
            key=lambda f: os.path.getctime(os.path.join(carpeta, f))
        )
    except FileNotFoundError:
        # Medida de seguridad, aunque os.path.isdir ya debería haberlo prevenido.
        error_msg = f"Error crítico: No se pudo acceder a la carpeta '{carpeta}' durante el escaneo."
        print(error_msg)
        return error_msg

    if not imgs:
        mensaje = "No se encontraron imágenes con las extensiones compatibles en la carpeta de origen."
        print(mensaje)
        informe_lineas.append(mensaje)
        return "\n".join(informe_lineas)

    # 5. PROCESAR LAS IMÁGENES Y CONSTRUIR EL INFORME
    print(f"\nSe encontraron {len(imgs)} imágenes. Renombrando y moviendo...")
    informe_lineas.append("Cambios realizados:")
    informe_lineas.append("-------------------")

    for i, img in enumerate(imgs, 1):
        # Generamos el nuevo nombre. Usamos :03d para tener ceros a la izquierda (001, 002...),
        # lo que asegura un orden correcto en el explorador de archivos.
        extension = os.path.splitext(img)[1].lower()
        nombre_nuevo = f"{nombre_prefijo}_{i:03d}{extension}"
        
        ruta_origen = os.path.join(carpeta, img)
        ruta_destino = os.path.join(destino, nombre_nuevo)
        
        # Registramos la acción tanto en consola como en el informe
        cambio_str = f"   '{img}' -> '{nombre_nuevo}'"
        print(cambio_str)
        informe_lineas.append(cambio_str)
        
        # Movemos el archivo a su nueva ubicación con su nuevo nombre
        shutil.move(ruta_origen, ruta_destino)

    print(f"\n✅ {len(imgs)} imágenes renombradas y movidas exitosamente a la carpeta '{nombre_prefijo}'.")

    # 6. FINALIZAR Y DEVOLVER EL INFORME COMPLETO
    informe_lineas.append("\n--- RESUMEN DE LA OPERACIÓN ---")
    informe_lineas.append(f"Total de imágenes renombradas: {len(imgs)}")
    
    return "\n".join(informe_lineas)