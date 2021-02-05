

def myStrategy(pastPriceVec, currentPrice, stockType):
	# Explanation of my approach:
	# 1. Technical indicator used: MA
	# 2. if price-ma>alpha ==> buy
	#    if price-ma<-beta ==> sell
	# 3. Modifiable parameters: alpha, beta, and window size for MA
	# 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
	
	# stockType='SPY', 'IAU', 'LQD', 'DSI'
	# Set parameters for different stocks
	import numpy as np
	import talib
	paramSetting={'SPY': {'fast':150, 'slow':300, 'windowSize':4},
					'IAU': {'fast':50, 'slow':150, 'windowSize':26},
					'LQD': {'fast':3, 'slow':7, 'windowSize':5},
					'DSI': {'fast':50, 'slow':150, 'windowSize':17}}
	windowSize=paramSetting[stockType]['windowSize']
	fast=paramSetting[stockType]['fast']
	slow=paramSetting[stockType]['slow']
	
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	dataLen=len(pastPriceVec)		# Length of the data vector
	if dataLen==0: 
		return action
	# Compute MA
	dataWindow=pastPriceVec[-200:]
	ma200=np.mean(dataWindow)
	macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=12, slowperiod=26, signalperiod=9)
	if ((macd[-1] > 0) and ((macdhist[-1] > 0) and (macdhist[-2] < 0)) and (currentPrice > ma200)):
		#print("hist[-1]:", macdhist[-1], " hist[-2]:", macdhist[-2])
		action=1
	elif ((macd[-1] < 0) and ((macdhist[-1] < 0) and (macdhist[-2] > 0)) and (currentPrice < ma200)):
		#print("hist[-1]:", macd[-1], " hist[-2]:", macd[-2])
		action=-1

	return action
