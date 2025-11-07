def construir_red_cpm(datos_actividades):
    """
    Construye una red CPM (AOA) a partir de una lista de actividades,
    sus predecesores y duraciones.

    Esta versión es ALGORÍTMICA y LÓGICA. No está optimizada
    manualmente como el diagrama de 8 nodos.
    """

    # 1. Pre-procesar los datos
    tareas = {}
    todas_las_tareas = set()
    tareas_predecesoras = set()

    for item in datos_actividades:
        actividad = item[0]
        predecesores = set(item[1].split(',')) if item[1] != '-' else set()
        duracion = item[2]

        tareas[actividad] = {'pre': predecesores, 'dur': duracion}
        todas_las_tareas.add(actividad)
        tareas_predecesoras.update(predecesores)

    # Encontrar las actividades finales (las que no son predecesoras de nadie)
    tareas_finales = todas_las_tareas - tareas_predecesoras

    # 2. Inicializar estructuras del grafo
    grafo_aristas = []

    # Mapea un nombre de actividad al nodo donde TERMINA
    nodo_fin_actividad = {}

    procesadas = set()

    # El nodo 1 es siempre el inicio
    nodo_counter = 1
    nodo_inicio = nodo_counter
    nodo_counter += 1

    # El nodo final único
    nodo_final_proyecto = -1  # Se creará cuando sea necesario

    # 3. Construir el grafo iterativamente
    while len(procesadas) < len(todas_las_tareas):

        tareas_para_agregar = []
        for actividad, data in tareas.items():
            # Si la tarea no ha sido procesada Y todos sus predecesores sí...
            if actividad not in procesadas and data['pre'].issubset(procesadas):
                tareas_para_agregar.append(actividad)

        if not tareas_para_agregar:
            print("Error: Se detectó un ciclo o dependencia rota en la red.")
            return []

        for actividad in tareas_para_agregar:
            data = tareas[actividad]

            # --- Encontrar el NODO DE INICIO para esta actividad ---
            nodo_inicio_actual = -1

            if not data['pre']:
                # Es una actividad inicial
                nodo_inicio_actual = nodo_inicio
            else:
                # Tiene predecesores. Encontrar en qué nodos terminaron.
                nodos_fin_predecesores = {nodo_fin_actividad[p] for p in data['pre']}

                if len(nodos_fin_predecesores) == 1:
                    # Caso simple: todos los predecesores convergen en un único nodo
                    nodo_inicio_actual = nodos_fin_predecesores.pop()
                else:
                    # Caso complejo: Múltiples predecesores terminan en nodos diferentes.
                    # (Ej: 'e' necesita 'c' y 'd' del ejemplo)
                    # Creamos un nuevo nodo de convergencia y aristas ficticias.
                    nodo_convergencia = nodo_counter
                    nodo_counter += 1

                    for nodo_fin in nodos_fin_predecesores:
                        arista_ficticia = {
                            'actividad': f'Fic ({nodo_fin}->{nodo_convergencia})',
                            'inicio': nodo_fin,
                            'fin': nodo_convergencia
                        }
                        grafo_aristas.append(arista_ficticia)

                    nodo_inicio_actual = nodo_convergencia

            # --- Encontrar el NODO DE FIN para esta actividad ---
            nodo_fin_actual = -1

            if actividad in tareas_finales:
                # Es una actividad final. Debe apuntar al nodo final del proyecto.
                if nodo_final_proyecto == -1:
                    # Creamos el nodo final si es la primera vez que lo necesitamos
                    nodo_final_proyecto = nodo_counter
                    nodo_counter += 1
                nodo_fin_actual = nodo_final_proyecto
            else:
                # No es una actividad final, así que creamos un nuevo nodo de evento para ella.
                nodo_fin_actual = nodo_counter
                nodo_counter += 1

            # Añadir la arista de la actividad real al grafo
            grafo_aristas.append({
                'actividad': actividad,
                'inicio': nodo_inicio_actual,
                'fin': nodo_fin_actual
            })

            # Registrar dónde termina esta actividad
            nodo_fin_actividad[actividad] = nodo_fin_actual
            procesadas.add(actividad)

    # 4. Manejar el caso donde múltiples tareas finales terminan en nodos separados
    # (Deben converger al nodo_final_proyecto)
    for arista in grafo_aristas:
        actividad = arista['actividad']
        if actividad in tareas_finales and arista['fin'] != nodo_final_proyecto:
            # Esta actividad final se creó antes de que supiéramos del nodo final.
            # La redirigimos al nodo final.
            arista['fin'] = nodo_final_proyecto

    return grafo_aristas


# --- Datos de entrada del ejemplo ---
# [Actividad, Predecesor(es), Duración]
datos = [
    ['a', '-', 20],
    ['b', 'a', 10],
    ['c', 'b', 8],
    ['d', 'a', 11],
    ['e', 'c,d', 7],
    ['f', 'e', 6],
    ['g', 'd', 12],
    ['h', 'e', 13],
    ['i', 'g,h', 5]
]

# --- Ejecutar el programa ---
red_generada = construir_red_cpm(datos)

print("--- Red CPM Generada (Nodos y Aristas) ---")
print(f"{'Actividad':<10} | {'Nodo Inicio':<12} | {'Nodo Fin':<10}")
print("-" * 45)

for arista in red_generada:
    print(f"{arista['actividad']:<10} | {arista['inicio']:<12} | {arista['fin']:<10}")