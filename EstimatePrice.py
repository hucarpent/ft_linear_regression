import sys
import re


def estimatePrice(mileage, intercept, slope):
    result = intercept + mileage * slope
    return result

def parseData():
    with open("data.txt") as file:
        lines = file.readlines()
    intercept = None
    slope = None
    for line in lines:
        match = re.match("intercept=(.*?)($|\n)", line)
        if match:
            if intercept:
                raise("there are several intercept values in data.txt")
            intercept = float(match.group(1))
            continue
        match = re.match("slope=(.*?)($|\n)", line)
        if match:
            if slope:
                raise("there are several slope values in data.txt")
            slope = float(match.group(1))
    if not intercept or not slope:
        errorMsg = "can't find "
        if not intercept:
            errorMsg += "intercept "
        if not slope:
            if not intercept:
                errorMsg += "and "
            errorMsg += "slope "
        errorMsg += "in data.txt"
        raise(errorMsg)
    mileage = float(sys.argv[1])
    return mileage, intercept, slope

def main():
    mileage, intercept, slope = parseData()
    print(estimatePrice(mileage, intercept, slope))
            
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)