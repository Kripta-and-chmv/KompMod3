import sympy as sp
import math 
import matplotlib.pyplot as plt
import random

#считывание входных параметров
def Input(filename):
    f = open(filename, 'r')
    for line in f:
        data = line.split(' ')
    f.close()
    return data
#моделируем последовательность псевдослучайных чисел   
def GeneratorRav(N):
    y =[]
    for k in range(N):
       #генерация сл чисел в промежутке от 0 до 1
        y.append(random.uniform(0,1))
    return y   
#моделируем дискретные числа стандартным алгоритмом
def ModelDiscreteValuesStandart(table):
    result = []
    Oiter= 0
    for i in range (len(table[2])):
        k = table[2][i] #идем по массиву псевдослучайных чисел   
        Oiter += 1        
        for j in range(len(table[0])):
            k = k - table[0][j] #идем по массиву чисел
                                    #пуассоновского распределения
            Oiter += 2        
            
            if k<0:
                break
        result.append(j)
        Oiter += 1              
    print('IterModel: ', Oiter)
    return result 
#моделируем дискретные числа нестандартным алгоритмом
def ModelDiscreteValuesUnStandart(table, lymbda):
    result = []
    P = table[0]
    L = table[2] #массив псевдослучайных чисел
    Q = table[1][lymbda]
    Oiter = 0  #для подсчета кол-ва итераций     
       
    for i in range(len(L)):
        
        k = L[i] - Q #сраниваем со значением при заданном lymbda
        Oiter += 2        
               
        if k < 0: #если меньше, то увеличиваем до тех пор, 
                    #пока значение не станет положительным
            cur = lymbda
            Oiter += 2        
       
            while k < 0:
                k = k + P[cur]
                cur -= 1
                Oiter += 3        
       
            result.append(cur+1) 
            Oiter += 1        
       
        else: #иначе уменьшаем до тех пор, пока значение не станет отрицательным  
            cur = lymbda + 1
            Oiter += 1        
       
            while k > 0:
                k = k - P[cur]
                cur += 1
                Oiter += 3      
       
            result.append(cur-1) 
            Oiter += 1        
    print('IterModel: ', Oiter)
    return result
#вычисления вероятности по распределению Пуассона
def Poisson(k, lymbda):
    f = ((lymbda**k)/math.factorial(k))*math.exp(-lymbda)
    return f
#обрабатываем массив полученных вероятности пуассона,те значения где вероятности меньше е складываем в один интервал
def ProcessP(arrayP, e):
    
    l = 0
    p = 0
    newP = []
    
    for i in range(len(arrayP)-1):
        if(arrayP[i+1] > arrayP[i] and arrayP[i] < e):
            l +=1 
        if(arrayP[i+1] < arrayP[i] and arrayP[i] < e):
            p = i
            break
    if l!=0:
        newP.append(sum(arrayP[0:l]))
    for i in range(p-l+1):
        newP.append(arrayP[i+l])
    newP.append(1 - sum(newP))
    return newP
#пуассоновкое распределение, создание таблицы
def CreateTable(Size, lymbda):
    result = []    
    p = []
    p_sum = []
    seq = []
    Oiter = 0
    #генерируем последовательность чисел, принадлежащих пуассоновскому распр.
    for k in range(Size):   
        p.append(Poisson(k, lymbda))
        Oiter += 1+k+3
        
    p = ProcessP(p, 1.0/Size)
    #генерируем последовательность чисел, накопления вероятности 
    p_sum.append(p[0])    
    for k in range(len(p)-1):
        p_sum.append(p_sum[k]+p[k+1])
        Oiter+=2
    #генерируем случайноую выборку
    seq = GeneratorRav(Size)
    Oiter += Size
    
    result.append(p)
    result.append(p_sum)
    result.append(seq)
    print('iterTable: ', Oiter)
    return result   
