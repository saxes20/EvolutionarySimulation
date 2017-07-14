import MutatedGenes
import collections
from random import randint

sizeText = input("Enter the size of your base population (all WT): ")
size = int(sizeText)
#print(size)

rateText = input("What will be your rate of mutation? ")
rate = float(rateText)
MutatedGenes.rateOfMutation = rate

#foodText = input("Enter the amount of food per generation: ")
#food = int(foodText)

foodSurvivalText = input("Enter the amount of food needed for survival: ")
foodSurvival = int(foodSurvivalText)

goThroughText = input("Go through generations one-by-one? Type True if so, and False to make it run automatically: ")
goThrough = False
if goThroughText == "True" or goThroughText == "true":
    goThrough = True

generations = []

numOfOrgs = 0
popSize = 0

prevArray = {}

class organism():
    def __init__(self):
        self.eyeColor = ""
        self.reproductiveAbility = 0
        self.survivalAbility = 0
        self.overallFitness = 0
        self.generation = 0

class fly(organism):
    def __init__(self, geneSequence, eyeColor, generation):
        organism.__init__(self)
        self.number = 0
        self.eyeColor = eyeColor
        self.geneSequence = geneSequence
        self.generation = generation
        self.alive = True
        self.parents = 0
        self.reproductiveAbility = 50
        self.survivalAbility = 50
        self.overallFitness = 50
        self.food = 0
        self.children = []
        self.protein = 1
        #self.spouse = "N/A"

class baby(fly):
    def __init__(self, geneSequence, eyeColor, generation, parents):
        organism.__init__(self)
        self.eyeColor = eyeColor
        self.geneSequence = geneSequence
        self.generation = generation
        self.alive = True
        self.parents = parents
        self.reproductiveAbility = 50
        self.survivalAbility = 50
        self.overallFitness = 50
        self.food = 0
        self.children = []

#algorithm determines how fit each organism is and how much they will be able to reproduce
#fit - increases chance of survival by obtaining more food and water, able to therefore reproduce more

def determineFitness(fly, trait):
    #purple, red, scarlet, brown, white
    #1. purple - sexual advantage leads to higher reproduction
    #2. red - normal wild type
    #5. white - pale eyes may lead to problems in presence of sunlight
    reproductiveAbility = fly.reproductiveAbility
    survivalAbility = fly.survivalAbility
    if trait == "purple":
        reproductiveAbility += 40
    elif trait == "scarlet":
        reproductiveAbility -= 40
    elif trait == "brown":
        survivalAbility += 40
    elif trait == "white":
        survivalAbility -= 40
    fly.reproductiveAbility = reproductiveAbility
    fly.survivalAbility = survivalAbility
    fly.overallFitness = (reproductiveAbility + survivalAbility) / 2
    return fly

def generateBasePopulation(previousGeneration, psize, genNum, currentNum):
    population = previousGeneration
    for i in range(psize):
        population[i + 1 + (genNum * psize)] = fly(MutatedGenes.eyeGeneSequences["Wild"], MutatedGenes.trait["Eye Color"][0], genNum)
        population[i + 1 + (genNum * psize)].number = i + 1 + (genNum * psize)
    #print(len(population))
    for i in range(len(population)):
        originalFly = population[i + 1]
        population[i + 1] = determineFitness(originalFly, originalFly.eyeColor)
    currentNum = psize
    global popSize
    popSize = psize
#    print(popSize)
    prevArray["red"] = popSize
#    print(prevArray)
    return population

def generatePopulation(previousGeneration, psize, genNum, currentNum, inputT):
    theDictionary = {}
    if genNum == 1:
        theDictionary = previousGeneration
        previousGeneration = retrieveValues(previousGeneration)
 #   print(previousGeneration)
    newPopulation = {}
    global foodSurvival
    for myFly in previousGeneration:
        if myFly.food >= foodSurvival or myFly.generation == 0:
            amtOfKids = numberOfKids(myFly)
            for f in range(amtOfKids):
                childFly = fly(MutatedGenes.eyeGeneSequences["Wild"], MutatedGenes.trait["Eye Color"][0], genNum)
                childFly.number = currentNum + 1
                currentNum += 1
                global popSize
                popSize += 1
 #               print("Added organism to population, popSize now " + str(popSize))
                if myFly.eyeColor != "red":
                    #print("Before setting stats")
                    #printPopulation([myFly, childFly])
                    setStats(childFly, myFly, False)
                else:
                    setStats(childFly, myFly, False)
                newPopulation[childFly.number] = childFly
    #print(newPopulation)
    global generations
    global food
    #print("First -" + str(generations))
    od = collections.OrderedDict(sorted(newPopulation.items()))
    myGeneration = retrieveValues(od)
    if genNum != 1:
        del generations[-1]
        generations.append(previousGeneration)
    #print("My Generation - " + str(myGeneration))
    generations.append(myGeneration)
    #print(generations)
    distributeFood(foodSurvival, generations, genNum)
    if inputT == "p" and genNum == 1:
        printBasePopulation(theDictionary)
    elif inputT == "p" and genNum != 1:
        #print("PRINTING")
        printPrevPopulation(previousGeneration)
    return myGeneration

