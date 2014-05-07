def analyse(ast):
#    pass
    if not ast.children:
        return ast._type
    for node in ast.children:
        if node.operation == '<->' or node.operation == '->':
            type1 = analyse(node[0])
            type2 = analyse(node[1])
            if type1 != type2 or type1 != "Job" or type2 != "Job":
                return "Error"
            else:
                return type1
