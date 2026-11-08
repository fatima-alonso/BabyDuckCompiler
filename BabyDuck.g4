grammar BabyDuck;

// Regla principal
programa
    : PROGRAM ID SEMICOLON vars funcs MAIN body END EOF
    ;

vars 
    : (VAR lista_id COLON type SEMICOLON)*
    ;

funcs
    : funcion*
    ;

funcion
    : retorno ID LPAREN parametros_opt RPAREN
      LBRACKET vars body RBRACKET SEMICOLON
    ;

retorno
    : VOID
    | type
    ;

parametros_opt
    : parametros?
    ;

parametros
    : ID COLON type (COMMA ID COLON type)*
    ;

lista_id
    : ID (COMMA ID)*
    ;

type 
    : INT
    | FLOAT
    ;

body
    : LBRACE statement+ RBRACE
    ;

statement
    : assign
    | return_stmt
    | print_stmt
    | read_stmt
    | condition
    | cycle
    | f_call
    | body
    ;

return_stmt
    : RETURN expresion SEMICOLON
    ;

expresion : exp (rel_op exp)?;

rel_op : GT | LT | NE;

exp : termino ((PLUS | MIN) termino)*;

termino : factor ((MULT | DIV) factor)*;

factor
    : LPAREN expresion RPAREN
    | PLUS factor
    | MIN factor
    | ID
    | cte
    | f_call_sin_pyc
    ;

cte : CTE_INT | CTE_FLOAT;

assign : ID ASSIGN expresion SEMICOLON;

print_stmt
    : PRINT LPAREN arg_print (COMMA arg_print)* RPAREN SEMICOLON
    ;

arg_print
    : expresion
    | CTE_STRING
    ;

read_stmt
    : READ LPAREN ID RPAREN SEMICOLON
    ;

condition
    : IF LPAREN expresion RPAREN statement (ELSE statement)?
    ;

cycle
    : WHILE LPAREN expresion RPAREN DO statement
    ;

f_call
    : ID LPAREN argumentos_opt RPAREN SEMICOLON
    ;

argumentos_opt
    : argumentos?
    ;

argumentos
    : expresion (COMMA expresion)*
    ;
    
f_call_sin_pyc
    : ID LPAREN argumentos_opt RPAREN
    ;


// Palabras reservadas
PROGRAM : 'program';
VAR : 'var';
INT : 'int';
FLOAT : 'float';
MAIN    : 'main';
END     : 'end';
VOID : 'void';
RETURN : 'return';
PRINT : 'print';
READ : 'read';
IF : 'if';
ELSE : 'else';
WHILE : 'while';
DO : 'do';

// Símbolos
SEMICOLON : ';';
COLON : ':';
COMMA : ',';
LBRACE    : '{';
RBRACE    : '}';
LBRACKET : '[';
RBRACKET : ']';
LPAREN : '(';
RPAREN : ')';
ASSIGN : '=';

// Operadores
PLUS : '+';
MIN  : '-';
MULT : '*';
DIV  : '/';

GT : '>';
LT : '<';
NE : '!=';

// CTEs
CTE_FLOAT : [0-9]+ '.' [0-9]+;
CTE_INT : [0-9]+;
CTE_STRING : '"' .*? '"';

// Identificadores
ID : [a-zA-Z_] [a-zA-Z0-9_]*;

// Espacios y saltos de línea
WHITESPACE : [ \t\r\n]+ -> skip;