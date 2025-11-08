import csv
import os


def cargar_todos_los_datos(ruta_actual, ruta_base):
    """
    Recorre recursivamente la estructura de carpetas desde ruta_actual.
    Devuelve una lista de diccionarios, donde cada diccionario representa
    una canción y contiene los 3 niveles jerárquicos + sus atributos.
    
    Parámetros:
        ruta_actual (str): Ruta actual que se está explorando.
        ruta_base (str): Ruta raíz del sistema (para calcular niveles).
    
    Retorna:
        list[dict]: Lista de canciones con metadatos de jerarquía.
    """
    items = []
    
    # Caso base: si es un archivo CSV llamado 'canciones.csv'
    if os.path.isfile(ruta_actual) and os.path.basename(ruta_actual) == "canciones.csv":
        # Calcular los 3 niveles: género, subgénero, artista
        rel_path = os.path.relpath(os.path.dirname(ruta_actual), ruta_base)
        partes = rel_path.split(os.sep)
        
        # Validar que haya exactamente 3 niveles
        if len(partes) == 3:
            genero, subgenero, artista = partes
        elif len(partes) == 2:
            # Esto puede pasar si empezamos desde una carpeta intermedia
            genero, subgenero = partes
            artista = ""
        elif len(partes) == 1:
            genero = partes[0]
            subgenero = artista = ""
        else:
            genero = subgenero = artista = ""
        
        try:
            with open(ruta_actual, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convertir tipos numéricos
                    try:
                        row["duracion_seg"] = int(row["duracion_seg"])
                        row["reproducciones_spotify"] = int(row["reproducciones_spotify"])
                    except (ValueError, KeyError):
                        print(f"Advertencia: dato inválido en {ruta_actual}, fila ignorada.")
                        continue
                    
                    # Añadir metadatos de jerarquía
                    item_con_jerarquia = {
                        "genero": genero,
                        "subgenero": subgenero,
                        "artista": artista,
                        "nombre": row["nombre"],
                        "duracion_seg": row["duracion_seg"],
                        "reproducciones_spotify": row["reproducciones_spotify"]
                    }
                    items.append(item_con_jerarquia)
        except (OSError, csv.Error) as e:
            print(f"Error al leer {ruta_actual}: {e}")
        return items

    # Paso recursivo: si es un directorio, explorar su contenido
    if os.path.isdir(ruta_actual):
        try:
            for nombre in os.listdir(ruta_actual):
                ruta_siguiente = os.path.join(ruta_actual, nombre)
                items.extend(cargar_todos_los_datos(ruta_siguiente, ruta_base))
        except OSError as e:
            print(f"No se pudo acceder a {ruta_actual}: {e}")
    
    return items

RUTA_RAIZ = "datos"
os.makedirs(RUTA_RAIZ, exist_ok=True)