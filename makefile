parser: yacc flex
	gcc lex.yy.c y.tab.c -o c2flow_parser -lfl
	echo "Finished compiling!"
	
yacc:
	bison -dyl 488_c2flow.yacc
	
flex:
	flex 488_c2flow.flex
	
clean:
	rm c2flow_parser lex.yy.c y.tab.c y.tab.h
	
# See rant in ./tester.sh, but the testing got outsourced there.
#empty = ""
#test_output = "1"
test: parser
	echo "begun testing" 
	./tester.sh