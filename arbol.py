def shunting_yard(regex):
    expresion_postfija = ''
    operadores = ['?', '|', '+', '.', '*']
    pila = []
    regex_formateado = formatear_regex(regex)
    
    indice = 0
    print("\n----Línea-----")
    while indice < len(regex_formateado):
        caracter = regex_formateado[indice]
        print('Carácter:' + caracter)
        
        if caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            while pila[-1] != '(':
                expresion_postfija += pila.pop()
            
            pila.pop()
        elif caracter in operadores:
            while len(pila) > 0:
                operador_alcanzado = pila[-1]
                precedencia_operador_alcanzado = obtener_precedencia(operador_alcanzado)
                precedencia_operador_actual = obtener_precedencia(caracter)
                
                if precedencia_operador_alcanzado >= precedencia_operador_actual:
                    expresion_postfija += pila.pop()
                else:
                    break
            
            pila.append(caracter)
        elif caracter == '\\':
            if indice + 1 < len(regex_formateado):
                print('Carácter escapado:' + regex_formateado[indice + 1])
                expresion_postfija += regex_formateado[indice + 1]
                indice += 1
        else:
            expresion_postfija += caracter
        
        indice += 1
        
        print('Pila:' + str(pila))
        print('Cola:' + expresion_postfija + '\n')
    
    while len(pila) > 0:
        expresion_postfija += pila.pop()
    
    return expresion_postfija

def obtener_precedencia(operador):
    if operador == '(':
        return 1
    elif operador == '|':
        return 2
    elif operador == '.':
        return 3
    elif operador == '?':
        return 4
    elif operador == '*':
        return 4
    elif operador == '+':
        return 4
    elif operador == '/':
        return 4
    elif operador == '-':
        return 4

def formatear_regex(regex):
    operadores_todos = ['|', '?', '+', '*']
    operadores_binarios = ['|']
    resultado = ''
    
    while '+' in regex:
        indice = regex.index('+')
        if regex[indice - 1] != ')':
            regex = regex.replace(regex[indice - 1] + "+", regex[indice - 1] + regex[indice - 1] + "*")
        elif regex[indice - 1] == ')':
            j = indice - 2
            contador = 0
            
            while (regex[j] != '(' or contador != 0) and j >= 0:
                if regex[j] == ')':
                    contador += 1
                elif regex[j] == '(':
                    contador -= 1
                j -= 1
            if regex[j] == '(' and contador == 0:
                sub_expresion = regex[j:indice]
                regex = regex.replace(sub_expresion + "+", sub_expresion + sub_expresion + "*")
                
    while '?' in regex:
        indice = regex.index('?')
        if regex[indice - 1] != ')':
            regex = regex.replace(regex[indice - 1] + "?", "(" + regex[indice - 1] + "|ε)")
        elif regex[indice - 1] == ')':
            j = indice - 2
            contador = 0
            
            while (regex[j] != '(' or contador != 0) and j >= 0:
                if regex[j] == ')':
                    contador += 1
                elif regex[j] == '(':
                    contador -= 1
                j -= 1
            if regex[j] == '(' and contador == 0:
                sub_expresion = regex[j:indice]
                regex = regex.replace(sub_expresion + "?", "(" + sub_expresion + "|ε)")
                
    indice = 0
    while indice < len(regex):
        char1 = regex[indice]
        
        if indice + 1 < len(regex):
            char2 = regex[indice + 1]
            
            if char1 == '\\':
                char1 += char2
                if indice + 2 < len(regex):
                    char2 = regex[indice + 2]
                else:
                    char2 = ''
                indice += 1
            elif char1 == '[':
                j = indice + 1
                while j < len(regex) and regex[j] != ']':
                    char1 += regex[j]
                    j += 1
                char1 += regex[j]
                indice = j
                if indice + 1 < len(regex):
                    char2 = regex[indice + 1]
                else:
                    char2 = ''
            resultado += char1
            
            if char2 != '' and char1 != '(' and char2 != ')' and char2 not in operadores_todos and char1 not in operadores_binarios:
                resultado += '.'
        else:
            resultado += char1
        indice += 1
    
    return resultado


def crear_arbol_sintaxis(postfijo):
    pila = []
    operadores = ['|', '*', '.']

    for caracter in postfijo:
        if caracter not in operadores:
            nuevo_nodo = Nodo(caracter)
            pila.append(nuevo_nodo)
        else:
            nuevo_nodo = Nodo(caracter)
            nuevo_nodo.derecha = pila.pop()
            if caracter != '*':
                nuevo_nodo.izquierda = pila.pop()
            pila.append(nuevo_nodo)
            
    return pila[0] if pila else None

def graficar_arbol(root, grafo=None):
    if grafo is None:
        grafo = Digraph()
        grafo.node(name=str(id(root)), label=root.valor)
    if root.izquierda:
        grafo.node(name=str(id(root.izquierda)), label=root.izquierda.valor)
        grafo.edge(str(id(root)), str(id(root.izquierda)))
        graficar_arbol(root.izquierda, grafo)
    if root.derecha:
        grafo.node(name=str(id(root.derecha)), label=root.derecha.valor)
        grafo.edge(str(id(root)), str(id(root.derecha)))
        graficar_arbol(root.derecha, grafo)
    return grafo

