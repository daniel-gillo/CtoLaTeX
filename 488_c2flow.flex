%{
    #include "y.tab.h"
    #include <stdlib.h>
    void yyerror(char *);
%}

%option noyywrap
%option yylineno

DIGIT 		[0-9]
ID       [a-z][A-Za-z0-9_]*

%%
"="					{ return ASSIGN; }
"&"					{ return GETADDR; }
"++"				{ return PLUSINCREMENT; }
"--"				{ return MINUSINCREMENT; }
"+"					{ return PLUS; }
"-"					{ return MINUS; }
"*"					{ return MULTI; }
"/"					{ return DIVIDE; }
"%"					{ return MOD; }
"("					{ return LBRACKET; }
")"					{ return RBRACKET; }
"{"					{ return LCURLY; }
"}"					{ return RCURLY; }
";"					{ return SEMICOLON; }
","					{ return COMMA; }
"."					{ return PERIOD; }
"=="				{ return EQL; }
"!="				{ return NEQL; }
"||"				{ return OR; }
"&&"				{ return AND; }
"<"					{ return LESS; }
">"					{ return GREATER; }
"<="				{ return LESSEQUAL; }
">="				{ return GREATEREQUAL; }
"if"				{ return CONDIF; }
"else"				{ return CONDELSE; }
"return"			{ return RETURN; }
"while"				{ return LOOPSTART; }
"int"|"float" 		{ 
						yylval.lex_token_str = strdup(yytext);
						return TYPE; 
					}
"sizeof"			{ return SIZEOF; }
"void"				{ return VOID; }
"printf"			{ return PRINT; }
{DIGIT}+ 			{	
						yylval.ival=atoi(yytext); 
						return INTEGER;
					}
{DIGIT}+"."{DIGIT}+ {	
						yylval.fval=atof(yytext); 
						return FLOAT;
					}
{ID} 				{	
						yylval.lex_token_str = strdup(yytext);
						return ID;
					}
[ \t\n]+
"/*".*"*/"		
"\"".*"\"" 			{
						yylval.lex_token_str = strdup(yytext);
						return PRINTSTR;				
					}

%%

/*
int yywrap(void){return 0;}
*/

/*
Program ::= (Token | Whitespace)*
Token ::= ID | Integer | Float | ReservedWord | Operator | Delimiter
ID ::= Letter (Letter | Digit)*
Integer ::= Digit+
Float ::= Digit+"."Digit+
Types ::= "void" | "int" | "float"
ReservedWord ::= "if" | "else" | "return" | "main" | "printf" | "sizeof" | "while"
Operator ::= "+" | "-" | "*" | "/" | "!" | "%" | "&" | "<" | "<=" | ">=" | ">" | "==" | "!=" | "&&" | "||" | "++" | "--"
Delimiter ::= ";" | "." | "," | "=" | "(" | ")" | "{" | "}"
Letter ::= "a" | ... | "z" | "A" | ... | "Z"
Digit ::= "0" | ... | "9"
Whitespace ::= <space> | <tab> | <newline>

https://en.wikipedia.org/wiki/Flex_(lexical_analyser_generator)
http://stackoverflow.com/questions/1756275/bison-end-of-file
http://stackoverflow.com/questions/36705292/end-of-grammar-rule-in-yacc

*/