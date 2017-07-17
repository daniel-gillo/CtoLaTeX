/* Should fail becuse we are defining an int in an if statement. */
void wrong () {
    if (float f = 0.0 == 0.0){
        return void;
    }
}