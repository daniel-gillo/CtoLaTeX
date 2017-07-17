/* Should fail. Else if called in an else if statement. */
void wrong () {
    int i = 0;
    if (i == 1){}
    else if (i == 0){
        else if (i == 0){
            i == 1;
        }
    }
}