def numberOfKids(theFly):
    addOn = theFly.reproductiveAbility
    percentages = [addOn + (-55), addOn + (-35), addOn + (-15), addOn + 5, addOn + 25]
    for i in range(5):
        randNum = randint(0, 100)
        if randNum < percentages[i]:
            return (5 - i)
    return 0
    

def distributeFood (foodPer, generations, genNum):
    #print(generations)
    populationArray = []
    populationArray.extend(generations[genNum])
    for theFly in populationArray:
        baseRangeMin = 1
        baseRangeMax = 5
        if theFly.survivalAbility > 40:
            add = (theFly.survivalAbility - 40)/10
            baseRangeMin += add
            baseRangeMax += add
        #print("Food Stat: " + str(theFly.survivalAbility))
        baseRangeMin = int(round(baseRangeMin, 0))
        #print("Range Minimum: " + str(baseRangeMin))
        baseRangeMax = int(round(baseRangeMax, 0))
        #print("Range Maximum: " + str(baseRangeMax))
        foodCreated = randint(baseRangeMin, baseRangeMax)
        #print("Food Given: " + str(foodCreated))
        theFly.food += foodCreated
        #print(theFly.food)

def killGrandPop (genArray, genNumber):
    if genNumber > 1:
        global popSize
        if genNumber > 1:
            kPopulation = genArray[genNumber - 2]
            if genNumber == 2:
                kPopulation = retrieveValues(kPopulation)
            for dFly in kPopulation:
                if dFly.alive:
                    popSize -= 1
 #                   print("Killed organism #" + str(dFly.number) + " from grandfather generation")
                    reduceFood(dFly)
    fPopulation = []
    fPopulation.extend(genArray[genNumber])
    if genNumber == 1:
        fPopulation.extend(retrieveValues(genArray[genNumber - 1]))
    else:
        fPopulation.extend(genArray[genNumber - 1])
    global foodSurvival
    for theFly in fPopulation:
        if theFly.food < foodSurvival and theFly.generation != 0 and theFly.alive:
            theFly.alive = False
            popSize -= 1
#            print("Killed organism #" + str(theFly.number) + " and popSize is now " + str(popSize))
            reduceFood(theFly)

def reduceFood(theFly):
    global prevArray
    currentVal = prevArray[theFly.eyeColor]
    currentVal -= 1
    prevArray[theFly.eyeColor] = currentVal
    #print(prevArray)
    
def retrieveValues(dictionary):
    keys = list(dictionary.keys())
    values = []
    for i in keys:
        values.append(dictionary[i])
    return values

def getPopStats(population, genNum):
    traits = list(MutatedGenes.trait.keys())
    global prevArray
    pop = []
    if genNum < 1:
        pop = retrieveValues(population)
    else:
        pop = population
    for tr in traits:
        for allele in MutatedGenes.trait[tr]:
            if genNum > 0:
                prevCount = prevArray[allele]
            cnt = 0
            for fl in pop:
                if fl.eyeColor == allele:
                    cnt += 1
            if genNum > 0:
                cnt += prevCount
            print(str(allele) + ": " + str(cnt))
            prevArray[allele] = cnt
    print("      ")

def setStats(babyFly, parent, doPrint):
    if doPrint:
        print("Parent Eye Color B " + str(parent.eyeColor))
        print("Child Eye Color B " + str(babyFly.eyeColor))
    ogeyecolor = parent.eyeColor
    oggenesequence = parent.geneSequence
    results = []
    if doPrint:
        results = MutatedGenes.runPrints(oggenesequence)
    else:
        results = MutatedGenes.run(oggenesequence)
    if doPrint:
        print(results)
    if results[2] == parent.protein:
        babyFly.eyeColor = parent.eyeColor
    else:
        babyFly.eyeColor = results[0]
    babyFly.geneSequence = results[1]
    babyFly.protein = results[2]
    if doPrint:
        print("Child Eye Color and Gene Sequence After: " + str(babyFly.eyeColor) + " " + str(babyFly.geneSequence))
        printPopulation([babyFly])
    babyFly.parents = parent.number
    babyFly = determineFitness(babyFly, babyFly.eyeColor)
    parent.children.append(babyFly.number)

def printBasePopulation(population):
    #print("New Population")
    #print(population)
    print(population)
    for i in range(len(population)):
        print("    ")
        print("Organism #" + str(population[i + 1].number) + ":")
        print("Generation:" + str(population[i + 1].generation))
        print("Parents:" + str(population[i + 1].parents))
        print("Children: " + str(population[i + 1].children))
        print("Eye Color:" + str(population[i + 1].eyeColor))
        print("Gene Sequence:" + str(population[i + 1].geneSequence))
        print("Reproductive Ability:" + str(population[i + 1].reproductiveAbility))
        print("Survival Ability:" + str(population[i + 1].survivalAbility))
        print("Overall Fitness:" + str(population[i + 1].overallFitness))
        print("Alive:" + str(population[i + 1].alive))
        print("     ")

