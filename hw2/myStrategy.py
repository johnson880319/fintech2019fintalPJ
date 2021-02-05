def myStrategy(pastPriceVec, currentPrice, stockType):
    # Explanation of my approach:
    # 1. Technical indicator used: MA, RSI
    # 2. used both MA and RSI crossover to determin buy or sell(IAU and SPY)
    #    ,also check upper and lower RSI bound to pervent market overreact
    #    LQD and DSI used MA from sample strategy
    # 3. Modifiable parameters: alpha, beta, and window size for MA, timeperiod for RSI
    # 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
 
    import numpy as np
    import talib
    # stockType='SPY', 'IAU', 'LQD', 'DSI'
    # Set parameters for different stocks
    paramSetting={'SPY': {'alpha':6, 'beta':16, 'windowSize':4},
                    'IAU': {'alpha':0, 'beta':2, 'windowSize':26},
                    'LQD': {'alpha':0, 'beta':1, 'windowSize':5},
                    'DSI': {'alpha':2, 'beta':10, 'windowSize':17}}
    windowSize=paramSetting[stockType]['windowSize']
    alpha=paramSetting[stockType]['alpha']
    beta=paramSetting[stockType]['beta']
 
    action=0        # action=1(buy), -1(sell), 0(hold), with 0 as the default action
    dataLen=len(pastPriceVec)        # Length of the data vector
    if dataLen==0: 
        return action
    if stockType=='IAU':
        shortrsi=talib.RSI(pastPriceVec, timeperiod=3)
        longrsi=talib.RSI(pastPriceVec, timeperiod=15)
        macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=2, slowperiod=7, signalperiod=8)
        if (macd[-1] - macdsignal[-1] > 0) and (macd[-2] - macdsignal[-2] < 0) and (shortrsi[-1] < 79) and (shortrsi[-1] > longrsi[-1]) and (shortrsi[-2] < longrsi[-2]):
            #print("currentprice:%f buy!!" % (currentPrice))
            action=1
        elif (macd[-1] - macdsignal[-1] < 0) and (macd[-2] - macdsignal[-2] > 0) and ((shortrsi[-1] > 16)) and (shortrsi[-1] < longrsi[-1]) and (shortrsi[-2] > longrsi[-2]):
            #print("currentprice:%f sell!!" % (currentPrice))
            action=-1
    elif stockType=='SPY':
        shortrsi=talib.RSI(pastPriceVec, timeperiod=6)
        longrsi=talib.RSI(pastPriceVec, timeperiod=12)
        macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=2, slowperiod=8, signalperiod=8)
        if (macd[-1] - macdsignal[-1] > 0) and (macd[-2] - macdsignal[-2] < 0) and (shortrsi[-1] < 80) and (shortrsi[-1] > longrsi[-1]) and (shortrsi[-2] < longrsi[-2]):
            #print("currentprice:%f buy!!" % (currentPrice))
            action=1
        elif (macd[-1] - macdsignal[-1] < 0) and (macd[-2] - macdsignal[-2] > 0) and ((shortrsi[-1] > 36)) and (shortrsi[-1] < longrsi[-1]) and (shortrsi[-2] > longrsi[-2]):
            #print("currentprice:%f sell!!" % (currentPrice))
            action=-1
    else:
        # Compute MA
        if dataLen<windowSize:
            ma=np.mean(pastPriceVec)    # If given price vector is small than windowSize, compute MA by taking the average
        else:
            windowedData=pastPriceVec[-windowSize:]        # Compute the normal MA using windowSize 
            ma=np.mean(windowedData)
        # Determine action
        if (currentPrice-ma)>alpha:        # If price-ma > alpha ==> buy
            action=1
        elif (currentPrice-ma)<-beta:    # If price-ma < -beta ==> sell
            action=-1
 
    return action