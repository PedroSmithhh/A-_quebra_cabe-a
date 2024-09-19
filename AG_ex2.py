import numpy as np
import random
import matplotlib.pyplot as plt

# Função para calcular a distância total de uma rota
def calcular_distancia(rota, matriz_distancias):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += matriz_distancias[rota[i]][rota[i + 1]]
    distancia_total += matriz_distancias[rota[-1]][rota[0]]  # Retorno à cidade de origem
    return distancia_total

# Função para criar a população inicial
def criar_populacao(tamanho_populacao, num_cidades):
    populacao = []
    for _ in range(tamanho_populacao):
        rota = list(range(num_cidades))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao

# Função de seleção por torneio (k=3)
def selecao_torneio(populacao, aptidao, k=3):
    selecionados = random.sample(list(zip(populacao, aptidao)), k)
    selecionados.sort(key=lambda x: x[1])
    return selecionados[0][0]

# Função de crossover de um ponto
def crossover(pai1, pai2, probabilidade_crossover=0.9):
    if random.random() < probabilidade_crossover:
        ponto_corte = random.randint(1, len(pai1) - 2)
        filho1 = pai1[:ponto_corte] + [cidade for cidade in pai2 if cidade not in pai1[:ponto_corte]]
        filho2 = pai2[:ponto_corte] + [cidade for cidade in pai1 if cidade not in pai2[:ponto_corte]]
        return filho1, filho2
    return pai1, pai2

# Função de mutação (troca de duas cidades aleatórias)
def mutacao(rota, probabilidade_mutacao=0.02):
    if random.random() < probabilidade_mutacao:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]
    return rota

# Função principal do Algoritmo Genético
def algoritmo_genetico(matriz_distancias, num_geracoes=250, tamanho_populacao=50, probabilidade_crossover=0.9, probabilidade_mutacao=0.02):
    num_cidades = len(matriz_distancias)
    populacao = criar_populacao(tamanho_populacao, num_cidades)
    melhor_distancia_historico = []
    media_distancia_historico = []

    for geracao in range(num_geracoes):
        aptidao = [calcular_distancia(rota, matriz_distancias) for rota in populacao]
        nova_populacao = []
        
        # Salva as métricas de convergência
        melhor_distancia_historico.append(min(aptidao))
        media_distancia_historico.append(np.mean(aptidao))
        
        # Gera a nova população
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, aptidao)
            pai2 = selecao_torneio(populacao, aptidao)
            filho1, filho2 = crossover(pai1, pai2, probabilidade_crossover)
            filho1 = mutacao(filho1, probabilidade_mutacao)
            filho2 = mutacao(filho2, probabilidade_mutacao)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao[:tamanho_populacao]  # Garante que a população não exceda o tamanho
    
    # Seleciona o melhor indivíduo após todas as gerações
    aptidao_final = [calcular_distancia(rota, matriz_distancias) for rota in populacao]
    melhor_rota = populacao[np.argmin(aptidao_final)]
    melhor_distancia = min(aptidao_final)

    # Resultados finais
    print(f"Melhor rota encontrada: {melhor_rota}")
    print(f"Distância total percorrida: {melhor_distancia}")
    print(f"Distância média da população inicial: {media_distancia_historico[0]}")
    print(f"Distância média da população final: {media_distancia_historico[-1]}")

    # Gráfico de convergência
    plt.plot(melhor_distancia_historico, label="Melhor indivíduo")
    plt.plot(media_distancia_historico, label="Média da população")
    plt.xlabel("Geração")
    plt.ylabel("Distância")
    plt.legend()
    plt.title("Convergência do AG para o TSP")
    plt.show()

