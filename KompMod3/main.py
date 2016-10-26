import standart_algorithm_with_rec as std_alg
import poisson
import chi2
import scipy
import scipy.stats

s = 4
p = 0.1
lambd = 20

binom_probs = [binom_negative(s, p, i) for i in range (100)]

i = 0
while binom_probs[i] < 0.001:
    i += 1
intervals_amount = len(binom_probs) - i


ksi = std_alg.Diskret_Number(s, p)

print(ksi)

a = std_alg.Diskret_Number(s, p)

arr401 = [std_alg.Diskret_Number(s, p) for x in range(40)]
arr402 = [poisson.Puasson(40, lambd) for x in range(40)]

chi2.chisqr_test(arr402, 0.05, False, False)

arr100 = [std_alg.Diskret_Number(s, p) for x in range(100)]

print (arr)