assign = []
def analyse(ast):
    error = {'->':"dependency operator",
            '<->':"non dependency operator",
            '-':"minus operator",
            '+':"plus operator"}
    new = type(ast)
    if new is str or new is list:
        return str(new)
    if ast.operation == "id":
        if ast.value not in assign:
            print "Variable " + ast.value + " not previously declared\
                     at line " + str(ast.line)
            return None
        return ast._type
    #for being dynamic
    if ast.operation == "=":
        assign.append(ast.children[0])
        typex = "assign"
        for node in ast.children:
            typex = analyse(node)
            if typex == None:
                break
        return typex
    #if -> or <->
    if ast.operation == '<->' or ast.operation == '->' \
       or ast.operation == '<~>' or ast.operation == '~>' \
        or ast.operation == '~<':
        #find type of first child
        type1 = analyse(ast.children[0])
        #find of second
        type2 = analyse(ast.children[1])
        #if both the same and job return job
        if type1 == type2 and type1 == "job":
            return type1
        else:
            print "Type error(sem) " + xstr(type1) + " " \
                    + ast.operation + " " + xstr(type2) + \
                    " at line " + str(ast.line)
            return None
    if ast.operation == '-' or ast.operation == '/':
        type1 = analyse(ast.children[0])
        type2 = analyse(ast.children[1])
        if type1 == type2 and type1 == "int":
            return type1
        else:
            print "minus error"
            return None
    if ast.operation == "range":
        child = ast.children[0].children[0]
        type1 = analyse(child)
        if type1 != "int":
            print "Function range needs int as argument got " + type1 \
                    + " at line " + str(ast.line)
            return None
        return type1
    if ast.operation == "reduce":
        child_type = ast.children[0].children[0].children[0]._type 
        if child_type != "list":
            print "Function reduce needs list as first argument got " + child_type \
                    + " at line " + str(ast.line)
            return None
        child_type = ast.children[0].children[1]._type
        if child_type != "string":
            print "Function reduce needs string as second argument got " + child_type \
                    + " at line " + str(ast.line)
            return None
        return "list"
    if ast.operation == "map":
        child_type = ast.children[0].children[1]._type
        if child_type != "int":
            print "Function map needs int as first argument got " + child_type \
                    + " at line " + str(ast.line)
            return None
        child_type = ast.children[0].children[0].children[1]._type
        if child_type != "string":
            print "Function map needs string as second argument got " + child_type \
                    + " at line " + str(ast.line)
            return None
        return child_type
    if ast.operation == "Job":
        leaf=[]
        analyse_leafs(ast,leaf)
        if sorted(leaf)[0] != sorted(leaf)[-1]:
            print "Job argument not a string at line "+ str(ast.line)
            return None
        return ast._type
    #for leaf int, str,....
    if not ast.children:
        return ast._type
    for node in ast.children:
        typex = analyse(node)
        if typex == None:
            break
    return typex


def analyse_leafs(node,leafs):
    if node.leaf:
        leafs.append(node._type)
    else:
        for n in node.children:
            analyse_leafs(n,leafs)


def xstr(s):
    if s is None:
        return 'None'
    return str(s)


def traverse(ast, level=0):
    if type(ast) is str:
        print "\t" * level + ast
        return
#    if ast.operation == 'id':
#        print "\t" * level + xstr(ast._type) + " " + xstr(ast.value)
    if ast.operation == "=":
        print "\t" * level + xstr(ast._type) + " " + xstr(ast.operation) \
                    + " " + xstr(ast.value) + " " + xstr(ast.leaf)
    else:
        print "\t" * level + xstr(ast._type) + " " + xstr(ast.operation) \
                    + " " + xstr(ast.value) + " " + xstr(ast.leaf)
    for node in ast.children:
#        print node
#        for l in node:
        traverse(node, level + 1)
