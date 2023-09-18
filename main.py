# Universidad del Valle de Guatemala
# Teoria de la computacion
# Gabriel Brolo
# Jose Daniel Gomez Cabrera 21429
# Gonzalo Santizo 21504
# Actividad: Proyecto 1

# importar graphviz
from graphviz import Digraph

# importar archivos con funciones
from arbol import *

with open("expresiones.txt", 'r') as archivo:
  num_de_expresion = 1

  for expresion in archivo:
    # infix a postfix
    expresion = expresion.strip() # remover espacios en blanco
    expresion_postfix = shunting_yard(expresion, num_de_expresion) # infix a postfix
    print(f"Expresion regular: {expresion}") # imprimir expresion regular original
    print(f"Notacion postfix: {expresion_postfix}") # imprimir en nbotacion postfix

    # crear arbol
    arbol = crear_arbol_sintaxis(expresion_postfix) # crear arbol
    gafico_arbol = graficar_arbol(arbol) # crear grafico
    gafico_arbol.view(filename=f"Arbol No.{num_de_expresion}", cleanup=True) # Crear y mostrar archivo

    print("######################")

    num_de_expresion += 1

