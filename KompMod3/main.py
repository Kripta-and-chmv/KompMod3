import random
from math import factorial as fact

def binom_negative(s, p, i, oper=0):
    oper += 13
    return fact(s + i - 1) / (fact(i) * fact(s - 1)) * p**s * (1 - p)**i

def Diskret_Number(s, p, oper=0):
    def r(s, p, i, oper):
        oper += 5
        return (s + i) * (1 - p) / (i + 1)

    operations = 0
    m = random.random()
    i = 0

    P = binom_negative(s, p, 0, operations)

    m_greater_than_zero = m > 0

    m -= P

    while m_greater_than_zero:
        P *= r(s, p, i, operations)
        i += 1
        m -= P
        m_greater_than_zero = m > 0
        operations += 4

    return i, operations


s = 4
p = 0.1

#binom_probs = [binom_negative(s, p, i) for i in range (100)]
#binom_probs.sort()

#i = 0
#while binom_probs[i] < 0.001:
#    i += 1
#intervals_amount = len(binom_probs) - i


ksi = Diskret_Number(s, p)

print(ksi)

arr40 = [Diskret_Number(s, p)[0] for x in range(40)]

binom_probs = [binom_negative(s, p, arr40[i]) for i in range (40)]
binom_probs.sort()

arr100 = [Diskret_Number(s, p) for x in range(100)]

print (arr)