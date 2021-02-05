def myStrategy(pastPriceVec, currentPrice, stockType):
	# Explanation of my approach:
	# 1. Technical indicator used: MA
	# 2. if price-ma>alpha ==> buy
	#    if price-ma<-beta ==> sell
	# 3. Modifiable parameters: alpha, beta, and window size for MA
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
	
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	dataLen=len(pastPriceVec)		# Length of the data vector
	if dataLen==0: 
		return action
	if stockType=='LQD':
		rsi=talib.RSI(pastPriceVec, timeperiod=5)
		macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=6, slowperiod=7, signalperiod=5)
		if (macd[-1] - macdsignal[-1] > 0) and (macd[-2] - macdsignal[-2] < 0) and (rsi[-1] > 60):
			action=1
		elif (macd[-1] - macdsignal[-1] < 0) and (macd[-2] - macdsignal[-2] > 0) and (rsi[-1] < 40):
			action=-1
	else:
		# Compute MA
		if dataLen<windowSize:
			ma=np.mean(pastPriceVec)	# If given price vector is small than windowSize, compute MA by taking the average
		else:
			windowedData=pastPriceVec[-windowSize:]		# Compute the normal MA using windowSize 
			ma=np.mean(windowedData)
		# Determine action
		if (currentPrice-ma)>alpha:		# If price-ma > alpha ==> buy
			action=1
		elif (currentPrice-ma)<-beta:	# If price-ma < -beta ==> sell
			action=-1

	return action
