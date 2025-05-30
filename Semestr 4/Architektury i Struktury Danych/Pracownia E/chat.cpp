#include <iostream>

struct Node
{
    int value;
    int size;
    long long sum;
    Node *left, *right;

    Node(int val) : value(val), size(1), sum(val), left(nullptr), right(nullptr) {}
};

int getSize(Node *node)
{
    return node ? node->size : 0;
}

long long getSum(Node *node)
{
    return node ? node->sum : 0;
}

void update(Node *node)
{
    if (node)
    {
        node->size = 1 + getSize(node->left) + getSize(node->right);
        node->sum = node->value + getSum(node->left) + getSum(node->right);
    }
}

Node *insert(Node *root, int index, int value)
{
    if (!root)
        return new Node(value);

    int leftSize = getSize(root->left);

    if (index <= leftSize)
    {
        root->left = insert(root->left, index, value);
    }
    else
    {
        root->right = insert(root->right, index - leftSize - 1, value);
    }
    update(root);
    return root;
}

Node *findMin(Node *root)
{
    while (root->left)
        root = root->left;
    return root;
}

Node *remove(Node *root, int index)
{
    if (!root)
        return nullptr;

    int leftSize = getSize(root->left);

    if (index < leftSize)
    {
        root->left = remove(root->left, index);
    }
    else if (index > leftSize)
    {
        root->right = remove(root->right, index - leftSize - 1);
    }
    else
    {
        if (!root->left)
        {
            Node *temp = root->right;
            delete root;
            return temp;
        }
        else if (!root->right)
        {
            Node *temp = root->left;
            delete root;
            return temp;
        }
        else
        {
            Node *temp = findMin(root->right);
            root->value = temp->value;
            root->right = remove(root->right, 0);
        }
    }
    update(root);
    return root;
}

long long prefixSum(Node *root, int index)
{
    if (!root)
        return 0;

    int leftSize = getSize(root->left);

    if (index < leftSize)
    {
        return prefixSum(root->left, index);
    }
    else if (index == leftSize)
    {
        return getSum(root->left) + root->value;
    }
    else
    {
        return getSum(root->left) + root->value + prefixSum(root->right, index - leftSize - 1);
    }
}

long long findSum(Node *root, int p1, int p2)
{
    return prefixSum(root, p2) - (p1 > 0 ? prefixSum(root, p1 - 1) : 0);
}

int main()
{
    int n;
    Node *root = nullptr;

    scanf("%d", &n);

    for (int i = 0; i < n; i++)
    {
        char op;
        scanf("\n%c", &op);

        if (op == 'I')
        {
            int p, x;
            scanf("%d %d", &p, &x);
            root = insert(root, p, x);
        }
        else if (op == 'D')
        {
            int p;
            scanf("%d", &p);
            root = remove(root, p - 1);
        }
        else if (op == 'S')
        {
            int p1, p2;
            scanf("%d %d", &p1, &p2);
            printf("%lld\n", findSum(root, p1 - 1, p2 - 1));
        }
    }

    return 0;
}
