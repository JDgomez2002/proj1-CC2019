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
from afn import *
from afd import *
from minimizacion import *

with open("expresiones.txt", 'r') as archivo:
  # encabezado
  print("############################")
  print("Proyecto no.1")

  num_de_expresion = 1

  for expresion in archivo:
    print("############################")
    # infix a postfix
    expresion = expresion.strip() # remover espacios en blanco " "
    expresion_postfix = shunting_yard(expresion, num_de_expresion) # infix a postfix
    print(f"Expresion regular: {expresion}") # imprimir expresion regular original
    print(f"Notacion postfix: {expresion_postfix}") # imprimir en nbotacion postfix

    # crear arbol
    arbol = crear_arbol_sintaxis(expresion_postfix) # crear arbol
    gafico_arbol = graficar_arbol(arbol) # crear grafico
    gafico_arbol.view(filename=f"Arbol {num_de_expresion}", cleanup=True) # Crear y mostrar archivo pdf

    afn = arbol_a_afn(arbol) # arbol a afn
    afn.estados = EstadoAFN.estados # tomar estados
    afn_graph = graficar_afn(afn.inicio) # graficar AFN
    afn_graph.view(filename=f"AFN {num_de_expresion}", cleanup=True) # crear y mostrar archivo pdf

    alfabeto = obtener_alfabeto(expresion_postfix) # obtiene el alfabeto del afd
    afd = afn_a_afd(alfabeto, afn) # crear afd con su alfabeto
    afd.estados = EstadoAFD.estados # obtiene los estados del afd
    afd_graph = graficar_afd(afd.inicio) # grafica el afd
    afd_graph.view(filename=f"AFD {num_de_expresion}", cleanup=True) # crear y mostrar archivo pdf

    # afd_min = afd_minimizado(alfabeto, afd) # minimizar afd
    # print(afd_min.estados_aceptacion) # imprimir estados de minimizacion
    # afdmin_graph = graficar_afd(afd_min.estado_inicial) # graficar afd minimizado
    # afdmin_graph.view(filename=f"AFD min{num_de_expresion}", cleanup=True) # crear y mostrar archivo pdf

    print("############################")

    num_de_expresion += 1

