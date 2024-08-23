import heapq

matriz_experimento_1 = [
    [2,8,3],
    [1,6,4],
    [None,7,5]
]

matriz_objetivo_1 = [
    [1,2,3],
    [8,None,4],
    [7,6,5]
]

def h1 (matriz_atual, matriz_objetivo):
    count = 0
    for i in range(3):
        for j in range(3):
            if matriz_atual[i][j] is not None and matriz_atual[i][j] != matriz_objetivo[i][j]:
                count +=1
    return count
    

abertos = [matriz_experimento_1]
fechados = []


for linha in matriz_experimento_1:
    print(linha)

