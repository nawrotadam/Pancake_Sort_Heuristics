import random
import sys
import time
import pyqt_pancakes
import matplotlib.pyplot as plt

import math
import numpy as np

PANCAKES_MIN = 10
PANCAKES_MAX = 11


# randomise starting problem
def randomiseProblem():
    quantity = random.randrange(PANCAKES_MIN, PANCAKES_MAX)
    pancakesArr = []
    for i in range(1, quantity + 1):
        # randomSize = random.randrange(1, 30)
        # if not pancakesArr.__contains__(randomSize):
        #     pancakesArr.append(randomSize)
        # else:
        #     if i == 0:
        #         i = 0
        #     else:
        #         i = i - 1
        pancakesArr.append(i)

    random.shuffle(pancakesArr)
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


def estimateGeneticQuality(pancakes, pancake_sequence):
    qualityMark = 0.0  # ideal solution
    sortedPancakes = pancakes.copy()
    sortedPancakes.sort()
    sortedPancakes.reverse()

    pancakes = simulateFlipping(pancakes, pancake_sequence)

    for i in range(0, len(sortedPancakes)):
        if pancakes[i] != sortedPancakes[i]:
            qualityMark += 1

    # we prefer shorter sequences so we subtract from quality mark 1/length of sequence table
    qualityMark -= 1 / len(pancake_sequence)

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
    return [sortedPancakes + unsorted, pancakeSequence]


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
            return [best_pancakes, pancakeSequence]  # we can't move, return unsorted pancakes
    print("flips: " + str(number_of_flips))
    print("sequence:", end="")
    print(pancakeSequence)
    return [best_pancakes, pancakeSequence]  # it returns sorted pancakes here


def climbingAlghoritm_ver2(pancakes):
    number_of_flips = 0
    best_pancakes = pancakes.copy()
    best_quality = estimateQuality(best_pancakes)
    pancakeSequence = []  # all flip sequences
    times_blocked = 0

    while best_quality != 0:
        local_pancakeSequence = pancakeSequence.copy()
        random_flip = random.randrange(0, len(pancakes))
        local_pancakeSequence.append(random_flip)  # append local pancake sequence with random flip
        local_pancakeSequence.append(random.randrange(0, len(pancakes)))
        local_pancakeSequence.append(random.randrange(0, len(pancakes)))
        local_pancake = simulateFlipping(pancakes, local_pancakeSequence)

        if estimateQuality(local_pancake) < best_quality:
            best_quality = estimateQuality(local_pancake)
            best_pancakes = local_pancake.copy()
            pancakes = best_pancakes.copy()
            best_sequence = random_flip
            number_of_flips += 1
            times_blocked = 0
            pancakeSequence.append(best_sequence)

        if times_blocked > 25:  # we are in local max, can't move from there
            random_deleted_quantity = random.randrange(0, 1)
            del(pancakeSequence[len(pancakeSequence)-random_deleted_quantity:])

        times_blocked += 1
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
            return [tabu_pancakes, pancakeSequence]

        tabu_pancakes = best_neighbor.copy()
        tabuArr.append(tabu_pancakes)
        tabu_quality = best_neighbor_quality

    print("flips: " + str(number_of_flips))
    print("sequence:", end="")
    print(pancakeSequence)
    return [tabu_pancakes, pancakeSequence]


