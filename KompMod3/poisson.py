import random
from math import factorial as fact
from math import exp
import scipy
import scipy.stats as st

def calculate_interv_amount(sequence, lambd):
    count = 0
    for el in sequence:
        if distrib(el, lambd) >= 0.001:
            count += 1
    return count

def distrib(el, lambd):
    """пуассоновский закон распределения.
    Аргументы:
        el - вычисляется вроятность этого числа;
        lambd - параметры
    """
    return st.poisson.pmf(el, lambd)

def nonstandart_alg(p_pois, lamb):   
    """Вычисление дискретного числа стандартным алкоритмом с рекуррентными формулами
    """
    
    oper = 0

    Q = sum(p_pois[:lamb + 1])
    oper += lamb

    number = 0

    p = random.random()
    p -= Q

    oper += 2

    if p >= 0:
        k = lamb + 1
        while p >= 0:
            p -= p_pois[k]
            k += 1
            oper += 3
        number = k - 1
        oper += 2

    else:
        k = lamb
        while p < 0:
            p += p_pois[k]
            k -= 1
            oper += 3
        number = k + 1
        oper += 1
    oper += 1

    return number, oper
