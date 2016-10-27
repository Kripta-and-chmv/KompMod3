import random
from math import factorial as fact
import scipy
import scipy.stats as st


def calculate_interv_amount(sequence, s, p):
    count = 0
    for el in sequence:
        if distrib(el, s, p) >= 0.001:
            count += 1
    return count

def distrib(el, s, p):
    """отрицательный биномаиальный закон распределения.
    Аргументы:
        el - вычисляется вроятность этого числа;
        s, p - параметры
    """
    return st.nbinom.pmf(el, s, p)

def diskret_number(s, p):
    """Вычисление дискретного числа стандартным алкоритмом с рекуррентными формулами
    """
    def r(s, p, k):
        return (s + k) * (1 - p) / (k + 1)
    
    oper = 0

    m = random.random()
    i = 0

    P = distrib(0, s, p)

    oper += 2 * s - 1

    m -= P

    oper += 2

    while m > 0:
        P *= r(s, p, i)
        i += 1
        m -= P
        oper += 9

    oper +=1

    return i, oper