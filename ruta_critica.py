def encontrar_rutas_cpm(datos):
    """
    Encuentra todas las rutas posibles en una red CPM y las ordena de más larga a más corta.

    Args:
        datos: Lista de listas con formato [actividad, predecesores, duración]

    Returns:
        Lista de tuplas (ruta, duración_total) ordenadas de mayor a menor duración
    """

    # Crear diccionario de actividades
    actividades = {}
    for item in datos:
        nombre = item[0]
        predecesores = item[1].split(',') if item[1] != '-' else []
        duracion = item[2]
        actividades[nombre] = {
            'predecesores': predecesores,
            'duracion': duracion,
            'sucesores': []
        }

    # Identificar sucesores de cada actividad
    for nombre, info in actividades.items():
        for predecesor in info['predecesores']:
            if predecesor != '-':
                actividades[predecesor]['sucesores'].append(nombre)

    # Encontrar actividad inicial (sin predecesores)
    inicio = [nombre for nombre, info in actividades.items()
              if not info['predecesores'] or info['predecesores'] == ['-']]

    # Encontrar actividades finales (sin sucesores)
    finales = [nombre for nombre, info in actividades.items()
               if not info['sucesores']]

    # Función recursiva para encontrar todas las rutas
    def buscar_rutas(nodo_actual, ruta_actual, duracion_actual):
        ruta_actual = ruta_actual + [nodo_actual]
        duracion_actual += actividades[nodo_actual]['duracion']

        # Si llegamos a un nodo final, guardamos la ruta
        if nodo_actual in finales:
            rutas.append((ruta_actual[:], duracion_actual))
            return

        # Continuar con los sucesores
        for sucesor in actividades[nodo_actual]['sucesores']:
            buscar_rutas(sucesor, ruta_actual[:], duracion_actual)

    # Buscar todas las rutas desde cada nodo inicial
    rutas = []
    for nodo_inicio in inicio:
        buscar_rutas(nodo_inicio, [], 0)

    # Ordenar rutas de más larga a más corta
    rutas_ordenadas = sorted(rutas, key=lambda x: x[1], reverse=True)

    return rutas_ordenadas


def mostrar_rutas(rutas):
    """Muestra las rutas de forma legible"""
    print("\n" + "=" * 70)
    print("RUTAS CPM ORDENADAS POR DURACIÓN (Mayor a Menor)")
    print("=" * 70)

    for i, (ruta, duracion) in enumerate(rutas, 1):
        ruta_str = " → ".join(ruta)
        print(f"\nRuta #{i}: {ruta_str}")
        print(f"Duración total: {duracion} unidades")
        if i == 1:
            print("⭐ RUTA CRÍTICA (más larga)")

    print("\n" + "=" * 70)


# Datos de ejemplo
datos = [
    ['a', '-', 20],
    ['b', 'a', 10],
    ['c', 'b', 8],
    ['d', 'a', 11],
    ['e', 'c,d', 7],
    ['f', 'e', 6],
    ['g', 'd', 12],
    ['h', 'e', 13],
    ['i', 'g,h', 5],
]

# Ejecutar análisis
rutas = encontrar_rutas_cpm(datos)
mostrar_rutas(rutas)

# Información adicional
print("\nRESUMEN:")
print(f"Total de rutas encontradas: {len(rutas)}")
print(f"Ruta más larga (crítica): {rutas[0][1]} unidades")
print(f"Ruta más corta: {rutas[-1][1]} unidades")