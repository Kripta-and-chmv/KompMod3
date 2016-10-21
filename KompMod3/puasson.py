import random
from math import factorial as fact
from math import exp


def CalculateProbabil(lamb, k):
    return lamb**k / fact(k) * exp(-lamb)

def Puasson(length, lamb):
    seq = [x for x in range(1, length+1)]

    Q = 0
    for i in range(0, lamb):
        Q += CalculateProbabil(lamb, seq[i])

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
