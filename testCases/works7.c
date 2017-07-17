/* Should work. Tests nested if / else if statements. */
int correct () {
    int i = 2;
    if (i == 0){
        i = 1;
    }
    else if (i == 1){
        i = 2;
        if (i == 1){}
        else if (sizeof(i) >= 1){
            i = 3;
        }
    }
    else{
        i = 4;
    }
    return i;
}