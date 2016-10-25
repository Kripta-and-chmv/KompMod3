import standart_algorithm_with_rec as std_alg
import poisson
import chi2
import scipy
import scipy.stats

s = 4
p = 0.1

#binom_probs = [binom_negative(s, p, i) for i in range (100)]
#binom_probs.sort()

#i = 0
#while binom_probs[i] < 0.001:
#    i += 1
#intervals_amount = len(binom_probs) - i


ksi = std_alg.Diskret_Number(s, p)

print(ksi)

a = std_alg.Diskret_Number(s, p)

arr401 = [std_alg.Diskret_Number(s, p) for x in range(40)]
arr401.sort()
arr402 = [poisson.Puasson(40, 20) for x in range(40)]
arr402.sort()

binom_probs = [scipy.stats.nbinom.pmf(arr401[i], s, p) for i in range (40)]
sm = sum(binom_probs)

chi2.chisqr_test(arr401, max(arr401), 0.05,  20, False, False)

arr100 = [std_alg.Diskret_Number(s, p) for x in range(100)]

print (arr)