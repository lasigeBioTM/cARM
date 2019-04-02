from openCSV import *
from dbConnection import *
from cluster import *
import requests
import json
import time
import configargparse
import sys
from clusterNameRules import *



'''
File exclusive to get simbadIDs and fill the name, 
simbadid and flag of the table clusters
'''


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


def getSimbadCode(name):
    # URL to access the SIMBAB TAP interface (see also http://simbad.u-strasbg.fr/simbad/sim-tap in your browser)
    OBJECTS_SIMBAD_TAP_URL = 'http://simbad.u-strasbg.fr/simbad/sim-tap/sync'
    # URL to access the NED interface
    OBJECTS_NED_URL = 'http://ned.ipac.caltech.edu/srs/ObjectLookup'

    object_name = name
    simbad_id = None
    ned_id = None

    print("Translating '{}' to Simbad ID...".format(object_name))
    params = {
        'request': 'doQuery',
        'lang': 'adql',
        'format': 'json',
        'query': "SELECT basic.OID FROM basic JOIN ident ON oidref = oid WHERE id='{}';".format(object_name)
    }
    r = requests.post(OBJECTS_SIMBAD_TAP_URL, data=params)
    if r.ok:
        results = r.json()
        if len(results['data']) > 0:
            simbad_id = results['data'][0][0]

    print("Translating '{}' to NED ID...".format(object_name))
    payload = {"name": {"v": "{}".format(object_name)}}
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }
    r = requests.post(OBJECTS_NED_URL, data=json.dumps(payload), headers=headers)
    if r.ok:
        results = r.json()
        if 'Preferred' in results:
            ned_id = results['Preferred']['Name'].replace(' ', '_')

    if simbad_id and ned_id:
        id = ("{{\"(simbid:{}) OR (nedid:{})\"}}".format(simbad_id, ned_id))
        # id = ("{{\"query\": \"(simbid:{}) OR (nedid:{})\"}}".format(simbad_id, ned_id))
    elif simbad_id:
        id = ("{{\"(simbid:{})\"}}".format(simbad_id, ned_id))
    elif ned_id:
        id = ("{{\"(nedid:{})\"}}".format(simbad_id, ned_id))
    else:
        print("...object not found in Simbad nor NED")
        id = None

    print id
    return id


def create_clusters_table(clustersNames, conn):
    for name in clustersNames:
        print name
        newName = getNewName(name) # sript that corrects the names of the clusters

        if checkIfclusterNameExists(conn, name, newName):
            print name, " already exists"
            continue

        elif checkIfclusterNameExists(conn, name, newName) is None:
            print "updating existenting entry"
            # get new name acording to rules
            simbadID = getSimbadCode(newName)
            time.sleep(1)

            clusterID = getClusterID(conn, name, newName)

            updateName(conn, clusterID, newName)

            updateSimbID(conn, clusterID, simbadID)

        else:
            # create new entry
            simbadID = getSimbadCode(newName)
            time.sleep(1)

            clusterSQL = (newName, simbadID, 0); # sql to update name, simbadId, and flag (which is always zero in these phase)

            create_cluster(conn, clusterSQL)

            sys.stdout.flush()


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
    print(aggloCSVPath)
    columnName = options.columnName
    columnLimit = options.columnDevLimit
    db_file = options.db_file

    agglomerates = getAllDataFrame(aggloCSVPath) #gets all the data from the csv file

    clustersNameColumn = getColumn(agglomerates, columnName) # get the column "names"

    if columnLimit != 0:
        clustersNames = np.array(clustersNameColumn.head(n=columnLimit))  # returns only the 10 firts clusters

    else:
        clustersNames = clustersNameColumn

    clustersNames = deleteWhitesFromArray(np.array(clustersNames))

    conn = create_connection(db_file)

    with conn:

        create_clusters_table(clustersNames, conn)  # creates clustersTable
