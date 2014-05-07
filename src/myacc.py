import sys
import ply.yacc as yacc
import pipeline.semantic_analysis as sa
import pipeline.translation as t

# Get the token map from the lexer
from mlex import tokens
from maestro_cmd import Console
precedence = (
    ('left', 'ASSIGN'),
    ('left', 'DEP'),
    ('left', 'NODEP'),
)

lines = 0

def p_program(p):
    'PRGM : STMTLIST'
    node = Node('prgm', [p[1].node])
    p[0] = AST_obj(node)

def p_stmt_list(p):
    '''STMTLIST : STMTLIST STMT
                | STMT'''
    if len(p) == 2:
        node = Node('stmt-list', [p[1].node])
    else:
        node = Node('stmt-list', [p[1].node, p[2].node])
    p[0] = AST_obj(node)

def p_stmt(p):
    'STMT : E SC'
    p[0] = p[1]

def p_stmt_error(p):
    'STMT : error'
    line = p.lineno(p[1]) # line number of error
    print "Syntax error in statement line " + line

# LII is a comma separated list of Expressions
def p_func_call(p):
    'E : ID LP LII RP'
    _type = type_for_func(p[1])
    node = Node(p[1], [p[3].node], _type)
    p[0] = AST_obj(node)

def p_func_call_error(p):
    'E : ID LP error RP'
    line = p.lineno(p[0]) # line number of error
    print "Syntax error in function call, line ", line

# assign a variable:
# - put the name in the sym_table
# - the expresion gets the value for 1 liners
def p_assign(p):
    'E : ID ASSIGN E'
    _type = p[3].node._type
    sym_table[p[1]] = [None, _type]
    node = Node('=', [p[1], p[3].node], _type)
    p[0] = AST_obj(node)

# strings for Job names
def p_e_str(p):
    'E : STR'
    _type = 'sting'
    node = Node('str', [], _type, value=p[1], leaf=True)
    p[0] = AST_obj(node)

# do we need that later?
# please do not remove
# def p_e_list(p):
    # 'E : LI'
    # p[0] = p[1]
# def p_list(p):
    # 'LI : LP LII RP'
    # p[0] = p[2]
# arguments of a function or inside of a list for later
def p_list_inside_grow(p):
    'LII : LII COMMA E'
    _type = 'list'
    node = Node('list-concat', [p[1].node, p[3].node], _type)
    p[0] = AST_obj(node)

def p_list_inside_orig(p):
    'LII : E'
    _type = 'list'
    node = Node('list-orig', [p[1].node], _type)
    p[0] = AST_obj(node)

# <->
def p_e_nodep(p):
    'E : E NODEP E'
    _type = 'list'
    node = Node('<->', [p[1].node, p[3].node], _type)
    p[0] = AST_obj(node)

# ->
def p_e_dep(p):
    'E : E DEP E'
    _type = 'list'
    node = Node('->', [p[1].node, p[3].node], _type)
    p[0] = AST_obj(node)

# ()
def p_e_parenthesize(p):
    'E : LP E RP'
    p[0] = p[2]

# that's a variable: fetch it in the symbol table
def p_e_id(p):
    'E : ID'
    _type = sym_table[p[1]][-1]
    node = Node('id', [], _type, value=p[1], leaf=True)
    p[0] = AST_obj(node)

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input: " + str(p)

#type helpers
def type_for_func(name):
    if name == 'Job' or name == 'Wait':
        return 'job'
    elif name == 'run' or name == 'range':
        return 'list'

# Symbol table
sym_table = {}  # map[symbol][value, type]

# AST node structure
class Node:
    def __init__(self, operation, children=None,  \
                       _type=None, value=None, leaf=False):
        self._type = _type
        self.operation = operation
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.value = value

# we add one layer of abstraction to be able to get values and syblings
# on top of node
class AST_obj:
    def __init__(self, node=None, value=None, syblings=None):
        self.node = node
        self.syblings = syblings

# Build the parser
parser = yacc.yacc()

# pipeline for execution
def pipeline(code):
    ast = parser.parse(code).node
    sa.analyse(ast)
    result = t.execute(ast, sym_table)
    return result

if __name__ == '__main__':
    if len(sys.argv) == 1:
        console = Console(parser)  # while True:
        console.cmdloop()  # try:
    elif len(sys.argv) == 2:
        try:
            f = open(sys.argv[1])
        except IOError:
            print 'cannot open', sys.argv[1]
            sys.exit(-1)
        # first = f.next()
        # if first != "#!maestro\n":
            # print "No maestro file specified!"
            # sys.exit(-1)
        prgm = f.read()
        result = pipeline(prgm)
        print result
        f.close()
    else:
        print "Usage: python myacc.py <file_name>"

