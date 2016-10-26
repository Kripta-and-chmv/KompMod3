from IPython.display import display
import copy
import scipy
import sympy
import scipy.stats
import numpy
import mpmath
import random
import matplotlib.pyplot as plt
from collections import Counter
 
 
def get_prng(seed, a, c, modulus, N=1000):
    x = seed
    for i in range(0, N):
        x = (a * x ** 2 + c) % modulus
        yield x
 
 
def find_period(sequence):
    """c = Counter()
   for a in reversed(sequence):
       oldsz = len(c)
       c += Counter([a])
       if oldsz == len(c):
           return oldsz
       .
       : sequence - .
       : period -  .
 
       """
    #     
    #    3      
    length = len(sequence)
    a = list(reversed(sequence[length - 3: length]))
    for i in range(length - 4, -1, -1):
        if (a[0] == sequence[i]):
            if (i - 2 > -1):
                if (a[1] == sequence[i - 1] and a[2] == sequence[i - 2]):
                    #  ,
                    # .. i     
                    i += 1
                    #     
                    break
 
    period = length - i
    return period
 
 
def test1(sequence, alpha):
    def count_q(sequence):
        """  
           [2,1] -> 1
       """
        return [j < i for i, j in zip(sequence[:-1], sequence[1:])].count(True)
 
    U = scipy.stats.norm.ppf(1 - alpha / 2.0)
    delta = U * mpmath.sqrt(len(sequence)) / 2.0
 
    q = count_q(sequence)
    print(" : [%.3f,%.3f],  : %.3f" % (
    len(sequence) / 2 - delta, len(sequence) / 2 + delta, q))
    return numpy.abs(len(sequence) / 2 - q) <= delta
 
 
def test2(sequence, modulus, alpha, K, add_graph=True):
    n = len(sequence)
    intervals = numpy.resize(range(modulus), (K, int(modulus / K)))
    counts = [sum([list(interval).count(x) for x in sequence]) for interval in intervals]
    frequency = [c / len(sequence) for c in counts]
    print(": ", frequency)
    width = intervals[-1, -1] / n
 
    if add_graph:
        plt.bar(numpy.arange(0, modulus, modulus / K), frequency, width)
        plt.title('Frecuency Histogram')
        plt.xlabel('intervals')
        plt.ylabel('relative frequency')
        plt.xticks(numpy.arange(0, modulus, modulus / K))
        plt.show()
    seq_ = sequence
    sequence = numpy.array(sequence)
    mean = sequence.mean()
 
    U = scipy.stats.norm.ppf(1 - alpha / 2.0)
    delta_nu = U / K * mpmath.sqrt((K - 1) / n)
    print("   : ")
    nu_test_result = [numpy.abs(nu - 1 / K) <= delta_nu for nu in frequency].count(False) == 0
    for nu in frequency:
        print("[%.3f,%.3f]" % (nu - delta_nu, nu + delta_nu))
 
    print(": %.3f" % mean)
    variance = sequence.var()
    delta_mean = U * mpmath.sqrt(variance / n)
    print("   : [%.3f,%.3f]" % (mean - delta_mean, mean + delta_mean))
    mean_test_result = numpy.abs(mean - modulus / 2) <= delta_mean
 
    print(": %.3f" % variance)
    delta_var = (n - 1) * variance
    chi2_1 = scipy.stats.chi2.ppf(1 - alpha / 2.0, n - 1)
    chi2_2 = scipy.stats.chi2.ppf(alpha / 2.0, n - 1)
    var_test_result = delta_var / chi2_1 <= modulus ** 2 / 12 <= delta_var / chi2_2
    print("   : [%.3f,%.3f]" % (delta_var / chi2_1, delta_var / chi2_2))
 
    sequence = seq_
 
    return nu_test_result and mean_test_result and var_test_result
 
 
def test3(seq, mod, alpha, r, K, add_graph=True):
    t = int((len(seq) - 1) / r)
 
    sub_seqs = numpy.resize(seq, (t, r)).transpose()
 
    is_test1 = True
    is_test2 = True
 
    for sub_seq in sub_seqs:
        is_test1 = is_test1 if test1(sub_seq, alpha) else False
        is_test2 = is_test2 if test2(sub_seq, mod, alpha, K, add_graph) else False
 
    return is_test1 and is_test2
 
 
# In[49]:
 
