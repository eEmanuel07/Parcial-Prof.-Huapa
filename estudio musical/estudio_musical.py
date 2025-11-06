import os
import csv

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

if __name__ == "__main__":
    RUTA_RAIZ = "datos"
    os.makedirs(RUTA_RAIZ, exist_ok=True)
    todas_las_canciones = cargar_todos_los_datos(RUTA_RAIZ, RUTA_RAIZ)
    for c in todas_las_canciones:
        print(f"{c['genero']} / {c['subgenero']} / {c['artista']} → {c['nombre']}")



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



RUTA_RAIZ = "datos_musica"
os.makedirs(RUTA_RAIZ, exist_ok=True)

# --- Funciones ya implementadas (resumen para integridad) ---
# cargar_todos_los_datos(ruta_actual, ruta_base)
# alta_cancion(ruta_raiz)

# --- NUEVAS FUNCIONES AUXILIARES ---

def mostrar_estructura_y_filtrar(todos_los_datos):
    """Muestra todos los ítems y permite filtrar por género."""
    if not todos_los_datos:
        print("\n📦 No hay canciones registradas aún.")
        return

    print(f"\n🎧 Total de canciones: {len(todos_los_datos)}")
    print("\n--- Lista Completa ---")
    for idx, c in enumerate(todos_los_datos, 1):
        print(f"{idx}. {c['genero']} → {c['subgenero']} → {c['artista']} | {c['nombre']} "
                f"({c['duracion_seg']}s, {c['reproducciones_spotify']:,} reproducciones)")

    # Filtrado simple: por género
    print("\n🔍 Filtrar por género (dejar vacío para omitir):")
    filtro = input("Género: ").strip()
    if filtro:
        filtrados = [c for c in todos_los_datos if c['genero'].lower() == filtro.lower()]
        if filtrados:
            print(f"\n--- Resultados para '{filtro}' ---")
            for c in filtrados:
                print(f"• {c['artista']} - {c['nombre']} ({c['reproducciones_spotify']:,})")
        else:
            print("⚠️ No se encontraron canciones en ese género.")

def encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre_cancion, todos_los_datos):
    """
    Busca una canción específica y devuelve:
    - la ruta del CSV donde está
    - la lista actual de canciones en ese CSV
    - el índice de la canción en esa lista
    """
    ruta_csv = os.path.join(RUTA_RAIZ, genero, subgenero, artista, "canciones.csv")
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

def modificar_cancion(todos_los_datos):
    print("\n--- Modificar Canción ---")
    if not todos_los_datos:
        print("⚠️ No hay canciones para modificar.")
        return

    # Pedir identificación única
    genero = input("Género: ").strip()
    subgenero = input("Subgénero: ").strip()
    artista = input("Artista: ").strip()
    nombre = input("Nombre de la canción a modificar: ").strip()

    if not all([genero, subgenero, artista, nombre]):
        print("❌ Todos los campos son obligatorios.")
        return

    ruta_csv, lista_local, idx = encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre, todos_los_datos)
    if idx == -1:
        print("❌ Canción no encontrada.")
        return

    # Mostrar opciones de modificación
    print("\n¿Qué atributo desea modificar?")
    print("1. Duración (segundos)")
    print("2. Reproducciones en Spotify")
    opcion = input("Opción: ").strip()

    if opcion == '1':
        try:
            nuevo_valor = int(input("Nueva duración (segundos): "))
            if nuevo_valor <= 0:
                raise ValueError
            lista_local[idx]["duracion_seg"] = nuevo_valor
        except ValueError:
            print("❌ Valor inválido.")
            return
    elif opcion == '2':
        try:
            nuevo_valor = int(input("Nuevas reproducciones: "))
            if nuevo_valor < 0:
                raise ValueError
            lista_local[idx]["reproducciones_spotify"] = nuevo_valor
        except ValueError:
            print("❌ Valor inválido.")
            return
    else:
        print("❌ Opción no válida.")
        return

    # Sobrescribir el CSV completo
    try:
        with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "duracion_seg", "reproducciones_spotify"])
            writer.writeheader()
            writer.writerows(lista_local)
        print("✅ Canción modificada exitosamente.")
    except OSError as e:
        print(f"❌ Error al guardar: {e}")

