import configargparse
import numpy as np
from dbConnection import *
import pandas as pd
import sys

def getUniqueShortNames(conn):

    '''
    :param conn: connection to database
    :return: 1d numpy array with the unique shortNames
    '''

    cur = conn.cursor()

    cur.execute("select distinct shortName from authors order by shortName")

    rows = cur.fetchall()
    rows = np.array(rows, dtype=str).flatten()

    return rows


def getUniqueNames(conn):

    '''
    :param conn: connection to database
    :return: 1d numpy array with the unique shortNames
    '''

    cur = conn.cursor()

    cur.execute("select distinct name from authors order by name")

    rows = cur.fetchall()
    rows = np.array(rows, dtype=str).flatten()

    return rows


def getAuthorIDForUniqueShortName(conn, name):
    print name
    cur = conn.cursor()

    cur.execute("select id from authors where shortName=?", (name,))

    rows = cur.fetchall()
    rows = np.array(rows, dtype=int).flatten()

    return rows

def getAuthorIDForUniqueName(conn, name):
    print name
    cur = conn.cursor()

    cur.execute("select id from authors where name=?", (name,))

    rows = cur.fetchall()
    rows = np.array(rows, dtype=int).flatten()

    return rows


def getArticleID(conn,authorIDs):
    articlesID = []

    for id in authorIDs:
        cur = conn.cursor()
        cur.execute("select idArticle from author_article where idAuthor=?", (id,))

        rows = cur.fetchall()

        articlesID.append(rows[0][0])

    return np.array(articlesID)

def getClusterIDForUniqueAuthor(conn,articlesIDs):
    clustersID = []
    print "size ", articlesIDs.size
    for id in articlesIDs:
        cur = conn.cursor()
        cur.execute("select idCluster from cluster_article where idArticle=?", (id,))

        rows = cur.fetchall()
        rows = np.array(rows, dtype=int).flatten().tolist()
        clustersID.extend(rows)



    return np.array(clustersID)




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

    options = p.parse_args()

    aggloCSVPath = options.clustersCSVpath
    columnName = options.columnName
    columnLimit = options.columnDevLimit
    db_file = options.db_file
    att = "shortName"


    conn = create_connection(db_file)

    if att == "shortName":
        shortNamesUniqueArray = getUniqueShortNames(conn)

        recMatrix = np.zeros((len(shortNamesUniqueArray), 2166), dtype=int)
        print(recMatrix.shape)

        nameCount = 0
        for name in shortNamesUniqueArray:
            authorIDs = getAuthorIDForUniqueShortName(conn, name)
            articlesIDs = getArticleID(conn, authorIDs)
            clustersIDS = getClusterIDForUniqueAuthor(conn, articlesIDs)

            clusterID, count = np.unique(clustersIDS, return_counts=True)

            for clust, c in zip(clusterID, count):
                recMatrix[nameCount][clust-1] = c

            nameCount += 1

        print "max in user/item matrix ", np.amax(recMatrix)
        df = pd.DataFrame(recMatrix, columns=np.arange(1, 2167))
        df.insert(0, 'user', shortNamesUniqueArray)

        df.to_csv("../data/user_item_shortNames_unique.csv")



    elif att == "name":
        namesUniqueArray = getUniqueNames(conn)

        recMatrix = np.zeros((len(namesUniqueArray), 2166), dtype=int)
        print(recMatrix.shape)

        nameCount = 0
        for name in namesUniqueArray:
            authorIDs = getAuthorIDForUniqueName(conn, name)
            articlesIDs = getArticleID(conn, authorIDs)
            clustersIDS = getClusterIDForUniqueAuthor(conn, articlesIDs)

            clusterID, count = np.unique(clustersIDS, return_counts=True)

            for clust, c in zip(clusterID, count):
                recMatrix[nameCount][clust - 1] = c

            nameCount += 1

        print "max in user/item matrix ", np.amax(recMatrix)
        df = pd.DataFrame(recMatrix, columns=np.arange(1, 2167))
        df.insert(0, 'user', namesUniqueArray)

        df.to_csv("../data/user_item_names_unique.csv")



