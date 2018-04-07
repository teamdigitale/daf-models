# So, What can AI and Machine Learning do for Italian Public Administration?

Many public administrations (P.A.) in Italy still operate in an analogue world. They have several stand-alone solutions for data management and a plethora of offices that handle human resources, regulation, citizen requests, incoming and out-coming documents, payments and everything else correlated to public services.
All this cost to public employee time and resource, while to public citizen and private companies time and money.
In P.A. offices, there are a lot of everyday tasks that can be automated and where it can be possible leveraging [Machine Learning](https://en.wikipedia.org/wiki/Machine_learning) and [Artificial Intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence) to let the P.A. become more effective, efficient, and responsive. relate to that, a recent article from [Il Sole 24 Ore](http://www.infodata.ilsole24ore.com/2017/07/18/quanto-efficace-la-pubblica-amministrazione-italiana-lindice-oxford/) shows that Italy is at the 27th place with respect to the International Civil Service Effectiveness Index.

One question that could arise is `Are we proposing that Artificial Intelligence should replace public employees?` Of course not!, what we want is that machines address repetitive tasks and the employees work on other activities where human capabilities are required.

> We envision a society where humans take decision supported by data and not by subjective analysis.

With respect this goal as members of the [Digital Transformation Team](https://teamdigitale.governo.it/en/) we want to contribute by
sharing code, trained models, and tutorials to generate conversations and build value for diverse stakeholders of the public life. The open-sourcing of AI tools are likely to spur rapid innovation in P.A., where there is a need of updating and learning from each other.

### AI and Machine Learning for the P.A.

There are four clear techniques that be deployed to improve the P.A.:

1. Predictive Analytics: better predictions can enable better decisions
2. Detection: detect patterns within massive dataset in order to identify those that are abnormal or unusual
3. Computer Vision: identify objects, actions or characteristics; describe content; and, overall, automate labour-intensive cognitive tasks that would usually require human supervision
4. Natural Language Processing: enable machines to process and understand test and audio for automating tasks such as translation, interactive dialogue, classification and sentiment analysis.

## Automatic Documents Classification

Our first contribution is related to automatic classification of documents. In particular, we address the problem of classify the documents received by `Regione Toscana` using the text contained in their subject. Only in 2017 `Regione Toscana` received 302734 documents that has to be manually labeled and dispatched to 19 directive offices. Moreover, each office as a hierarchy of sub-offices and documents should be dispatched accordingly to that. This is a case of hierarchical [1](https://en.wikipedia.org/wiki/Hierarchical_classifier) multi-label classification [1](https://en.wikipedia.org/wiki/Multi-label_classification), [2](http://scikit-learn.org/stable/modules/multiclass.html) for which one sample can be assigned to more than one class.

The **goal** is to create a classifier exposed via [rest api](https://en.wikipedia.org/wiki/Representational_state_transfer) that can be use to automatically categorize documents. This allows `Regione Toscana` to save a lot of time of their employees while paying a small price in terms of wrongly classified documents.

Since these documents contains sensitive data, but we still want to share our exploration the subsequent posts uses as dataset built from all the [official documents published by Regione Toscana](http://www.regione.toscana.it/regione/leggi-atti-e-normative/atti-regionali). These are related to the same offices, while focusing on published documents and not on received.

The posts will focus on:
1. data wrangling and exploration
2. building a basic classifier that used Neural Networks
3. how to use regularization to improve the model accuracy while addressing over-fitting
4. the effect of distributed representations of words to improve the models
5. how to use [Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) to handle text as sequences of words
6. how to tune the model
7. how to deploy the model as a web service.

# References
- [Evaluation Measures for Hierarchical Classification: a unified view and novel approaches](https://arxiv.org/abs/1306.6802)
- [HiNet: Hierarchical Classification with Neural Network](https://arxiv.org/abs/1705.11105)
