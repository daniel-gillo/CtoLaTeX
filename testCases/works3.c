/* Should work. */
int correct () {
    int i = (1+2)*3/4 == 12;
    int j = i <= -1;
    int k = j-- -i;
    return k * 1 >= i;
}