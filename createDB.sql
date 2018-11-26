In the command line:

sqlite3 dbName.db

CREATE TABLE IF NOT EXISTS articles (
    id integer PRIMARY KEY,
    bibcode text NOT NULL,
    title text,
    year integer,
    doi text
);

CREATE TABLE IF NOT EXISTS clusters (
    id integer PRIMARY KEY,
    name text NOT NULL,
    simbadID text,
    flag integer
);

CREATE TABLE IF NOT EXISTS cluster_article (
	idCluster integer,
	idArticle integer,
	FOREIGN KEY(idCluster) REFERENCES clusters(id),
	FOREIGN KEY(idArticle) REFERENCES articles(id)
);

CREATE TABLE IF NOT EXISTS authors (
    id integer PRIMARY KEY,
    name text NOT NULL,
    shortName text,
    affiliation text
);

CREATE TABLE IF NOT EXISTS author_article (
	idAuthor integer,
	idArticle integer,
	FOREIGN KEY(idAuthor) REFERENCES authors(id),
	FOREIGN KEY(idArticle) REFERENCES articles(id)
);


####add columns to table clusters

ALTER TABLE clusters ADD COLUMN RAJ2000 text;
ALTER TABLE clusters ADD COLUMN DEJ2000 text;
ALTER TABLE clusters ADD COLUMN Diam real;
ALTER TABLE clusters ADD COLUMN Dist real;
ALTER TABLE clusters ADD COLUMN E_BV real;
ALTER TABLE clusters ADD COLUMN Age real;
ALTER TABLE clusters ADD COLUMN pmRA real;
ALTER TABLE clusters ADD COLUMN pmDE real;
ALTER TABLE clusters ADD COLUMN Nc real;
ALTER TABLE clusters ADD COLUMN RV real;
ALTER TABLE clusters ADD COLUMN o_RV real;
ALTER TABLE clusters ADD COLUMN Fe_H real;
ALTER TABLE clusters ADD COLUMN raDeg real;
ALTER TABLE clusters ADD COLUMN decDeg real;
ALTER TABLE clusters ADD COLUMN l real;
ALTER TABLE clusters ADD COLUMN b real;
