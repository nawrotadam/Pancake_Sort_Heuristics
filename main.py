import random
import numpy as np
import time
import sys
import math

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
    sortedPancakes = pancakes.copy()
    sortedPancakes.sort()
    sortedPancakes.reverse()

    for i in range(0, len(sortedPancakes)):
        if pancakes[i] != sortedPancakes[i]:
            qualityMark += 1

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


def climbingAlghoritm(pancakes):
    number_of_flips = 0
    best_pancakes = pancakes.copy()
    best_quality = estimateQuality(best_pancakes)
    pancakeSequence = []  # all flip sequences
    best_sequence = None  # best sequence for neighbors
    while best_quality != 0:
        isBlocked = True

        for i in range(0, len(pancakes)):
            first_split = pancakes[0:i]  # part which is not reversed
            second_split = pancakes[i:len(pancakes)]  # part prepared to reverse
            second_split.reverse()
            el = first_split + second_split
            if el == pancakes:  # remove self cause you are not a neighbors
                continue

            if estimateQuality(el) < best_quality:
                best_quality = estimateQuality(el)
                best_pancakes = el.copy()
                pancakes = best_pancakes.copy()
                best_sequence = i
                number_of_flips += 1
                isBlocked = False

        pancakeSequence.append(best_sequence)

        if isBlocked:  # we are in local max, can't move from there
            print("Blocade")
            print("flips: " + str(number_of_flips))
            print("sequence:", end="")
            print(pancakeSequence)
            return best_pancakes  # we can't move, return unsorted pancakes
    print("flips: " + str(number_of_flips))
    print("sequence:", end="")
    print(pancakeSequence)
    return best_pancakes  # it returns sorted pancakes here


def tabuAlghoritm(pancakes):
    # pancakes = [19, 4, 9, 18, 8, 14]  # prove that it works
    number_of_flips = 0
    tabu_pancakes = pancakes.copy()
    tabu_quality = estimateQuality(pancakes)
    tabuArr = [pancakes]
    pancakeSequence = []  # all flip sequences
    best_sequence = None  # best sequence for neighbor

    while tabu_quality != 0:
        isBlocked = True
        best_neighbor = []
        best_neighbor_quality = len(pancakes)  # indykator bledu, zawsze najgorsza mozliwa opcja

        for i in range(0, len(tabu_pancakes)):
            first_split = tabu_pancakes[0:i]  # part which is not reversed
            second_split = tabu_pancakes[i:len(tabu_pancakes)]  # part prepared to reverse
            second_split.reverse()
            el = first_split + second_split

            if el == tabu_pancakes:  # remove self cause you are not a neighbor
                continue

            if estimateQuality(el) < best_neighbor_quality and not tabuArr.__contains__(el):
                best_neighbor_quality = estimateQuality(el)
                best_neighbor = el.copy()
                best_sequence = i
                number_of_flips += 1
                isBlocked = False

        pancakeSequence.append(best_sequence)

        if isBlocked:  # if you cannot move
            print("Blocade")
            print("flips: " + str(number_of_flips))
            print("sequence:", end="")
            print(pancakeSequence)
            return tabu_pancakes

        tabu_pancakes = best_neighbor.copy()
        tabuArr.append(tabu_pancakes)
        tabu_quality = best_neighbor_quality

    print("flips: " + str(number_of_flips))
    print("sequence:", end="")
    print(pancakeSequence)
    return tabu_pancakes


def statistics(name, size, time, flips, score):
    print()


def getAllNeighbors(pancakes):
    neighbors = []
    for i in range(0, len(pancakes)):
        first_split = pancakes[0:i]  # part which is not reversed
        second_split = pancakes[i:len(pancakes)]  # part prepared to reverse
        second_split.reverse()
        neighbors.append(first_split + second_split)

    if neighbors.__contains__(pancakes):
        neighbors.remove(pancakes)  # remove self cause you are not a neighbor
    return neighbors


def simmannealing(pancakes):
    initial_temp = 90
    final_temp = .1
    alpha = 0.01
    current_temp = initial_temp
    current_state = pancakes.copy()

    while current_temp > final_temp:
        neighbor = random.choice(getAllNeighbors(current_state))
        cost_diff = estimateQuality(current_state) - estimateQuality(neighbor)

        if estimateQuality(current_state) == 0:
            return current_state

        if cost_diff > 0:
            current_state = neighbor.copy()
        elif random.uniform(0, 1) < math.exp(cost_diff / current_temp):
            current_state = neighbor.copy()
        current_temp -= alpha

    return current_state


def geneticAlghoritm():
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
    # pancakes = bruteForce(pancakes)
    # pancakes = climbingAlghoritm(pancakes)
    # pancakes = tabuAlghoritm(pancakes)
    pancakes = simmannealing(pancakes)
    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)

    return 0


if __name__ == "__main__":
    main()
