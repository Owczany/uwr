#include <cstdio>
#include <limits>

const int N = 1'000'000;

struct Point
{
    int x, y;
};

Point points[N];
Point points_x[N];
Point points_y[N];
Point buffor[12 * N];

Point best_p, best_q;
long long best_dist = 10000000000000000;

void print_point(Point p)
{
    printf("%d %d\n", p.x, p.y);
}

void merge(int ls, int le, int rs, int re)
{
    int s = ls;
    int i = ls;
    while (ls <= le && rs <= re)
    {
        if (points_x[ls].x < points_x[rs].x)
            points[i++] = points_x[ls++];
        else
            points[i++] = points_x[rs++];
    }
    while (ls <= le)
        points[i++] = points_x[ls++];
    while (rs <= re)
        points[i++] = points_x[rs++];
    for (int j = s; j <= re; j++)
        points_x[j] = points[j];

    i = s;
    ls = s;
    rs = le + 1;
    while (ls <= le && rs <= re)
    {
        if (points_y[ls].y < points_y[rs].y)
            points[i++] = points_y[ls++];
        else
            points[i++] = points_y[rs++];
    }
    while (ls <= le)
        points[i++] = points_y[ls++];
    while (rs <= re)
        points[i++] = points_y[rs++];
    for (int j = s; j <= re; j++)
        points_y[j] = points[j];
}

void merge_sort(int l, int r)
{
    if (l >= r)
        return;
    int mid = (l + r) / 2;
    merge_sort(l, mid);
    merge_sort(mid + 1, r);
    merge(l, mid, mid + 1, r);
}

long long distance(const Point &a, const Point &b)
{
    long long dx = (long long)a.x - b.x;
    long long dy = (long long)a.y - b.y;
    return dx * dx + dy * dy;
}

void closestPair(int l, int r, Point aux_y[], int yCount, Point buf[])
{
    int n = r - l + 1;
    if (n <= 3)
    {
        for (int i = l; i <= r; i++)
        {
            for (int j = i + 1; j <= r; j++)
            {
                long long d_curr = distance(points_x[i], points_x[j]);
                if (d_curr < best_dist)
                {
                    best_dist = d_curr;
                    best_p = points_x[i];
                    best_q = points_x[j];
                }
            }
        }
        
        return;
    }

    int mid = (l + r) / 2;
    int midX = points_x[mid].x;

    Point *left_buf = buf;
    Point *right_buf = buf + yCount;

    int left_count = 0, right_count = 0;
    for (int i = 0; i < yCount; i++)
    {
        if (aux_y[i].x < midX || (aux_y[i].x == midX && left_count < right_count))
            left_buf[left_count++] = aux_y[i];
        else
            right_buf[right_count++] = aux_y[i];
    }

    closestPair(l, mid, left_buf, left_count, buf + 2 * yCount); // LEFT
    closestPair(mid + 1, r, right_buf, right_count, buf + 2 * yCount); // RIGHT

    int i = 0, j = 0, k = 0;
    while (i < left_count && j < right_count)
    {
        if (left_buf[i].y < right_buf[j].y)
            aux_y[k++] = left_buf[i++];
        else
            aux_y[k++] = right_buf[j++];
    }
    while (i < left_count)
        aux_y[k++] = left_buf[i++];
    while (j < right_count)
        aux_y[k++] = right_buf[j++];

    int strip_count = 0;
    for (i = 0; i < yCount; i++)
    {
        long long dx = (long long)aux_y[i].x - midX;
        if (dx * dx < best_dist)
            buf[strip_count++] = aux_y[i];
    }

    for (i = 0; i < strip_count; i++)
    {
        for (j = i + 1; j < strip_count &&
                            ((long long)buf[j].y - buf[i].y) * ((long long)buf[j].y - buf[i].y) < best_dist;
             j++)
        {
            long long d_curr = distance(buf[i], buf[j]);
            if (d_curr < best_dist)
            {
                best_dist = d_curr;
                best_p = buf[i];
                best_q = buf[j];
            }
        }
    }
}

int main()
{
    int n;
    if (scanf("%d", &n) != 1)
        return 1;
    for (int i = 0; i < n; i++)
    {
        scanf("%d %d", &points_x[i].x, &points_x[i].y);
        points_y[i] = points_x[i];
    }

    merge_sort(0, n - 1);
    closestPair(0, n - 1, points_y, n, buffor);
    print_point(best_p);
    print_point(best_q);

    return 0;
}