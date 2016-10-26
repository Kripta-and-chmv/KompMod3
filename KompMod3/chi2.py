import numpy
import sympy
import scipy
import scipy.stats as st
import math
import collections


def chisqr_test(sequence, probs, interv_amount, alpha, drawing_graph, wfile):
    """Тест хи квадрат.
    Аргументы:
        sequence - выборка;
        probs - соответствия элемента и его вероятности, словарь;
        alpha - уровень значимости;
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

    hits_amount = collections.Counter()
    for i in sequence:
        hits_amount[i] += 1
            
    if drawing_graph is True:
        draw_histogram(hits_amount, intervals)

    len_seq = len(sequence)
    # вычисляется статистика
    addition = [(hit / len_seq - prob)**2 / prob for hit, prob in zip(hits_amount.values(), probs.values())]
    addition = sum(addition[:interv_amount])

    S = len_seq * addition

    # вычисляется S*
    r = 5
    def integrand(x, r):
        return x ** (r / 2 - 1) * sympy.exp(-x / 2)

    s_star = scipy.integrate.quad(integrand, S, numpy.inf, args = (r))
    s_star = s_star[0] / 2 ** (r / 2) * math.gamma(int(r / 2))

    hit_s_star = s_star > alpha

    S_crit = 18.307
    S_crit = scipy.stats.chi2.ppf(1 - 0.05, r)

    hit = S <= S_crit

    return hit and hit_a2
