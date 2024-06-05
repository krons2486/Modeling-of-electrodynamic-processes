import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as pp

class FieldDisplay:
    def __init__(self, size_m, dx, ymin, ymax, probePos, sourcePos, dt):
        pp.ion()
        self.fig, self.ax = pp.subplots()
        self.line = self.ax.plot(np.arange(0, size_m, dx), [0]*int(size_m/dx))[0]
        self.ax.plot(probePos*dx, 0, 'xr')
        self.ax.plot(sourcePos*dx, 0, 'ok')
        self.ax.set_xlim(0, size_m)
        self.ax.set_ylim(ymin, ymax)
        self.ax.set_xlabel('x, м')
        self.ax.set_ylabel('Ez, В/м')
        self.probePos = probePos
        self.sourcePos = sourcePos
        self.dt = dt
        self.time_text = self.fig.text(0.5, 0.95, '', transform=self.fig.transFigure, ha='center')

    def update(self, data, t):
        self.line.set_ydata(data)
        time_str = '{:.5f}'.format(t * self.dt * 1e9)  # преобразуем время в наносекунды
        self.time_text.set_text(f'Время = {time_str} нс')  # выводим время над графиком
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

class Probe:
    def __init__(self, probePos, maxT, dt):
        self.maxT = maxT
        self.dt = dt
        self.probePos = probePos
        self.t = 0
        self.E = np.zeros(self.maxT)
    def add(self, data):
        self.E[self.t] = data[self.probePos]
        self.t += 1

    def showSpectrum(self):
        sp= fftshift(np.abs(fft(self.E)))
        df = 1/(self.maxT*self.dt)
        freq = np.arange(-self.maxT*df /2, self.maxT*df/2, df)
        fig, ax = pp.subplots()
        ax.plot(freq, sp/max(sp))
        ax.set_xlabel('f, Гц')
        ax.set_ylabel('|S|/|S|max')
        ax.set_xlim(0, 1e9)  # изменен диапазон для правильного отображения частотного пика
    
    def showSignal(self):
        fig, ax = pp.subplots()
        ax.plot(np.arange(0, self.maxT*self.dt, self.dt), self.E)
        ax.set_xlabel('t, c')
        ax.set_ylabel('Ez, В/м')
        ax.set_xlim(0, self.maxT*self.dt)

eps = 2.5  # относительная диэлектрическая проницаемость
W0 = 120*np.pi  # волновое сопротивление свободного пространства
Sc = 1  # число Куранта
maxT = 3000  # увеличенное максимальное количество временных шагов
size_m = 5.0  # размер области моделирования вдоль оси X
dx = size_m / 900  # пространственный шаг
maxSize = int(size_m / dx)
probePos = int(maxSize / 4)  # позиция датчика
sourcePos = int(maxSize / 2)  # позиция источника
dt = dx * np.sqrt(eps) * Sc / 3e8
probe = Probe(probePos, maxT, dt)
display = FieldDisplay(size_m, dx, -1, 1, probePos, sourcePos, dt)
Ez = np.zeros(maxSize)
Hy = np.zeros(maxSize)
Sc1 = Sc / np.sqrt(eps)
k1 = -1 / (1 / Sc1 + 2 + Sc1)
k2 = 1 / Sc1 - 2 + Sc1
k3 = 2 * (Sc1 - 1 / Sc1)
k4 = 4 * (1 / Sc1 + Sc1)
Ezq = np.zeros(3)
Ezq1 = np.zeros(3)
f = 0.5e9  # частота гармонического сигнала
omega = 2 * np.pi * f  # угловая скорость
A = 1  # амплитуда
phi = 0  # начальная фаза

for q in range(1, maxT):
    # Обновление Hy
    Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / W0
    # Обновление Ez
    Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * W0 / eps
    Ez[sourcePos] += A * np.sin(omega * q * dt + phi)
    Hy[0] = 0  # идеальный магнитный проводник (PMC)
    Ez[0] = Ez[1]
    # Правая граница (ABC)
    Ez[-1] = (k1 * (k2 * (Ez[-3] + Ezq1[-1]) + k3 * (Ezq[-1] + Ezq[-3] - Ez[-2] - Ezq1[-2]) - k4 * Ezq[-2]) - Ezq1[-3])
    # Обновление Ezq
    Ezq1[:] = Ezq[:]
    Ezq[:] = Ez[-3:]
    # Добавление данных в датчик
    probe.add(Ez)
    if q % 10 == 0:
        display.update(Ez, q)

pp.ioff()
probe.showSignal()
probe.showSpectrum()
pp.show()
