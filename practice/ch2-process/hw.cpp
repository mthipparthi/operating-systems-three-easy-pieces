#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    printf("hello world (pid:%d)\n", (int) getpid());
    int var = 100;
    int rc = fork();
    if (rc < 0) {
        // fork failed; exit
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {
        // child (new process)
        var = var + 1;
        printf("hello, I am child (pid:%d)\n", (int) getpid());
        printf("Value of child var is = %d", var);
	sleep(1);
    } else {
        // parent goes down this path (original process)
        int wc = wait(NULL);
        var = var+2;
        printf("hello, I am parent of %d (wc:%d) (pid:%d)\n",
	       rc, wc, (int) getpid());
        printf("Value of parent var is = %d", var);
    }
    return 0;
}