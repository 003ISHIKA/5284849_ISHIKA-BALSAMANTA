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

char* isValid(char* s) {
    int freq[26] = {0};
    int len = strlen(s);

    for (int i = 0; i < len; i++) {
        freq[s[i] - 'a']++;
    }

    int vals[26], vcount = 0;
    for (int i = 0; i < 26; i++) {
        if (freq[i] > 0) vals[vcount++] = freq[i];
    }

    int min = INT_MAX, max = INT_MIN;
    for (int i = 0; i < vcount; i++) {
        if (vals[i] < min) min = vals[i];
        if (vals[i] > max) max = vals[i];
    }

    if (min == max) return "YES"; // all same

    int minCount = 0, maxCount = 0;
    for (int i = 0; i < vcount; i++) {
        if (vals[i] == min) minCount++;
        if (vals[i] == max) maxCount++;
    }

  
    if (min == 1 && minCount == 1 && (minCount + maxCount == vcount)) {
        return "YES";
    }

    if (max == min + 1 && maxCount == 1 && (minCount + maxCount == vcount)) {
        return "YES";
    }

    return "NO";
}

int main()
{
    FILE* fptr = fopen(getenv("OUTPUT_PATH"), "w");

    char* s = readline();

    char* result = isValid(s);

    fprintf(fptr, "%s\n", result);

    fclose(fptr);

    return 0;
}

char* readline() {
    size_t alloc_length = 1024;
    size_t data_length = 0;

    char* data = malloc(alloc_length);

    while (true) {
        char* cursor = data + data_length;
        char* line = fgets(cursor, alloc_length - data_length, stdin);

        if (!line) {
            break;
        }

        data_length += strlen(cursor);

        if (data_length < alloc_length - 1 || data[data_length - 1] == '\n') {
            break;
        }

        alloc_length <<= 1;
        data = realloc(data, alloc_length);

        if (!data) {
            data = '\0';
            break;
        }
    }

    if (data[data_length - 1] == '\n') {
        data[data_length - 1] = '\0';
        data = realloc(data, data_length);
        if (!data) {
            data = '\0';
        }
    } else {
        data = realloc(data, data_length + 1);
        if (!data) {
            data = '\0';
        } else {
            data[data_length] = '\0';
        }
    }

    return data;
}
