#include <stdio.h>
#include <stdlib.h>

typedef struct Stack {
    int *data;
    int top;
    int capacity;
} Stack;


typedef struct Queue {
    Stack* stack1;
    Stack* stack2;
} Queue;


Stack* createStack(int capacity);
Queue* createQueue(int capacity);
void enqueue(Queue* queue, int item);
int dequeue(Queue* queue);
int front(Queue* queue);

Stack* createStack(int capacity) {
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    stack->capacity = capacity;
    stack->top = -1;
    stack->data = (int*)malloc(stack->capacity * sizeof(int));
    return stack;
}

int isFull(Stack* stack) {
    return stack->top == stack->capacity - 1;
}

int isEmpty(Stack* stack) {
    return stack->top == -1;
}

void push(Stack* stack, int item) {
    if (isFull(stack)) return; // Stack overflow
    stack->data[++stack->top] = item;
}

int pop(Stack* stack) {
    if (isEmpty(stack)) return -1; // Stack underflow
    return stack->data[stack->top--];
}

int peek(Stack* stack) {
    if (isEmpty(stack)) return -1; // Stack is empty
    return stack->data[stack->top];
}

Queue* createQueue(int capacity) {
    Queue* queue = (Queue*)malloc(sizeof(Queue));
    queue->stack1 = createStack(capacity);
    queue->stack2 = createStack(capacity);
    return queue;
}

void enqueue(Queue* queue, int item) {
    push(queue->stack1, item);
}

int dequeue(Queue* queue) {
    if (isEmpty(queue->stack2)) {
        while (!isEmpty(queue->stack1)) {
            push(queue->stack2, pop(queue->stack1));
        }
    }
    return pop(queue->stack2);
}

int front(Queue* queue) {
    if (isEmpty(queue->stack2)) {
        while (!isEmpty(queue->stack1)) {
            push(queue->stack2, pop(queue->stack1));
        }
    }
    return peek(queue->stack2);
}

int main() {
    int q;
    scanf("%d", &q);
    
    Queue* queue = createQueue(q);
    
    for (int i = 0; i < q; i++) {
        int queryType;
        scanf("%d", &queryType);
        
        if (queryType == 1) {
            int value;
            scanf("%d", &value);
            enqueue(queue, value);
        } else if (queryType == 2) {
            dequeue(queue);
        } else if (queryType == 3) {
            printf("%d\n", front(queue));
        }
    }

    free(queue->stack1->data);
    free(queue->stack1);
    free(queue->stack2->data);
    free(queue->stack2);
    free(queue);
    
    return 0;
}
