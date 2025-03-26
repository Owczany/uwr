from collections import deque

def bfs_farthest(n, tree, start):
    """ Znajduje najdalszy wierzchołek i jego odległość od startu. """
    queue = deque([start])
    visited = [-1] * n
    visited[start] = 0
    farthest_node, max_dist = start, 0

    while queue:
        node = queue.popleft()
        for neighbor in tree[node]:
            if visited[neighbor] == -1:
                visited[neighbor] = visited[node] + 1
                queue.append(neighbor)
                if visited[neighbor] > max_dist:
                    max_dist = visited[neighbor]
                    farthest_node = neighbor

    return farthest_node, max_dist, visited

def find_diameter(n, tree):
    """ Znajduje średnicę drzewa oraz jej ścieżkę. """
    u, _, _ = bfs_farthest(n, tree, 0)  
    v, _, dist_from_v = bfs_farthest(n, tree, u)  

    path = []
    node = v
    while node != u:
        path.append(node)
        for neighbor in tree[node]:
            if dist_from_v[neighbor] == dist_from_v[node] - 1:
                node = neighbor
                break
    path.append(u)
    return path[::-1]  # Odwracamy, aby mieć od u do v

def color_tree(n, tree, k):
    """ Pokolorowanie drzewa tak, aby na każdej ścieżce było maksymalnie k pokolorowanych wierzchołków. """
    
    # Znajdź ścieżkę średnicy drzewa
    diameter_path = find_diameter(n, tree)
    
    # Kolorowanie co k-ty wierzchołek na średnicy
    colored = set()
    for i in range(0, len(diameter_path), k):
        colored.add(diameter_path[i])

    # BFS, aby rozszerzyć kolorowanie na resztę drzewa
    queue = deque()
    distance_from_colored = [-1] * n

    for node in colored:
        queue.append(node)
        distance_from_colored[node] = 0  # Pokolorowane wierzchołki mają odległość 0

    while queue:
        node = queue.popleft()
        for neighbor in tree[node]:
            if distance_from_colored[neighbor] == -1:  # Jeszcze nie odwiedzony
                distance_from_colored[neighbor] = distance_from_colored[node] + 1
                if distance_from_colored[neighbor] >= k:  # Kolorujemy co k-ty
                    colored.add(neighbor)
                    queue.append(neighbor)
                else:
                    queue.append(neighbor)  # Nie kolorujemy, ale przetwarzamy dalej
    
    return colored

# Przykładowe użycie:
n = 7
tree = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5, 6],
    3: [1],
    4: [1],
    5: [2],
    6: [2]
}
k = 2
print(color_tree(n, tree, k))