def statistics():
    first_method_name = "Bruteforce"
    second_method_name = "Hill Climb"
    third_method_name = "Tabu"

    # clean all files every time we run the program
    brute_file = open(first_method_name + ".txt", "w")
    brute_file.write("")
    hill_file = open(second_method_name + ".txt", "w")
    hill_file.write("")
    hill_file = open(third_method_name + ".txt", "w")
    hill_file.write("")

    startTime = time.time()
    quantity_tab = []
    quality_tab = []

    pancakes = randomiseProblem()
    quantity_to_time_tab = []
    quality_to_time_tab = []
    for i in range(25):
        startTime = time.time()
        brute_force_reference = bruteForce(pancakes)
        pancakes_quantity = len(pancakes)
        pancakes_quality = len(brute_force_reference[1])  # number of flips

        quantity_tab.append(pancakes_quantity)
        quality_tab.append(pancakes_quality)

    stop_time = time.time() - startTime
    workTime = stop_time / 25

    # TODO DOKONCZ

    # todo poprawic i odkomentowac
    # workTime = round(workTime, 6)
    # brute_file = open(first_method_name + ".txt", "a")
    # brute_file.write(first_method_name + " " + str(pancakes_quantity) + " " + str(workTime) + " " + str(pancakes_quality))

    # draw plots
    drawPlot(quantity_to_time_tab)
    drawPlot(quality_to_time_tab)

    quantity_to_time_tab = []
    quality_to_time_tab = []
    for i in range(25):
        startTime = time.time()
        hill_climb_reference = climbingAlghoritm(pancakes)
        pancakes_quantity = len(pancakes)
        pancakes_quality = len(hill_climb_reference[1])  # number of flips
        workTime = time.time() - startTime

        quantity_to_time_tab.append(pancakes_quantity / workTime)
        quality_to_time_tab.append(pancakes_quality / workTime)

        workTime = round(workTime, 6)
        hill_climb_file = open(second_method_name + ".txt", "a")
        hill_climb_file.write(second_method_name + " " + str(pancakes_quantity) + " " + str(workTime) + " " + str(pancakes_quality))

    # draw plots
    drawPlot(quantity_to_time_tab)
    drawPlot(quality_to_time_tab)

    quantity_to_time_tab = []
    quality_to_time_tab = []
    for i in range(25):
        startTime = time.time()
        tabu_reference = tabuAlghoritm(pancakes)
        pancakes_quantity = len(pancakes)
        pancakes_quality = len(tabu_reference[1])  # number of flips
        workTime = time.time() - startTime

        quantity_to_time_tab.append(pancakes_quantity / workTime)
        quality_to_time_tab.append(pancakes_quality / workTime)

        workTime = round(workTime, 6)
        tabu_file = open(third_method_name + ".txt", "a")
        tabu_file.write(third_method_name + " " + str(pancakes_quantity) + " " + str(workTime) + " " + str(pancakes_quality))

    # draw plots
    drawPlot(quantity_to_time_tab)
    drawPlot(quality_to_time_tab)


def drawPlot(tab):
    plt.plot(tab)
    plt.xlabel("Quality")
    plt.ylabel("Time")
    plt.show()


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


def simulateFlipping(pancakes, pancakeSequence):
    for el in pancakeSequence:
        first_split = pancakes[0:el]  # part which is not reversed
        second_split = pancakes[el:len(pancakes)]  # part prepared to reverse
        second_split.reverse()
        pancakes = first_split + second_split

    return pancakes


