/* Should fail becuse we are defining int with value in parameter. */
void wrong (int i = 0) {
    return 1;
}