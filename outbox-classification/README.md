# Outbox Classifaction

This project investigates the use of neural network based methods to automatically classify documents released by public administrations.

This is with the idea of automating the dispatching of the mail received by the public administrations to the appropriate office.

Since the incoming mail is protected by privacy law, we provide an example using the outgoing mail.

As case study we considered the documents published by [Regione Toscana Atti](http://www.regione.toscana.it/bancadati/atti/).

The case study is composed by the following steps:

1. [web service exploration](./notebook/web_service _exploration) : it describe how to get data from the service
1. document crawling: the script to crawl the documents
2. data preprocessing: a set of jupyter notebook with data exploration and wrangling
3. model creation: the approaches used to create the classification model.
4. web service: how the serve the final model via rest api.