def chisqr_test(sequence, mod, alpha, K, draw_graph=True):
    n = len(sequence)
    print(" -")
    intervals = numpy.resize(range(mod), (K, int(mod / K)))
    hits_amount = [sum([list(interval).count(x) for x in sequence]) for interval in intervals]
    frequency = [c / len(sequence) for c in hits_amount]
 
    probabil = [len(intervals[0]) / mod] * len(intervals)
    print("len(probabil): ", len(probabil))
    if (draw_graph is True):
        width = intervals[-1, -1] / n
        plt.bar(numpy.arange(0, mod, mod / K), frequency, width)
        plt.title('Chi2 Histogram')
        plt.xlabel('intervals')
        plt.ylabel('hits amount')
        plt.xticks(numpy.arange(0, mod, mod / K))
        plt.show()
 
    Ssum = 0
    for i in range(K):
        Ssum += (hits_amount[i] / len(sequence) -
                 probabil[i]) ** 2 / probabil[i]
    S = len(sequence) * Ssum
    print(": %.3f" % S)
    r = K - 1
    print(" : ", r)
 
    def integrand(x, r):
        return x ** (r / 2 - 1) * sympy.exp(-x / 2)
 
    a2 = scipy.integrate.quad(integrand, S, numpy.inf, args=(r))
    a2 = a2[0] / (2 ** (r / 2) * mpmath.gamma(r / 2))
    print("P(S > S*): %.3f" % a2)
 
    hit_a2 = a2 > 1 - alpha
 
    S_crit = scipy.stats.chi2.ppf(1 - alpha, r)  # 18.307-
    print(" : %.3f" % S_crit)
    hit = S <= S_crit
 
    return hit and hit_a2
 
 
# In[50]:
 
def anderson_test(sequence, mod):
    print(" ")
 
    def udf(x, a, b):
        """   """
        return 0 if x < a else (x - a) / (b - a) if x < b else 1
 
    ssequence = sorted(copy.copy(sequence))
 
    Ssum = 0
    length = len(sequence)
 
    for i in range(1, length + 1):
        F = udf(ssequence[i - 1], 0, mod)
        Ssum += (2 * i - 1) * mpmath.log(F) / (2 * length)
        Ssum += (1 - (2 * i - 1) / (2 * length)) * mpmath.log(1 - F)
 
    S = -length - 2 * Ssum
    print(": %.3f" % S)
    critical_value = 2.4924  # alpha 0.05
    print(" : %.3f" % critical_value)
 
    hit = S <= critical_value
 
    def integrand(x, S, j):
        return sympy.exp(S / (8 * (x ** 2 + 1)) - ((4 * j + 1) * mpmath.pi * x) ** 2 / (8 * S))
 
    def calculate_a2(S):
        j = 0
        return (mpmath.sqrt(2 * mpmath.pi) / S) * \
               scipy.sum((-1) ** j * (mpmath.gamma(j + 0.5) * (4 * j + 1)) / \
                         (mpmath.gamma(0.5) * mpmath.gamma(j + 1)) * \
                         sympy.exp(-((4 * j + 1) ** 2 * mpmath.pi ** 2) / (8 * S)) * \
                         scipy.integrate.quad(integrand, 0, numpy.inf, args=(S, j))[0], j)
 
    a2 = 1 - calculate_a2(S)
    print("P(S > S*): %.3f" % a2)
    a2_hit = a2 > 0.05
 
    return hit and a2_hit
 
 
# In[53]:
 
def generate_good_seq():
    count_ = 0
    maxP = 0
    while True:
        a = random.randrange(1, 1000)
        c = random.randrange(1, 1000)
        modulus = random.randrange(1, 1000)
        seed = random.randrange(1, 1000)
        count_ += 1
        prng = get_prng(seed, a, c, modulus)
        seq = [i for i in prng]
        P = find_period(seq)
        maxP = P if P > maxP else maxP
        if P >= 100:
            print("a = ", a)
            print("c = ", c)
            print("modulus = ", modulus)
            print("seed = ", seed)
            return (a, c, modulus, seed)
        if (count_ % 10000 == 0): print(maxP)
 
 
def test_seq(seq, mod, K2, K3, r3):
    print(": ", seq)
    seq40 = seq[-40:]
    seq100 = seq[-100:]
    P = find_period(seq)
    print(": ", P)
    test1_40 = test1(seq40, 0.05)
    print(" 1 40: ", test1_40)
    test1_100 = test1(seq100, 0.05)
    print(" 1 100: ", test1_100)
    test2_40 = test2(seq40, mod, 0.05, K2, False)
    print(" 2 40: ", test2_40)
    test2_100 = test2(seq100, mod, 0.05, K2, False)
    print(" 2 100: ", test2_100)
    test3_40 = test3(seq40, mod, 0.05, r3, K3, False)
    print(" 3 40: ", test3_40)
    test3_100 = test3(seq100, mod, 0.05, r3, K3, False)
    print(" 3 100: ", test3_100)
    chisqr = chisqr_test(seq[-P:], mod, 0.05, int(5 * mpmath.log10(P)), False)
    print(" -: ", chisqr)
    anderson = anderson_test(seq[-P:], mod)
    print(" : ", anderson)
    succ = test1_40 and test1_100 and test2_40 and test2_100 and test3_40 and test3_100 and anderson and chisqr
    print("   (95%): ", succ)
 
 
def main():
    # a,c,mod,seed=generate_good_seq()
    # a,c,mod,seed=257,510,841,147 #False
    a, c, mod, seed = 307, 211, 486, 763  # True
    seq = [i for i in get_prng(seed, a, c, mod)]
    test_seq(seq, mod, 16, 10, 4)
 
    seq = numpy.random.uniform(0, mod, 1000)
    test_seq(seq, mod, 16, 10, 4)
 
 
main()