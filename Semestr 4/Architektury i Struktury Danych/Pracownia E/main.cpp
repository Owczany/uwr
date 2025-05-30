#include <iostream>

struct Node
{
    int value;
    int size;
    long long sum;
    Node *left;
    Node *right;

    Node(int val) : value(val), size(1), sum(val), left(nullptr), right(nullptr) {}
};

int getSum(Node *node)
{
    return node ? node->sum : 0;
}

int getSize(Node *node)
{
    return node ? node->size : 0;
}

void updateSum(Node *node)
{
    if (node)
    {
        node->sum = node->value + getSum(node->left) + getSum(node->right);
    }
}

void updateSize(Node *node)
{
    if (node)
    {
        node->size = 1 + getSize(node->left) + getSize(node->right);
    }
}

void inorder(Node *root)
{
    if (!root)
        return;
    inorder(root->left);
    printf("%d ", root->value);
    inorder(root->right);
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
    updateSize(root);
    updateSum(root);
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
    updateSize(root);
    updateSum(root);
    return root;
}

long long findSum(Node *root, int p1, int p2)
{
    if (!root)
        return 0;

    int leftSize = getSize(root->left);

    // najpierw szukamy pierwszego wspolnego

    if (p1 < leftSize && p2 < leftSize)
    {
        return findSum(root->left, p1, p2);
    }
    else if (p1 > leftSize && p2 > leftSize)
    {
        return findSum(root->right, p1 - leftSize - 1, p2 - leftSize - 1);
    }

    long long res = getSum(root);

    int lSize = leftSize;
    int rSize = leftSize;
    Node *leftRoot = root;
    Node *rightRoot = root;

    // Przeszukiwanie lewej strony
    while (p1 != lSize)
    {

        if (p1 < lSize)
        {
            leftRoot = leftRoot->left;
        }
        else if (p1 > lSize)
        {

            res -= getSum(leftRoot->left) + leftRoot->value;
            p1 = p1 - lSize - 1;
            leftRoot = leftRoot->right;
        }
        else
        {
            res -= getSum(leftRoot->left);
        }

        lSize = getSize(leftRoot->left);
    }

    // Przeszukiwanie prawej strony
    while (p2 != rSize)
    {

        if (p2 < rSize)
        {
            res -= getSum(rightRoot->right) + rightRoot->value;
            rightRoot = rightRoot->left;
        }
        else if (p2 > rSize)
        {
            p2 = p2 - rSize - 1;
            rightRoot = rightRoot->right;
        }
        else
        {
            res -= getSum(rightRoot->right);
        }

        rSize = getSize(rightRoot->left);
    }

    return res;
}

void printSum(Node *root, int p1, int p2)
{
    printf("%lld\n", findSum(root, p1, p2));
}

int main()
{
    int n;
    Node *root = nullptr;

    scanf("%d\n", &n);

    for (int i = 0; i < n; i++)
    {
        char op;
        scanf("\n%c", &op);

        if (op == 'I')
        {
            int p, x;
            scanf("%d %d", &p, &x);
            root = insert(root, p, x);
            inorder(root);
            printf("\n");
        }
        else if (op == 'D')
        {
            int p;
            scanf("%d", &p);
            root = remove(root, p - 1);
            inorder(root);
            printf("\n");
        }
        else if (op == 'S')
        {
            int p1, p2;
            scanf("%d %d", &p1, &p2);
            printSum(root, p1 - 1, p2 - 1);
        }
    }

    return 0;
}