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

def diskret_number(s, p, oper=0):
    """Вычисление дискретного числа стандартным алкоритмом с рекуррентными формулами
    """
    def r(s, p, k, oper=0):
        oper += 5
        return (s + k) * (1 - p) / (k + 1)

    m = random.random()
    i = 0

    P = distrib(0, s, p)

    m -= P
    m_greater_than_zero = m > 0

    while m_greater_than_zero:
        P *= r(s, p, i, oper)
        i += 1
        m -= P
        m_greater_than_zero = m > 0
        oper += 4

    return i