from funciones import(
    mis_funciones,
    
)
import csv
import os

def encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre_cancion, todos_los_datos):
    """
    Busca una canción específica y devuelve:
    - la ruta del CSV donde está
    - la lista actual de canciones en ese CSV
    - el índice de la canción en esa lista
    """
    ruta_csv = os.path.join(mis_funciones.RUTA_RAIZ, genero, subgenero, artista, "canciones.csv")
    if not os.path.isfile(ruta_csv):
        return None, [], -1

    # Leer el CSV completo
    lista_local = []
    try:
        with open(ruta_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                fila["duracion_seg"] = int(fila["duracion_seg"])
                fila["reproducciones_spotify"] = int(fila["reproducciones_spotify"])
                lista_local.append(fila)
    except Exception as e:
        print(f"❌ Error al leer {ruta_csv}: {e}")
        return None, [], -1

    # Buscar la canción por nombre
    for i, cancion in enumerate(lista_local):
        if cancion["nombre"] == nombre_cancion:
            return ruta_csv, lista_local, i

    return ruta_csv, lista_local, -1