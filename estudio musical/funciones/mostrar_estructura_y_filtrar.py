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