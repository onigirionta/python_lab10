from module import *
from matplotlib import pylab as pl
import os
import time


# Функция формирования выходного сигнала
def out_signal(xs, k1, k2, k3):
    # Постоянные времени
    t1, t2, t3, t4, t5 = 0.134, 0.0303, 0.0616, 0.134, 0.15
    
    # Начальные нулевые условия
    v2 = 0
    damp_prev_in = 0
    damp_prev_out = 0
    ampl2_out = 0
    inert1_prev = 0
    inert2_prev = 0 
    diff_prev_in = 0
    diff_prev_out = 0
    integrator_prev = 0

    ys = []
    # Формирование выходного сигнала
    for i in range(len(xs)):
      sum1_out = summator(xs[i], v2)
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
      ys.append(integrator_out)
    return ys

# Функция проверки устойчивости
def control(ys):
    ref = ys[-1]
    for i in range(5):
            if round(ref, 5) != round(ys[-(i+1)], 5):
                conclusion = 'Неустойчивая система'
                break
            else:
               conclusion = 'Устойчивая система'
    return conclusion

# Функция формирования графика
def response_plot(xs, ys, k1, k3, name, mode):
    stability = control(y)
    pl.plot(xs, ys)
    format_str = 'Выходной сигнал при k1 = {} и k3 = {}\n{}'.format(k1, k3, stability)
    pl.title(format_str)
    pl.xlabel('Время')
    pl.ylabel('Выход')
    pl.grid()
    fig = pl.gcf()
    fig.savefig(name, format='png')
    if mode == 'show':
        pl.show()
    pl.clf()

# Функция записи в файл
def record_in_file(filename, deltas, xs, ys):
    file = open(filename, 'w')
    file.write('{:^7}{:^7}{:^7}\n'.format('delta', 'X', 'Y'))
    for i in range(len(xs)):
      file.write('{:^7.4}{:^7}{:^7.4}\n'.format(deltas[i], xs[i], ys[i]))
    file.close()

# Основная часть программы

# Коэффициенты усиления
k2 = -0.1
k1 = float(input('Введите коэффициент усиления 1: '))
k3 = float(input('Введите коэффициент усиления 3: '))

# Формирование выходного сигнала
x = [0]*3 + [1]*9997 

# Формирование отклика системы
y = out_signal(x, k1, k2, k3)

# Формирование временных промежутков
delta = 0.8
x_time = []
for i in range(len(x)):
  x_time.append(i*delta)

# Запись в файл
filename = input('Введите имя файла для записи отчета в формате \"*имя*.txt\": ')
record_in_file(filename, x_time, x, y)

# График
mode = 'show'
plotname = 'Plot_k1={}_k3={}.png'.format(k1, k3)
response_plot(x_time, y, k1, k3, plotname, mode) 

# Исследование областей

# Формирование области исследования
k1_list = list(range(-1, 2, 1))
k3_list = list(range(-1, 2, 1))

# Создание и переход в рабочую папку
dir_name = input('Введите имя папки для складывания результатов: ')
os.mkdir(dir_name)
os.chdir(dir_name)

mode = 'not show'
for k1 in k1_list:
    for k3 in k3_list:
        y = out_signal(x, k1, k2, k3)
        filename = 'Output_k1={}_k3={}.txt'.format(k1, k3)
        plotname = 'Plot_k1={}_k3={}.png'.format(k1, k3)
        record_in_file(filename, x_time, x, y)
        response_plot(x_time, y, k1, k3, plotname, mode)
        
        


