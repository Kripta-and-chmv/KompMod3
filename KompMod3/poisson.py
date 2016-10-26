import random
from math import factorial as fact
from math import exp
import scipy
import scipy.stats as st


def Puasson(length, lamb):    
    
    seq = [x for x in range(length)]

    p_pois = [st.poisson.pmf(el, lamb) for el in seq]

    Q = sum(p_pois[:lamb + 1])

    number = 0

    p = random.random()
    p -= Q

    if p >= 0:
        k = lamb + 1
        while p >= 0:
            p -= p_pois[k]
            k += 1
        number = k

    else:
        k = lamb
        while p < 0:
            p += p_pois[k]
            k -= 1
        number = k
    return number
