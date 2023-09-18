from graphviz import Digraph

class AFD:
  def __init__(self):
    self.inicio = None
    self.aceptacion = set()
    self.estados = set()

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

def cierre_epsilon_estado(estado, visitados=None):
  if visitados is None:
    visitados = set()

  if estado in visitados:
    return
      
  visitados.add(estado)

  for simbolo, estados_siguientes in estado.transiciones.items():
    for estado_siguiente in estados_siguientes:
      if simbolo == 'ε':
        cierre_epsilon_estado(estado_siguiente, visitados)

  return visitados

def mover(S, c):
  resultado = set()
    
  for estado in S:
    for simbolo, estados_siguientes in estado.transiciones.items():
      for estado_siguiente in estados_siguientes:
        if simbolo == c:
          resultado.add(estado_siguiente)
    
  return resultado

def cierre_epsilon(S):
  resultado = set()
  for estado in S:
    resultado = resultado.union(cierre_epsilon_estado(estado))
        
  return resultado

def obtener_alfabeto(postfijo):
  alfabeto = set()
  reservados = ['|', '*', '.', 'ε']
    
  for caracter in postfijo:
    if caracter not in reservados:
      alfabeto.add(caracter)
            
  return alfabeto

def afn_a_afd(alfabeto, afn):
  F = set()
  F.add(afn.aceptacion)
  estados = []
    
  So = set()
  So.add(afn.inicio)
    
  afd = AFD()
    
  estados.append(EstadoAFD(subconjunto=cierre_epsilon(So)))
  afd.inicio = estados[0]
    
  if afn.aceptacion in estados[0].subconjunto:
    afd.aceptacion.add(estados[0])
    estados[0].es_aceptacion = True
    
  contador = 0
  nuevos_estados = 0
    
  while contador != nuevos_estados or (contador == 0 and nuevos_estados == 0):
    if nuevos_estados != 0:
      contador += 1
        
    for simbolo in alfabeto:
      cambio = False
      subconjunto = cierre_epsilon(mover(estados[contador].subconjunto, simbolo))
            
      for estado in estados:
        if estado.subconjunto == subconjunto:
          estados[contador].transiciones[simbolo] = [estado]
          cambio = True
          break
            
      if not cambio:
        nuevo_estado = EstadoAFD(subconjunto)
                
        if afn.aceptacion in subconjunto:
          afd.aceptacion.add(nuevo_estado)
          nuevo_estado.es_aceptacion = True
                
        estados[contador].transiciones[simbolo] = [nuevo_estado]
        estados.append(nuevo_estado)
        nuevos_estados += 1
    
  return afd

def graficar_afd(estado, grafo=None, visitados=None):
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
      graficar_afd(estado_siguiente, grafo, visitados)

  return grafo
