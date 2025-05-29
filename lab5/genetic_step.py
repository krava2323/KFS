import random
import math

class TSPSolver:
    def __init__(self, cities, population_size, mutation_rate, elitism_count): #кроки та дані для однієї  популяції  
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.distance_matrix = self._compute_distance_matrix()
        self.population = self._initialize_population()
        self.best_solution = None

    #  ініціалізація популяції
    def _create_individual(self):
        individual = list(range(len(self.cities)))
        random.shuffle(individual)
        return individual

    def _initialize_population(self):  # початкова популяція
        return [self._create_individual() for _ in range(self.population_size)]

    
    def _get_tour_distance(self, tour):    # дистанція маршруту 
        distance = 0
        num_cities = len(tour)
        for i in range(num_cities):
            from_city = tour[i]
            to_city = tour[(i + 1) % num_cities] 
            distance += self.distance_matrix[from_city][to_city]
        return distance

    def _calculate_fitness(self, tour):      # визначення якості маршруту 
        distance = self._get_tour_distance(tour)
        return 1.0 / distance if distance > 0 else 0.0

    #  вибір батьків 
    def _tournament_selection(self, population_with_fitness, tournament_size=5):
        tournament_contenders = random.sample(population_with_fitness, tournament_size)   # вибираємо найкращу особину 
        return max(tournament_contenders, key=lambda item: item[1])[0]

    #  створення нащадків 
    def _ordered_crossover(self, parent1, parent2):
        size = len(parent1)
        child = [None] * size
        start, end = sorted(random.sample(range(size), 2))
        child[start:end+1] = parent1[start:end+1]
        
        pointer = 0
        for i in range(size):
            if child[i] is None:
                while parent2[pointer] in child:
                    pointer += 1
                child[i] = parent2[pointer]
        return child
        
    #  створення нащадків мутація
    def _swap_mutation(self, tour):
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(tour)), 2)
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
        return tour

    #  вибір для наступної популяції 
    def _create_next_generation(self):
        pop_with_fitness = sorted(
            [(tour, self._calculate_fitness(tour)) for tour in self.population],
            key=lambda item: item[1],
            reverse=True
        )
        
        new_population = []
        
        #  зберігаємо найкращих особин
        for i in range(self.elitism_count):
            new_population.append(pop_with_fitness[i][0])
        
        # заповнюємо решту популяції нащадками
        while len(new_population) < self.population_size:
            parent1 = self._tournament_selection(pop_with_fitness)
            parent2 = self._tournament_selection(pop_with_fitness)
            child = self._ordered_crossover(parent1, parent2)
            mutated_child = self._swap_mutation(child)
            new_population.append(mutated_child)
            
        self.population = new_population

    def evolve_one_generation(self):     # цикл евол
        self._create_next_generation()
        # оновлення найкращого рішення 
        current_best_tour = self.get_best_in_population()
        if self.best_solution is None or self._get_tour_distance(current_best_tour) < self._get_tour_distance(self.best_solution):
            self.best_solution = current_best_tour

    # вивід результатів 
    def get_best_in_population(self):
        pop_with_fitness = [(tour, self._calculate_fitness(tour)) for tour in self.population]
        return max(pop_with_fitness, key=lambda item: item[1])[0]
        
    # функція для обчислення матриці 
    def _compute_distance_matrix(self):
        num_cities = len(self.cities)
        matrix = [[0.0] * num_cities for _ in range(num_cities)]
        for i in range(num_cities):
            for j in range(i, num_cities):
                dist = math.sqrt(
                    (self.cities[i][0] - self.cities[j][0])**2 +
                    (self.cities[i][1] - self.cities[j][1])**2
                )
                matrix[i][j] = matrix[j][i] = dist
        return matrix
