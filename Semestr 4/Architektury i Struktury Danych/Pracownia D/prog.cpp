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

Point best_p, best_q;
long long best_dist = 1e18;

void print_point(Point p)
{
    printf("%d %d\n", p.x, p.y);
}

void merge(int ls, int le, int rs, int re)
{
    int s = ls;
    int i = ls;
    while (ls <= le && rs <= re)
        points[i++] = (points_x[ls].x < points_x[rs].x) ? points_x[ls++] : points_x[rs++];
    while (ls <= le) points[i++] = points_x[ls++];
    while (rs <= re) points[i++] = points_x[rs++];
    for (int j = s; j <= re; j++) points_x[j] = points[j];

    i = s; ls = s; rs = le + 1;
    while (ls <= le && rs <= re)
        points[i++] = (points_y[ls].y < points_y[rs].y) ? points_y[ls++] : points_y[rs++];
    while (ls <= le) points[i++] = points_y[ls++];
    while (rs <= re) points[i++] = points_y[rs++];
    for (int j = s; j <= re; j++) points_y[j] = points[j];
}

void merge_sort(int l, int r)
{
    if (l >= r) return;
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

void closestPair(int l, int r)
{
    int n = r - l + 1;
    if (n <= 3)
    {
        for (int i = l; i <= r; ++i)
        {
            for (int j = i + 1; j <= r; ++j)
            {
                long long d = distance(points_x[i], points_x[j]);
                if (d < best_dist)
                {
                    best_dist = d;
                    best_p = points_x[i];
                    best_q = points_x[j];
                }
            }
        }
        return;
    }

    int mid = (l + r) / 2;
    int midX = points_x[mid].x;

    closestPair(l, mid);
    closestPair(mid + 1, r);

    // Strip: przeszukaj wszystkie punkty w points_y, które są blisko midX
    for (int i = 0; i < r - l + 1; i++)
    {
        if ((long long)(points_y[i].x - midX) * (points_y[i].x - midX) < best_dist)
        {
            for (int j = i + 1; j < r - l + 1 &&
                (long long)(points_y[j].y - points_y[i].y) * (points_y[j].y - points_y[i].y) < best_dist; j++)
            {
                long long d = distance(points_y[i], points_y[j]);
                if (d < best_dist)
                {
                    best_dist = d;
                    best_p = points_y[i];
                    best_q = points_y[j];
                }
            }
        }
    }
}

int main()
{
    int n;
    if (scanf("%d", &n) != 1) return 1;

    for (int i = 0; i < n; i++)
    {
        scanf("%d %d", &points_x[i].x, &points_x[i].y);
        points_y[i] = points_x[i];
    }

    merge_sort(0, n - 1);
    closestPair(0, n - 1);
    print_point(best_p);
    print_point(best_q);
    return 0;
}
