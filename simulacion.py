from graphviz import Digraph
from afd import *
from afn import *

def menu(tipo):
  print()
  print("#############################################")
  print("Desea realizar la simulacion de ", end="")
  if tipo == "afn": print("AFN?", end="")
  elif tipo == "afd": print("AFD?", end="")
  else: print("AFD minimizado?", end="")
  print(" (1/2):")
  print("1. Si")
  print("2. Salir")
  desicion = input(">> ")
  return desicion

def e_closure_state(state, visited=None):
    if visited is None:
        visited = set()

    if state in visited:
        return set()  # Return an empty set to prevent NoneType error
      
    visited.add(state)
    result = {state}  # Start with the current state in the result set

    for symbol, next_states in state.transiciones.items():
        for next_state in next_states:
            if symbol == 'ε':
                result.update(e_closure_state(next_state, visited))  # Update the result set

    return result


def e_closure(S):
    res = set()
    for state in S:
        res = res.union(e_closure_state(state))

    return res

def move(S,c):
  res = set()
  
  for state in S:
    for symbol,next_states in state.transiciones.items():
      for next_state in next_states:
        if symbol == c:
          res.add(next_state)

  return res

def simulacion_afn(afn):
  opcion = ""
  while(opcion != "2"):
    opcion = menu("afn")
    if opcion == "1":
      #simulacion
      w = input("Ingrese una cadena w: ")
      F = set()
      F.add(afn.aceptacion)
      So = set()
      So.add(afn.inicio)
      S = e_closure(So)
      for c in w:
        S = e_closure(move(S,c))

      if F.intersection(S):
        print("\nLa cadena es aceptada!")
      else:
        print("\nLa cadena NO es aceptada!")
    elif opcion == "2":
      print("Saliendo...")
      print("\n#############################################")
    else:
      print("\tError, ingreso incorrecto.")
      print("\n#############################################")

def simulacion_afd(afd):
  opcion = ""
  while(opcion != "2"):
    opcion = menu("afd")
    if opcion == "1":
      #simulacion
      w = input("Ingrese una cadena w: ")
      F = afd.aceptacion
      So = set()
      So.add(afd.inicio)
      S = So
      for char in w:
        S = move(S,char)
      if S:
        s = S.pop()
      else:
        s = None
      if s in F:
        print("\nLa cadena es aceptada!")
      else:
        print("\nLa cadena NO es aceptada!")
    elif opcion == "2":
      print("Saliendo...")
      print("\n#############################################")
    else:
      print("\tError, ingreso incorrecto.")
      print("\n#############################################")

def simulacion_afd_min(afd):
  opcion = ""
  while(opcion != "2"):
    opcion = menu("afd min")
    if opcion == "1":
      #simulacion
      w = input("Ingrese una cadena w: ")
      F = afd.aceptacion
      So = set()
      So.add(afd.inicio)
      S = So
      for char in w:
        S = move(S,char)
      if S:
        s = S.pop()
      else:
        s = None
      if s in F:
        print("\nLa cadena es aceptada!")
      else:
        print("\nLa cadena NO es aceptada!")
    elif opcion == "2":
      print("Saliendo...")
      print("\n#############################################")
    else:
      print("\tError, ingreso incorrecto.")
      print("\n#############################################")
