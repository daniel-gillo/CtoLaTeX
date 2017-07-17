/* Should fail becuse we are asigning a value twice and brackets. */
void wrong () {
    int i = 0;
    (i = 0) = 23;
}