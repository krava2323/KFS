import unittest
import numpy as np
from scipy.integrate import odeint

# Імпортуємо функції з нашої моделі

SIGMA = 10
RHO = 28
BETA = 8/3

def lorenz_system(state, t):
    x, y, z = state
    dx_dt = SIGMA * (y - x)
    dy_dt = x * (RHO - z) - y
    dz_dt = x * y - BETA * z
    return [dx_dt, dy_dt, dz_dt]

def run_lorenz_simulation(initial_state, total_time=1.0, num_steps=100):
    t = np.linspace(0, total_time, num_steps)
    solution = odeint(lorenz_system, initial_state, t)
    return t, solution


class TestLorenzAttractor(unittest.TestCase):

    def test_lorenz_system_derivative_calculation(self):
       
        # Перевірка в  точці
        state = [1.0, 2.0, 3.0]
       
        expected_derivatives = [10.0, 23.0, -6.0]
        calculated_derivatives = lorenz_system(state, 0)
        self.assertAlmostEqual(calculated_derivatives[0], expected_derivatives[0], places=5)
        self.assertAlmostEqual(calculated_derivatives[1], expected_derivatives[1], places=5)
        self.assertAlmostEqual(calculated_derivatives[2], expected_derivatives[2], places=5)
        print("Тест: обчислення похідних пройшов успішно.")

    def test_run_lorenz_simulation_output_shape(self):
        
        initial_state = [0.0, 1.0, 1.0]
        total_time = 1.0
        num_steps = 100
        t, sol = run_lorenz_simulation(initial_state, total_time, num_steps)

        self.assertEqual(len(t), num_steps) # Кількість часових точок
        self.assertEqual(sol.shape, (num_steps, 3))
        print("Тест: форма вихідних даних симуляції пройшов успішно.")

    def test_run_lorenz_simulation_initial_condition(self):
        
        initial_state = [10.0, 20.0, 30.0]
        t, sol = run_lorenz_simulation(initial_state)
        # Перевіряємо чи перша точка рішення відповідає початковим умовам
        np.testing.assert_array_almost_equal(sol[0], initial_state, decimal=5)
        print("Тест: початкові умови симуляції пройшов успішно.")

    def test_lorenz_attractor_sensitivity(self):
        
        initial_state_1 = [0.0, 1.0, 1.0]
        initial_state_2 = [0.0, 1.0 + 1e-7, 1.0]
        total_time = 30 
        num_steps = 3000 
        
        t1, sol1 = run_lorenz_simulation(initial_state_1, total_time, num_steps)
        t2, sol2 = run_lorenz_simulation(initial_state_2, total_time, num_steps)

        initial_diff = np.max(np.abs(sol1[0] - sol2[0]))
        self.assertLess(initial_diff, 1e-6) 
        final_diff = np.max(np.abs(sol1[-1] - sol2[-1]))
        self.assertGreater(final_diff, 1.0)
        print("Тест початкових умов пройшов успішно.")


# Запуск тестів
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
