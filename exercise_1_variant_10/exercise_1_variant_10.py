import json
import os
import numpy as np
import matplotlib.pyplot as plt

def f(x,A):
    return 0.5 + (np.cos(np.sin(x**2 - A**2))**2 - 0.5) / (1+0.001*(x**2 + A**2))

#параметры
A=1.25313
x_values = np.linspace(-100, 100, 800)

#расчёт координат
y_values = f(x_values, A)
data = [{"x": x, "y": y} for x, y in zip(x_values, y_values)]

'''
for x, y in zip(x_values, y_values):
    print(f"x: {x}, y: {y}")
'''

#cоздание директории
if not os.path.exists('results'):
    os.makedirs('results')

#сохранение в JSON
with open('results/function_values.json', 'w') as file:
    json.dump({"data": data}, file, indent=4)

#построение графика функции
plt.figure(figsize=(16, 9))
plt.plot(x_values, y_values, label='f(x)', color='blue')
plt.title('График функции f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
#plt.xscale('symlog')
plt.grid(True)
plt.legend()
#plt.savefig('results/function_plot.png')
plt.show()
