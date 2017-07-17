%{
	#include<stdio.h>
	#include <stdlib.h>
	#include <errno.h>
	extern int yylex(void);
    void yyerror(char const *s) { 
		extern int yylineno;
		fprintf(stderr, "$%s: starting on line %d\n", s, yylineno); 
	}
	
	struct astNode{
		char *token;
		struct astNode *left;
		struct astNode *right;
	};
	
	struct astNode* newNode(char *token, struct astNode *left, struct astNode *right) {
		/* page 55 flex & bison */
		 struct astNode *node = malloc(sizeof(struct astNode));

		 if(!node) {
			yyerror("out of space");
			return 0;
		 }
		 node->token = token;
		 node->left = left;
		 node->right = right;
		 return node;
	}
	char *stringifyTree(struct astNode *node){
		/* http://stackoverflow.com/questions/804288/creating-c-formatted-strings-not-printing-them */
		char *output = NULL;
		if (node != NULL) {
			char *left = stringifyTree(node->left);
			char *right = stringifyTree(node->right);
			if (asprintf(&output, "{\"token\":\"%s\", \"left\":%s , \"right\":%s}", node->token, left, right) < 0) {return "error";}
			free(left);
			free(right);
		} else {
			if (asprintf(&output, "null") < 0) {return "error";}
		}
		return output;
	}
	void freeTree(struct astNode *node){
		if (node != NULL) {
			if (strncmp(node->token,"^",1) == 0) {
				free(node->token);
			}
			freeTree(node->left);
			freeTree(node->right);
			free(node);
		}
	}
%}

%locations

%union 
{
    int ival; 
    float fval;
	char *lex_token_str;
	struct astNode *astNode;
}

/* types */
%token <ival> INTEGER
%token <fval> FLOAT
%token <lex_token_str> ID
%token <lex_token_str> PRINTSTR
%token <lex_token_str> TYPE



/* type void */
%token VOID
/* Delimiters */
%token LBRACKET RBRACKET LCURLY RCURLY SEMICOLON COMMA PERIOD
/* = for assignment and & for getting address */
%token ASSIGN GETADDR 
/* ++ and -- */
%token PLUSINCREMENT MINUSINCREMENT
/* Number operators */
%token PLUS MINUS MULTI DIVIDE MOD
/* Boolean operations */
%token OR AND LESS GREATER LESSEQUAL GREATEREQUAL EQL NEQL
/* Reserved words */
%token CONDIF CONDELSE RETURN LOOPSTART PRINT

/* non terminal type def*/
%type <astNode> program function function_type parameters parameters_prime function_body assign_statement return_statement shorthand_statement init_statement value expr variables loop_statement if_statement if_extension function_call

/* Order of presedence */
%left OR
%left AND
%left EQL NEQL
%left LESS GREATER LESSEQUAL GREATEREQUAL
%left PLUS MINUS
%left MULTI DIVIDE MOD
%right SIZEOF GETADDR
%left PLUSINCREMENT MINUSINCREMENT LBRACKET RBRACKET


%%
/* 
-----------------------
Program Creation
-----------------------
*/
program : function program {char *tree=stringifyTree($1);printf(tree); free(tree); freeTree($1);}
| {$$ = NULL;}
;

/* 
-----------------------
Function Creation
-----------------------
*/ 

/* type def for the function and name of it */
function : function_type ID LBRACKET parameters RBRACKET LCURLY function_body RCURLY {$$ = newNode("function", $1, newNode($2, newNode("args+ret",$4,NULL),$7));}
;

function_type : TYPE {$$ = newNode($1,NULL,NULL);}
| VOID {$$ = newNode("void",NULL,NULL);}
;

/* handles single input or no input */
parameters: TYPE ID parameters_prime {$$ = newNode($2,$3,newNode($1, NULL, NULL));}
| {$$ = NULL;}
;

/* multiple inputs */
parameters_prime : COMMA TYPE ID parameters_prime {$$ = newNode($3,$4, newNode($2, NULL, NULL));}
| {$$ = NULL;}
;

/* 
-----------------------
Body Code
-----------------------
*/ 

function_body : assign_statement SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);}
| shorthand_statement SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);}
| init_statement SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);}
| function_call SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);}
| if_statement function_body {$$ = newNode("bodyCode",$1,$2);}
| loop_statement function_body {$$ = newNode("bodyCode",$1,$2);}
/* | print SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);} */
| return_statement SEMICOLON function_body {$$ = newNode("bodyCode",$1,$3);}
| {$$ = NULL;}
;

