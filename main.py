import random
import numpy as np
import time
import sys

PANCAKES_MIN = 3
PANCAKES_MAX = 4


def randomiseProblem():
    quantity = random.randrange(PANCAKES_MIN, PANCAKES_MAX)
    pancakesArr = []
    for i in range(0, quantity):
        randomSize = random.randrange(1, 20)
        if not pancakesArr.__contains__(randomSize):
            pancakesArr.append(randomSize)

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


# na razie puste
def nextSolution(solution):
    print()


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


# def temp():
#     # find first element bigger than previous and save its index
#     splitIndex = 0
#     biggest =
#     # todo zmienna zapisujaca najwieksza liczbe i jej index
#     for i in range(1, len(pancakes)):
#         if pancakes[i] > pancakes[i - 1]:
#             splitIndex = i - 1
#             break  # todo ten break wyleci
#
#     # print("splitIndex: " + str(splitIndex))
#     unsorted = pancakes[splitIndex:]  # unsorted table
#     indexMax = np.argmax(unsorted) + len(pancakes[0:splitIndex])  # index of biggest pancake
#
#     if estimateQuality(pancakes[:splitIndex] + unsorted) == 0:
#         return pancakes[:splitIndex] + unsorted
#
#     # move biggest pancake to the right of the sorted pancakes
#     np.flip(unsorted[indexMax:])
#     np.flip(unsorted[splitIndex:])
#
#     pancakes = pancakes[:splitIndex] + unsorted  # concatenate final pancakes table

def bruteForce(pancakes):
    unsorted = pancakes.copy()
    sortedNumber = 0
    quality = estimateQuality(pancakes)
    while quality != 0:
        if sortedNumber == len(pancakes):  # TODO przy gotowym algorytmie to bedzie do wywalenia
            pancakes.reverse()
            return pancakes
        else:
            indexMax = np.argmax(pancakes[sortedNumber:])

        if indexMax == 0:
            unsorted.reverse()
        else:
            unsorted[:indexMax].append(unsorted[indexMax:].reverse())

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


def main():
    # startingPancakes = randomiseProblem()  # copy of clean input data to save them to file at the end
    # pancakes = list.copy(startingPancakes)
    fileOutput = "output.txt"
    if len(sys.argv) >= 2:  # if aditional terminal parameters are added, override default input/output
        pancakes = sys.argv[1]
        fileOutput = sys.argv[2]

    # TODO DEBUG
    startingPancakes = [5,3,2,4]
    pancakes = [5,3,2,4]

    startTime = time.time()
    # pancakes = generateRandomSolution(pancakes)
    pancakes = bruteForce(pancakes)

    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)

    return 0


if __name__ == "__main__":
    main()
