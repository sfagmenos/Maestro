assign = []
def analyse(ast):
    error = {'->':"dependency operator",
            '<->':"non dependency operator",
            '-':"minus operator",
            '+':"plus operator"}
    #if not ast.children:
        #in leaf
    #    return ast._type
    if ast.operation == "id":
        if ast.value not in assign:
            print "Variable " + ast.value + " not previously declared"
            return None
        return ast._type
    #for being dynamic
    if ast.operation == "=":
        assign.append(ast.children[0])
        return "assign"
    #if -> or <->
    if ast.operation == '<->' or ast.operation == '->':
        #find type of first child
        type1 = analyse(ast.children[0])
        #find of second
        type2 = analyse(ast.children[1])
        #if both the same and job return job
        if type1 == type2 and type1 == "job":
            return type1
        else:
            print "Type error(sem) " + xstr(type1) + " " \
                    + ast.operation + " " + xstr(type2)
            return None
    if ast.operation == '-' or ast.operation == '/':
        type1 = analyse(ast.children[0])
        type2 = analyse(ast.children[1])
        if type1 == type2 and type1 == "int":
            return type1
        else:
            print "minus error"
            return None
    for node in ast.children:
        type = analyse(node)
        if type == None:
            break
    return type


def xstr(s):
    if s is None:
        return 'None'
    return str(s)


def traverse(ast, level=0):
    if ast.operation == "=":
        print "\t" * level + xstr(ast._type) + " " + xstr(ast.operation) \
                    + " " + xstr(ast.value) + " " + xstr(ast.leaf)
        print "\t" * (level + 1) + ast.children[0]
        return
    else:
        print "\t" * level + xstr(ast._type) + " " + xstr(ast.operation) \
                    + " " + xstr(ast.value) + " " + xstr(ast.leaf)
    for node in ast.children:
#        print node
#        for l in node:
        traverse(node, level + 1)
