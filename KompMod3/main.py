import scipy
import random
from math import factorial as fact

def Diskret_Number(s, p):
    def r(s, p, i, oper):
        oper = oper + 5
        return (s + i) * (1 - p) / (i + 1)

    def binom_negative(s, p, i):
        oper = oper + 13
        return fact(s + i - 1) / (fact(i) * fact(s - 1)) * p**s * (1 - p)**i

    operations = 0
    m = random.random()
    operations = operations + 1
    i = 0
    

    P = binom_negative(s, p, 0, operations)

    m_greater_than_zero = m > 0

    while m_greater_than_zero:
        m = m - P
        P = P * r(s, p, i, operations)
        m_greater_than_zero = m > 0
        i = i + 1
        operarions = operations + 4

    return i, operations

s = 4
p = 0.1

ksi = Diskret_Number(s, p)

print(ksi)

arr40 = [Diskret_Number(s, p) for x in range(40)]

arr100 = [Diskret_Number(s, p) for x in range(100)]

print (arr)