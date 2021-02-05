import pandas as pd
import sys
taifex = pd.read_csv(sys.argv[1],encoding="big5")
taifex.drop(taifex.loc[taifex['商品代號']!='TX     '].index, inplace=True)
date = taifex.iat[-1,0]
taifex.drop(taifex.loc[taifex['成交日期']!=date].index, inplace=True)
expiremonth = taifex.iat[0,2]
taifex.drop(taifex.loc[taifex['到期月份(週別)']!=expiremonth].index, inplace=True)
taifex.drop(taifex.loc[taifex['成交時間']<84500].index, inplace=True)
taifex.drop(taifex.loc[taifex['成交時間']>134500].index, inplace=True)
open = taifex.iat[0,4]
close = taifex.iat[-1,4]
high = taifex['成交價格'].max()
low = taifex['成交價格'].min()
print('%d %d %d %d' % (open, high, low, close))