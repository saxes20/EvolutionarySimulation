#wild type gene sequences and gene sequences for variations of the trait
#reproduction - duplicate organism populations and use Punnett Squares
#base evolution on stats
#add different organisms with different characteristics and traits that affect fitness
#create fitness algorithm
#EVOLVE based on fitness
#take data and graph it
import random
from random import randint

trait = {"Eye Color": ["red", "white", "brown", "scarlet", "purple"]}
eyeGeneSequences = {"Wild": "TTACGTTCGTGTTGA"}
populationSize = 10
#percentOfMutation = .05
rateOfMutation = .5

def codonGenerator(geneSequence):
    codons = []
    first = 0
    second = 3
    for b in range(int((len(geneSequence)/3))):
        codons.append(geneSequence[first:second])
        first += 3
        second += 3
    return codons

def codonTable (codons):
    basePairs = ["T", "C", "A", "G"]
    codonTable = {}
    for first in basePairs:
        codon = ""
        aa = 0
        codon += first
        #print(codon)
        for second in basePairs:
            codon = "" + first
            codon += second
            #print(codon)
            for third in basePairs:
                codon = "" + first + second
                codon += third
                #print(codon)
                if first == "T" or first == "C":
                    aa = 1
                elif first == "A" and (second == "T" or second == "C"):
                    aa = 2
                elif first == "A" and (second == "A" or second == "G"):
                    aa = 3
                elif first == "G" and (second == "T" or second == "C"):
                    aa = 4
                else:
                    aa = 5
                codonTable[codon] = aa
    #for codon in codons:
    #    codonTable[codon] = 1
    return codonTable

def determineProtein (codons, table):
    proteins = []
    for codon in codons:
        protein = table[codon]
        proteins.append(protein)
    #print(proteins)
    summed = 0
    for pr in proteins:
        summed += pr
    average = 0
    if len(proteins) > 0:
        average = summed / len(proteins)
    if proteins.count(1) > ((len(proteins)/2) + 0.5):
        return 1
    return int(round(average, 0))

def randomChance(rate):
    rateString = str(rate)
    if rateString[:1] == "0":
        rateString = rateString[1:]
    rateString = rateString.replace(".", "")
    multiply = len(rateString) + 1
    baseNumber = rate * (10 ** multiply)
    outOf = (10 ** multiply)
    #print(str(baseNumber) + "/" + str(outOf))
    #print(baseNumber/ outOf)
    number = random.uniform(0.0, outOf)
    if number <= baseNumber:
        return True
    return False

def pickBasePair():
    number = randint(1,4)
    if number == 1:
        return "A"
    elif number == 2:
        return "T"
    elif number == 3:
        return "C"
    elif number == 4:
        return "G"

def mutate(geneSequence):
    first = 0
    second = 1
    newSequence = "" 
    for b in range(len(geneSequence)):
        doMutate = randomChance(rateOfMutation)
        if doMutate:
            number = randint(1, 3)
            if number == 1:
                newSequence += pickBasePair()
                #print("substitution")
                #print(newSequence)
            elif number == 2:
                newSequence += pickBasePair()
                newSequence += geneSequence[first:second]
                #print("insertion")
                #print(newSequence)
        else:
            newSequence += geneSequence[first:second]
            #print(newSequence)
        first += 1
        second += 1
    return newSequence

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest
            
class organism():
    def __init__(self):
        self.eyeColor = ""
    def sayHi (self):
        print("Hi!")

class fly(organism):
    def __init__(self):
        organism.__init__(self)
        self.eyeColor = "red"

def run(myGene):
    myOrganism = organism()
    myFly = fly()
    #print(myFly.eyeColor)
    
    #print(myGene)
    myCodon = codonGenerator(myGene)
    #print(myCodon)
    theCodonTable = codonTable(myCodon)
    #print(theCodonTable)

    mGene = mutate(myGene)
    #print(mGene)
    mutateCodon = codonGenerator(mGene)
    #print(mutateCodon)
    protein = determineProtein(mutateCodon, theCodonTable)
    #print(protein)
    variedTraits= []
    for tr in trait["Eye Color"]:
        variedTraits.append(tr)
    #print(variedTraits)
    finalTraits = [variedTraits[0]]
    variedTraits.pop(0)
    finalTraits.extend(scrambled(variedTraits))
    #print(finalTraits)
    
    result = finalTraits[protein - 1]
    return [result, mGene, protein]

def runPrints(myGene):
    myOrganism = organism()
    myFly = fly()
    print(myFly.eyeColor)
    
    print(myGene)
    myCodon = codonGenerator(myGene)
    print(myCodon)
    theCodonTable = codonTable(myCodon)
    print(theCodonTable)

    mGene = mutate(myGene)
    print(mGene)
    mutateCodon = codonGenerator(mGene)
    print(mutateCodon)
    protein = determineProtein(mutateCodon, theCodonTable)
    print(protein)
    variedTraits= []
    for tr in trait["Eye Color"]:
        variedTraits.append(tr)
    #print(variedTraits)
    finalTraits = [variedTraits[0]]
    variedTraits.pop(0)
    finalTraits.extend(scrambled(variedTraits))
    print(finalTraits)

    result = finalTraits[protein - 1]
    print(result)
    return [result, mGene, protein]

#runPrints(eyeGeneSequences["Wild"])
