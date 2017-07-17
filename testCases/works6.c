/* Should work. Tests nested if statements */
int correct () {
    int i = 1;
    if (i){
        if (i) {
            if (i == 1) {
                return i;
            }
        }
    }
    return 0;
}