#вывод полученных последовательностей
def OutPutSequence(fileName, seq, text):
    f = open(fileName, 'a')
    k = 0
    f.write(text+'\n')
    for i in range(len(seq)):
        f.write(str(seq[i]))
        f.write(' ')
        k+=1
        if (k == 25):
            k = 0
            f.write('\n')        
    f.close()   
    return
#очистка файла
def ClearFile(fileName):
    f = open(fileName, 'w')
    f.close()   
    return
# вывод таблицы
def outPutTable(fileName, table):
    f = open(fileName, 'w')
    f.write('k:\t')
    k = 0
    for i in range(len(table[2])):
        k += 1
        f.write('|'+str(k)+'\t')
    f.write('\n')
    for i in (table[2]):
        f.write('---------')
    f.write('\nPi:\t')
    for i in range(len(table[0])):
        f.write('|')
        f.write(str(round(table[0][i],4)))
        f.write('\t')
    f.write('\n') 
    for i in range(len(table[2])):
        f.write('---------')
    f.write('\nS(Pi):\t')  
    for i in range(len(table[1])):
        f.write('|')
        f.write(str(round(table[1][i],4)))
        f.write('\t')
    f.write('\n') 
    for i in (table[2]):
        f.write('---------')
    f.write('\nx:\t')    
    for i in range(len(table[2])):
        f.write('|'+str(round(table[2][i],4))+'\t')
    f.write('\n') 
    for i in range(len(table[2])):
        f.write('---------')
    f.write('\ne:\t')    
    for i in range(len(table[3])):
        f.write('|'+str(round(table[3][i],4))+'\t')
    
    f.close()
    return
def outPut(fileName, string):
    f = open(fileName, 'w')
    f.write(string)
    f.close()
    return
def outPutInEnd(nameFile, string):
    f = open(nameFile, 'a')
    f.write(string)
    f.close()
    return
#разбитие на интервалы
def SelectIntervals(P, k):
    mas = [] 
    for i in range(k+1):
        mas.append(int(P/k*i))
    return mas
import numpy as np
#рисуем гистограммы эмпирической и теоретической частоты
def DrawHistogram(masX, masY, nX, nY):
    fig = plt.figure()
    ax = fig.add_subplot(111)   # добавление области рисования ax
    ax.bar(nX, nY, label = u'Theoretical')    
    #Эмпирическая гистограмма
    rgb = np.array([10,200,0])/255
    plt.bar(masX, masY, color = rgb, alpha=0.5, label = u'Emperical')
    plt.title('Criterion hi^2')
    ax.grid(True)   # линии вспомогательной сетки 
    ax.legend(loc = 'best', frameon = True)
    plt.show()
    return
#проверка хи2
def hi2(Period, alpha, table, fileName):
    mas = table[3]    
    P = table[0]
    fe = []
    #кол-во интервалов
    K = len(P)
    intervals=SelectIntervals(len(P), len(P))
    #наблюдаемая частота    
    f0=[]       
      
    for i in range(int(K)):
        f0.append(0)
        
    #сколько значений попадает в интервал
    for i in range(len(mas)):
        for j in range(int(K)):
            if mas[i] <= intervals[j+1]:                 
                f0[j] += 1
                break
   
       
    #перемножим N*Pi
    for i in range(len(P)):
        fe.append(P[i])
        f0[i] /= Period 

    
    #расчет хи2 критерия согласия для распределения Пуассона
    S = 0
    for i in range(len(fe)):
        S += math.pow((f0[i]-fe[i]),2)/fe[i]

     
    intervals = intervals[0:int(K)]       
    DrawHistogram(intervals, f0, intervals, fe)

    outPut(fileName, "S*: "+str(S)+'\n')
    
    #количество степеней свободы
    r = 5
        
    znam = math.gamma(r/2) * 2**(r/2)
    
    f = sp.Function('f')
    g = sp.Function('g')
    x = sp.Symbol('x')
    
    f = x **(r/2 - 1)* sp.exp(-x/2)
    g = sp.integrate(f, (x, S, sp.oo))
    P = g.evalf() / znam

    outPutInEnd(fileName, "S: "+str(P)+'\n')
    
    if(abs(S) < abs(P)):
        outPutInEnd(fileName, "Гипотеза принимается")
    else:
        outPutInEnd(fileName, "Гипотеза отвергается")
 
    return 
