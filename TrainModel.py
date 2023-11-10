import csv


def estimatePrice(mileage, intercept, slope):
    result = intercept + mileage * slope
    return result

def parseData():
    with open("data.csv") as file:
        csvReader = csv.reader(file)
        header = next(csvReader)
        data = {}
        for key in header:
            data[key] = []
        for row in csvReader:
            for i, key in enumerate(data):
                data[key].append(float(row[i]))
    return data

def main():
    data = parseData()
    learningRate = 0.000000001
    intercept = 0
    slope = 0
    for _ in range(100000):
        interceptDiff = learningRate / len(data) * sum(estimatePrice(data["km"][i], intercept, slope) - data["price"][i] for i in range(len(data))) 
        slopeDiff = learningRate / len(data) * sum((estimatePrice(data["km"][i], intercept, slope) - data["price"][i]) * data["km"][i] for i in range(len(data)))
        intercept = interceptDiff
        slope = slopeDiff
        print("intercept:", intercept, "slope:", slope)
        if intercept > 0 and slope < 0:
            print("HEYY!!!!!!!!!!")
            break
    # linearRegression(data)

if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(e)