def printPopulation(population):
    #print("New Population")
    #print(population)
    for i in range(len(population)):
        print("    ")
        print("Organism #" + str(population[i].number) + ":")
        print("Generation:" + str(population[i].generation))
        print("Parents:" + str(population[i].parents))
        print("Children: " + str(population[i].children))
        print("Eye Color:" + str(population[i].eyeColor))
        print("Gene Sequence:" + str(population[i].geneSequence))
        print("Food: " + str(population[i].food))
        print("Reproductive Ability:" + str(population[i].reproductiveAbility))
        print("Survival Ability:" + str(population[i].survivalAbility))
        print("Overall Fitness:" + str(population[i].overallFitness))
        print("Alive:" + str(population[i].alive))
        print("     ")

def printPrevPopulation(population):
    #print("New Population")
    #print(population)
    for i in range(len(population)):
        if population[i].alive:
            print("    ")
            print("Organism #" + str(population[i].number) + ":")
            print("Generation:" + str(population[i].generation))
            print("Parents:" + str(population[i].parents))
            print("Children: " + str(population[i].children))
            print("Eye Color:" + str(population[i].eyeColor))
            print("Gene Sequence:" + str(population[i].geneSequence))
            print("Food: " + str(population[i].food))
            print("Reproductive Ability:" + str(population[i].reproductiveAbility))
            print("Survival Ability:" + str(population[i].survivalAbility))
            print("Overall Fitness:" + str(population[i].overallFitness))
            print("Alive:" + str(population[i].alive))
            print("     ")


def runMain():
    global size
    global rate
    global food
    global foodSurvival
    global popLimit
    global generations
    global numOfOrgs
    global popSize
    global prevArray
    global goThrough
    
    basePopulation = generateBasePopulation({}, size, 0, numOfOrgs)
 #   printBasePopulation(basePopulation)
    print("")
    print("Generation: 0")
    getPopStats(basePopulation, 0)

    generations.append(basePopulation)

    numOfOrgs += size

 #   inp = input("Press any key to generate next generation: ")
    nextGeneration = generatePopulation(basePopulation, size, 1, numOfOrgs, "hello")
    killGrandPop(generations, 1)
 #   printPopulation(nextGeneration)
    print("Generation: 1")
    getPopStats(nextGeneration, 1)
    #print("Population Size: " + str(popSize))

    numOfOrgs += len(nextGeneration)

    generationNumber = 1
    while True:
        generationNumber += 1
        inp = ""
        if goThrough: 
            inp = input("Press any key to generate next generation (type 'p' to print every organism): ")
        newGeneration = generatePopulation(generations[-1], size, generationNumber, numOfOrgs, inp)
        #print("NEW GENERATION")
        #generations.append(newGeneration)
        #distributeFood(food, foodSurvival, generations, generationNumber)
        numOfOrgs += len(newGeneration)
        #print("generation: " + str(generations))
        killGrandPop(generations, generationNumber)
        if inp == "p":
           printPopulation(newGeneration)
        print("")
        print("Generation: " + str(generationNumber))
        getPopStats(generations[-1], generationNumber)
 #       print("Population Size: " + str(popSize))
        if popSize <= 0:
            break

def runMainPrint():
    global size
    global rate
    global food
    global foodSurvival
    global popLimit
    global generations
    global numOfOrgs
    global popSize
    global prevArray
    
    basePopulation = generateBasePopulation({}, size, 0, numOfOrgs)
 #  printBasePopulation(basePopulation)
    getPopStats(basePopulation, 0)

    generations.append(basePopulation)

    numOfOrgs += size

 #   inp = input("Press any key to generate next generation: ")
    nextGeneration = generatePopulation(basePopulation, size, 1, numOfOrgs)
    killGrandPop(generations, 1)
 #   printPopulation(nextGeneration)
    getPopStats(nextGeneration, 1)
 #   print("Population Size: " + str(popSize))

    numOfOrgs += len(nextGeneration)

    generationNumber = 1
    while True:
        generationNumber += 1
 #       inp = input("Press any key to generate next generation: ")
        newGeneration = generatePopulation(generations[-1], size, generationNumber, numOfOrgs)
        #print("NEW GENERATION")
        #generations.append(newGeneration)
        #distributeFood(food, foodSurvival, generations, generationNumber)
        numOfOrgs += len(newGeneration)
        #print("generation: " + str(generations))
        killGrandPop(generations, generationNumber)
 #       printPopulation(newGeneration)
        getPopStats(generations[-1], generationNumber)
        print("Population Size: " + str(popSize))

runMain()
