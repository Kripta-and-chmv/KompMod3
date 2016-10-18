import random
from math import factorial as fact
from math import exp


def CalculateProbabil(lamb, k):
    return lamb**k / fact(k) * exp(-lamb)

def Puasson(seq, n, lamb):
    Q = 0
    for i in range(1, lamb+1):
        Q += CalculateProbabil(lamb, i)

    number = 0

    p = random.random()
    p0 = p - Q

    if p0 >= 0:
        i = lamb
        while p0 >= 0:
            p0 -= seq[i]
            i += 1
        number = i

    else:
        i = lamb - 1
        while p0 < 0:
            p0 += seq[i]
            i -= 1
        number = i
    return number
