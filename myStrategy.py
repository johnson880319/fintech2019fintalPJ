def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice, fast, slow, signal):
    import talib
    pastPriceVec = dailyOhlcvFile['close'].values
    macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=fast, slowperiod=slow, signalperiod=signal)
    
    if (macd[-1] - macdsignal[-1]) > 0 and (macd[-2] - macdsignal[-2]) < 0 :
        return 1
    elif (macd[-1] - macdsignal[-1]) < 0 and (macd[-2] - macdsignal[-2]) > 0:
        return -1
    else:
        return 0