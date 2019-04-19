#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    char *command;
    char cmd[256];
    scanf("%s", &cmd+2);
    command = malloc(256*sizeof(char));
    gets(command);

    if (argc != 2)
    {
        printf("Error: Please enter a program to time!\n");
        return -1;
    }

    memset(&command, 0, sizeof(command));

    strcat(command, "time ./");
    strcat(command, argv[1]);
    system(command);
    exec(cmd, NULL);
    return 0;
}