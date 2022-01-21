import configargparse
import numpy as np
import sqlite3
from sqlite3 import Error
import pandas as pd
import sys
import csv


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


def getAuthorIDForUniqueShortName(conn, u_name):
    #con = sqlite3.connect("data/portal_mammals.sqlite")
    df = pd.read_sql_query("SELECT * from authors", conn)

    df['shortName'] = df['shortName'].str.decode("utf-8")
    df['name'] = df['name'].str.decode("utf-8")
    df['affiliation'] = df['affiliation'].str.decode("utf-8")

    author_ids = np.array(df[df.shortName==u_name].id).flatten()

    # print (u_name)
    # cur = conn.cursor()
    #
    # #cur.execute("select id from authors where shortName like ?", (name,))
    #
    # textvar = '{}'.format('a')
    #
    #
    # #cur.execute("SELECT * FROM authors WHERE `shortName` like ?", (textvar,))
    # #cur.execute("SELECT * FROM authors WHERE shortName = ?", (u_name,))
    # cur.execute('''SELECT * FROM authors WHERE `shortName` like \', C.\'''')
    #
    # #cur.execute("select * from `authors` where `shortName` like ', C.'")
    #
    # #cur.execute("select * from authors where `shortName` like \"%a%\"")
    #
    # rows = cur.fetchall()
    # print(rows)
    # rows = np.array(rows, dtype=str).flatten()

    return author_ids

def getAuthorIDForUniqueName(conn, name):
    print (name)
    cur = conn.cursor()

    cur.execute("select id from authors where name like ?", (name,))

    rows = cur.fetchall()
    rows = np.array(rows, dtype=int).flatten()

    return rows


def getArticleID(conn,authorIDs):
    df = pd.read_sql_query("SELECT * from author_article", conn)

    df_articles = df[df.idAuthor.isin(authorIDs)]

    return df_articles

def getClusterIDForUniqueAuthor(conn,articlesIDs):
    df = pd.read_sql_query("SELECT * from cluster_article", conn)

    df_clusters = df[df.idArticle.isin(articlesIDs)]



    return df_clusters


def get_articles(conn, articles_ids):
    df = pd.read_sql_query("SELECT * from articles", conn)

    df_articles = df[df.id.isin(articles_ids)]

    df_articles['bibcode'] = df_articles['bibcode'].str.decode("utf-8")
    df_articles['title'] = df_articles['title'].str.decode("utf-8")
    df_articles['doi'] = df_articles['doi'].str.decode("utf-8")

    return df_articles


def get_clusters_table(conn):

    df = pd.read_sql_query("SELECT * from clusters", conn)

    return df

def get_articles_table(conn):

    df = pd.read_sql_query("SELECT * from articles", conn)
    df['bibcode'] = df['bibcode'].str.decode("utf-8")
    df['title'] = df['title'].str.decode("utf-8")
    df['doi'] = df['doi'].str.decode("utf-8")

    return df

def get_author_article_table(conn):

    df = pd.read_sql_query("SELECT * from author_article", conn)

    return df


def get_authors_table(conn):

    df = pd.read_sql_query("SELECT * from authors", conn)

    df['shortName'] = df['shortName'].str.decode("utf-8")
    df['name'] = df['name'].str.decode("utf-8")
    df['affiliation'] = df['affiliation'].str.decode("utf-8")

    return df


def get_cluster_article_table(conn):

    df = pd.read_sql_query("SELECT * from cluster_article", conn)

    return df



def map_clusterid_to_name(df, clusters):


    df["item_name"] = df["idCluster"].map(clusters.set_index('id')["name"]).fillna(0)

    #print(df)

    return df


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
    att = "shortName"


    conn = create_connection(db_file)

    clusters = get_clusters_table(conn)
    all_articles = get_articles_table(conn)
    authors = get_authors_table(conn)
    author_article = get_author_article_table(conn)
    cluster_article = get_cluster_article_table(conn)




    with open("/data/astro_data/user_item_rating_user_name_item_name_year.csv",'w') as file:

        if att == "shortName":
            shortNamesUniqueArray = getUniqueShortNames(conn)

            writer = csv.writer(file, delimiter=',')
            nameCount = 0
            for name in shortNamesUniqueArray:
                print(name)
                print(nameCount, ' - ', len(shortNamesUniqueArray))
                #authorIDs = getAuthorIDForUniqueShortName(conn, name)
                authorIDs = np.array(authors[authors.shortName==name].id).flatten()

                #authorid_articleid = getArticleID(conn, authorIDs) #autor,article
                authorid_articleid  = author_article[author_article.idAuthor.isin(authorIDs)]

                #articles = get_articles(conn, authorid_articleid.idArticle)
                articles = all_articles[all_articles.id.isin(authorid_articleid.idArticle)]


                #clustersIDS = getClusterIDForUniqueAuthor(conn, authorid_articleid.idArticle)
                clustersIDS = cluster_article[cluster_article.idArticle.isin(articles.id)]


                clustersIDS['year'] = articles[articles.id.isin(clustersIDS.idArticle)].year



                clustersIDS['user'] = nameCount
                clustersIDS['user_name'] = name
                clustersIDS['rating'] = 1
                #print(clusters[clusters.id.isin(clustersIDS.idCluster)].name)
                clustersIDS = map_clusterid_to_name(clustersIDS, clusters)
                #clustersIDS['item_name'] = np.array(clusters[clusters.id.isin(clustersIDS.idCluster)].name)
                #print(clustersIDS)


                to_save = clustersIDS[['user', 'idCluster', 'rating', 'user_name', 'item_name', 'year']]
                #print(to_save)

                to_save.to_csv(file, mode='a', header=False, index=False)



                # for item in clustersIDS.idCluster:
                #     article_year = clustersIDS[clustersIDS.year]
                #     cluster_name = clusters[clusters.id==item].name.iloc[0]
                #
                #
                #
                #     writer.writerow([nameCount, item, 1, name, cluster_name, article_year])
                #     file.flush()


                nameCount += 1

        elif att == "name":
            shortNamesUniqueArray = getUniqueNames(conn)

            recMatrix = np.zeros((len(shortNamesUniqueArray), 2166), dtype=int)
            print(recMatrix.shape)
            writer = csv.writer(file, delimiter=',')
            nameCount = 0
            for name in shortNamesUniqueArray:
                authorIDs = getAuthorIDForUniqueShortName(conn, name)
                articlesIDs = getArticleID(conn, authorIDs)
                clustersIDS = getClusterIDForUniqueAuthor(conn, articlesIDs)

                clusterID, count = np.unique(clustersIDS, return_counts=True)

                for clust, c in zip(clusterID, count):
                    array = np.array([nameCount, clust, c])

                    writer.writerow(array)

                    # np.savetxt("user_item_shortNames_unique_teste.csv", array, delimiter=",")

                    # recMatrix[nameCount][clust-1] = c

                nameCount += 1


        file.close()




