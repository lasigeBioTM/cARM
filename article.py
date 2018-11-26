import unicodedata
import sys

def articleToSQL(bibcode, title, year, doi):

    bibcode = unicodedata.normalize('NFKD',bibcode).encode('ascii', 'ignore')
    if title is not None:
        title = unicodedata.normalize('NFKD',title[0]).encode('ascii', 'ignore')
    if year is not None:
        year = int(year)

    if doi is not None:
        doi = unicodedata.normalize('NFKD',doi[0]).encode('ascii', 'ignore')

    return bibcode, title, year, doi


def create_article(conn, article):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO articles(bibcode, title, year, doi)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, article)
    conn.commit()

    return cur.lastrowid

def getArticleID(conn, bibcodeID):
    print bibcodeID
    cur = conn.cursor()
    cur.execute("SELECT id FROM articles WHERE bibcode==?", (bibcodeID,))
    rows = cur.fetchall()

    return rows[0][0]

def checkIfArticleExists(conn, bibcodeID):
    checker = False

    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM articles WHERE bibcode==?", (bibcodeID,))

    rows = cur.fetchall()
    if rows[0][0]!=0:

        checker = True

    return checker