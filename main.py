from module import *
from matplotlib import pylab as pl 

# Коэффициенты усиления
k2=-0.1
k1=float(input('Введите коэффициент усиления 1: '))
k3=float(input('Введите коэффициент усиления 3: '))

# Постоянные времени
t1, t2, t3, t4, t5 = 0.134, 0.0303, 0.0616, 0.134, 0.15

# Векторы входного и выходного сигнала
x = [0]*3 + [1]*997
y = []

# Начальные нулевые условия
v2, damp_prev_in, damp_prev_out, ampl2_out, inert1_prev, inert2_prev, diff_prev_in, diff_prev_out, integrator_prev = 0, 0, 0, 0, 0, 0, 0, 0, 0

# Формирование выходных значений
for i in range(len(x)):
  sum1_out = summator(x[i], v2)
  ampl1_out = amplifier(sum1_out, k1)
  dampfer_out = dampfer(ampl1_out, damp_prev_in, damp_prev_out, t1, t2)
  damp_prev_out = dampfer_out # Предыдущий выход
  damp_prev_in = ampl1_out # Предыдущий вход
  sum2_out = summator(dampfer_out, ampl2_out)
  inert1_out = inertional(sum2_out, inert1_prev, t3)
  inert1_prev = inert1_out # Предыдущий выход
  diff_out = real_differential(inert1_out, diff_prev_in, diff_prev_out, t4)
  diff_prev_in = inert1_out # Предыдущий вход
  diff_prev_out = diff_out # Предыдущий выход
  ampl2_out = amplifier(diff_out, k2)
  inert2_out = inertional(inert1_out, inert2_prev, t5)
  inert2_prev = inert2_out # Предыдущий выход
  integrator_out = integrator(inert2_out, integrator_prev)
  integrator_prev = integrator_out # Предыдущий выход
  v2 = amplifier(integrator_out, k3) 
  y.append(integrator_out)

# Формирование временных промежутков
quantum = 0.8
x_time = []
for i in range(len(x)):
  x_time.append(i*quantum)

# Запись в файл
file = open('output.txt', 'a')
file.write('{:^7}{:^7}{:^7}\n'.format('delta', 'X', 'Y'))
for i in range(len(x)):
  file.write('{:^7.4}{:^7}{:^7.4}\n'.format(x_time[i], x[i], y[i]))
file.close()

# Формирование графика
pl.plot(x_time, y)
pl.title('Выходной сигнал')
pl.xlabel('Время')
pl.ylabel('Выход')
pl.grid()
pl.show()
