import argparse
import csv
import pandas as pd
import math


# entropy calculation
def entropyCalculation(inputdata, originaldata):
    frequency = findfrequency(inputdata, len(inputfiledf.columns) - 1)
    uniqueValues = findUniqueValues(inputfiledf, len(inputfiledf.columns) - 1)
    entropy = 0
    for x in frequency:
        if ((x / (len(inputdata))) != 1):
            entropy += -(x / (len(inputdata))) * (math.log((x / (len(inputdata))), len(uniqueValues)))
        else:
            entropy += 0
    return entropy


# split and calculate entropy
def calculateEntropyForSplit(inputdata, coloumnNumber, entropyS):
    uniqueValues = findUniqueValues(inputdata, coloumnNumber)
    frequency = findfrequency(inputdata, coloumnNumber)
    entropy = []
    averageInformationEntropy = 0
    for x in range(0, len(uniqueValues)):
        # select only required rows
        dupinputfile = inputdata.loc[inputdata[coloumnNumber] == uniqueValues[x]]
        # select only required columns
        splitInputFile = splitIntoColoumns(dupinputfile, coloumnNumber, len(inputfiledf.columns) - 1)
        averageInformationEntropy += (frequency[uniqueValues[x]] / len(inputdata)) * entropyCalculation(splitInputFile,
                                                                                                        inputdata)
        entropy.append(entropyCalculation(splitInputFile, inputdata))
    gain = entropyS - averageInformationEntropy
    return entropy, gain


# id3 algorithm
def algorithm(inputdata, entropy):
    entropyClass = []
    informationGain = []
    # calculate class entropy
    for x in inputdata.columns:
        if (x != len(inputfiledf.columns) - 1):
            result = calculateEntropyForSplit(inputdata, x, entropy)
            entropyClass.append(result[0])
            informationGain.append(result[1])

    maximumGain = 0
    attIndex = 0
    otherIndex = 0
    # # find attribute with maximum gain
    for x in range(0, len(informationGain)):
        if informationGain[x] > maximumGain:
            maximumGain = informationGain[x]
            attIndex = inputdata.columns[x]
            otherIndex = x

    uniqueValues = findUniqueValues(inputdata, attIndex)
    # # finding the decision root
    for x in range(0, len(uniqueValues)):
    #     # leaf nodes
         if (entropyClass[otherIndex][x]) == 0:
             classes = ""
             for row in inputdata.iterrows():
                 if row[1][attIndex] == uniqueValues[x]:
                     classes = row[1][len(inputfiledf.columns) - 1]
                     break
             with open('car.xml', "a") as text_file:
                 print("<node entropy=\"" + str(float(entropyClass[otherIndex][x])) +
                       "\" feature=\"" + coloumnNames[attIndex] +
                       "\" value=\"" + uniqueValues[x] +
                       "\">" + classes +
                       "</node>", end="\n", file=text_file, flush=True)
    #             # internal nodes
         else:
             with open('car.xml', "a") as text_file:
                 print("<node entropy=\"" + str(entropyClass[otherIndex][x]) +
                       "\" feature=\"" + coloumnNames[attIndex] +
                       "\" value=\"" + uniqueValues[x] +
                       "\">", end="\n", file=text_file, flush=True)
    #             # select only required rows for particular value of the node
             dupinputfilex = inputdata.loc[inputdata[inputdata.columns[otherIndex]] == uniqueValues[x]]
    # #         # skip the attribute already selected as node
             skipinputfilex = skipColoumn(dupinputfilex, attIndex)
             entropySx = entropyCalculation(skipinputfilex, skipinputfilex)
             algorithm(skipinputfilex, entropySx)
             with open('car.xml', "a") as text_file:
                  print("</node>", end="\n", file=text_file)


# utilities
def splitIntoColoumns(inputdata, col1, col2):
    splitInputFile = inputdata[[col1, col2]]
    return splitInputFile


def skipColoumn(inputdata, col1):
    splitInputFile = inputdata
    del splitInputFile[col1]
    return splitInputFile


def findfrequency(inputdata, coloumnNumber):
    frequency = inputdata[coloumnNumber].value_counts()
    return frequency


def findUniqueValues(inputdata, coloumnNumber):
    differentClasses = inputdata[coloumnNumber].unique()
    return differentClasses


# read arguments from command line
#parser = argparse.ArgumentParser()
#parser.add_argument("--data")
#parser.add_argument("--output")
#arguments = parser.parse_args()
#with open(arguments.data) as csvfile:
with open('car.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    inputfiledf = pd.read_csv(csvfile, header=None)
# assigning column names
coloumnNames = []
for x in range(0, len(inputfiledf.columns) - 1):
    coloumnNames.append("att" + str(x))
# root node
entropyS = entropyCalculation(inputfiledf, inputfiledf)
with open('car.xml', "w") as text_file:
    print("<tree entropy=\"" + str(entropyS) + "\">", end="\n", file=text_file)
# starting id3 algorithm
algorithm(inputfiledf, entropyS)
with open('car.xml', "a") as text_file:
    print("</tree>", file=text_file)
