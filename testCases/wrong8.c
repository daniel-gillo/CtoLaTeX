/* Should fail becuse we are initializing int in a return statement. */
int wrong () {
    return int i = 42;
}