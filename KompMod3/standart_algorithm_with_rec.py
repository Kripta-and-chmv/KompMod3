import random
from math import factorial as fact

def binom_negative(s, p, k, oper=0):
    oper += 13
    return fact(s + k - 1) / (fact(k) * fact(s - 1)) * p**s * (1 - p)**k

def Diskret_Number(s, p, oper=0):
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