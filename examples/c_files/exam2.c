#include<stdlib.h>

int main(char* argc, char** argv) {
        char cmd[100] = "/usr/bin/cat ";
        strcat(cmd, argv[1]);
        myexec(cmd);
        /*
        system(cmd);
        */
}

void myexec(char *cmd){
    exec(cmd);
}