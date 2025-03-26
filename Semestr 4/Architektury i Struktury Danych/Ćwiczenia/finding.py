graph = {
    0: [1],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [],
}


# Nie optymalne
def find_longest_path(graph):
    max_path = []  # Lista przechowująca najdłuższą znalezioną ścieżkę

    def search(v, current_path):
        nonlocal max_path  # Odwołanie do zmiennej zewnętrznej (nie tworzymy nowej)
        
        # Jeśli bieżąca ścieżka jest dłuższa niż dotychczasowa najdłuższa, aktualizujemy
        if len(current_path) > len(max_path):
            max_path = current_path[:]
        
        # Przeglądanie sąsiadów i rekurencyjne przeszukiwanie
        for neighbour in graph[v]:
            search(neighbour, current_path + [neighbour])

    # Przeszukiwanie zaczynamy od każdego wierzchołka w grafie
    for v in graph:
        search(v, [v])

    return max_path

print(find_longest_path(graph))



from collections import defaultdict, deque

def topological_sort(graph):
    indegree = {node: 0 for node in graph}  # Liczba krawędzi wchodzących
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    # Kolejka do przetwarzania wierzchołków bez krawędzi wchodzących
    queue = deque([v for v in graph if indegree[v] == 0])
    topo_order = []

    while queue:
        v = queue.popleft()
        topo_order.append(v)
        for neighbor in graph[v]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return topo_order

def find_longest_path(graph):
    topo_order = topological_sort(graph)
    dp = {node: 0 for node in graph}  # Maksymalna długość ścieżki kończącej się w node
    parent = {node: None for node in graph}  # Poprzednik na najdłuższej ścieżce

    for u in topo_order:
        for v in graph[u]:
            if dp[v] < dp[u] + 1:
                dp[v] = dp[u] + 1
                parent[v] = u

    # Znalezienie końcowego wierzchołka najdłuższej ścieżki
    end_node = max(dp, key=dp.get)

    # Odtworzenie ścieżki
    path = []
    while end_node is not None:
        path.append(end_node)
        end_node = parent[end_node]

    return path[::-1]  # Odwrócenie ścieżki (bo zbieraliśmy ją od końca)

graph = {
    0: [1],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [],
}

print(find_longest_path(graph))  # [0, 1, 2, 3, 4, 5, 6]


from collections import deque

def topological_sort(graph):
    indegree = {node: 0 for node in graph}  # Liczba krawędzi wchodzących
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque([v for v in graph if indegree[v] == 0])  # Wierzchołki bez krawędzi wchodzących
    topo_order = []

    while queue:
        v = queue.popleft()
        topo_order.append(v)
        for neighbor in graph[v]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return topo_order

def find_shortest_path(graph, start, end):
    topo_order = topological_sort(graph)
    dp = {node: float('inf') for node in graph}  # Najkrótsza długość ścieżki kończącej się w node
    parent = {node: None for node in graph}  # Poprzednik na najkrótszej ścieżce
    dp[start] = 0  # Startowy wierzchołek ma długość ścieżki 0

    for u in topo_order:
        for v in graph[u]:
            if dp[v] > dp[u] + 1:  # Jeśli znaleźliśmy krótszą ścieżkę, to aktualizujemy
                dp[v] = dp[u] + 1
                parent[v] = u

    # Jeśli `dp[end]` pozostało nieskończonością, to znaczy, że `end` nie jest osiągalny
    if dp[end] == float('inf'):
        return None  

    # Odtworzenie ścieżki od `end` do `start`
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]

    return path[::-1]  # Odwrócenie ścieżki (bo zbieraliśmy ją od końca)

graph = {
    0: [1, 4],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [],
}

start, end = 0, 6
print(find_shortest_path(graph, start, end))  # [0, 1, 2, 3, 4, 5, 6]
