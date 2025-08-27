#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LEN 1000000

typedef struct {
    int type;       // 1 = append, 2 = delete
    char *data;     // saved string for undo
} Operation;

int main() {
    int Q;
    scanf("%d", &Q);

    char *S = malloc(MAX_LEN + 1); 
    S[0] = '\0';
    int length = 0;

    Operation *stack = malloc(Q * sizeof(Operation));
    int top = -1;

    for (int i = 0; i < Q; i++) {
        int type;
        scanf("%d", &type);

        if (type == 1) { // append
            char buffer[MAX_LEN + 1];
            scanf("%s", buffer);
            int addLen = strlen(buffer);

            stack[++top].type = 1;
            stack[top].data = strdup(buffer);

            strcpy(S + length, buffer);
            length += addLen;

        } else if (type == 2) { // delete
            int k;
            scanf("%d", &k);

            stack[++top].type = 2;
            stack[top].data = strndup(S + length - k, k);

            length -= k;
            S[length] = '\0';

        } else if (type == 3) { // print
            int k;
            scanf("%d", &k);
            printf("%c\n", S[k - 1]);

        } else if (type == 4) { // undo
            if (top >= 0) {
                Operation last = stack[top--];
                if (last.type == 1) {
                    int len = strlen(last.data);
                    length -= len;
                    S[length] = '\0';
                } else if (last.type == 2) {
                    strcpy(S + length, last.data);
                    length += strlen(last.data);
                }
                free(last.data);
            }
        }
    }

    free(S);
    free(stack);
    return 0;
}
