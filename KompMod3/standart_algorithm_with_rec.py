import random
from math import factorial as fact
import scipy
import scipy.misc

def binom_negative(s, p, k, oper=0):
    """Отрицательный биномиальный закон распределения с параметрами s и p.
    Аргументы:
        k - число, вероятность которого находим, int;
        s, p - параметры закона распределения, int.
    Вывод:
        вероятность выпадения числа k, double.
    """
    oper += 13
    return scipy.misc.comb(s, k, True, True) * p**s * (1 - p)**k
    #return fact(s + k - 1) / (fact(k) * fact(s - 1)) * p**s * (1 - p)**k

def Diskret_Number(s, p, oper=0):
    """Вычисление дискретного числа стандартным алкоритмом с рекуррентными формулами
    """
    def r(s, p, k, oper=0):
        oper += 5
        return (s + k) * (1 - p) / (k + 1)

    m = random.random()
    i = 0

    P = binom_negative(s, p, 0, oper)

    m -= P
    m_greater_than_zero = m > 0

    while m_greater_than_zero:
        P *= r(s, p, i, oper)
        i += 1
        m -= P
        m_greater_than_zero = m > 0
        oper += 4

    return i