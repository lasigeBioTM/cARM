# cARM
create Astro Ratings Matrix

cARM is a software tool that creates a dataset suitable for evaluating recommender systems for Open Cluster of Stars using Scientific Literature.

###Dependencies:
* python 2.7
* sqlite
* numpy
* pandas
* configargparse


###Configuration steps
* The first step is to create an account at ADS - follow the instructions in https://github.com/adsabs/adsabs-dev-api
to create your ADS API token

* Second, you need to create the sqlite database - the commands are in createDB.sql

* Third, make sure to complete the info at config.ini file, including the correct paths to the database and clusters file


###RUN

* Now you need to fill the database with the information about the clusters: 

```
python fillClustersTable.py
```

* Next step is performed to find all the articles for each cluster in our database

```
python fillTables.py 
```

###Create <user,item,rating> dataset
```
python /authorClusterMatrix/createAuthorClusterMatrix.py
```


#####Note:
<sub><sup>The script /clustersNameAnalysis/clustersNameAnalysis.py returns groups of names of clusters whose
simbadID was not found</sup></sub>


###Dataset 
For download of an example of dataset created with this software:
https://drive.google.com/drive/folders/17a5rSq1iIy4vsgAuj0TGHTY3UbaVpvqq?usp=sharing