import pandas as pd


def getAllDataFrame(csvPath):
    csvFile = pd.read_csv(csvPath)

    return csvFile


def getColumn(pdDF, columnName):
    column = pdDF[columnName]

    return column
