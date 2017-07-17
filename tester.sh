# What this does: Print the variable length returned by yacc, the test file
# and the output of yacc. The "-le 20" is arbirtrary until yacc's output is 
# fixed.
#
# Old if stmt: if [ ${#TEST_OUTPUT} -le 20 ]
# If stmt using error code by parser if [ $? != 0 ];
#
# Rant:
# This took way too long. For reasons beyond me the for loop only works if the
# entire command is a single line and seperated via ";"s. Otherwise there will
# be a a SyntaxError "near do". This happens even if there's nothing in the
# loop.
#
# This file exists seperatly because running this complex line of code screws
# with make. It just goes nuts. Also at the moment the IF statement doesn't do
# anything. The length of $TEST_OUTPUT is totally random. The correst file
# output something, so I can't check if the output termianted properly
# (for now).
#
# Also the shebang is screwy so I removed it.
#
# Don't ask me how long it took me to firgure this out.
#
# If you're dumb enough to debug this, use: https://www.shellcheck.net/
#
# Sources:
# http://unix.stackexchange.com/questions/118433/quoting-within-command-substitution-in-bash
# http://stackoverflow.com/questions/2559076/how-do-i-redirect-output-to-a-variable-in-this-shell-function
# https://www.cyberciti.biz/faq/bash-loop-over-file/
# https://github.com/koalaman/shellcheck/wiki/SC1068
echo "In shell script"
FILES=./testCases/*
#echo "$FILES"
for FILE in ./testCases/*.c; do TEST_OUTPUT=$(./c2flow_parser < $FILE &); if [ ${#TEST_OUTPUT} -le 20 ]; then echo ${#TEST_OUTPUT} "$FILE"; echo "$TEST_OUTPUT"; else echo ${#TEST_OUTPUT} "$FILE"; fi; done