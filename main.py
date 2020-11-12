import random
import numpy as np
import time
import sys

PANCAKES_MIN = 3
PANCAKES_MAX = 50


def randomiseProblem():
    quantity = random.randrange(PANCAKES_MIN, PANCAKES_MAX)
    pancakesArr = []
    for i in range(0, quantity):
        randomSize = random.randrange(1, 20)
        if not pancakesArr.__contains__(randomSize):
            pancakesArr.append(randomSize)
        else:
            if i == 0:
                i = 0
            else:
                i = i - 1

    return pancakesArr


def estimateQuality(pancakes):
    qualityMark = 0  # ideal solution
    for i in range(0, len(pancakes)-1):
        if pancakes[i+1] < pancakes[i]:
            qualityMark += 1  # for every mistake increment number of mistakes

    return qualityMark


# it takes pancakes portion and reverse it
def generateRandomSolution(pancakes):
    swapPosition = random.randrange(0, len(pancakes))  # randomise place where you start to reverse
    pancakes[swapPosition:len(pancakes)] = pancakes[swapPosition:len(pancakes)][::-1]  # reverses part of list in place
    return pancakes


def printSolution(solution):
    for el in solution:
        for i in range(el):  # print number of dashes relative to size of pancake
            print("-", end="")
        print("\n")

    print("\n")


def readFile(filename):
    file = open(filename, "r")
    data = file.readline()
    file.close()
    return data


def writeFile(filename, inputData, solution, workTime):
    file = open(filename, "w")

    file.write("Input: ")
    for el in inputData:
        file.write(str(el) + " ")
    file.write("\n")

    file.write("Output: ")
    for el in solution:
        file.write(str(el) + " ")
    file.write("\n")

    file.write("Alghoritm work time: " + str(workTime))
    file.close()


def bruteForce(pancakes):
    unsorted = pancakes.copy()
    sortedNumber = 0
    quality = estimateQuality(pancakes)
    while quality != 0:
        if sortedNumber == len(pancakes):
            pancakes.reverse()
            return pancakes
        else:
            indexMax = np.argmax(pancakes[sortedNumber:])

        if indexMax == 0:
            unsorted.reverse()
        else:
            reversePart = unsorted[indexMax:]
            unsorted = unsorted[:indexMax]
            reversePart.reverse()
            unsorted.extend(reversePart) #to miejsce nie działa

        unsorted.reverse()
        if sortedNumber == 0:
            pancakes = unsorted.copy()
        else:
            pancakes = pancakes[:sortedNumber]
            pancakes.extend(unsorted)

        del(unsorted[0])

        sortedNumber += 1
        quality = estimateQuality(pancakes)
    pancakes.reverse()
    return pancakes


def climbingAlghoritm(pancakes):
    best_pancakes = pancakes
    best_quality = estimateQuality(best_pancakes)
    while best_quality != 0:
        print(best_pancakes, end="")
        print(" " + str(best_quality))
        new_pancakes = generateRandomSolution(best_pancakes)
        new_quality = estimateQuality(new_pancakes)
        if new_quality < best_quality:
            best_quality = new_quality
            best_pancakes = new_pancakes
    return best_pancakes


def main():
    pancakes = randomiseProblem()
    startingPancakes = pancakes.copy()
    fileOutput = "output.txt"
    if len(sys.argv) >= 2:  # if aditional terminal parameters are added, override default input/output
        pancakes = sys.argv[1]
        fileOutput = sys.argv[2]

    startTime = time.time()
    # pancakes = generateRandomSolution(pancakes)
    pancakes = bruteForce(pancakes)
    # pancakes = climbingAlghoritm(pancakes)

    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)

    return 0


if __name__ == "__main__":
    main()
