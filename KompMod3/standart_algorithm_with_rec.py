import random
from math import factorial as fact
import scipy
import scipy.stats

def Diskret_Number(s, p, oper=0):
    """Вычисление дискретного числа стандартным алкоритмом с рекуррентными формулами
    """
    def r(s, p, k, oper=0):
        oper += 5
        return (s + k) * (1 - p) / (k + 1)

    m = random.random()
    i = 0

    P = scipy.stats.nbinom.pmf(0, s, p)

    m -= P
    m_greater_than_zero = m > 0

    while m_greater_than_zero:
        P *= r(s, p, i, oper)
        i += 1
        m -= P
        m_greater_than_zero = m > 0
        oper += 4

    return i