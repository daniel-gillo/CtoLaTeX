/* Should fail becuse we are defining int in an if that will never be called. */
void wrong () {
    if (1){
        int i = 0;
    }
    else {
        int ii = 1;
    }
    ii = i;
}