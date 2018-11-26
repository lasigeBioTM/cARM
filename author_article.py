def create_author_article(conn, auth_art):

    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO author_article(idAuthor,idArticle)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, auth_art)
    conn.commit()