#include <assert.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* readline();
char* ltrim(char*);
char* rtrim(char*);

int parse_int(char*);

#define ALPHA 10

typedef struct TrieNode {
    struct TrieNode* child[ALPHA];
    bool end;                  
} TrieNode;

static TrieNode* newNode(void) {
    TrieNode* n = (TrieNode*)malloc(sizeof(TrieNode));
    n->end = false;
    for (int i = 0; i < ALPHA; ++i) n->child[i] = NULL;
    return n;
}


static bool trie_insert(TrieNode* root, const char* s) {
    TrieNode* cur = root;
    for (int i = 0; s[i]; ++i) {
        int idx = s[i] - 'a';              
        if (cur->child[idx] == NULL) {
            cur->child[idx] = newNode();
        }
        cur = cur->child[idx];

   
        if (cur->end) return false;
    }

    for (int c = 0; c < ALPHA; ++c) {
        if (cur->child[c] != NULL) return false;
    }

    cur->end = true; /* mark end of this word */
    return true;
}

void noPrefix(int words_count, char** words) {
    TrieNode* root = newNode();

    for (int i = 0; i < words_count; ++i) {
        if (!trie_insert(root, words[i])) {
            printf("BAD SET\n");
            printf("%s\n", words[i]);
            return;
        }
    }
    printf("GOOD SET\n");
}

int main()
{
    int n = parse_int(ltrim(rtrim(readline())));

    char** words = malloc(n * sizeof(char*));
    for (int i = 0; i < n; i++) {
        char* words_item = readline();
        *(words + i) = words_item;
    }

    noPrefix(n, words);
    return 0;
}

char* readline() {
    size_t alloc_length = 1024;
    size_t data_length = 0;
    char* data = malloc(alloc_length);

    while (true) {
        char* cursor = data + data_length;
        char* line = fgets(cursor, alloc_length - data_length, stdin);
        if (!line) break;
        data_length += strlen(cursor);
        if (data_length < alloc_length - 1 || data[data_length - 1] == '\n') break;
        alloc_length <<= 1;
        data = realloc(data, alloc_length);
        if (!data) { data = '\0'; break; }
    }

    if (data[data_length - 1] == '\n') {
        data[data_length - 1] = '\0';
        data = realloc(data, data_length);
        if (!data) data = '\0';
    } else {
        data = realloc(data, data_length + 1);
        if (!data) data = '\0';
        else data[data_length] = '\0';
    }
    return data;
}

char* ltrim(char* str) {
    if (!str) return '\0';
    if (!*str) return str;
    while (*str != '\0' && isspace(*str)) str++;
    return str;
}

char* rtrim(char* str) {
    if (!str) return '\0';
    if (!*str) return str;
    char* end = str + strlen(str) - 1;
    while (end >= str && isspace(*end)) end--;
    *(end + 1) = '\0';
    return str;
}

int parse_int(char* str) {
    char* endptr;
    int value = strtol(str, &endptr, 10);
    if (endptr == str || *endptr != '\0') exit(EXIT_FAILURE);
    return value;
}
