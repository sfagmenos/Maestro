INPUT=example
LEXER=lex.yy.c
PARSER=y.tab.c
HEADER=y.tab.h
CC=gcc
OUT=lex_yacc

all:$(LEXER) $(PARSER) $(HEADER)
	$(CC) -o $(OUT)  $(LEXER) $(PARSER)

$(LEXER): $(INPUT).l
	flex $(INPUT).l

$(PARSER): $(INPUT).y
	yacc -d $(INPUT).y

clean:
	rm -f $(LEXER) $(PARSER) $(HEADER) $(OUT)
