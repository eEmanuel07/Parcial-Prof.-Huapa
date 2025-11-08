import os
import csv

def alta_cancion(ruta_raiz):
    """
    Permite al usuario crear una nueva canción en la jerarquía.
    Crea las carpetas necesarias y añade la canción al CSV correspondiente.
    """
    print("\n--- Alta de Nueva Canción ---")
    
    # 1. Solicitar y validar los 3 niveles
    genero = input("Género (ej: Rock, Pop): ").strip()
    subgenero = input("Subgénero/Origen (ej: Nacional, Internacional): ").strip()
    artista = input("Artista (ej: Soda Stereo): ").strip()
    
    if not genero or not subgenero or not artista:
        print("❌ Error: Los tres niveles (género, subgénero, artista) son obligatorios.")
        return

    # 2. Solicitar y validar atributos de la canción
    nombre = input("Nombre de la canción: ").strip()
    if not nombre:
        print("❌ Error: El nombre de la canción no puede estar vacío.")
        return

    try:
        duracion = int(input("Duración en segundos (ej: 213 para 3:33): "))
        if duracion <= 0:
            print("❌ Error: La duración debe ser un número positivo.")
            return
    except ValueError:
        print("❌ Error: La duración debe ser un número entero.")
        return

    try:
        reproducciones = int(input("Reproducciones en Spotify (ej: 150000000): "))
        if reproducciones < 0:
            print("❌ Error: Las reproducciones no pueden ser negativas.")
            return
    except ValueError:
        print("❌ Error: Las reproducciones deben ser un número entero.")
        return

    # 3. Construir la ruta completa
    ruta_artista = os.path.join(ruta_raiz, genero, subgenero, artista)
    
    try:
        # Crear toda la jerarquía si no existe
        os.makedirs(ruta_artista, exist_ok=True)
    except OSError as e:
        print(f"❌ Error al crear la carpeta '{ruta_artista}': {e}")
        return

    # 4. Ruta del archivo CSV
    ruta_csv = os.path.join(ruta_artista, "canciones.csv")

    # 5. Verificar si el archivo ya existe para decidir si escribir encabezado
    archivo_existe = os.path.isfile(ruta_csv)

    # 6. Escribir en modo 'append'
    try:
        with open(ruta_csv, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "duracion_seg", "reproducciones_spotify"])
            
            # Escribir encabezado solo si es la primera canción
            if not archivo_existe:
                writer.writeheader()
            
            # Escribir la nueva canción
            writer.writerow({
                "nombre": nombre,
                "duracion_seg": duracion,
                "reproducciones_spotify": reproducciones
            })
        print(f"✅ Canción '{nombre}' agregada exitosamente a {genero} → {subgenero} → {artista}.")
    except OSError as e:
        print(f"❌ Error al escribir en el archivo: {e}")