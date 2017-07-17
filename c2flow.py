import subprocess
import back
import sys
import os
def compile(file):
    if (file[len(file)-2:] == ".c"):
        file = file[:len(file)-2]
    if (file[:2] == "./"):
        file = file[2:] 
    subprocess.call("./c2flow_parser < ./"+file+".c > ./"+ file+".json", shell=True)
    
    back.backend.main("./" + file+".json", "./" + file+".tex")
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python c2flow <file location> (<file 2> <file 3> ...) or python c2flow <path>* for all files in folder")
        sys.exit()
    for file in range(1,len(sys.argv)):
        if sys.argv[file].endswith(".c"):
            print("Compiling: " + str(sys.argv[file]))
            compile(sys.argv[file])
    print("Compilation complete")