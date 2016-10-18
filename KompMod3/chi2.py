def chisqr_test(sequence, mod, alpha, intervals_amount, drawing_graph, wfile):
    """Тест Хи-квадрат.
    Аргументы:
        sequence - выборка, list числовых значений;
        mod - размерность алфавита выборки, int;
        alpha - уровень значимости, float;
        intervals_amount - количество интервалов, int;
        drawing_graph - нужно ли рисовать гистограмму, bool;
        wfile - файл, куда записываются результаты теста, file.
    Вывод:
        hit and hit_a2 - успешность прохождения теста по двум критериям, bool.

    """
    def create_intervals(mod, intervals_amount):
        """Разбивает отрезок от 0 до mod на интервалы.
        Аргументы:
            mod - верхняя граница отрезка, число;
            intervals_amount - количество интервалов, int.
        Вывод:
            intervals - список с границами интервалов, list числовых значений.

        """
        intervals = []
        intervals.append(0)
        inter_length = mod / intervals_amount
        last_point = inter_length
        for i in range(intervals_amount - 1):
            intervals.append(last_point)
            last_point += inter_length
        intervals.append(mod)
        return intervals

    def calculate_hits_amount(intervals, sequence):
        """Вычисляется количество элементов выборки, попавших в каждый интервал.
        Аргументы:
            intervals - список границ интервалов, list;
            sequence - выборка, list числовых значений.
        Вывод:
            frequency - список количества попаданий для каждого интервала, list of int.

        """
        frequency = numpy.zeros(len(intervals) - 1)
        length = len(sequence)
        for i in range(length):
            for j in range(len(intervals) - 1):
                if (intervals[j] <= sequence[i] < intervals[j + 1]):
                    frequency[j] += 1

        return frequency

    def calculate_probability_intervals(intervals, a, b):
        """Вычисляется вероятность попадания слчайной величины в заданные
        интервалы при равномерном распределении.
        
        Аргументы:
            intervals - список границ интервалов, list;
            a - нижняя граница функции равномерного распределения;
            b - верхняя граница функции равномерного распределения.
        Вывод:
            probabil - список вероятностей для каждого интервала, list of float.

        """
        probabil = []
        for i in range(len(intervals) - 1):
            probabil.append((intervals[i + 1] - intervals[i]) / (b - a))
        return probabil

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

    intervals = create_intervals(mod, intervals_amount)
    hits_amount = calculate_hits_amount(intervals, sequence)

    probabil = calculate_probability_intervals(intervals, 0, mod)

    if(drawing_graph is True):
        draw_histogram(hits_amount, intervals)

    # вычисляется статистика
    addition = 0
    for i in range(intervals_amount):
        addition += (hits_amount[i] / len(sequence) -
                     probabil[i]) ** 2 / probabil[i]
    S = len(sequence) * addition

    # вычисляется a2
    r = 5
    def integrand(x, r):
        return x ** (r / 2 - 1) * sympy.exp(-x / 2)

    a2 = scipy.integrate.quad(integrand, S, numpy.inf, args = (r))
    a2 = a2[0] / 2 ** (r / 2) * math.gamma(int(r / 2))

    hit_a2 = a2 > alpha

    S_crit = 18.307

    hit = S <= S_crit

    writing_in_file(wfile, len(sequence), S, S_crit, hit, a2, hit_a2, intervals_amount)

    return hit and hit_a2
