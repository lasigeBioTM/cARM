import numpy as np
import sys

def create_cluster(conn, cluster):

    #cluster = (name);
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO clusters(original_name, name,simbadId,flag)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, cluster)
    print (cur.lastrowid)
    conn.commit()
    return cur.lastrowid

def getClusterID(conn, name, newName):
    '''

    :param conn:
    :param name:
    :param newName:
    :return: cluster id
    '''
    cur = conn.cursor()

    cur.execute("SELECT id FROM clusters WHERE name==? or name==?", (name,newName))

    rows = cur.fetchall()

    return rows[0][0]


def checkIfclusterNameExists(conn, name, newName):
    '''

    :param conn: db connection
    :param name: name of the cluster
    :param newName: newName of the clusters (may be the same as name)
    :return: None, False, or True
    '''

    checker = False # neither name nor simbid exist

    cur = conn.cursor()

    cur.execute("SELECT simbadId, count(*) FROM clusters WHERE name==? or name==?", (name,newName))

    rows = cur.fetchall()
    print (rows)
    if rows[0][1]!=0 and rows[0][0] is not None:

        checker = True # name exists and have simbid

    elif rows[0][0] is None and rows[0][1]!=0 :
        checker = None # name exists but simbid is none

    print ("returning ", checker)
    return checker


def updateFlag(conn, id, newFlag):
    cur = conn.cursor()
    cur.execute("UPDATE clusters SET flag=? WHERE id=?", (newFlag, id))
    conn.commit()


def getClusterNameSimbIdNull(conn):
    '''

    :param conn: connection to database
    :return: 1d numpy array with the names without simbadID
    '''

    cur = conn.cursor()

    cur.execute("SELECT name FROM clusters WHERE simbadID is NULL GROUP BY name")

    rows = cur.fetchall()
    rows = np.array(rows, dtype=str).flatten()

    return rows


def updateName(conn, id, name):
    cur = conn.cursor()
    cur.execute("UPDATE clusters SET name=? WHERE id=?", (name, id))
    conn.commit()


def updateSimbID(conn, id, simbID):
    cur = conn.cursor()
    cur.execute("UPDATE clusters SET simbadID=? WHERE id=?", (simbID, id))
    conn.commit()