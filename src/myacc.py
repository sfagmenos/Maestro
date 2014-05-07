import sys
import ply.yacc as yacc
import helpers.jobs as hj

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

def p_stmt_list(p):
    '''STMTLIST : STMTLIST STMT
                | STMT'''

def p_stmt(p):
    'STMT : E SC'

def p_stmt_error(p):
    'STMT : error'
    line = p.lineno(p[1]) # line number of error
    print "Syntax error in statement line " + line

# LII is a comma separated list of Expressions
def p_func_call(p):
    'E : ID LP LII RP'
    val = eval_func(p[1], p[3].node.value)
    _type = 'list'
    node = Node(p[1], [p[3].node], _type, val)
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
    val = p[3].node.value
    _type = p[3].node._type
    node = Node('=', [p[3].node], _type, val)
    sym_table[p[1]] = node
    p[0] = AST_obj(node)


# strings for Job names
def p_e_str(p):
    'E : STR'
    val = p[1]
    _type = 'sting'
    node = Node('str', [], _type, val, leaf=True)
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
    val = p[1].node.value + [p[3].node.value]
    _type = None
    node = Node('list-concat', [p[1].node, p[3].node], _type, val)
    p[0] = AST_obj(node)


def p_list_inside_orig(p):
    'LII : E'
    val = [p[1].node.value]
    _type = p[1].node._type
    node = Node('list-orig', [p[1].node], _type, val, leaf=True)
    p[0] = AST_obj(node)


# <->
def p_e_nodep(p):
    'E : E NODEP E'
    val = nodep(p[1].node.value, p[3].node.value)
    _type = 'list'
    node = Node('<->', [p[1].node, p[3].node], _type, val)
    p[0] = AST_obj(node)


# ->
def p_e_dep(p):
    'E : E DEP E'
    val = dep(p[1].node.value, p[3].node.value)
    _type = 'list'
    node = Node('->', [p[1].node, p[3].node], _type, val)
    p[0] = AST_obj(node)


# ()
def p_e_parenthesize(p):
    'E : LP E RP'
    p[0] = p[2]


# that's a variable: fetch it in the symbol table
def p_e_id(p):
    'E : ID'
    val = sym_table[p[1]].value
    _type = sym_table[p[1]]._type
    node = Node('id', [], _type, val, leaf=True)
    p[0] = AST_obj(node)

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input: " + str(p)


# Symbol table
sym_table = {}  # map[name]node


# Eval function helper
# TODO check types
def eval_func(name, args):
    if name == "Job":
        return hj.Job(args[0], args[0])
    if name == "run":
        hj.run([j for j in args])
        return args  # useful to reuse in a one liner


# Dependencies helper
# TODO check types
def nodep(ljobs, rjobs):
    if type(ljobs) is not list:
        ljobs = [ljobs]
    if type(rjobs) is not list:
        rjobs = [rjobs]
    return ljobs + rjobs


# TODO check types
def dep(jobs, depend_on_jobs):
    if type(jobs) is not list:
        jobs = [jobs]
    if type(depend_on_jobs) is not list:
        depend_on_jobs = [depend_on_jobs]
    hj.add_dependencies(jobs, depend_on_jobs)
    return jobs + depend_on_jobs

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
        result = parser.parse(prgm)
        f.close()
    else:
        print "Usage: python myacc.py <file_name>"
