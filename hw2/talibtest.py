import talib

file=sys.argv[1];
close = numpy.random.random(100)
output = talib.MACD(close)
print(output)