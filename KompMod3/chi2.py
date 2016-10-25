import numpy
import scipy
import math

def chisqr_test(sequence, mod, alpha, intervals_amount, drawing_graph, wfile):
    """Тест Хи-квадрат.
    Аргументы:
        sequence - выборка, list числовых значений;
        mod - размерность алфавита выборки, int;
        alpha - уровень значимости, double;
        intervals_amount - количество интервалов, int;
        drawing_graph - нужно ли рисовать гистограмму, bool;
        wfile - файл, куда записываются результаты теста, file.
    Вывод:
        hit and hit_a2 - успешность прохождения теста по двум критериям, bool.

    """
    def draw_histogram(frequency, intervals):
        """Рисует гистограмму частот.
        Аргументы:
            frequency - частота попаданий в интервалы, int;
            intervals - списо границ интервалов, list.
        """

        # ширина стобца - размер алфавита делаится на количество интервалов
        width = intervals[len(intervals) - 1] / (len(intervals) - 1)

        plt.bar(intervals[:len(intervals) - 1], frequency, width)
        plt.title('Chi2 Histogram')
        plt.xlabel('intervals')
        plt.ylabel('hits amount')
        plt.xticks(intervals)
        plt.show()

    def writing_in_file(wfile, length, S, Scrit, hit, a2, hit_a2, interv_amount):
        """Запись результатов в файл    
        Аргументы:
            wfile - файл, куда происходит запись, file;
            length - длина выборки, int;
            S - вычисленное значение статистики, float;
            Scrit - критическе значение статистики;
            hit - успешность прохождения теста по критерию сравнения с крит. значением, bool;
            a2 - a2, float;
            hit_a2 - успешность прохождения теста по критерию a2, bool;
            interv_amount - количество интервалов, int.

        """
        wfile.write(
            '============================== Тест Хи квадрат '
            '==============================\n\n')
        wfile.write('Количество интервалов: %s\n\n' % (interv_amount))
        wfile.write('Успешность прохождения по Sкрит: %s\n' % (hit))
        wfile.write('Значение статистики: %s\n' % (S))
        wfile.write('Критическое значение: %s\n\n' % (Scrit))
        wfile.write('Успешность прохождения по a2: %s\n' % (hit_a2))
        wfile.write('Значение a2: %s\n' % (a2))

    # разбиваем отрезок от 0 до mod на интервалы
    K = intervals_amount
    lngth = mod/K   
    intervals = [x * lngth for x in range(0, K+1)]
    
    #определяем количество попаданий в интервалы
    hits_amount = []    
    for a, b in zip(intervals[:-1], intervals[1:]):
            count = sum([a <= x < b for x in sequence])
            hits_amount.append(count)
    #определяем частоту попаданий
    len_seq = len(sequence)
    frequency = [c / len_seq for c in hits_amount]

    # Вычисляется вероятность попадания слчайной величины в заданные
    # интервалы при равномерном распределении.
    def calc_prob(top, bott, intervals):
        return [(x - y) / (top - bott) for x, y in zip(intervals[1:], intervals[:-1])]

    probabils = calc_probs(0, mod, intervals)


    if drawing_graph is True:
        draw_histogram(hits_amount, intervals)

    # вычисляется статистика
    addition = sum([(hits / len_seq - probs)**2 / probs for hits, probs in zip(hits_amount, probabils)])

    S = len_seq * addition

    # вычисляется S*
    r = 5
    def integrand(x, r):
        return x ** (r / 2 - 1) * sympy.exp(-x / 2)

    star = scipy.integrate.quad(integrand, S, numpy.inf, args = (r))
    star = star[0] / 2 ** (r / 2) * math.gamma(int(r / 2))

    hit_a2 = a2 > alpha

    S_crit = 18.307

    hit = S <= S_crit

    writing_in_file(wfile, len(sequence), S, S_crit, hit, a2, hit_a2, intervals_amount)

    return hit and hit_a2
