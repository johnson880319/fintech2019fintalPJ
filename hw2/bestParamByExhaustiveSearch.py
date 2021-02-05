import sys
import numpy as np
import pandas as pd

# Decision of the current day by the current price, with 3 modifiable parameters
def myStrategy(pastPriceVec, currentPrice, fast, slow, signal):
	import numpy as np
	import talib
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	dataLen=len(pastPriceVec)		# Length of the data vector
	if dataLen==0:
		return action
	macd, macdsignal, macdhist = talib.MACD(pastPriceVec, fastperiod=fast, slowperiod=slow, signalperiod=signal)
	if ((macd[-1] - macdsignal[-1] > 0) and (macd[-2] - macdsignal[-2] < 0)):
		action=1
	elif ((macd[-1] - macdsignal[-1]) < 0 and (macd[-2] - macdsignal[-2] > 0)):
		action=-1
	return action

# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec,fast, slow, signal):
	capital=1000	# Initial available capital
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, fast, slow, signal)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

if __name__=='__main__':
	fileList=['SPY.csv', 'DSI.csv', 'IAU.csv', 'LQD.csv']
	fileCount=len(fileList)
	rr=np.zeros((fileCount,1))
	alphaBest=np.zeros((fileCount,1)); betaBest=np.zeros((fileCount,1)); signalbest=np.zeros((fileCount,1)); returnRateBest=np.zeros((fileCount,1));
	for ic in range(fileCount):
		returnRateBest=-1.00	 # Initial best return rate
		file = fileList[ic]
		df=pd.read_csv(file)	# read stock file
		adjClose=df["Adj Close"].values		# get adj close as the price vector
		windowSizeMin=3; windowSizeMax=6	# Range of windowSize to explore
		alphaMin=5; alphaMax=10			# Range of alpha to explore
		betaMin=13; betaMax=18				# Range of beta to explore
		# Start exhaustive search
		print("searching for %s" %(file))
		for fast in range(2, 100, 3):	    	# For-loop for alpha
			print("\tfast=%d" %(fast))
			for slow in range(fast+1,200, 3):		# For-loop for beta
				print("\t\tslow=%d" %(slow))	# No newline
				for signal in range(2, 100, 3):
					print("\t\tsignal=%d" %(signal), end="")
					returnRate=computeReturnRate(adjClose, fast, slow, signal)		# Start the whole run with the given parameters
					print(" ==> returnRate=%f " %(returnRate))
					if returnRate > returnRateBest:		# Keep the best parameters
						alphaBest[ic]=fast
						betaBest[ic]=slow
						signalbest[ic] = signal
						returnRateBest[ic]=returnRate
	for ic in range(fileCount):					
		print("%s Best settings: alpha=%d, beta=%d, signal=%d ==> returnRate=%f" %(fileList[ic],alphaBest[ic],betaBest[ic],signalbest[ic],returnRateBest[ic]))		# Print the best result
