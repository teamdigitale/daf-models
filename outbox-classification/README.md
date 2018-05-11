# Outbox Classifaction

This project investigates the use of neural network based methods to automatically classify documents released by public administrations.

This is with the idea of automating the dispatching of the mail received by the public administrations to the appropriate office.

Since the incoming mail is protected by privacy law, we provide an example using the outgoing mail.

As case study we considered the documents published by [Regione Toscana Atti](http://www.regione.toscana.it/bancadati/atti/).

The case study is composed by the following steps:

1. [web service exploration](./notebook/web_service_exploration): it describe how to get data from the service
2. document crawling: the script to crawl the documents
3. data preprocessing: a set of jupyter notebook with data exploration and wrangling
4. model creation: the approaches used to create the classification model.
5. web service: how the serve the final model via rest api.

## 2. Crawler

In order to crawl all the documents from the api endpoint we can run the following scripts:

```
$ python src/crawler.py -from_year 1998 -to_year 2019 -save_path data/atti_dirigente -act_type atti_dirigente

$ python src/crawler.py -from_year 1998 -to_year 2019 -save_path data/atti_giunta -act_type atti_giunta

$ python src/crawler.py -from_year 1998 -to_year 2019 -save_path data/atti_presidente -act_type atti_presidente
```

### 3. Data Preprocessing

 
