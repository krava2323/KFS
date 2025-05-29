import random
from parallel_ga_tsp import ParallelGeneticAlgorithm

# Параметри алгоритму
CITIES_COUNT = 25
POPULATION_PER_ISLAND = 50
NUM_ISLANDS = 4  # Кількість паралельних процесів
GENERATIONS = 200
MUTATION_RATE = 0.02
ELITISM_PER_ISLAND = 2
MIGRATION_RATE = 0.1 
MIGRATION_INTERVAL = 25 

if __name__ == '__main__':
    cities = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(CITIES_COUNT)]    # Створення випадкові міста 


    # Ініціалізуємо паралельний алгоритм
    pga = ParallelGeneticAlgorithm(
        cities=cities,
        num_islands=NUM_ISLANDS,
        generations=GENERATIONS,
        pop_per_island=POPULATION_PER_ISLAND,
        mutation_rate=MUTATION_RATE,
        elitism_per_island=ELITISM_PER_ISLAND,
        migration_rate=MIGRATION_RATE,
        migration_interval=MIGRATION_INTERVAL
    )

    # Запускаємо та отримуємо результат
    best_tour, best_distance = pga.run()

    # Виводимо  результат
    print("\n" + "="*40)
    print("Найкращий знайдений маршрут!")
    print(f"Дистанція: {best_distance:.2f}")
    print(f"Порядок міст: {best_tour}")
    print("="*40)
