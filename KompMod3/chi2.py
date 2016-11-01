import numpy
import sympy
import scipy
import scipy.stats as st
import math
import collections
import matplotlib.pyplot as plt
import random
import scipy.special
import scipy.integrate as integrate
import numpy.random


def chisqr_test(sequence, seq_probs, teor_probs, interv_amount, alpha, is_graph):
    """Тест хи квадрат.
    Аргументы:
        sequence - выборка;
        seq_probs - соответствия элемента и его вероятности, словарь;
        alpha - уровень значимости;
        """
    def draw_histogram(hits, points, teor_probs, seq):
        """Рисует гистограмму частот.
        Аргументы:
            hits - количество попаданий в точки, list;
            points - точки, list;
            teor_probs - теоретические вероятности.
        """
        # ширина стобца
        width = 0.5
        h = [x / len(seq) for x in hits]

        plt.bar(points[:len(points) - 1], h, width)

        plt.plot(teor_probs, 'r')
        plt.title('Chi2 Histogram')
        plt.xlabel('points')
        plt.ylabel('hits amount')
        plt.xticks(points)
        plt.show()

    print("количество элементов с вероятностью больше 0.001 - {}".format(interv_amount))

    hits_amount = collections.Counter()
    for i in sequence:
        hits_amount[i] += 1
    interv_amount = len(hits_amount)

    points = [0]
    points.extend(hits_amount.keys())
    points.sort()

    if is_graph is True:
        draw_histogram(hits_amount.values(), points, teor_probs, sequence)

    len_seq = len(sequence)
    # вычисляется статистика
    addition = [(hit / len_seq - prob)**2 / prob for hit, prob in zip(hits_amount.values(), seq_probs.values())]
    addition = sum(addition[:interv_amount])

    s_star = len_seq * addition
    print("значение статистики - {}".format(s_star))

    # вычисляется P(S>S*)
    r = interv_amount - 1
    def integrand(x, r):
        return x ** (r / 2 - 1) * sympy.exp(-x / 2)
    #def calculate_a2(S, r):
    #    x = sympy.symbols('x')
    #    f = x ** (r / 2 - 1) * sympy.exp(-x / 2)
    #    a2 = sympy.integrate(f, (x, S, sympy.oo)).doit().evalf()
    #    return numpy.abs(a2 / (2 ** (r / 2.) * scipy.special.gamma(r / 2.)))

    #prob_s = calculate_a2(s_star, r)

    prob_s = scipy.integrate.quad(integrand, s_star, numpy.inf, args = (r))
    prob_s = prob_s[0] / (2 ** (r / 2) * scipy.special.gamma(r / 2))
    
    print("P(S>S*) - {}".format(prob_s))
    hit_s_star = prob_s > alpha
    
    s_crit = scipy.stats.chi2.ppf(1 - 0.05, r)

    print("критическое значение статистики - {}".format(s_crit))

    hit = s_star <= s_crit

    print("прохождение теста хи квадрат сравнением с alpha: {}".format(hit_s_star))
    print("прохождение теста хи квадрат сравнением с критическим значением: {}\n".format(hit))

    return hit and hit_s_star
