import sys

def create_cluster_article(conn, clust_art):

    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """

    sql = ''' INSERT INTO cluster_article(idCluster,idArticle)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, clust_art)
    conn.commit()


def checkIfClusterArticleExist(conn, id_cluster, id_article):
    '''
    verifies if set cluster-article exists in the table
    :param conn:
    :param id_cluster:
    :param id_article:
    :return:
    '''


    checker = False
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM cluster_article WHERE idCluster==? AND idArticle==?", (id_cluster,id_article))

    rows = cur.fetchall()

    if rows[0][0]!=0:
        checker = True

    return checker
