import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from mlex import tokens
precedence = (
    ('left', 'DEP'),
    ('left', 'NODEP'),
)

def p_e_nodep(p):
    'E : E NODEP E'
    p[0] = p[1] + p[3]

def p_e_dep(p):
    'E : E DEP E'
    p[0] = p[1] + p[3]

def p_e_parent(p):
    'E : LP E RP'
    p[0] = p[2]

def p_e_id(p):
    'E : ID'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('maestro> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print result
