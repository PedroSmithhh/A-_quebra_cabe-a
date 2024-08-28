import heapq
import time

def h1(state, goal):
    """Heuristica 1: Contar o numero de pecas fora do lugar"""
    return sum([1 if state[i][j] != goal[i][j] and state[i][j] != 0 else 0 
                for i in range(len(state)) for j in range(len(state[0]))])

def h2(state, goal):
    """Heuristica 2: Distancia de Manhattan"""
    return sum([abs(i - goal_i) + abs(j - goal_j)
                for i in range(len(state)) for j in range(len(state[0]))
                for goal_i in range(len(goal)) for goal_j in range(len(goal[0]))
                if state[i][j] == goal[goal_i][goal_j] and state[i][j] != 0])

def a_star(start, goal, heuristic):
    """Implementacao do algoritmo A*"""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {str(start): 0}
    f_score = {str(start): heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while str(current) in came_from:
                path.append(current)
                current = came_from[str(current)]
            path.reverse()
            return path, g_score

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[str(current)] + 1
            if str(neighbor) not in g_score or tentative_g_score < g_score[str(neighbor)]:
                came_from[str(neighbor)] = current
                g_score[str(neighbor)] = tentative_g_score
                f_score[str(neighbor)] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[str(neighbor)], neighbor))

    return None, None

def get_neighbors(state):
    """Retorna os vizinhos de um estado"""
    neighbors = []
    zero_row, zero_col = next((r, c) for r in range(len(state)) 
                               for c in range(len(state[0])) if state[r][c] == 0)
    possible_moves = [(zero_row - 1, zero_col), (zero_row + 1, zero_col),
                      (zero_row, zero_col - 1), (zero_row, zero_col + 1)]

    for r, c in possible_moves:
        if 0 <= r < len(state) and 0 <= c < len(state[0]):
            new_state = [list(row) for row in state]
            new_state[zero_row][zero_col], new_state[r][c] = new_state[r][c], new_state[zero_row][zero_col]
            neighbors.append(tuple(tuple(row) for row in new_state))

    return neighbors

def run_experiments(start_state, goal_state):
    print("Estado inicial do Experimento:")
    for row in start_state:
        print(row)

    print("\nEstado objetivo do Experimento:")
    for row in goal_state:
        print(row)

    # Executa A* com h1
    start_time = time.time()
    path_h1, g_score_h1 = a_star(start_state, goal_state, h1)
    time_h1 = time.time() - start_time
    nodes_h1 = len(path_h1) - 1 if path_h1 else 0

    print(f"\nExecutando Experimento com h1...")
    print(f"h1 - Nos gerados: {nodes_h1}, Tempo: {time_h1:.4f} segundos, Valor g(n): {g_score_h1[str(goal_state)] if path_h1 else 'Infinito'}")

    # Executa A* com h2
    start_time = time.time()
    path_h2, g_score_h2 = a_star(start_state, goal_state, h2)
    time_h2 = time.time() - start_time
    nodes_h2 = len(path_h2) - 1 if path_h2 else 0

    print(f"\nExecutando Experimento com h2...")
    print(f"h2 - Nos gerados: {nodes_h2}, Tempo: {time_h2:.4f} segundos, Valor g(n): {g_score_h2[str(goal_state)] if path_h2 else 'Infinito'}")

    # Resultados comparativos
    print("\nResultados comparativos:")
    print(f"{'Heuristica':<20} {'Nos gerados':<15} {'Tempo (s)':<15} {'Valor g(n)':<15}")
    print(f"{'h1 (pecas fora)':<20} {nodes_h1:<15} {time_h1:<15.4f} {g_score_h1[str(goal_state)] if path_h1 else 'Infinito':<15}")
    print(f"{'h2 (Manhattan)':<20} {nodes_h2:<15} {time_h2:<15.4f} {g_score_h2[str(goal_state)] if path_h2 else 'Infinito':<15}")

# Definir os estados iniciais e finais para os experimentos
start_state_01 = (
    (2, 8, 3),
    (1, 6, 4),
    (0, 7, 5)
)

goal_state_01 = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

start_state_05 = (
    (7, 2, 4),
    (5, 0, 6),
    (8, 3, 1)
)

goal_state_05 = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

# Executar os experimentos
run_experiments(start_state_01, goal_state_01)
print("\n" + "="*50 + "\n")
run_experiments(start_state_05, goal_state_05)
