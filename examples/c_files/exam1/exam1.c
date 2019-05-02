#include <stdio.h>
// #include <unistd.h>

int main(int argc, char **argv)
{
    char cat[] = "cat ";
    char *command;
    size_t commandLength;

    char *argument = argv[1];
    commandLength = strlen(cat) + strlen(argv[1]) + 1;
    command = (char *)malloc(commandLength);
    strncpy(command, cat, commandLength);
    strncat(command, argument, (commandLength - strlen(cat)));
    printf("%s", command);
    system(command, NULL, NULL);
    return (0);
}
