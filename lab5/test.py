import unittest
import math
from unittest.mock import patch
from genetic_steps import TSPSolver

class TestGeneticSteps(unittest.TestCase):

    def setUp(self):
        self.cities = [(0, 0), (10, 0), (10, 10), (0, 10)] 
        self.solver = TSPSolver(self.cities, population_size=10, mutation_rate=0.1, elitism_count=1)

    def test_tour_distance_calculation(self):
        tour = [0, 1, 2, 3]
        distance = self.solver._get_tour_distance(tour)
        self.assertAlmostEqual(distance, 40.0, msg="Дистанція для простого квадрату має бути 40")

    def test_fitness_calculation(self):
        """ТЕСТ Обчислення якості """
        tour = [0, 1, 2, 3] 
        fitness = self.solver._calculate_fitness(tour)
        self.assertAlmostEqual(fitness, 1.0 / 40.0, msg="Fitness має бути 1 / дистанція")

    def test_parent_selection(self):
        """ТЕСТ Вибір батьків """
        best_tour = [0, 1, 2, 3] 
        worst_tour = [0, 2, 1, 3]
        population = [worst_tour] * 9 + [best_tour]
        pop_with_fitness = [(tour, self.solver._calculate_fitness(tour)) for tour in population]
        
        selected_parent = self.solver._tournament_selection(pop_with_fitness, tournament_size=10)
        self.assertEqual(selected_parent, best_tour, "Турнірний відбір має знайти найкращу особину")

    @patch('random.sample', return_value=[1, 2]) 
    def test_ordered_crossover(self, mock_sample):
        """ТЕСТ Створення нащадків """
        parent1 = [0, 1, 2, 3, 4, 5]
        parent2 = [5, 4, 3, 2, 1, 0]
        child = self.solver._ordered_crossover(parent1, parent2)
        expected_child = [5, 1, 2, 4, 3, 0]
        self.assertEqual(child, expected_child, "Результат впорядкованого кросоверу невірний")

    @patch('random.random', return_value=0.05) 
    @patch('random.sample', return_value=[1, 3]) 
    def test_swap_mutation(self, mock_indices, mock_random):
        tour = [0, 1, 2, 3, 4]
        self.solver.mutation_rate = 0.1
        mutated_tour = self.solver._swap_mutation(list(tour)) 
        expected_tour = [0, 3, 2, 1, 4]
        self.assertEqual(mutated_tour, expected_tour, "Swap-мутація не спрацювала, як очікувалося")

    def test_elitism_selection(self):
        """ТЕСТ Вибір для наступної популяції """
        best_tour = [0, 1, 2, 3] 
        worst_tour = [0, 2, 1, 3] 
        self.solver.population = [worst_tour] * 9 + [best_tour]
        
        self.solver._create_next_generation()
        
        self.assertIn(best_tour, self.solver.population, "Найкраща особина має бути збережена завдяки елітизму")

    def test_get_best_result(self):
        """ТЕСТ Вивід результатів """
        best_tour = [0, 1, 2, 3]
        worst_tour = [0, 2, 1, 3]
        self.solver.population = [worst_tour] * 5 + [best_tour] * 5
        
        found_best = self.solver.get_best_in_population()
        self.assertEqual(found_best, best_tour, "Метод  має повертати найкращу особину")


if __name__ == '__main__':
    unittest.main()
