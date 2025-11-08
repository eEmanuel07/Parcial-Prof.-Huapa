from funciones import(
    mis_funciones,
)
import csv
import os

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