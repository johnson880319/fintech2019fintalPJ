import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy
import itertools
import multiprocessing

i = range(2, 17)
j = range(2, 17)
k = range(2, 17)

paramlist = list(itertools.product(i, j, k))

bestreturn = 0
bestfast = 0
bestslow = 0
bestsignal = 0

def calReturn(params):
    i = params[0]
    j = params[1]
    k = params[2]
    dailyOhlcv = pd.read_csv(sys.argv[1])
    minutelyOhlcv = pd.read_csv(sys.argv[2])
    capital = 500000.0
    capitalOrig=capital
    transFee = 100
    evalDays = 14
    action = np.zeros((evalDays,1))
    realAction = np.zeros((evalDays,1))
    total = np.zeros((evalDays,1))
    total[0] = capital
    Holding = 0.0
    openPricev = dailyOhlcv["open"].tail(evalDays).values
    clearPrice = dailyOhlcv.iloc[-3]["close"]
    for ic in range(evalDays,0,-1):
        dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
        dateStr = dailyOhlcvFile.iloc[-1,0]
        minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
        action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic], i, j, k)
        currPrice = openPricev[evalDays-ic]
        if action[evalDays-ic] == 1:
            if Holding == 0 and capital > transFee:
                Holding = (capital-transFee)/currPrice
                capital = 0
                realAction[evalDays-ic] = 1
        elif action[evalDays-ic] == -1:
            if Holding > 0 and Holding*currPrice > transFee:
                capital = Holding*currPrice - transFee
                Holding = 0
                realAction[evalDays-ic] = -1
        elif action[evalDays-ic] == 0:
            realAction[evalDays-ic] = 0
        else:
            assert False
        if ic == 3 and Holding > 0: #遇到每個月的第三個禮拜三要平倉，請根據data的日期自行修改
            capital = Holding*clearPrice - transFee
            Holding = 0

        total[evalDays-ic] = capital + float(Holding>0) * (Holding*currPrice-transFee)

    returnRate = (total[-1] - capitalOrig)/capitalOrig
    if returnRate > bestreturn:
        bestfast = i
        bestslow = j
        bestsignal = k
    print("fast:%d, slow:%d, signal:%d" % (i, j, k))
    print("returnRate:%f" % returnRate)
    return returnRate, i, j, k

pool = multiprocessing.Pool()
res = pool.map(calReturn, paramlist)

print("max:")
print(max(res))

print("bestfast:%d, bestslow:%d, bestsignal:%d" % (bestfast, bestslow, bestsignal))
print("bestreturnRate:%f" % bestreturn)