#main
#получаем необходимые параметры
data = Input('data.txt')
N1 = int(data[0])
N2 = int(data[1])
l2 = int(data[2])
l4 = int(data[3])
l6 = int(data[4])
l12 =int(data[5])
alpha = float(data[6])

#исследование для стандартного алгоритма
#моделирование дискретных величин с помощью poisson(2)    
ClearFile("Lyambda2.txt")

print(1)
table1 = CreateTable(N1, l2)
table1.append(ModelDiscreteValuesStandart(table1))  
outPutTable('1Table40.txt', table1)
OutPutSequence("Lyambda2.txt", table1[3], 'Смоделированные дискретные величины, при л = 2'+'\n'+'Размерность 40: ')
hi2(N1, alpha, table1, 'hi1.txt')

print(2)
table2 = CreateTable(N2, l2)
table2.append(ModelDiscreteValuesStandart(table2))  
outPutTable('1Table100.txt', table2)
OutPutSequence("Lyambda2.txt", table2[3], '\n'+'Размерность 100: ')
hi2(N2, alpha, table2, 'hi2.txt')

#моделирование дискретных величин с помощью poisson(6)   
ClearFile("Lyambda6.txt")

print(3)
table12 = CreateTable(N1, l6)
table12.append(ModelDiscreteValuesStandart(table12))  
outPutTable('2Table40.txt', table12)
OutPutSequence("Lyambda6.txt", table12[3], 'Смоделированные дискретные величины, при л = 6'+'\n'+'Размерность 40: ')
hi2(N1, alpha, table12, 'hi3.txt')

print(4)
table22 = CreateTable(N2, l6)
table22.append(ModelDiscreteValuesStandart(table22))  
outPutTable('2Table100.txt', table22)
OutPutSequence("Lyambda6.txt", table22[3], '\n'+'Размерность 100: ')
hi2(N2, alpha, table22, 'hi4.txt')

#моделирование дискретных величин с помощью poisson(12)     
ClearFile("Lyambda12.txt")

print(5)
table13 = CreateTable(N1, l12)
table13.append(ModelDiscreteValuesStandart(table13))  
outPutTable('3Table40.txt', table13)
OutPutSequence("Lyambda12.txt", table13[3], 'Смоделированные дискретные величины, при л = 12'+'\n'+'Размерность 40: ')
hi2(N1, alpha, table13, 'hi5.txt')

print(6)
table23 = CreateTable(N2, l12)
table23.append(ModelDiscreteValuesStandart(table23))  
outPutTable('3Table100.txt', table23)
OutPutSequence("Lyambda12.txt", table23[3], '\n'+'Размерность 100: ')
hi2(N2, alpha, table23, 'hi6.txt')

#исследование для нестандартного алгоритма
print(7)
ClearFile("Lyambda4.txt")
table41 = CreateTable(N1, l4)
table41.append(ModelDiscreteValuesUnStandart(table41,l4))  
outPutTable('4Table40.txt', table41)
OutPutSequence("Lyambda4.txt", table41[3], 'Смоделированные дискретные величины, при л = 4'+'\n'+'Размерность 40: ')
hi2(N1, alpha, table41, 'hi7.txt')

print(8)
table24 = CreateTable(N2, l4)
table24.append(ModelDiscreteValuesUnStandart(table24,l4))  
outPutTable('4Table100.txt', table24)
OutPutSequence("Lyambda4.txt", table24[3], '\n'+'Размерность 100: ')
hi2(N2, alpha, table24, 'hi8.txt')

