def calcular_tiempos_cpm(datos):
    """
    Calcula ES, EF, LS, LF y holgura para cada actividad en una red CPM.
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
            'sucesores': [],
            'ES': 0,
            'EF': 0,
            'LS': float('inf'),
            'LF': float('inf'),
            'holgura': 0
        }

    # Identificar sucesores
    for nombre, info in actividades.items():
        for predecesor in info['predecesores']:
            if predecesor != '-':
                actividades[predecesor]['sucesores'].append(nombre)

    # FORWARD PASS: Calcular ES y EF
    def calcular_forward(nodo):
        if actividades[nodo]['EF'] > 0:  # Ya calculado
            return actividades[nodo]['EF']

        # ES = máximo EF de los predecesores
        es = 0
        for pred in actividades[nodo]['predecesores']:
            if pred != '-':
                pred_ef = calcular_forward(pred)
                es = max(es, pred_ef)

        actividades[nodo]['ES'] = es
        actividades[nodo]['EF'] = es + actividades[nodo]['duracion']
        return actividades[nodo]['EF']

    # Calcular ES y EF para todas las actividades
    for nombre in actividades:
        calcular_forward(nombre)

    # Encontrar duración del proyecto (máximo EF de TODAS las actividades)
    duracion_proyecto = max(info['EF'] for info in actividades.values())

    # Identificar actividades finales
    finales = [nombre for nombre, info in actividades.items()
               if not info['sucesores']]

    # BACKWARD PASS: Calcular LF y LS
    # CORRECCIÓN: Todas las actividades finales tienen LF = duración del proyecto
    for nodo in finales:
        actividades[nodo]['LF'] = duracion_proyecto
        actividades[nodo]['LS'] = duracion_proyecto - actividades[nodo]['duracion']

    # Procesar en orden topológico inverso
    visitados = set()

    def calcular_backward(nodo):
        if nodo in visitados:
            return

        # Primero procesar todos los sucesores
        for sucesor in actividades[nodo]['sucesores']:
            calcular_backward(sucesor)

        # Si no es actividad final, calcular LF como mínimo LS de sucesores
        if nodo not in finales:
            lf = float('inf')
            for sucesor in actividades[nodo]['sucesores']:
                lf = min(lf, actividades[sucesor]['LS'])
            actividades[nodo]['LF'] = lf
            actividades[nodo]['LS'] = lf - actividades[nodo]['duracion']

        visitados.add(nodo)

    # Calcular backward para todas las actividades
    for nombre in actividades:
        calcular_backward(nombre)

    # Calcular holgura
    for nombre, info in actividades.items():
        info['holgura'] = info['LS'] - info['ES']

    return actividades, duracion_proyecto


def encontrar_rutas_cpm(datos):
    """Encuentra todas las rutas posibles en una red CPM."""

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

    for nombre, info in actividades.items():
        for predecesor in info['predecesores']:
            if predecesor != '-':
                actividades[predecesor]['sucesores'].append(nombre)

    inicio = [nombre for nombre, info in actividades.items()
              if not info['predecesores'] or info['predecesores'] == ['-']]

    finales = [nombre for nombre, info in actividades.items()
               if not info['sucesores']]

    def buscar_rutas(nodo_actual, ruta_actual, duracion_actual):
        ruta_actual = ruta_actual + [nodo_actual]
        duracion_actual += actividades[nodo_actual]['duracion']

        if nodo_actual in finales:
            rutas.append((ruta_actual[:], duracion_actual))
            return

        for sucesor in actividades[nodo_actual]['sucesores']:
            buscar_rutas(sucesor, ruta_actual[:], duracion_actual)

    rutas = []
    for nodo_inicio in inicio:
        buscar_rutas(nodo_inicio, [], 0)

    rutas_ordenadas = sorted(rutas, key=lambda x: x[1], reverse=True)
    return rutas_ordenadas


def mostrar_analisis_completo(datos):
    """Muestra análisis completo de CPM"""

    print("\n" + "=" * 80)
    print("ANÁLISIS CPM COMPLETO")
    print("=" * 80)

    # Calcular tiempos
    actividades, duracion_proyecto = calcular_tiempos_cpm(datos)

    # Mostrar tabla de tiempos
    print("\nTABLA DE TIEMPOS POR ACTIVIDAD:")
    print("-" * 80)
    print(f"{'Act':<5} {'Dur':<5} {'ES':<6} {'EF':<6} {'LS':<6} {'LF':<6} {'Holgura':<8} {'Estado':<15}")
    print("-" * 80)

    for nombre in sorted(actividades.keys()):
        info = actividades[nombre]
        estado = "⭐ CRÍTICA" if info['holgura'] == 0 else ""
        print(f"{nombre:<5} {info['duracion']:<5} {info['ES']:<6} {info['EF']:<6} "
              f"{info['LS']:<6} {info['LF']:<6} {info['holgura']:<8} {estado:<15}")

    print("-" * 80)
    print(f"\nDuración total del proyecto: {duracion_proyecto} unidades")

    # Identificar ruta crítica
    criticas = [nombre for nombre, info in actividades.items() if info['holgura'] == 0]
    print(f"\nActividades críticas (holgura = 0): {', '.join(sorted(criticas))}")

    # Mostrar rutas
    print("\n" + "=" * 80)
    print("RUTAS POSIBLES (Ordenadas de mayor a menor duración)")
    print("=" * 80)

    rutas = encontrar_rutas_cpm(datos)
    for i, (ruta, duracion) in enumerate(rutas, 1):
        ruta_str = " → ".join(ruta)
        critica = "⭐ RUTA CRÍTICA" if duracion == duracion_proyecto else ""
        print(f"\nRuta #{i}: {ruta_str}")
        print(f"Duración: {duracion} unidades {critica}")

    print("\n" + "=" * 80)


# Datos de ejemplo
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

# Ejecutar análisis completo
mostrar_analisis_completo(datos)