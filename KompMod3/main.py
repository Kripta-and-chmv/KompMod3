import standart_algorithm_with_rec as std_alg
import poisson
import chi2
import scipy
import scipy.stats
import sys

def tests_for_binom_neg(s, p, alpha, length):
    # генерация выборки стандартным алгоритмом с реккур формулами
    oper = 0
    arr_binom_neg = []
    for x in range(length):
        number, one_oper = std_alg.diskret_number(s, p)
        arr_binom_neg.append(number)
        oper += one_oper

    with open("binom_neg.txt", "w") as f:
        f.write(str(arr_binom_neg))
    # сопоставление каждого значения с вероятностью его получения по
    # отрицательному биномиальному закону распределения
    binom_neg_prob = {}
    for el in arr_binom_neg:    
        binom_neg_prob[el] = std_alg.distrib(el, s, p)
    #  подсчитывается кол-во элементов, вероятность которых больше 0.001
    binom_neg_count = std_alg.calculate_interv_amount(arr_binom_neg, s, p)

    factor = 100
    binom_neg_teor_probs = [std_alg.distrib(x, s, p) * factor for x in range(max(arr_binom_neg))]
    print("Отрицательное биномиальное распределение:\n\ts - {}\n\tp - {}\n\tуровень значимости - {}\n\t"
          "длина последовательности - {}\n\tколичество операций - {}\n".format(s, p, alpha, length, oper))
    chi2.chisqr_test(arr_binom_neg, binom_neg_prob, binom_neg_teor_probs, binom_neg_count, alpha, True)
    

def tests_for_poisson(lambd, alpha, length):
    # генерация выборки нестандартным алгоритмом пуассона
    oper = 0
    arr_pois = []
    p_pois = []
    for x in range(length):
        p = poisson.distrib(x, lambd)
        p_pois.append(p)
        oper += 2 + x

    for x in range(length):
        number, one_oper = poisson.nonstandart_alg(p_pois, lambd)
        arr_pois.append(number)
        oper += one_oper

    with open("poisson.txt", "w") as f:
        f.write(str(arr_pois))
    # сопоставление каждого значения с вероятностью его получения по
    # пауссоновскому закону распределения
    pois_prob = {}
    for el in arr_pois:    
        pois_prob[el] = poisson.distrib(el, lambd)
    #подсчитывается кол-во элементов, вероятность которых больше 0.001
    poisson_count = poisson.calculate_interv_amount(arr_pois, lambd)

    factor = 100
    pois_teor_probs = [poisson.distrib(x, lambd) * factor for x in range(max(arr_pois))]
    print("Пуассоновское распределение:\n\tлямбда - {}\n\tуровень значимости - {}\n\t"
        "длина последовательности - {}\n\tсложность алгоритма - {}".format(lambd, alpha, length, oper))

    chi2.chisqr_test(arr_pois, pois_prob, pois_teor_probs, poisson_count, alpha, True)

def get_arguments():
    with open("arguments.txt", "r") as f:
        file_str = f.read()
        args = file_str.split(" ")
        s, p, alpha, lambd = float(args[0]), float(args[1]), float(args[2]), int(args[3])
        return s, p, alpha, lambd

def main():    
    sys.stdout = open("output.txt", "w+")
    s, p, alpha, lambd = get_arguments()

    tests_for_binom_neg(s, p, alpha, 40)
    tests_for_poisson(lambd, alpha, 40)

    tests_for_binom_neg(s, p, alpha, 100)
    tests_for_poisson(lambd, alpha, 100)

main()