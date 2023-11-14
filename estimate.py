import csv
import sys


def estimatePrice(mileage, intercept, slope):
	result = intercept + mileage * slope
	return result

def parseData():
	if len(sys.argv) != 2:
		sys.exit("wrong number of arguments")
	try:
		mileage = float(sys.argv[1])
	except:
		sys.exit("wrong mileage value")
	with open("estimation.csv") as file:
		csvReader = csv.reader(file)
		header = next(csvReader)
		if len(header) != 2 or header[0] != "intercept" or header[1] != "slope":
			sys.exit("wrong header")
		values = next(csvReader)
		if len(values) != 2:
			sys.exit("wrong number of values")
		try:
			intercept = float(values[0])
			slope = float(values[1])
		except:
			sys.exit("wrong values")
	return mileage, intercept, slope

def main():
	mileage, intercept, slope = parseData()
	print(estimatePrice(mileage, intercept, slope))
			
if __name__ == "__main__":
	main()