matriz_distancias_uk12 = [
    [0, 300, 352, 466, 217, 238, 431, 336, 451, 47, 415, 515],
    [300, 0, 638, 180, 595, 190, 138, 271, 229, 236, 214, 393],
    [352, 638, 0, 251, 88, 401, 189, 386, 565, 206, 292, 349],
    [466, 180, 251, 0, 139, 371, 169, 316, 180, 284, 206, 198],
    [217, 595, 88, 139, 0, 310, 211, 295, 474, 130, 133, 165],
    [238, 190, 401, 371, 310, 0, 202, 122, 378, 157, 362, 542],
    [431, 138, 189, 169, 211, 202, 0, 183, 67, 268, 117, 369],
    [336, 271, 386, 316, 295, 122, 183, 0, 483, 155, 448, 108],
    [451, 229, 565, 180, 474, 378, 67, 483, 0, 299, 246, 418],
    [47, 236, 206, 284, 130, 157, 268, 155, 299, 0, 202, 327],
    [415, 214, 292, 206, 133, 362, 117, 448, 246, 202, 0, 394],
    [515, 393, 349, 198, 165, 542, 368, 108, 418, 327, 394, 0]
]

matriz_distancias_ha30 = [
    [0, 39, 22, 59, 54, 33, 57, 32, 89, 73, 29, 46, 16, 83, 120, 45, 24, 32, 36, 25, 38, 16, 43, 21, 50, 57, 46, 72, 121, 73],
    [39, 0, 20, 20, 81, 8, 49, 64, 63, 84, 10, 61, 25, 49, 81, 81, 58, 16, 72, 60, 78, 24, 69, 18, 75, 88, 68, 44, 83, 52],
    [22, 20, 0, 39, 74, 18, 60, 44, 71, 73, 11, 46, 6, 61, 99, 61, 37, 10, 51, 40, 59, 5, 62, 7, 57, 78, 51, 51, 100, 56],
    [59, 20, 39, 0, 93, 27, 51, 81, 48, 80, 30, 69, 45, 32, 61, 97, 75, 31, 89, 78, 97, 44, 83, 38, 84, 100, 77, 31, 63, 42],
    [54, 81, 74, 93, 0, 73, 43, 56, 104, 76, 76, 77, 69, 111, 72, 46, 56, 84, 49, 53, 33, 69, 12, 69, 64, 7, 69, 122, 73, 114],
    [33, 8, 18, 27, 73, 0, 45, 61, 71, 64, 26, 65, 18, 56, 92, 60, 32, 25, 47, 33, 58, 14, 61, 26, 56, 71, 44, 57, 99, 45],
    [57, 49, 60, 51, 43, 45, 0, 37, 74, 36, 55, 32, 61, 83, 49, 14, 25, 63, 9, 15, 11, 55, 33, 56, 32, 47, 23, 85, 42, 85],
    [32, 64, 44, 81, 56, 61, 37, 0, 76, 71, 63, 28, 50, 82, 99, 38, 26, 53, 34, 37, 37, 48, 51, 43, 32, 62, 41, 69, 99, 61],
    [89, 63, 71, 48, 104, 71, 74, 76, 0, 109, 55, 86, 73, 65, 49, 84, 73, 75, 66, 59, 77, 73, 92, 78, 91, 106, 83, 50, 63, 48],
    [73, 84, 73, 80, 76, 64, 36, 71, 109, 0, 82, 68, 88, 106, 67, 50, 52, 88, 36, 42, 42, 78, 65, 81, 47, 69, 53, 98, 52, 103],
    [29, 10, 11, 30, 76, 26, 55, 63, 55, 82, 0, 58, 17, 53, 87, 57, 36, 18, 61, 52, 69, 21, 67, 21, 67, 81, 57, 54, 93, 57],
    [46, 61, 46, 69, 77, 65, 32, 28, 86, 68, 58, 0, 49, 84, 71, 32, 48, 62, 29, 29, 41, 47, 64, 54, 46, 78, 60, 75, 94, 71],
    [16, 25, 6, 45, 69, 18, 61, 50, 73, 88, 17, 49, 0, 67, 104, 62, 35, 12, 50, 38, 58, 11, 61, 13, 56, 77, 50, 48, 97, 58],
    [83, 49, 61, 32, 111, 56, 83, 82, 65, 106, 53, 84, 67, 0, 39, 82, 75, 76, 86, 74, 93, 64, 106, 64, 101, 118, 97, 20, 51, 29],
    [120, 81, 99, 61, 72, 92, 49, 99, 49, 67, 87, 71, 104, 39, 0, 71, 85, 104, 58, 56, 49, 92, 66, 92, 65, 66, 60, 117, 92, 121],
    [45, 81, 61, 97, 46, 60, 14, 38, 84, 50, 57, 32, 62, 82, 71, 0, 14, 55, 14, 16, 25, 47, 47, 55, 14, 53, 21, 87, 47, 89],
    [24, 58, 37, 75, 56, 32, 25, 26, 73, 52, 36, 48, 35, 75, 85, 14, 0, 39, 21, 16, 26, 28, 37, 37, 27, 50, 28, 73, 64, 72],
    [32, 16, 10, 31, 84, 25, 63, 53, 75, 88, 18, 62, 12, 76, 104, 55, 39, 0, 59, 48, 66, 23, 65, 21, 61, 80, 60, 59, 108, 65],
    [36, 72, 51, 89, 49, 47, 9, 34, 66, 36, 61, 29, 50, 86, 58, 14, 21, 59, 0, 15, 19, 53, 25, 60, 23, 39, 23, 91, 43, 82],
    [25, 60, 40, 78, 53, 33, 15, 37, 59, 42, 52, 29, 38, 74, 56, 16, 16, 48, 15, 0, 28, 46, 38, 51, 24, 47, 33, 82, 58, 75],
    [38, 78, 59, 97, 33, 58, 11, 37, 77, 42, 69, 41, 58, 93, 49, 25, 26, 66, 19, 28, 0, 65, 21, 67, 44, 26, 31, 98, 35, 91],
    [16, 24, 5, 44, 69, 14, 55, 48, 73, 78, 21, 47, 11, 64, 92, 47, 28, 23, 53, 46, 65, 0, 57, 18, 53, 73, 46, 52, 97, 53],
    [43, 69, 62, 83, 12, 61, 33, 51, 92, 65, 67, 64, 61, 106, 66, 47, 37, 65, 25, 38, 21, 57, 0, 62, 55, 5, 57, 106, 66, 109],
    [21, 18, 7, 38, 69, 26, 56, 43, 78, 81, 21, 54, 13, 64, 92, 55, 37, 21, 60, 51, 67, 18, 62, 0, 62, 73, 50, 50, 99, 56],
    [50, 75, 57, 84, 64, 56, 32, 32, 91, 47, 67, 46, 56, 101, 65, 14, 27, 61, 23, 24, 44, 53, 55, 62, 0, 59, 33, 81, 61, 85],
    [57, 88, 78, 100, 7, 71, 47, 62, 106, 69, 81, 78, 77, 118, 66, 53, 50, 80, 39, 47, 26, 73, 5, 73, 59, 0, 69, 118, 71, 111],
    [46, 68, 51, 77, 69, 44, 23, 41, 83, 53, 57, 60, 50, 97, 60, 21, 28, 60, 23, 33, 31, 46, 57, 50, 33, 69, 0, 82, 42, 82],
    [72, 44, 51, 31, 122, 57, 85, 69, 50, 98, 54, 75, 48, 20, 117, 87, 73, 59, 91, 82, 98, 52, 106, 50, 81, 118, 82, 0, 41, 29],
    [121, 83, 100, 63, 73, 99, 42, 99, 63, 52, 93, 94, 97, 51, 92, 47, 64, 108, 43, 58, 35, 97, 66, 99, 61, 71, 42, 41, 0, 59],
    [73, 52, 56, 42, 114, 45, 85, 61, 48, 103, 57, 71, 58, 29, 121, 89, 72, 65, 82, 75, 91, 53, 109, 56, 85, 111, 82, 29, 59, 0]
]

# Executa o algoritmo genético
algoritmo_genetico(matriz_distancias_uk12)

# Executa o algoritmo genético
algoritmo_genetico(matriz_distancias_ha30)
