def extractUncertainty(fileName, ensLen, xLen, yLen):
	file = open(fileName, 'rb')
	readData = file.read(ensLen * xLen * yLen * 4)
	file.close()