import standart_algorithm_with_rec as std_alg
import poisson
import chi2
import scipy
import scipy.stats

def tests_for_binom_neg(s, p, alpha):
    # генерация выборки стандартным алгоритмом с реккур формулами
    arr_binom_neg40 = [std_alg.diskret_number(s, p) for x in range(40)]
    # сопоставление каждого значения с вероятностью его получения по
    # отрицательному биномиальному закону распределения
    binom_neg_prob = {}
    for el in arr_binom_neg40:    
        binom_neg_prob[el] = std_alg.distrib(el, s, p)
    #  подсчитывается кол-во элементов, вероятность которых больше 0.001
    binom_neg_count = std_alg.calculate_interv_amount(arr_binom_neg40, s, p)    

    return chi2.chisqr_test(arr_binom_neg40, binom_neg_prob, binom_neg_count, alpha, True)

def tests_for_poisson(lambd, alpha):
    # генерация выборки нестандартным алгоритмом пуассона
    arr_pois40 = [poisson.nonstandart_alg(40, lambd) for x in range(40)]
    # сопоставление каждого значения с вероятностью его получения по
    # пауссоновскому закону распределения
    pois_prob = {}
    for el in arr_pois40:    
        pois_prob[el] = poisson.distrib(el, lambd)
    #подсчитывается кол-во элементов, вероятность которых больше 0.001
    poisson_count = poisson.calculate_interv_amount(arr_pois40, lambd)

    return chi2.chisqr_test(arr_pois40, pois_prob, poisson_count, alpha, True)

def main():    
    s = 4
    p = 0.1
    alpha = 0.05
    lambd = 20

    tests_for_binom_neg(s, p, alpha)
    tests_for_poisson(lambd, alpha)

main()