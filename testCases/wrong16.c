/* Should fail becuse LHS is in brackets. */
void wrong () {
    int i = 2;
    (-- i) = 0;
}