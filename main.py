# Universidad del Valle de Guatemala
# Teoria de la computacion
# Gabriel Brolo
# Jose Daniel Gomez Cabrera 21429
# Gonzalo Santizo 21504
# Actividad: Proyecto 1



def shunting_yard(regex):
    postfix_expression = ''
    operators = ['|', '?', '+', '*', '.']
    operator_stack = []
    formatted_regex = format_regular_expression(regex)
    
    index = 0
    print("\n----Line-----")
    while index < len(formatted_regex):
        character = formatted_regex[index]
        print('Character:' + character)
        
        if character == '(':
            operator_stack.append(character)
        elif character == ')':
            while operator_stack[-1] != '(':
                postfix_expression += operator_stack.pop()
            
            operator_stack.pop()
        elif character in operators:
            while len(operator_stack) > 0:
                peeked_operator = operator_stack[-1]
                peeked_operator_precedence = get_precedence(peeked_operator)
                current_operator_precedence = get_precedence(character)
                
                if peeked_operator_precedence >= current_operator_precedence:
                    postfix_expression += operator_stack.pop()
                else:
                    break
            
            operator_stack.append(character)
        elif character == '\\':
            if index + 1 < len(formatted_regex):
                print('Escaped character:' + formatted_regex[index + 1])
                postfix_expression += formatted_regex[index + 1]
                index += 1
        else:
            postfix_expression += character
        
        index += 1
        
        print('Stack:' + str(operator_stack))
        print('Queue:' + postfix_expression + '\n')
    
    while len(operator_stack) > 0:
        postfix_expression += operator_stack.pop()
    
    return postfix_expression

def get_precedence(operator):
    if operator == '(':
        return 1
    elif operator == '|':
        return 2
    elif operator == '.':
        return 3
    elif operator == '?':
        return 4
    elif operator == '*':
        return 4
    elif operator == '+':
        return 4

def format_regular_expression(regex):
    all_operators = ['|', '?', '+', '*']
    binary_operators = ['|']
    result = ''
    
    while '+' in regex:
        index = regex.index('+')
        if regex[index - 1] != ')':
            regex = regex.replace(regex[index - 1] + "+", regex[index - 1] + regex[index - 1] + "*")
        elif regex[index - 1] == ')':
            j = index - 2
            count = 0
            
            while (regex[j] != '(' or count != 0) and j >= 0:
                if regex[j] == ')':
                    count += 1
                elif regex[j] == '(':
                    count -= 1
                j -= 1
            if regex[j] == '(' and count == 0:
                sub_expression = regex[j:index]
                regex = regex.replace(sub_expression + "+", sub_expression + sub_expression + "*")
                
    while '?' in regex:
        index = regex.index('?')
        if regex[index - 1] != ')':
            regex = regex.replace(regex[index - 1] + "?", "(" + regex[index - 1] + "|ε)")
        elif regex[index - 1] == ')':
            j = index - 2
            count = 0
            
            while (regex[j] != '(' or count != 0) and j >= 0:
                if regex[j] == ')':
                    count += 1
                elif regex[j] == '(':
                    count -= 1
                j -= 1
            if regex[j] == '(' and count == 0:
                sub_expression = regex[j:index]
                regex = regex.replace(sub_expression + "?", "(" + sub_expression + "|ε)")
                
    index = 0
    while index < len(regex):
        char1 = regex[index]
        
        if index + 1 < len(regex):
            char2 = regex[index + 1]
            
            if char1 == '\\':
                char1 += char2
                if index + 2 < len(regex):
                    char2 = regex[index + 2]
                else:
                    char2 = ''
                index += 1
            elif char1 == '[':
                j = index + 1
                while j < len(regex) and regex[j] != ']':
                    char1 += regex[j]
                    j += 1
                char1 += regex[j]
                index = j
                if index + 1 < len(regex):
                    char2 = regex[index + 1]
                else:
                    char2 = ''
            result += char1
            
            if char2 != '' and char1 != '(' and char2 != ')' and char2 not in all_operators and char1 not in binary_operators:
                result += '.'
        else:
            result += char1
        index += 1
    
    return result


