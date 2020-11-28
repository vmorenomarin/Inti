[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cbe9dad067f94b799d4b5d79ab913a4e)](https://www.codacy.com/gh/colav/Inti?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=colav/Inti&amp;utm_campaign=Badge_Grade)

# Inti
Capture system from non scrapping data sources

## Example running save MAG in MongoDB
`python3 run_mamagloader.py --mag_dir=/storage/colav/mag_sample/ --db=MA`

## Example running request SciELO and build a MongoDB
`python3 run_scieloloader.py --db=scielo`

### Running creating an instance

```from ScieloRequest import ScieloRequest```\
```sr=ScieloRequest(db="Scielo")```

ScieloRequest has three methods to get collections, journals and articles. The next run secuence is recommended for good results.

- ```get_collections()```: To get collections from SciELO and its info about number of documents, countries, and other data. 
    - **How to use:** only run the method in the created instance.\
    **Example:** ```sr.get_collections()```
- ```get_journals()```: To get whole the journals from Scielo, saving the journals data.
    - **How to use:** only run the method in the created instance.\
    **Example:** ```sr.get_journals()```
- ```get_articles()```: To get whole the articles from Scielo, saving the articles data.
    - **How to use:** only run the method in the created instance.\
    **Example:** ```sr.get_journals()```

When run first method, a Mongo database is builded. After run is finished correctly, the Mongo database has three collections: collections, journals and stage (articles). 

### Using checkpoints methods

To get a chechpoint to recover the donwloaded articles state, the class has three methods.

* ```create_cache()```: This method builds a collection to verifies full downloaded journals.
    - **How to use:** only run the method in the created instance.\
    **Example:** ```sr.create_cache()```

If articles downloading is broke up, ```get_articles()method``` has to inner method to verifies the download articles, delete articles if journal has incompleted download items (articles) and continua from the 

#### **Checkpoint methods used by ```get_articles()``` method**

Next methods are used used in  



