import heapq
import time

# Funcao para calcular h1 (numero de pecas fora da posicao)
def h1(state, goal):
    return sum(1 for i in range(len(state)) for j in range(len(state)) if state[i][j] != goal[i][j] and state[i][j] != 0)

# Funcao para calcular h2 (distancia Manhattan)
def h2(state, goal):
    distance = 0
    goal_positions = {value: (i, j) for i, row in enumerate(goal) for j, value in enumerate(row)}  # Mapeia cada valor para sua posição no estado objetivo
    for i in range(len(state)):
        for j in range(len(state)):
            value = state[i][j]
            if value != 0:  # Ignora o zero
                goal_i, goal_j = goal_positions[value]  # Obtém a posição do valor no estado objetivo
                distance += abs(goal_i - i) + abs(goal_j - j)
    return distance

# Funcao para obter os movimentos possiveis
def get_neighbors(state):
    neighbors = []
    zero_pos = [(ix, iy) for ix, row in enumerate(state) for iy, val in enumerate(row) if val == 0][0]
    x, y = zero_pos
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # baixo, cima, direita, esquerda

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(state) and 0 <= new_y < len(state):
            new_state = [list(row) for row in state]  # copia do estado atual
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]  # troca
            neighbors.append(new_state)

    return neighbors

# Funcao A* para encontrar o caminho
def a_star(start, goal, heuristic):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {str(start): 0}
    f_score = {str(start): heuristic(start, goal)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            return reconstruct_path(came_from, current), g_score

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[str(current)] + 1

            if str(neighbor) not in g_score or tentative_g_score < g_score[str(neighbor)]:
                came_from[str(neighbor)] = current
                g_score[str(neighbor)] = tentative_g_score
                f_score[str(neighbor)] = tentative_g_score + heuristic(neighbor, goal)
                if str(neighbor) not in [i[1] for i in open_list]:
                    heapq.heappush(open_list, (f_score[str(neighbor)], neighbor))

    return None, g_score

# Funcao para reconstruir o caminho
def reconstruct_path(came_from, current):
    total_path = [current]
    while str(current) in came_from:
        current = came_from[str(current)]
        total_path.append(current)
    return total_path[::-1]

# Funcao para executar os experimentos
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
    print(f"h1 - Nos gerados: {nodes_h1}, Tempo: {time_h1:.4f} segundos, Valor g(n): {g_score_h1[str(start_state)] if path_h1 else 'Infinito'}")

    # Executa A* com h2
    start_time = time.time()
    path_h2, g_score_h2 = a_star(start_state, goal_state, h2)
    time_h2 = time.time() - start_time
    nodes_h2 = len(path_h2) - 1 if path_h2 else 0

    print(f"\nExecutando Experimento com h2...")
    print(f"h2 - Nos gerados: {nodes_h2}, Tempo: {time_h2:.4f} segundos, Valor g(n): {g_score_h2[str(start_state)] if path_h2 else 'Infinito'}")

    # Resultados comparativos
    print("\nResultados comparativos:")
    print(f"{'Heuristica':<20} {'Nos gerados':<15} {'Tempo (s)':<15} {'Valor g(n)':<15}")
    print(f"{'h1 (pecas fora)':<20} {nodes_h1:<15} {time_h1:<15.4f} {g_score_h1[str(start_state)] if path_h1 else 'Infinito':<15}")
    print(f"{'h2 (Manhattan)':<20} {nodes_h2:<15} {time_h2:<15.4f} {g_score_h2[str(start_state)] if path_h2 else 'Infinito':<15}")

# Experimento 01
start_state_01 = [
    [2, 8, 3],
    [1, 6, 4],
    [0, 7, 5]
]

goal_state_01 = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

# Experimento 02
start_state_02 = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]

goal_state_05 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Executa os experimentos
run_experiments(start_state_01, goal_state_01)
print("\n" + "="*50 + "\n")
run_experiments(start_state_02, goal_state_05)
