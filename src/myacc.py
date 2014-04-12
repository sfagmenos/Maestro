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


# LII is a comma separated list of Expressions
def p_func_call(p):
    'E : ID LP LII RP'
    p[0] = eval_func(p[1], p[3])


# assign a variable:
# - put the name in the sym_table
# - the expresion gets the value for 1 liners
def p_assign(p):
    'E : ID ASSIGN E'
    sym_table[p[1]] = p[3]
    p[0] = p[3]  # do that to have assign return the var


# strings for Job names
def p_e_str(p):
    'E : STR'
    p[0] = p[1]


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
    p[0] = p[1] + [p[3]]


def p_list_inside_orig(p):
    'LII : E'
    p[0] = [p[1]]


# <->
def p_e_nodep(p):
    'E : E NODEP E'
    p[0] = nodep(p[1], p[3])


# ->
def p_e_dep(p):
    'E : E DEP E'
    p[0] = dep(p[3], p[1])


# ()
def p_e_parenthesize(p):
    'E : LP E RP'
    p[0] = p[2]


# that's a variable: fetch it in the symbol table
def p_e_id(p):
    'E : ID'
    p[0] = sym_table[p[1]]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Symbol table
sym_table = {}  # map[name]node


# Eval function helper
# TODO check types
def eval_func(name, args):
    if name == "Job":
        return hj.Job(args[0], args[0])
    if name == "run":
        if type(args) is list:
            hj.run(args[0])
        else:
            hj.run(args)
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


# AST structure
# TODO use it instead of doing stuff directly
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


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
        first = f.next()
        if first != "#!maestro\n":
            print "No maestro file specified!"
            sys.exit(-1)
        for line in f:
            if line == "\n":
                continue
            result = parser.parse(line)
        f.close()
    else:
        print "Usage: python myacc.py <file_name>"
#       s = raw_input('maestro> ')
#   except EOFError:
#       break
#   if not s: continue
#   result = parser.parse(s)
#   print result
