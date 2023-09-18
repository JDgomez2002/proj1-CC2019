import operator
class Node:
    def __init__(self, value):
        self.left = None
        self.data = value
        self.right = None

    def postorder(self):

        if self.left:
            self.left.postorder()
        if self.right:
            self.right.postorder()
        print(self.data, end=" ")

def is_greater_precedence(op1, op2):
    pre = {'+':0, '-': 0, '*':1, '/':1, '^':2}
    return pre[op1] >= pre[ op2]


def associativity(op):
    ass = {'+':0, '-':0, '*':0, '/':0, '^':1}
    return ass[op]


def build_tree(exp):
    exp_list = exp.split()
    print(exp_list)
    stack = []
    tree_stack = []
    for i in exp_list:
        if i not in ['+', '-', '*', '/', '^', '(', ')']:
            t = Node(int(i))
            tree_stack.append(t)

        elif i in ['+', '-', '*', '/', '^']:
                if not stack or stack[-1] == '(':
                    stack.append(i)

                elif is_greater_precedence(i, stack[-1]) and           associativity(i) == 1:
                    stack.append(i)

                else:
                    while stack and is_greater_precedence(stack[-1], i) and associativity(i) == 0:
                        popped_item = stack.pop()
                        t = Node(popped_item)
                        t1 = tree_stack.pop()
                        t2 = tree_stack.pop()
                        t.right = t1
                        t.left = t2
                        tree_stack.append(t)
                    stack.append(i)

        elif i == '(':
            stack.append('(')

        elif i == ')':
            while stack[-1] != '(':
                popped_item = stack.pop()
                t = Node(popped_item)
                t1 = tree_stack.pop()
                t2 = tree_stack.pop()
                t.right = t1
                t.left = t2
                tree_stack.append(t)
            stack.pop()
    while stack:
        popped_item = stack.pop()
        t = Node(popped_item)
        t1 = tree_stack.pop()
        t2 = tree_stack.pop()
        t.right = t1
        t.left = t2
        tree_stack.append(t)

    t = tree_stack.pop()

    return t



def evaluate(expTree):
    opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv, '^':operator.pow}

    leftC = expTree.left
    rightC = expTree.right

    if leftC and rightC:
        fn = opers[expTree.data]
        return fn(evaluate(leftC), evaluate(rightC))
    else:
        return expTree.data




t = build_tree("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")
print(evaluate(t))
t.postorder()