make compiles the parser
make test runs the test cases, note some of "wrong" caes will currently pass since they are type errors rather then grammer errors
the tester.sh file needs to be executable so chmod 0700

How to run:
Run the c2flow.py <file location without .c> <file location without .c>
will generate a .tex file. 
To see the graph compile that .tex file using LuaTex compiler.