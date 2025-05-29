import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#   Задаємо параметри атрактора Л
SIGMA = 10
RHO = 28
BETA = 8/3

def lorenz_system(state, t):
  
    x, y, z = state
    dx_dt = SIGMA * (y - x)
    dy_dt = x * (RHO - z) - y
    dz_dt = x * y - BETA * z
    return [dx_dt, dy_dt, dz_dt]

def run_lorenz_simulation(initial_state, total_time=50, num_steps=5000): # Запускаємо атрактор
    
    t = np.linspace(0, total_time, num_steps)
    # Використовуємо odeint для  розв'язання диференціальних рівнянь
    solution = odeint(lorenz_system, initial_state, t)
    return t, solution



# Початкові умови для першої симуляції 
initial_state_1 = [0.0, 1.0, 1.05]

# Початкові умови для другої симуляції 
initial_state_2 = [0.0, 1.0 + 0.00001, 1.05]

print(f"Початкові умови 1: {initial_state_1}")
print(f"Початкові умови 2: {initial_state_2}")
print("-" * 30)

# Запускаємо симуляції
t, sol1 = run_lorenz_simulation(initial_state_1)
_, sol2 = run_lorenz_simulation(initial_state_2)

# Побудова графіків
fig = plt.figure(figsize=(14, 10))

# Графік X1
ax1 = fig.add_subplot(3, 1, 1)
ax1.plot(t, sol1[:, 0], label='Траєкторія 1 (базова)', color='blue')
ax1.plot(t, sol2[:, 0], label='Траєкторія 2 (з похибкою)', color='red', linestyle='--')
ax1.set_xlabel('Час')
ax1.set_ylabel('X')
ax1.set_title('Порівняння X-координат з часом')
ax1.legend()
ax1.grid(True)

# Графік різниці X2
ax2 = fig.add_subplot(3, 1, 2)
difference_x = np.abs(sol1[:, 0] - sol2[:, 0])
ax2.plot(t, difference_x, color='green')
ax2.set_xlabel('Час')
ax2.set_ylabel('Абсолютна різниця |X1 - X2|')
ax2.set_title('Наростання різниці між X-координатами')
ax2.grid(True)
ax2.set_yscale('log') 

# 3D графік 
ax3 = fig.add_subplot(3, 1, 3, projection='3d')
ax3.plot(sol1[:, 0], sol1[:, 1], sol1[:, 2], label='Траєкторія 1 ', color='blue', alpha=0.7)
ax3.plot(sol2[:, 0], sol2[:, 1], sol2[:, 2], label='Траєкторія 2 ', color='red', alpha=0.7, linestyle='--')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('3D-візуалізація траєкторій атрактора Лоренца')
ax3.legend()

plt.tight_layout()
plt.show()

# Розрахунок точки де різниця стає суттєхвою
threshold = 1.0 
divergence_time_idx = np.argmax(difference_x > threshold)
if divergence_time_idx > 0:
    print(f"Час, коли абсолютна різниця по X перевищує {threshold}: {t[divergence_time_idx]:.2f} одиниць часу.")
else:
    print(f"Різниця по X не досягла {threshold} за весь час симуляції.")
