/* Should fail becuse we are using a non existent var in sizeof. */
void wrong () {
    int i = 0;
    i = sizeof(j);
}