return_statement : RETURN expr {$$ = newNode("return",$2, NULL);}
| RETURN VOID {$$ = newNode("return",NULL, NULL);}
;

/* 
-----------------------
Assignments
-----------------------
*/ 

assign_statement : ID ASSIGN expr {$$ = newNode("=",newNode($1,NULL,NULL),$3);}
;

shorthand_statement : ID PLUS ASSIGN expr {$$ = newNode("+=",newNode($1,NULL,NULL),$4);}
| ID MINUS ASSIGN  expr {$$ = newNode("-=",newNode($1,NULL,NULL),$4);}
;

init_statement : TYPE ID ASSIGN expr {$$ = newNode("=",newNode($2,newNode($1, NULL, NULL),NULL),$4);}
;

/* 
-----------------------
Function Calls
-----------------------
*/ 

/* print : PRINT LBRACKET PRINTSTR variables RBRACKET {$$ = newNode("print",newNode($3,NULL,NULL), $4);}
; */

function_call : ID LBRACKET variables RBRACKET {$$ = newNode("functionCall",newNode($1,NULL,NULL),$3);}
;

variables : value {$$ = $1;}
| value COMMA variables {$$ = newNode(",",$1,$3);}
;

/* 
-----------------------
Loops
-----------------------
*/ 

loop_statement : LOOPSTART LBRACKET expr RBRACKET LCURLY function_body RCURLY {$$ = newNode("loop",$3,$6);}
;


/* 
-----------------------
Conditions
-----------------------
*/ 

if_statement : CONDIF LBRACKET expr RBRACKET LCURLY function_body RCURLY if_extension {$$ = newNode("if",$3,newNode("ifBodyExt",$6,$8));}
;

if_extension : CONDELSE LCURLY function_body RCURLY {$$=newNode("else", $3, NULL);}
| CONDELSE if_statement {$$ = newNode("elseif",$2,NULL);}
| {$$ = NULL;}
;


/* 
-----------------------
Expressions
-----------------------
*/ 

value : ID {$$ = newNode($1, NULL, NULL);}
| INTEGER {char* num = NULL; if (asprintf(&num, "^%d",$1) < 0) {return -1;} ; $$ = newNode(num, NULL, NULL);}
| FLOAT {char* num = NULL; if (asprintf(&num, "^%f",$1) < 0) {return -1;}; $$ = newNode(num, NULL, NULL);}
| function_call {$$ = $1;}
;

expr : expr PLUSINCREMENT {$$ = newNode("++", $1, NULL);}
| expr MINUSINCREMENT {$$ = newNode("--", $1, NULL);}
| LBRACKET expr RBRACKET {$$ = $2;}
| GETADDR expr {$$ = newNode("getAddr", $2, NULL);}
| MULTI expr %prec GETADDR {$$ = newNode("deref", $2, NULL);}
| PLUSINCREMENT expr %prec SIZEOF {$$ = newNode("++", $2, NULL);}
| MINUSINCREMENT expr %prec SIZEOF {$$ = newNode("--", $2, NULL);}
| PLUS expr %prec SIZEOF {$$ = newNode("unary+", $2, NULL);}
| MINUS expr %prec SIZEOF {$$ = newNode("unary-", $2, NULL);}
| SIZEOF LBRACKET expr RBRACKET %prec SIZEOF {$$ = newNode("sizeof", $3, NULL);}
| expr MULTI expr {$$ = newNode("*", $1, $3);}
| expr DIVIDE expr {$$ = newNode("/", $1, $3);}
| expr MOD expr {$$ = newNode("%", $1, $3);}
| expr PLUS expr {$$ = newNode("+", $1, $3);}
| expr MINUS expr {$$ = newNode("-", $1, $3);}
| expr LESS expr {$$ = newNode("<", $1, $3);}
| expr LESSEQUAL expr {$$ = newNode("<=", $1, $3);}
| expr GREATER expr {$$ = newNode(">", $1, $3);}
| expr GREATEREQUAL expr {$$ = newNode(">=", $1, $3);}
| expr EQL expr {$$ = newNode("==", $1, $3);}
| expr NEQL expr {$$ = newNode("!=", $1, $3);}
| expr AND expr {$$ = newNode("and", $1, $3);}
| expr OR expr {$$ = newNode("or", $1, $3);}
| value {$$ = $1;}
;

%%

int	main(void) {
	yyparse();
	return 0;
} 

/*
http://www.epaperpress.com/lexandyacc/index.html
http://archive.oreilly.com/pub/a/linux/excerpts/9780596155971/error-reporting-recovery.html
http://stackoverflow.com/questions/32427264/yylval-undefined-with-lex-and-yacc

*/