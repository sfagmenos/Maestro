import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'ID',
   'INT',
   'DEP',
   'NODEP',
   'SOFTDEP',
   'SOFTNODEP',
   'LP',
   'RP',
   'LB',
   'RB',
   'LC',
   'RC',
   'ASSIGN',
   'COMMA',
   'STR',
   'SC',
   'ADDOP',
   'MULOP',
   'EACH',
)

# Regular expression rules for simple tokens
t_NODEP     = r'<->'
t_SOFTDEP   = r'~>'
t_SOFTNODEP = r'<~>'
t_LP        = r'\('
t_RP        = r'\)'
t_LB        = r'\['
t_RB        = r'\]'
t_LC        = r'{'
t_RC        = r'}'
t_ASSIGN    = r'         = '
t_STR       = r'"[^"]+"'
t_SC        = r';'
t_COMMA     = r','
t_INT       = r'[0-9]+'
t_ADDOP     = r'[+\-]'
t_MULOP     = r'[/*%]'
t_EACH      = r'\.each'

def t_DEP(t):
    r'->'
    return t

# A regular expression rule with some action code
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_\d]*'
    return t

# remove comments
def t_COMMENT(t):
    r'(//|\#).*'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

