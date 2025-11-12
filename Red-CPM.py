def construir_red_cpm_optimizada(datos):
    """
    Construye una red CPM optimizada en formato AOA con el mínimo número de nodos.
    """

    # Crear diccionario de actividades
    actividades = {}
    for item in datos:
        nombre = item[0]
        predecesores = item[1].split(',') if item[1] != '-' else []
        duracion = item[2]
        actividades[nombre] = {
            'predecesores': [p.strip() for p in predecesores if p != '-'],
            'duracion': duracion,
            'nodo_inicio': None,
            'nodo_fin': None
        }

    # Ordenar topológicamente
    def ordenar_topologico():
        resultado = []
        visitadas = set()

        def dfs(act):
            if act in visitadas:
                return
            visitadas.add(act)
            for pred in actividades[act]['predecesores']:
                if pred in actividades:
                    dfs(pred)
            resultado.append(act)

        for act in actividades:
            dfs(act)
        return resultado

    orden = ordenar_topologico()

    # Asignar nodos progresivamente
    nodo_actual = 1
    nodos_terminacion = {}  # Mapea actividad → nodo donde termina

    # Nodo inicial
    nodo_inicio_proyecto = nodo_actual
    nodo_actual += 1

    aristas = []
    ficticias = []

    for actividad in orden:
        preds = actividades[actividad]['predecesores']

        if not preds:
            # Actividad inicial - empieza en nodo 1
            nodo_inicio = nodo_inicio_proyecto
        elif len(preds) == 1:
            # Un solo predecesor - empieza donde termina el predecesor
            pred = preds[0]
            if pred not in nodos_terminacion:
                # El predecesor aún no procesado (no debería pasar con orden topológico)
                nodo_inicio = nodo_actual
                nodo_actual += 1
            else:
                nodo_inicio = nodos_terminacion[pred]
        else:
            # Múltiples predecesores - necesita convergencia
            nodos_preds = [nodos_terminacion[p] for p in preds if p in nodos_terminacion]

            if len(set(nodos_preds)) == 1:
                # Todos los predecesores terminan en el mismo nodo
                nodo_inicio = nodos_preds[0]
            else:
                # Predecesores terminan en nodos diferentes - crear nodo de convergencia
                nodo_convergencia = nodo_actual
                nodo_actual += 1

                # Crear actividades ficticias desde cada predecesor al nodo de convergencia
                for pred in preds:
                    if pred in nodos_terminacion:
                        nodo_pred = nodos_terminacion[pred]
                        if nodo_pred != nodo_convergencia:
                            ficticias.append({
                                'desde': nodo_pred,
                                'hasta': nodo_convergencia,
                                'actividad': f'Fic({pred}→{actividad})',
                                'duracion': 0,
                                'ficticia': True
                            })

                nodo_inicio = nodo_convergencia

        # Determinar nodo de fin
        nodo_fin = nodo_actual
        nodo_actual += 1

        # Guardar la arista
        aristas.append({
            'desde': nodo_inicio,
            'hasta': nodo_fin,
            'actividad': actividad,
            'duracion': actividades[actividad]['duracion'],
            'ficticia': False
        })

        # Registrar dónde termina esta actividad
        nodos_terminacion[actividad] = nodo_fin

    # Encontrar nodo final (máximo nodo)
    todos_nodos = set()
    for arista in aristas + ficticias:
        todos_nodos.add(arista['desde'])
        todos_nodos.add(arista['hasta'])

    # Renumerar nodos secuencialmente
    nodos_ordenados = sorted(todos_nodos)
    mapeo = {viejo: nuevo for nuevo, viejo in enumerate(nodos_ordenados, 1)}

    # Aplicar renumeración
    for arista in aristas + ficticias:
        arista['desde'] = mapeo[arista['desde']]
        arista['hasta'] = mapeo[arista['hasta']]

    # Combinar aristas reales y ficticias
    todas_aristas = aristas + ficticias
    todas_aristas.sort(key=lambda x: (x['desde'], x['hasta']))

    nodos_lista = list(range(1, len(nodos_ordenados) + 1))

    return {
        'nodos': nodos_lista,
        'aristas': todas_aristas,
        'actividades_ficticias': [f['actividad'] for f in ficticias],
        'total_nodos': len(nodos_lista)
    }


def mostrar_red_cpm(datos):
    """Muestra la red CPM optimizada en formato texto"""

    red = construir_red_cpm_optimizada(datos)

    print("\n" + "=" * 80)
    print("RED CPM OPTIMIZADA (Formato AOA - Activity On Arrow)")
    print("=" * 80)

    print(f"\n📍 NODOS (Eventos): {red['total_nodos']} nodos")
    print("-" * 40)
    for nodo in red['nodos']:
        print(f"  • Nodo {nodo}")

    print(f"\n🔗 ARISTAS (Actividades): {len(red['aristas'])} aristas")
    print("-" * 40)
    print(f"{'Desde':<8} {'Hasta':<8} {'Actividad':<15} {'Duración':<10} {'Tipo':<10}")
    print("-" * 40)

    for arista in red['aristas']:
        tipo = "⚡Ficticia" if arista['ficticia'] else "Real"
        print(f"{arista['desde']:<8} {arista['hasta']:<8} {arista['actividad']:<15} "
              f"{arista['duracion']:<10} {tipo:<10}")

    if red['actividades_ficticias']:
        print(f"\n⚠️  Actividades ficticias creadas: {len(red['actividades_ficticias'])}")
        for fic in red['actividades_ficticias']:
            print(f"  • {fic}")
    else:
        print("\n✅ No se necesitan actividades ficticias")

    print("\n" + "=" * 80)
    print("INSTRUCCIONES PARA DIBUJAR:")
    print("=" * 80)
    print("1. Dibuja círculos numerados para cada nodo (1, 2, 3...)")
    print("2. Dibuja flechas desde 'Desde' hasta 'Hasta'")
    print("3. Etiqueta cada flecha con: actividad = duración")
    print("4. Las actividades ficticias se dibujan con línea punteada (duración=0)")
    print("5. El camino crítico: a→b→c→e→h→i (holgura = 0)")
    print("=" * 80 + "\n")

    return red


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

# Generar y mostrar la red
red = mostrar_red_cpm(datos)

# Exportar en formato simple para copiar
print("\n📋 FORMATO PARA COPIAR Y DIBUJAR:")
print("=" * 80)
print("\nNODOS:")
for nodo in red['nodos']:
    print(f"  Nodo {nodo}")

print("\nARISTAS (Flechas a dibujar):")
for arista in red['aristas']:
    tipo_str = " [FICTICIA - línea punteada]" if arista['ficticia'] else ""
    print(
        f"  Nodo {arista['desde']} → Nodo {arista['hasta']}: {arista['actividad']} (duración={arista['duracion']}){tipo_str}")
print("=" * 80)