#include <iostream>

using namespace std;

struct Node
{
    long long value;
    int row;
};

Node heap[1'000'000];

int heap_size;

void create_heap(int M)
{
    heap_size = M;
    long long value = M * M;
    heap[0] = {value, M};
    for (int i = 1; i < M; i++)
    {
        value -= ( (M - i) + (M - i) + 1);
        heap[i] = {value, (M - i)};
    }
}

// Debug
void print_heap(int M) {
    for (int i = 0; i < M; i++) {
        printf("heap[%d] = { value: %lld, row: %d }\n", i, heap[i].value, heap[i].row);
    }
}

void swap(Node &a, Node &b)
{
    Node temp = a;
    a = b;
    b = temp;
}

void heapifyDown(int index)
{
    while (true)
    {
        int left = 2 * index + 1;
        int right = 2 * index + 2;
        int largest = index;

        if (left < heap_size && heap[left].value > heap[largest].value)
            largest = left;
        if (right < heap_size && heap[right].value > heap[largest].value)
            largest = right;

        if (largest != index)
        {
            swap(heap[index], heap[largest]);
            index = largest;
        }
        else
            break;
    }
}

long long change() {
    long long res = heap[0].value;
    heap[0].value -= heap[0].row;
    heapifyDown(0);
    return res;
}


int main()
{
    int M, K;
    scanf("%d %d", &M, &K);
    create_heap(M);
    long long last_value = -1;

    while (K > 0)
    {
        long long value;
        value = change();
        if (value != last_value) {
            last_value = value;
            K--;
            printf("%lld\n", value);
        }
    }
    

    return 0;
}
