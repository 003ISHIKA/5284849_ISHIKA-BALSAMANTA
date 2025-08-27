#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define MAXN 100000

int heap[MAXN+1];
int heapSize = 0;

void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

void heapify_up(int idx) {
    while (idx > 1 && heap[idx] < heap[idx/2]) {
        swap(&heap[idx], &heap[idx/2]);
        idx /= 2;
    }
}

void heapify_down(int idx) {
    int smallest = idx;
    int left = 2*idx, right = 2*idx+1;

    if (left <= heapSize && heap[left] < heap[smallest]) smallest = left;
    if (right <= heapSize && heap[right] < heap[smallest]) smallest = right;

    if (smallest != idx) {
        swap(&heap[idx], &heap[smallest]);
        heapify_down(smallest);
    }
}

void insertHeap(int x) {
    heap[++heapSize] = x;
    heapify_up(heapSize);
}

void deleteHeap(int x) {
    int i;
    for (i = 1; i <= heapSize; i++) {
        if (heap[i] == x) break;
    }
    if (i <= heapSize) {
        heap[i] = heap[heapSize--];  // replace with last
        if (i > 1 && heap[i] < heap[i/2]) {
            heapify_up(i);
        } else {
            heapify_down(i);
        }
    }
}

int getMin() {
    return heap[1];
}

int main() {
    int Q;
    scanf("%d", &Q);

    while (Q--) {
        int type, x;
        scanf("%d", &type);

        if (type == 1) {          // insert
            scanf("%d", &x);
            insertHeap(x);
        } else if (type == 2) {   // delete
            scanf("%d", &x);
            deleteHeap(x);
        } else if (type == 3) {   // print min
            printf("%d\n", getMin());
        }
    }

    return 0;
}
