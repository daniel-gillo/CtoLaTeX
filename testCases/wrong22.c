/* Should fail becuse we are defining a number to be equal to be i. */
void wrong () {
    int i = 1;
    if (1 = i){
        return 0;
    }
}