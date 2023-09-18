# Universidad del Valle de Guatemala
# Teoria de la computacion
# Gabriel Brolo
# Jose Daniel Gomez Cabrera 21429
# Gonzalo Santizo 21504
# Actividad: Proyecto 1

# importar graphviz
from graphviz import Digraph

# importar archivos con funciones


with open("expresiones.txt", 'r') as archivo:
  for expresion in archivo:
    print(expresion, end="")
