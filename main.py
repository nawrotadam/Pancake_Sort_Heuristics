import random
import numpy as np
import time
import sys

PANCAKES_MIN = 3
PANCAKES_MAX = 7


# randomise starting problem
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
        if pancakes[i+1] > pancakes[i]:
            qualityMark += 1  # for every mistake increment number of mistakes

    # print(pancakes)
    # print(qualityMark)
    return qualityMark


# it takes pancakes portion and reverse it
def randomiseSolution(pancakes):
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
    elementsSorted = 0
    unsorted = pancakes.copy()
    sortedPancakes = []
    pancakeSequence = []  # sequence of flips needed to sort table
    i = -1

    quality = estimateQuality(pancakes)
    while quality != 0:
        indexMax = np.argmax(unsorted)
        reversePart = unsorted[indexMax:]
        unsorted = unsorted[:indexMax]

        reversePart.reverse()
        i += 1
        pancakeSequence.append(indexMax + i)
        unsorted.extend(reversePart)
        unsorted.reverse()
        pancakeSequence.append(i)  # flip whole table

        elementsSorted += 1
        sortedPancakes.append(unsorted[0])
        del(unsorted[0])
        quality = estimateQuality(sortedPancakes + unsorted)

    print(pancakeSequence)
    return sortedPancakes + unsorted


def getAllNeighbours(pancakes):
    neighbours = []
    for i in range(0, len(pancakes)):
        first_split = pancakes[0:i]  # part which is not reversed
        second_split = pancakes[i:len(pancakes)]  # part prepared to reverse
        second_split.reverse()
        neighbours.append(first_split + second_split)

    if neighbours.__contains__(pancakes):
        neighbours.remove(pancakes)  # remove self cause you are not a neighbour
    return neighbours


def climbingAlghoritm(pancakes):
    number_of_flips = 0
    best_pancakes = pancakes.copy()
    best_quality = estimateQuality(best_pancakes)
    while best_quality != 0:
        isBlocked = True
        neighbours = getAllNeighbours(pancakes)
        for el in neighbours:
            if estimateQuality(el) < best_quality:
                best_quality = estimateQuality(el)
                best_pancakes = el.copy()
                number_of_flips += 1
                isBlocked = False

        if isBlocked:  # we are in local max, can't move from there
            print("Blocade")
            print("flips: " + str(number_of_flips))
            return best_pancakes  # we can't move, return unsorted pancakes
    print("flips: " + str(number_of_flips))
    return best_pancakes  # it returns sorted pancakes here


def tabuAlghoritm(pancakes):
    number_of_flips = 0
    tabu_pancakes = pancakes.copy()
    tabu_quality = estimateQuality(pancakes)
    tabuArr = [pancakes]
    while tabu_quality != 0:
        best_neighbour = []
        best_neighbour_quality = len(pancakes)  # indykator bledu, zawsze najgorsza mozliwa opcja
        neighbours = getAllNeighbours(tabu_pancakes)
        isBlocked = True

        for el in neighbours:
            if estimateQuality(el) < best_neighbour_quality and not tabuArr.__contains__(el):
                best_neighbour_quality = estimateQuality(el)
                best_neighbour = el.copy()
                number_of_flips += 1
                isBlocked = False

        if isBlocked:  # if you cannot move
            print("Blocade")
            print("flips: " + str(number_of_flips))
            return tabu_pancakes

        tabu_pancakes = best_neighbour.copy()
        tabuArr.append(tabu_pancakes)
        tabu_quality = best_neighbour_quality

    print("flips: " + str(number_of_flips))
    return tabu_pancakes

def statistics(name, size, time, flips, score):
    print()


def main():
    pancakes = randomiseProblem()
    startingPancakes = pancakes.copy()
    fileOutput = "output.txt"
    if len(sys.argv) >= 2:  # if aditional terminal parameters are added, override default input/output
        pancakes = sys.argv[1]
        fileOutput = sys.argv[2]
    print(pancakes)
    startTime = time.time()
    # pancakes = randomiseSolution(pancakes)
    printSolution(pancakes)
    pancakes = bruteForce(pancakes)
    # pancakes = climbingAlghoritm(pancakes)
    # pancakes = tabuAlghoritm(pancakes)
    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)

    return 0


if __name__ == "__main__":
    main()
