from funciones import(
    mis_funciones,
    encontrar_ruta_csv_y_lista,
)
import csv

todos_los_datos = mis_funciones.cargar_todos_los_datos(mis_funciones.RUTA_RAIZ, mis_funciones.RUTA_RAIZ)

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

    ruta_csv, lista_local, idx = encontrar_ruta_csv_y_lista.encontrar_ruta_csv_y_lista(genero, subgenero, artista, nombre, todos_los_datos)
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