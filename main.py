import random
import numpy as np
import time
import sys

PANCAKES_MIN = 3
PANCAKES_MAX = 9


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
def generateSolution(pancakes):
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


# def flip(pancakes, n):
#     temp, start = 0
#     while start < n:
#         temp = pancakes[start]
#         pancakes[start] = pancakes[n]
#         pancakes[n] = temp
#         start += 1
#         n -= 1
#
#
# def pancakeSort(pancakes, n):
#     for currSize in range(n, 1, -1):
#         mi = max(pancakes, currSize)
#
#         if mi != currSize-1:
#             flip(pancakes, mi)
#             flip(pancakes, currSize-1)


def main():
    startingPancakes = randomiseProblem()  # copy of clean input data to save them to file at the end
    pancakes = list.copy(startingPancakes)
    fileOutput = "output.txt"
    if len(sys.argv) >= 2:  # if aditional terminal parameters are added, override default input/output
        pancakes = sys.argv[1]
        fileOutput = sys.argv[2]

    startTime = time.time()
    quality = estimateQuality(pancakes)
    while quality != 0:
        pancakes = generateSolution(pancakes)
        quality = estimateQuality(pancakes)

    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)
    return 0


if __name__ == "__main__":
    main()