def eliminar_cancion(todos_los_datos):
    print("\n--- Eliminar Canción ---")
    if not todos_los_datos:
        print("⚠️ No hay canciones para eliminar.")
        return

    genero = input("Género: ").strip()
    subgenero = input("Subgénero: ").strip()
    artista = input("Artista: ").strip()
    nombre = input("Nombre de la canción a eliminar: ").strip()

    if not all([genero, subgenero, artista, nombre]):
        print("❌ Todos los campos son obligatorios.")
        return

    ruta_csv, lista_local, idx = encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre, todos_los_datos)
    if idx == -1:
        print("❌ Canción no encontrada.")
        return

    # Confirmación
    conf = input(f"¿Está seguro de eliminar '{nombre}'? (s/n): ").lower()
    if conf != 's':
        print("Cancelado.")
        return

    # Eliminar de la lista local
    del lista_local[idx]

    # Sobrescribir el CSV
    try:
        with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "duracion_seg", "reproducciones_spotify"])
            if lista_local:  # Si hay canciones restantes
                writer.writeheader()
                writer.writerows(lista_local)
            else:
                # Opcional: eliminar el archivo si queda vacío
                pass
        print("✅ Canción eliminada exitosamente.")
    except OSError as e:
        print(f"❌ Error al guardar: {e}")

def mostrar_estadisticas_y_ordenar(todos_los_datos):
    if not todos_los_datos:
        print("\n📊 No hay datos para estadísticas.")
        return

    # Estadísticas
    total_canciones = len(todos_los_datos)
    total_reproducciones = sum(c["reproducciones_spotify"] for c in todos_los_datos)
    promedio_reproducciones = total_reproducciones / total_canciones
    artistas_por_genero = {}
    for c in todos_los_datos:
        artistas_por_genero[c["genero"]] = artistas_por_genero.get(c["genero"], set())
        artistas_por_genero[c["genero"]].add(c["artista"])
    conteo_artistas_por_genero = {g: len(a) for g, a in artistas_por_genero.items()}

    print("\n" + "="*50)
    print("📊 ESTADÍSTICAS")
    print("="*50)
    print(f"• Total de canciones: {total_canciones}")
    print(f"• Total de reproducciones: {total_reproducciones:,}")
    print(f"• Promedio de reproducciones por canción: {promedio_reproducciones:,.0f}")
    print("\n• Artistas por género:")
    for genero, cantidad in conteo_artistas_por_genero.items():
        print(f"  - {genero}: {cantidad} artistas")

    # Ordenamiento
    print("\n" + "="*50)
    print("📈 ORDENAR LISTA")
    print("="*50)
    print("1. Por nombre (A-Z)")
    print("2. Por reproducciones (descendente)")
    opcion = input("Elija criterio: ").strip()

    if opcion == '1':
        ordenada = sorted(todos_los_datos, key=lambda x: x["nombre"].lower())
    elif opcion == '2':
        ordenada = sorted(todos_los_datos, key=lambda x: x["reproducciones_spotify"], reverse=True)
    else:
        print("Opción inválida.")
        return

    print("\n--- Lista Ordenada ---")
    for c in ordenada[:10]:  # Mostrar primeras 10
        print(f"• {c['nombre']} - {c['reproducciones_spotify']:,}")
    if len(ordenada) > 10:
        print(f"... y {len(ordenada) - 10} más.")

# --- MENÚ PRINCIPAL ---
def menu_principal():
    while True:
        print("\n" + "="*50)
        print("🎵 GESTIÓN JERÁRQUICA DE CANCIONES 🎵")
        print("="*50)
        print("1. Alta de nueva canción")
        print("2. Mostrar todas las canciones y filtrar")
        print("3. Modificar una canción")
        print("4. Eliminar una canción")
        print("5. Estadísticas y ordenamiento")
        print("6. Salir")
        print("-"*50)

        opcion = input("Seleccione una opción: ").strip()

        # Recargar datos siempre desde disco (para reflejar cambios)
        todos_los_datos = cargar_todos_los_datos(RUTA_RAIZ, RUTA_RAIZ)

        if opcion == '1':
            alta_cancion(RUTA_RAIZ)
        elif opcion == '2':
            mostrar_estructura_y_filtrar(todos_los_datos)
        elif opcion == '3':
            modificar_cancion(todos_los_datos)
        elif opcion == '4':
            eliminar_cancion(todos_los_datos)
        elif opcion == '5':
            mostrar_estadisticas_y_ordenar(todos_los_datos)
        elif opcion == '6':
            print("👋 ¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")

# --- Punto de entrada ---
if __name__ == "__main__":
    menu_principal()