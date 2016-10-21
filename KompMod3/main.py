import standart_algorithm_with_rec as std_alg
import puasson

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

arr401 = [std_alg.Diskret_Number(s, p) for x in range(40)]
arr402 = [puasson.Puasson(40, 20) for x in range(40)]

binom_probs = [std_alg.binom_negative(s, p, arr401[i]) for i in range (40)]
binom_probs.sort()

arr100 = [std_alg.Diskret_Number(s, p) for x in range(100)]

print (arr)