from utils import *
from decisiontree import *
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import numba

numba.jit

def parkinson(ntree, numFolds, isGini, minInfoGainMaxGiniIndex):
    numFolds = 10
    dataset = pd.read_csv('./datasets/parkinsons.csv', sep=",",header=0)
    dataset = dataset.to_records(index=False)

    #create datatype array
    typeArray = []
    for i in range(len(dataset[0]) - 1):
        typeArray.append("numerical")

    #stratifiedkfolds
    folds = stratifiedKFold(dataset, numFolds)

    totalAccuracy = 0
    totalPrecision = 0
    totalRecall = 0
    totalF1 = 0
    for i in range(numFolds):
        forest = []
        testingSet = folds[i]
        trainingSet = []
        for j in range(0, i):
            trainingSet += folds[j]
        for j in range(i + 1, numFolds):
            trainingSet += folds[j]
        for j in range(ntree):
            forest.append(createDecisionTree(bootstrapping(trainingSet), len(dataset[0]) / 2, minInfoGainMaxGiniIndex, typeArray, isGini))
        accuracy, precision, recall, f1 = testing(forest, testingSet)
        totalAccuracy += accuracy
        totalPrecision += precision
        totalRecall += recall
        totalF1 += f1 
    averageAccuracy =  totalAccuracy / numFolds
    averagePrecision = totalPrecision / numFolds
    averageRecall = totalRecall / numFolds
    averageF1 = totalF1 / numFolds
    print("accuracy is:" + str(averageAccuracy))
    print("precision is:" + str(averagePrecision))
    print("recall is:" + str(averageRecall))
    print("F1 is:" + str(averageF1))
    print("----------------------------------------")
    return averageAccuracy, averagePrecision, averageRecall, averageF1

def runParkinson(isGini, minInfoGainMaxGiniIndex):
    accuracy = []
    precision = []
    recall = []
    f1 = []
    ntreeValues = [1, 5, 10, 20]
    for i in range(len(ntreeValues)):
        newAccuracy, newPrecision, newRecall, newF1 = parkinson(ntreeValues[i], 10, isGini, minInfoGainMaxGiniIndex)
        accuracy.append(newAccuracy)
        precision.append(newPrecision)
        recall.append(newRecall)
        f1.append(newF1)
    plt.plot(ntreeValues, accuracy)
    plt.ylabel('accuracy')
    plt.xlabel('number of trees')
    plt.title('correlation between accuracy and number of trees (wine)')
    plt.figure()
    plt.plot(ntreeValues, precision)
    plt.ylabel('precision')
    plt.xlabel('number of trees')
    plt.title('correlation between precision and number of trees (wine)')
    plt.figure()
    plt.plot(ntreeValues, recall)
    plt.ylabel('recall')
    plt.xlabel('number of trees')
    plt.title('correlation between recall and number of trees (wine)')
    plt.figure()
    plt.plot(ntreeValues, f1)
    plt.ylabel('f1')
    plt.xlabel('number of trees')
    plt.title('correlation between f1 score and number of trees (wine)')
    plt.show()

runParkinson(0, 0)
