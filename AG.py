import random
from deap import base, creator, tools

# Função para criar indivíduos (soluções)
def create_individual():
    N = 30
    return creator.Individual([random.randint(0, 1) for _ in range(N)])

# Função de avaliação (fitness)
def evaluate(individual, numbers):
    A = [numbers[i] for i in range(len(individual)) if individual[i] == 0]
    B = [numbers[i] for i in range(len(individual)) if individual[i] == 1]
    return abs(sum(A) - sum(B)),

# Função principal para executar o AG
def main():
    population = toolbox.population(n=50)
    
    # Definir parâmetros do algoritmo
    N_GER = 150  # Número de gerações
    PROB_CROSS = 0.9  # Probabilidade de crossover
    PROB_MUT = 0.02  # Probabilidade de mutação
    
    # Avaliar a população inicial
    fitnesses = list(map(toolbox.evaluate, population))
    for index, fit in zip(population, fitnesses):
        index.fitness.values = fit
    
    # Fitness médio da população inicial
    fits = [index.fitness.values[0] for index in population]
    fitness_avg_inicial = sum(fits) / len(population)
    
    # Algoritmo genético
    for gen in range(N_GER):
        # Selecionar a próxima geração
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        
        # Crossover e mutação
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < PROB_CROSS:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        for mutant in offspring:
            if random.random() < PROB_MUT:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Avaliar indivíduos com fitness inválidos
        invalid_ind = [index for index in offspring if not index.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for index, fit in zip(invalid_ind, fitnesses):
            index.fitness.values = fit
        
        # Substituir a população
        population[:] = offspring
    
    # Fitness médio da população final
    fits = [index.fitness.values[0] for index in population]
    fitness_avg_final = sum(fits) / len(population)
    
    # Imprimir fitness médio inicial e final
    print("Fitness médio inicial:", fitness_avg_inicial)
    print("Fitness médio final:", fitness_avg_final)

# Definir o problema de minimização
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Criar toolbox
toolbox = base.Toolbox()
toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Registrar operadores genéticos
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.02)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate, numbers=[random.randint(1, 100) for _ in range(30)])  # Exemplo de números

if __name__ == "__main__":
    main()
