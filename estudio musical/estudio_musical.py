from funciones import(
    mis_funciones,
    alta_cancion,
    eliminar_canciones,
    encontrar_ruta_csv_y_lista,
    modificar_canciones,
    mostrar_estadisticas_y_ordenar,
    mostrar_estructura_y_filtrar
)
import csv
import os

if __name__ == "__main__":
    RUTA_RAIZ = "datos"
    os.makedirs(RUTA_RAIZ, exist_ok=True)
    todas_las_canciones = mis_funciones.cargar_todos_los_datos(RUTA_RAIZ, RUTA_RAIZ)
    for c in todas_las_canciones:
        print(f"{c['genero']} / {c['subgenero']} / {c['artista']} → {c['nombre']}")

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
        todos_los_datos = mis_funciones.cargar_todos_los_datos(RUTA_RAIZ, RUTA_RAIZ)

        if opcion == '1':
            alta_cancion.alta_cancion(RUTA_RAIZ)
        elif opcion == '2':
            mostrar_estructura_y_filtrar.mostrar_estructura_y_filtrar(todos_los_datos)
        elif opcion == '3':
            modificar_canciones.modificar_cancion(todos_los_datos)
        elif opcion == '4':
            eliminar_canciones.eliminar_cancion(todos_los_datos)
        elif opcion == '5':
            mostrar_estadisticas_y_ordenar.mostrar_estadisticas_y_ordenar(todos_los_datos)
        elif opcion == '6':
            print("👋 ¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    try:
        menu_principal()
    except ValueError:
        print("Error de Sistema")