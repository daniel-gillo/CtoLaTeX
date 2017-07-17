/* Should fail becuse we are comparing two different filetypes. Can pass, because we don't care too much right now. */
void anal() {
    int i = 0;
    float f = 0.0;
    int bool = i == f;
}