def geneticAlghoritm(pancakes):
    generations_number = 1000
    starting_population_size = 200
    tournament_offsprings_quantity = 10  # number of groups
    tournament_offsprings_group_size = 20  # number of people in group
    starting_population_sequences = []
    random.seed(time.process_time())

    # starting population generation
    for i in range(0, starting_population_size):
        single_flip_sequence = []
        is_not_empty = False
        for k in range(len(pancakes)):
            if_flip = random.randint(0, 1)
            if if_flip == 1:
                random_flip = random.randrange(0, len(pancakes))
                single_flip_sequence.extend([random_flip])
                is_not_empty = True
        if is_not_empty is False:
            single_flip_sequence = [0]  # if we havent gotten any flips, we flip whole pancake
        starting_population_sequences.append(single_flip_sequence)

    for z in range(generations_number):
        # tournament method offsprings preparation
        tournament_offsprings = starting_population_sequences.copy()
        random.shuffle(tournament_offsprings)
        tournament_counter = 0
        tournament_winners = []
        for i in range(0, tournament_offsprings_group_size):
            # split all offsprings into groups
            single_group = []
            for k in range(0, tournament_offsprings_quantity):
                single_group.append(tournament_offsprings[tournament_counter])
                tournament_counter += 1

            # tournament fight
            group_best = single_group[0]
            group_best_quality = estimateGeneticQuality(simulateFlipping(pancakes, group_best), group_best)
            for n in range(len(single_group)):
                if estimateGeneticQuality(simulateFlipping(pancakes, single_group[n]), single_group[n]) < group_best_quality:
                    group_best = single_group[n]
                    group_best_quality = estimateGeneticQuality(simulateFlipping(pancakes, group_best), group_best)
            tournament_winners.append(group_best)

        for i in range(len(tournament_winners)):  # leave function if one of the tournament winners is an answer
            if estimateGeneticQuality(simulateFlipping(pancakes, tournament_winners[i]), tournament_winners[i]) <= 0:
                return [simulateFlipping(pancakes, tournament_winners[i]), tournament_winners[i]]

        starting_population_sequences = tournament_winners.copy()  # empty the list and add tournament winners to it
        # crossing
        for i in range(0, starting_population_size - tournament_offsprings_quantity):  # rebuild population
            taker = tournament_winners[random.randrange(0, len(tournament_winners))]
            giver = tournament_winners[random.randrange(0, len(tournament_winners))]

            taker_possibilities = [l for l in range(0, len(taker))]
            giver_possibilities = [l for l in range(0, len(giver))]

            random_taker_flips_number = random.choice(taker_possibilities)
            random_giver_flips_number = random.choice(giver_possibilities)

            if random_taker_flips_number == 0:
                crossed_sequence = taker.copy()
                crossed_sequence.extend(giver.copy())
            else:
                crossed_sequence = taker[0:random_taker_flips_number]
                crossed_sequence.extend(giver[0:random_giver_flips_number])
            starting_population_sequences.append(crossed_sequence)

        # mutation
        random_mutation_chance = random.randrange(0, 100)
        if random_mutation_chance < 10:
            random_mutation_position = random.randrange(0, len(starting_population_sequences))

            single_flip_sequence = []
            is_not_empty = False
            for k in range(len(pancakes)):
                if_flip = random.randint(0, 1)
                if if_flip == 1:
                    random_flip = random.randrange(0, len(pancakes))
                    single_flip_sequence.extend([random_flip])
                    is_not_empty = True
            if is_not_empty is False:
                single_flip_sequence = [0]  # if we havent gotten any flips, we flip whole pancake
            starting_population_sequences.append(single_flip_sequence)

            starting_population_sequences[random_mutation_position] = single_flip_sequence

        # check for an answer
        for i in range(len(starting_population_sequences)):  # leave function if one of the next generation is an answer
            if estimateGeneticQuality(simulateFlipping(pancakes, starting_population_sequences[i]), starting_population_sequences[i]) <= 0:
                return [simulateFlipping(pancakes, starting_population_sequences[i]), starting_population_sequences[i]]

    print("Alghoritm wasnt able to solve this problem")
    return [simulateFlipping(pancakes, starting_population_sequences[0]), starting_population_sequences[0]]


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
    pancake_reference = bruteForce(pancakes)
    # pancake_reference = climbingAlghoritm(pancakes)
    # pancake_reference = climbingAlghoritm_ver2(pancakes)
    # pancake_reference = tabuAlghoritm(pancakes)
    # pancake_reference = simmannealing(pancakes)
    pancake_reference = geneticAlghoritm(pancakes)
    pancakes = pancake_reference[0]
    print(pancake_reference[1])

    # statistics()
    # pyqt_pancakes.print_pancakes(pancakes)

    workTime = round(time.time() - startTime, 6)  # work time of alghoritm, rounded to 6 decimal places
    printSolution(pancakes)
    writeFile(fileOutput, startingPancakes, pancakes, workTime)

    return 0


if __name__ == "__main__":
    main()
