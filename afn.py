from graphviz import Digraph

# clase de afn
class AFN:
  def __init__(self):
    self.inicio = None
    self.aceptacion = None
    self.estados = set()

# clase de estados de afn
class EstadoAFN:
  contador_estados = 0
  estados = set()

  def __init__(self):
    self.nombre = str(EstadoAFN.contador_estados)
    EstadoAFN.contador_estados += 1
    EstadoAFN.estados.add(self)

    self.transiciones = {}
    self.es_aceptacion = False

# convertir arbol a afn
def arbol_a_afn(nodo, izquierdo_inicio=None, nodo_inicial=True):
  if not nodo:
    return None
  
  afn = AFN()
  
  if nodo.valor not in ['|', '.', '*']:
    if izquierdo_inicio:
      inicio = izquierdo_inicio
    else:
      inicio = EstadoAFN()

    aceptacion = EstadoAFN()

    if nodo_inicial:
      aceptacion.es_aceptacion = True

    inicio.transiciones[nodo.valor] = [aceptacion]
    afn.inicio = inicio
    afn.aceptacion = aceptacion
  elif nodo.valor == '|':
    if izquierdo_inicio:
      inicio = izquierdo_inicio
    else:
      inicio = EstadoAFN()

    afn_izquierdo = arbol_a_afn(nodo=nodo.izq, nodo_inicial=False)
    afn_derecho = arbol_a_afn(nodo=nodo.der, nodo_inicial=False)

    aceptacion = EstadoAFN()
    if nodo_inicial:
      aceptacion.es_aceptacion = True
    
    inicio.transiciones['ε'] = [afn_izquierdo.inicio, afn_derecho.inicio]
    afn_izquierdo.aceptacion.transiciones['ε'] = [aceptacion]
    afn_derecho.aceptacion.transiciones['ε'] = [aceptacion]
    
    afn.inicio = inicio
    afn.aceptacion = aceptacion
  elif nodo.valor == '*':
    if izquierdo_inicio:
      inicio = izquierdo_inicio
    else:
      inicio = EstadoAFN()

    afn_interno = arbol_a_afn(nodo=nodo.der, nodo_inicial=False)
    
    aceptacion = EstadoAFN()
    if nodo_inicial:
      aceptacion.es_aceptacion = True
    
    inicio.transiciones['ε'] = [afn_interno.inicio, aceptacion]
    afn_interno.aceptacion.transiciones['ε'] = [afn_interno.inicio, aceptacion]
    
    afn.inicio = inicio
    afn.aceptacion = aceptacion
  elif nodo.valor == '.':
    afn_izquierdo = arbol_a_afn(nodo=nodo.izq, nodo_inicial=False)
    afn_derecho = arbol_a_afn(nodo=nodo.der, izquierdo_inicio=afn_izquierdo.aceptacion, nodo_inicial=False)
    
    afn.inicio = afn_izquierdo.inicio
    afn.aceptacion = afn_derecho.aceptacion
    if nodo_inicial:
      afn.aceptacion.es_aceptacion = True

  return afn

# graficar afn
def graficar_afn(estado, grafo=None, visitados=None):
  if visitados is None:
    visitados = set()

  if estado in visitados:
    return grafo

  if grafo is None:
    grafo = Digraph(engine='dot', graph_attr={'rankdir': 'LR'})
  
  if estado.es_aceptacion:
    grafo.node(name=str(id(estado)), label=estado.nombre, shape='doublecircle')
  else:
    grafo.node(name=str(id(estado)), label=estado.nombre, shape='circle')
      
  visitados.add(estado)

  for simbolo, estados_siguientes in estado.transiciones.items():
    for estado_siguiente in estados_siguientes:
      grafo.edge(str(id(estado)), str(id(estado_siguiente)), label=simbolo)
      graficar_afn(estado_siguiente, grafo, visitados)

  return grafo
