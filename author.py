import unicodedata
from author_article import *

def unicodeToString(unicode):
    if unicode is not None:
        string = unicodedata.normalize('NFKD', unicode).encode('ascii', 'ignore')
    else:
        string = None

    return string


def unicodeToINT(unicode):
    if unicode is not None:
        myInt = int(unicode)

    else:
        myInt = None

    return myInt

def create_author(conn, author):
    #cluster = (bibcode, title, year, doi);
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO authors(name, shortName, affiliation)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, author)
    conn.commit()
    return cur.lastrowid


def processingAuthors(conn, authorsNames, authorsNamesNorm, affiliation, articleID):


    indexCount = 0
    for author in authorsNames:
        name = unicodeToString(author)

        nameNorm = unicodeToString(authorsNamesNorm[indexCount])

        aff = unicodeToString(affiliation[indexCount])

        indexCount+=1

        author = (name,nameNorm,aff);

        authorID = create_author(conn, author)

        auth_art = (authorID, articleID);

        create_author_article(conn, auth_art)


