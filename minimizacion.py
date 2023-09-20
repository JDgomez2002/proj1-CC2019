from afd import *

def afd_minimizado(alfabeto, afd):
  P = [set(afd.aceptacion), afd.estados - set(afd.aceptacion)]
  
  W = [set(afd.aceptacion), afd.estados - set(afd.aceptacion)]

  while W:
    A = W.pop(0)
    for char in alfabeto:
      estado_afectados = set()
      for estado in afd.estados:
        if char in estado.transiciones and estado.transiciones[char][0] in A:
          estado_afectados.add(estado)

      for Y in P:
        interseccion = Y.intersection(estado_afectados)
        diferencia = Y.difference(estado_afectados)

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

  afd_minimizado = AFD()
  
  estado_mapeado = {}
  for nuevo_grupo in P:
    nuevo_estado = EstadoAFD()
    for estado_anterior in nuevo_grupo:
      estado_mapeado[estado_anterior] = nuevo_estado
      if estado_anterior.es_aceptacion:
        nuevo_estado.is_accept = True
    afd_minimizado.estados.add(nuevo_estado)
  
  afd_minimizado.inicio = estado_mapeado[afd.inicio]
  
  for estado_anterior in afd.estados:
    nuevo_estado = estado_mapeado.get(estado_anterior)
    if nuevo_estado:
      for simbolo, transicion_anterior in estado_anterior.transiciones.items():
        estado_objetivo_anterior = transicion_anterior[0]
        estado_objetivo_actual = estado_mapeado.get(estado_objetivo_anterior)

        if estado_objetivo_actual:
          nuevo_estado.transiciones[simbolo] = [estado_objetivo_actual]
        else:
          print('{simbolo}')
    else:
      print('{estado_anterior}')
  
  return afd_minimizado