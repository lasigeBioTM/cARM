from dbConnection import *
import requests
from article import *
from author import *
from cluster_article import *
import time
import configargparse
from cluster import *


def db_size(conn):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM clusters")

    size = cur.fetchall()

    return size


def update_full_column(conn, myList):
    cur = conn.cursor()
    cur.executemany('UPDATE clusters SET flag= ?', ((val,) for val in myList))
    conn.commit()




def select_all_clusters(conn):
    """
    Query all rows in the clusters table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM clusters")

    rows = cur.fetchall()

    # for row in rows:
    #     print(row)

    return np.array(rows)[:,0], np.array(rows)[:,2], np.array(rows)[:,3], np.array(rows)[:,4]


# def getSimbadCode(name):
#
#     r = requests.post('https://ui.adsabs.harvard.edu/v1/objects/query',
#                       headers={"Authorization": "Bearer V7JtXot9vJuDMI7myqMvOR0HzaeRE0dVyQTo7Ovh",
#                                "Content-Yype": "application/json"},
#                       json={"query":["object:\""+name+"\""]}
#                       )
#     print r.status_code
#     a = r.json()
#
#     if 'query' in a:
#
#         return a['query']
#
#     else:
#         print a
#         print 'query not found'
#         return False


def getNewString(name):
    splitedName = name.split()

    newName = splitedName[0]+" "+splitedName[1]+"-"+splitedName[2]

    return newName


def fillTables(start, simbId, conn, count, idCluster, token):
    print (simbId)

    nrows = 2000

    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query",
                     params={'q':simbId,
                             'fl': 'id,author,bibcode,title,year,aff,author_norm,doi',
                             'rows': str(nrows), 'start': str(start), 'fq': 'database:astronomy',
                             'fq': 'year:[1998 TO 2020]'},
                     headers={"Authorization": "Bearer " + token})


    a = r.json()

    if r.ok:
        print ("ok")

    numFound = a["response"]["numFound"]

    #numFound = a['response']['numFound']

    print ('numfound = ', numFound)

    numberOfRunning = np.ceil(numFound/nrows)
    #print(numberOfRunning)
    #print(count)
    count += 1

    if len(a['response']['docs']) != 0:
        for doc in a['response']['docs']:
            #avoiding the record of articles without author names
            if 'author' in doc:
                author = doc['author']
            else:
                if 'bibcode' in doc:
                    print (doc['bibcode'], " paper without authors")

                continue

            if 'bibcode' in doc:
                bibcode = doc['bibcode']

                n = checkIfArticleExists(conn, bibcode)
                if n == True:

                    #criar uma entrada na tabela cluster_article
                    articleExistentID = getArticleID(conn, bibcode)

                    if checkIfClusterArticleExist(conn, idCluster, articleExistentID) == False:

                        clust_art = (idCluster, articleExistentID);
                        create_cluster_article(conn, clust_art)

                    print (bibcode + " already exists")
                    continue

            if 'title' in doc:
                title = doc['title']
            else:
                title = None

            if 'year' in doc:
                year = doc['year']
            else:
                year = None

            if 'doi' in doc:
                doi = doc['doi']
            else:
                doi = None


            bibcode, title, year, doi = articleToSQL(bibcode, title, year, doi)
            art = (bibcode, title, year, doi);

            articleID = create_article(conn, art)

            clust_art = (idCluster, articleID);
            create_cluster_article(conn, clust_art)

            if 'author_norm' in doc:
                author_norm = doc['author_norm']

            if 'aff' in doc:
                aff = doc['aff']

            if len(author_norm) != len(author):
                continue

            processingAuthors(conn, author, author_norm, aff, articleID)

    if count < numberOfRunning:

        start = start + nrows
        fillTables(start, name, conn, count, idCluster, token)

    else:
        #retorna true ou false
        return numFound > 0


if __name__ == '__main__':

    p = configargparse.ArgParser(default_config_files=['config.ini'])
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
    token = options.token
    update = options.update

    conn = create_connection(db_file)

    with conn:

        # if update:
        #     dbSize = db_size(conn)
        #
        #     myList = np.zeros(dbSize[0][0])
        #     update_full_column(conn, myList)



        clustersID, clustersName, simbId, flags = select_all_clusters(conn) #gets id, name, simbid,
        # flags for all clusters

        count = 0


        #mudar para for id in clustersID? mais pratico, sem count?

        for name in clustersName:

            flag = unicodeToINT(flags[count])
            print (count, " ", name)
            print ("flag ", flag)

            if flag == 1:
                print (name, " already queried")
                count += 1
                continue

            sys.stdout.flush()

            if simbId[count] is not None:
                print ("querying cluster")
                numFound = fillTables(1, simbId[count], conn, 0, clustersID[count], token)
                if numFound:
                    updateFlag(conn, clustersID[count], 1)

                time.sleep(1)

                count += 1

            else:
                count += 1
                continue

    conn.close()