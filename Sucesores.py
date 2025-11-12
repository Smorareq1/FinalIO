def encontrar_sucesores(datos_actividades):
    """
    Toma la lista de actividades y crea un diccionario
    que muestra qué actividades dependen de cada una (sus sucesores).
    """

    # 1. Inicializar el diccionario.
    #    Primero, obtenemos una lista de todas las actividades.
    todas_las_actividades = [item[0] for item in datos_actividades]

    # Creamos una entrada para cada una con una lista vacía.
    sucesores = {actividad: [] for actividad in todas_las_actividades}

    # 2. Llenar el diccionario de sucesores.
    #    Recorremos la tabla de nuevo.
    for item in datos_actividades:
        actividad_actual = item[0]
        predecesores_str = item[1]

        # Saltamos la actividad inicial
        if predecesores_str == '-':
            continue

        # Obtenemos la lista de predecesores
        predecesores_lista = predecesores_str.split(',')

        # Por cada predecesor en la lista...
        for pre in predecesores_lista:
            # ...agregamos la 'actividad_actual' como sucesora de ese predecesor.
            if pre in sucesores:
                sucesores[pre].append(actividad_actual)

    return sucesores


# --- Datos de entrada del ejemplo ---
# [Actividad, Predecesor(es), Duración]
datos = [
    ['A', '-', 18],
    ['B', '-', 15],
    ['C', 'A', 16],
    ['D', 'B', 16],
    ['E', 'B', 36],
    ['F', 'A', 16],
    ['G', 'C', 56],
    ['H', 'D', 61],
    ['I', 'A', 27],
    ['J', 'E,G,H', 10],
    ['K', 'F,I,J', 12],
]
# --- Ejecutar el programa ---
mapa_dependencias = encontrar_sucesores(datos)

print("--- Mapa de Sucesores (Qué depende de qué) ---")
print("Actividad | Depende(n) de ella:")
print("---------------------------------------------")

for actividad, lista_sucesores in mapa_dependencias.items():
    print(f"    {actividad}     | {lista_sucesores}")