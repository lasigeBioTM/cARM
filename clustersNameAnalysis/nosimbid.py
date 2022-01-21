import sys
sys.path.append("/cARM2021")
from cluster import *
#from cluster import *
import configargparse
import numpy as np
import sqlite3
from sqlite3 import Error
from difflib import SequenceMatcher
import pandas as pd

'''
verifies if there are any cluster with NULL simbID
and group the names 
'''

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def similar(a, b):
    '''
    :param a: string
    :param b: string
    :return: similarity between a and b (1 is the most similar)
    '''
    return SequenceMatcher(None, a, b).ratio()


def splitBySpace(array):
    '''
    :param array: array of strings
    :return: numpy array with first two words fo each string in array
    '''
    newArrayList = []

    for i in array:
        splited_i = i.split()

        if len(splited_i)<3:
            new_i = splited_i[0]
            newArrayList.append(new_i)
        else:
            new_i = splited_i[0]+" "+splited_i[1]
            newArrayList.append(new_i)

    return np.array(newArrayList)


def similarityMatrix(names):
    '''
    compares array of strings and create a similarity matrix
    :param names: array of strings
    :return:
    '''
    similarityMatrix = np.zeros((len(names), len(names)))

    for index1, n in np.ndenumerate(names):
        for index2, m in np.ndenumerate(names):
            similarityMatrix[index1][index2] = similar(n, m)

    for i in np.arange(len(names)):
        mask = np.where(similarityMatrix[i] > 0.8)
        print (similarityMatrix[i][mask])
        print (names[mask])

def deleteWhitesFromArray(array):
    '''
    needed because agglomerates csv comes with white spaces
    :param array: array or list with spaces
    :return: np array of strings without white spaces in the end
    '''
    arrayList = []
    for x in array:
        arrayList.append(x.rstrip())

    return arrayList


if __name__ == '__main__':

    p = configargparse.ArgParser(default_config_files=['../config.ini'])
    p.add('-mc', '--my-config', is_config_file=True, help='alternative config file path')
    p.add("-csvPath", "--clustersCSVpath", required=False, help="path to csv with clusters info", type=str)
    p.add("-clustName", "--columnName", required=False, help="name of the column with the name of the clusters",
          type=str)
    p.add("-limit", "--columnDevLimit", required=False, help="limit the number of clusters for dev",
          type=int)
    p.add("-db", "--db_file", required=True, help="path do database",
          type=str)

    p.add("-tk", "--token", required=True, help="ADS API person token",
          type=str)

    p.add("-up", "--update", required=True, help="update database",
          type=bool)



    options = p.parse_args()

    aggloCSVPath = options.clustersCSVpath
    columnName = options.columnName
    columnLimit = options.columnDevLimit
    db_file = options.db_file

    conn = create_connection(db_file)
    csvFile = pd.read_csv(aggloCSVPath)
    csvFile['name'] = csvFile['name'].str.strip()

    print(csvFile)

    with conn:
        names = getClusterNameSimbIdNull(conn) # creates clustersTable

        csvFile[csvFile.name.isin(names)][['name','RA_ICRS',  'DE_ICRS']].to_csv('nosimid.csv', index=False)

        # names = splitBySpace(names)
        #
        # name, count = np.unique(names, return_counts=True)
        #
        # for x, y in zip(name, count):
        #
        #     print (x, " - ", y)









