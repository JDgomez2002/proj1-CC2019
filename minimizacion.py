class EstadoAFD:
    contador_estados = 'A'
    estados = set()

    def __init__(self, subconjunto=set()):
        self.nombre = str(EstadoAFD.contador_estados)
        EstadoAFD.contador_estados = chr(ord(EstadoAFD.contador_estados) + 1)
        EstadoAFD.estados.add(self)
        self.subconjunto = subconjunto

        self.transiciones = {}
        self.es_aceptacion = False

class AFD:
    def __init__(self):
        self.estado_inicial = None
        self.estados_aceptacion = set()
        self.estados = set()

def cerradura_epsilon_estado(estados, visitado=None):
    if visitado is None:
        visitado = set()

    if estados in visitado:
        return
        
    visitado.add(estados)

    for symbol, next_states in estados.transitions.items():
        for next_state in next_states:
            if symbol == 'ε':
                cerradura_epsilon_estado(next_state,visitado)

def cerradura_epsilon(S):
    res = set()
    for state in S:
        res = res.union(cerradura_epsilon_estado(state))

def alfabeto_regex(postfijo):
    alfabeto = set()
    reservadas = ['|', '*', '.', 'ε']

    for caracter in postfijo:
        if caracter not in reservadas:
            alfabeto.add(caracter)

    return alfabeto

def mover(S,c):
    res = set()
    
    for state in S:
        for symbol,next_states in state.transitions.items():
            for next_state in next_states:
                if symbol == c:
                    res.add(next_state)

def afn_a_afd(alfabeto, afn):
    F = set()
    F.add(afn.aceptacion)
    estados = []

    So = set()
    So.add(afn.inicio)

    afd = AFD()

    estados.append(EstadoAFD(subconjunto=cerradura_epsilon(So)))
    afd.estado_inicial = estados[0]

    if afn.aceptacion in estados[0].subconjunto:
        afd.estados_aceptacion.add(estados[0])
        estados[0].es_aceptacion = True

    contador = 0
    nuevos_estados = 0

    while contador != nuevos_estados or (contador == 0 and nuevos_estados == 0):
        if nuevos_estados != 0:
            contador += 1

        for simbolo in alfabeto:
            cambio = False
            subconjunto = cerradura_epsilon(mover(estados[contador].subconjunto, simbolo))

            for estado in estados:
                if estado.subconjunto == subconjunto:
                    estados[contador].transiciones[simbolo] = [estado]
                    cambio = True
                    break

            if not cambio:
                nuevo_estado = EstadoAFD(subconjunto)

                if afn.aceptacion in subconjunto:
                    afd.estados_aceptacion.add(nuevo_estado)
                    nuevo_estado.es_aceptacion = True

                estados[contador].transiciones[simbolo] = [nuevo_estado]
                estados.append(nuevo_estado)
                nuevos_estados += 1

    return afd

def afd_a_afd_min(alfabeto, afd):
    P = [set(afd.estados_aceptacion), afd.estados - set(afd.estados_aceptacion)]

    W = [set(afd.estados_aceptacion), afd.estados - set(afd.estados_aceptacion)]

    while W:
        A = W.pop(0)
        for c in alfabeto:
            estados_afectados = set()
            for estado in afd.estados:
                if c in estado.transiciones and estado.transiciones[c][0] in A:
                    estados_afectados.add(estado)

            for Y in P:
                interseccion = Y.intersection(estados_afectados)
                diferencia = Y.difference(estados_afectados)

                if interseccion and diferencia:
                    P.remove(Y)
                    P.append(interseccion)
                    P.append(diferencia)

                    if Y in W:
                        W.remove(Y)
                        W.append(interseccion)
                        W.append(diferencia)
                    else:
                        W.append(interseccion)
                        W.append(diferencia)

    afd_min = AFD()

    mapeo_estados = {}
    for grupo_nuevo_estado in P:
        nuevo_estado = EstadoAFD()
        for estado_antiguo in grupo_nuevo_estado:
            mapeo_estados[estado_antiguo] = nuevo_estado
            if estado_antiguo.es_aceptacion:
                nuevo_estado.es_aceptacion = True
        afd_min.estados.add(nuevo_estado)

    afd_min.estado_inicial = mapeo_estados[afd.estado_inicial]

    for estado_antiguo in afd.estados:
        nuevo_estado = mapeo_estados.get(estado_antiguo)
        if nuevo_estado:
            for simbolo, transiciones_antiguas in estado_antiguo.transiciones.items():
                estado_destino_antiguo = transiciones_antiguas[0]
                estado_destino_nuevo = mapeo_estados.get(estado_destino_antiguo)

                if estado_destino_nuevo:
                    nuevo_estado.transiciones[simbolo] = [estado_destino_nuevo]
                else:
                    print(f'{simbolo}')
        else:
            print(f'{estado_antiguo}')

    return afd_min
