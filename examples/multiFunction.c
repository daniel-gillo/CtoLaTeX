/* Should work. */
float ca1ls () {
    int   i = 42;
    float f = 23.0;
    if (called(i) == 41){
        f = 1.0;
    }
    else {
        f = 0.0;
    }
    return f;
}

/* Works returns a value.*/
int called(int in){return final_cal1(in);}

/* Works, tests another layer of calls. */
int final_cal1(int in){return --in;}