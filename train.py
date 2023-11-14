import matplotlib.pyplot as plt
import csv
import sys


def plotData(data, dataLen, intercept, slope):
	plt.scatter(data["km"], data["price"], label="data")
	plt.plot(data["km"], [estimatePrice(data["km"][i], intercept, slope) for i in range(dataLen)], color="orange", label="estimation")
	plt.xlabel("mileage (in km)")
	plt.ylabel("price (in euro)")
	plt.title("price per mileage")
	plt.legend()
	plt.show()

def calculatePrecision(data, dataLen, intercept, slope):
	total = 0
	totalDiff = 0
	for i in range(dataLen):
		estimation = estimatePrice(data["km"][i], intercept, slope)
		totalDiff += abs(estimation - data["price"][i])
		total += estimation
	return (total - totalDiff) / total

def estimatePrice(mileage, intercept, slope):
	result = intercept + mileage * slope
	return result

def getDiffs(data, dataLen, intercept, slope):
	interceptDiff = 0
	slopeDiff = 0
	for i in range(dataLen):
		diff = estimatePrice(data["km"][i], intercept, slope) - data["price"][i]
		interceptDiff += diff
		slopeDiff += diff * data["km"][i]
	return interceptDiff, slopeDiff

def linearRegression(data, dataLen, prevIntercept, prevSlope, interceptDiff, slopeDiff, learningRate):
	intercept, slope = prevIntercept - learningRate * (1 / dataLen) * interceptDiff, prevSlope - learningRate * (1 / dataLen) * slopeDiff
	prevInterceptDiff, prevSlopeDiff = interceptDiff, slopeDiff
	interceptDiff, slopeDiff = getDiffs(data, dataLen, intercept, slope)
	if abs((prevInterceptDiff - interceptDiff) / prevInterceptDiff) < learningRate:
		return intercept, slope
	if abs(prevInterceptDiff) < abs(interceptDiff):
		return linearRegression(data, dataLen, prevIntercept, prevSlope, prevInterceptDiff, prevSlopeDiff, learningRate / 10)
	return linearRegression(data, dataLen, intercept, slope, interceptDiff, slopeDiff, learningRate)

def parseData():
	try:
		with open("data.csv") as file:
			csvReader = csv.reader(file)
			header = next(csvReader)
			if len(header) != 2 or header[0] != "km" or header[1] != "price":
				sys.exit("wrong header")
			data = {"km": [], "price": []}
			for row in csvReader:
				if len(row) != 2:
					sys.exit("wrong number of values")
				try:
					data["km"].append(float(row[0]))
					data["price"].append(float(row[1]))
				except:
					sys.exit("wrong values")
			dataLen = csvReader.line_num - 1
	except:
		sys.exit("data.csv missing")
	return data, dataLen

def main():
	data, dataLen = parseData()
	intercept = max([data["price"][i] for i in range(dataLen)])
	slope = 0
	interceptDiff, slopeDiff = getDiffs(data, dataLen, intercept, slope)
	intercept, slope = linearRegression(data, dataLen, intercept, slope, interceptDiff, slopeDiff, 1)
	if len(sys.argv) == 2 and sys.argv[1] == "-p":
		print("precision:", calculatePrecision(data, dataLen, intercept, slope))
	else:
		plotData(data, dataLen, intercept, slope)
		with open("estimation.csv", "w") as file:
			file.write(f"intercept,slope\n{intercept},{slope}")

if __name__ == "__main__":
	main()