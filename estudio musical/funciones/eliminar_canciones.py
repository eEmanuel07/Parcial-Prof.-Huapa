from funciones import(
    mis_funciones,
    encontrar_ruta_csv_y_lista,
)
import csv

todos_los_datos = mis_funciones.cargar_todos_los_datos(mis_funciones.RUTA_RAIZ, mis_funciones.RUTA_RAIZ)


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

    ruta_csv, lista_local, idx = encontrar_ruta_csv_y_lista.encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre, todos_los_datos)
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