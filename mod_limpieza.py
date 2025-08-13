import os
import subprocess
import time
import shutil

def limpiar_pantalla():
    """Limpia la consola, compatible con Windows y otros sistemas operativos."""
    os.system('cls' if os.name == 'nt' else 'clear')

def limpiar_carpeta(nombre_carpeta, ruta_carpeta):
    """
    Elimina de forma segura todos los archivos y subcarpetas dentro de una ruta dada.

    Args:
        nombre_carpeta (str): Un nombre descriptivo para la carpeta (ej: "Temporales de Usuario").
        ruta_carpeta (str): La ruta absoluta a la carpeta que se va a limpiar.

    Returns:
        str: Un resumen de la operación de limpieza.
    """
    print(f"\n--- Limpiando: {nombre_carpeta}... ---")
    if not os.path.exists(ruta_carpeta):
        mensaje = f"La carpeta '{nombre_carpeta}' no existe en la ruta '{ruta_carpeta}'. Saltando."
        print(mensaje)
        return f"INFO: {mensaje}"

    archivos_eliminados = 0
    carpetas_eliminadas = 0

    # Usamos os.walk con topdown=False para eliminar primero el contenido de las carpetas
    # y luego las carpetas vacías, evitando errores.
    for raiz, dirs, ficheros in os.walk(ruta_carpeta, topdown=False):
        for fichero in ficheros:
            ruta_fichero = os.path.join(raiz, fichero)
            try:
                os.remove(ruta_fichero)
                archivos_eliminados += 1
            except PermissionError:
                print(f"   Aviso: Permiso denegado para eliminar '{ruta_fichero}' (en uso).")
            except Exception as e:
                print(f"   Error eliminando archivo '{ruta_fichero}': {e}")

        for dir in dirs:
            ruta_dir = os.path.join(raiz, dir)
            try:
                # Usamos shutil.rmtree porque es más robusto que os.rmdir
                # si una carpeta no quedó completamente vacía por errores de permisos.
                shutil.rmtree(ruta_dir)
                carpetas_eliminadas += 1
            except OSError as e:
                print(f"   Error eliminando carpeta '{ruta_dir}': {e}")

    resumen = (
        f"Resultado para '{nombre_carpeta}':\n"
        f"  - Ruta: {ruta_carpeta}\n"
        f"  - Se eliminaron {archivos_eliminados} archivos y {carpetas_eliminadas} carpetas."
    )
    print(resumen)
    return resumen

def limpiar_temp_usuario():
    """Limpia la carpeta de archivos temporales del usuario actual."""
    ruta_temp = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')
    return limpiar_carpeta("Archivos Temporales de Usuario", ruta_temp)

def limpiar_temp_windows():
    """Limpia la carpeta de archivos temporales del sistema Windows."""
    ruta_temp_win = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Temp")
    return limpiar_carpeta("Archivos Temporales de Windows", ruta_temp_win)

def limpiar_prefetch():
    """Limpia la carpeta Prefetch de Windows."""
    ruta_prefetch = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Prefetch")
    return limpiar_carpeta("Archivos Prefetch", ruta_prefetch)

def limpiar_cache_updates():
    """
    Limpia la caché de descargas de Windows Update. Requiere permisos de Administrador.
    """
    print("\n--- Limpiando Caché de Actualizaciones de Windows (Requiere Admin)... ---")
    informe_partes = ["Limpieza de Caché de Windows Update:"]
    ruta_updates = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "SoftwareDistribution", "Download")

    try:
        print("Deteniendo servicios de Windows Update (wuauserv y bits)...")
        subprocess.run("net stop wuauserv", shell=True, check=True, capture_output=True)
        subprocess.run("net stop bits", shell=True, check=True, capture_output=True)
        print("Servicios detenidos con éxito.")
        informe_partes.append("  - Servicios (wuauserv, bits) detenidos correctamente.")
        time.sleep(2)

        # Llamamos a limpiar_carpeta y añadimos su resumen al informe
        resumen_limpieza = limpiar_carpeta("Caché de Windows Update", ruta_updates)
        informe_partes.append(f"  - {resumen_limpieza}")

    except subprocess.CalledProcessError as e:
        error_msg = ("Error al detener los servicios. Esta operación debe ejecutarse como Administrador.")
        print(f"ERROR: {error_msg}")
        print(f"Detalle: {e.stderr.strip()}")
        informe_partes.append(f"  - FALLO: {error_msg}")
        return "\n".join(informe_partes)
    except Exception as e:
        error_msg = f"Ocurrió un error inesperado: {e}"
        print(f"ERROR: {error_msg}")
        informe_partes.append(f"  - FALLO: {error_msg}")
        return "\n".join(informe_partes)
    finally:
        print("\nReiniciando servicios de Windows Update...")
        subprocess.run("net start wuauserv", shell=True, check=False)
        subprocess.run("net start bits", shell=True, check=False)
        print("Comando de reinicio enviado.")
        informe_partes.append("  - Servicios reiniciados.")
    
    return "\n".join(informe_partes)

def iniciar_menu_limpieza():
    """
    Muestra el sub-menú para las opciones de limpieza y devuelve un informe
    agregado de todas las acciones realizadas durante la sesión.
    
    Returns:
        str or None: Un informe multi-línea si se realizó alguna acción,
                     o None si el usuario salió sin hacer nada.
    """
    informe_final = [
        "Informe de Limpieza del Sistema",
        "=============================",
        ""
    ]
    acciones_realizadas = False

    while True:
        limpiar_pantalla()
        print("--- MENÚ DE LIMPIEZA DE CACHÉ PARA WINDOWS ---")
        print("1. Limpiar archivos temporales de Usuario")
        print("2. Limpiar archivos temporales de Windows")
        print("3. Limpiar archivos prefetch")
        print("4. Limpiar caché de Windows Update (Requiere Admin)")
        print("5. !EJECUTAR TODAS LAS LIMPIEZAS!")
        print("6. Volver al menú principal")

        opcion = input("\nIntroduce tu elección: ")
        
        informe_accion = None
        if opcion in ['1', '2', '3', '4', '5']:
            acciones_realizadas = True

        if opcion == '1':
            informe_accion = limpiar_temp_usuario()
        elif opcion == '2':
            informe_accion = limpiar_temp_windows()
        elif opcion == '3':
            informe_accion = limpiar_prefetch()
        elif opcion == '4':
            informe_accion = limpiar_cache_updates()
        elif opcion == '5':
            print("\n!!! INICIANDO LIMPIEZA COMPLETA !!!")
            resumenes = [
                limpiar_temp_usuario(),
                limpiar_temp_windows(),
                limpiar_prefetch(),
                limpiar_cache_updates()
            ]
            informe_accion = "\n\n".join(resumenes)
            print("\n*** LIMPIEZA COMPLETA FINALIZADA ***")
        elif opcion == '6':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida. Por favor, introduce un número del 1 al 6.")

        if informe_accion:
            informe_final.append(informe_accion)
            informe_final.append("\n" + "="*40 + "\n")

        input("\nPresiona Enter para continuar...")

    # Solo devolvemos un informe si el usuario efectivamente limpió algo.
    if acciones_realizadas:
        return "\n".join(informe_final)
    else:
        return None # No se hizo nada, no hay informe que enviar.