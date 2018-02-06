# Document Classification

This is a classical task in Machine Learning. However, here we investigate it application to classify documents received by a PA that need to be assigned to a predefined category.

This task is a time consuming task and it actually done manually by the protocol office.

### Data Definition

The dataset is composed by 4 attributes:

- ANNO: the year of the document
- NUMERO: a counter associated to the document
- OGGETTO: the subject of the document
- CLASSIFICA: the category assigned to the document

```
ANNO,NUMERO,OGGETTO,CLASSIFICA
2017,1,"APE 2016_12_28_02267130488_006 ...","P"
2017,2,"ape condominio via pa ..","P"
2017,3,"APE 2016_12_28_02267130488_006 ...","P"
2017,4,"APE 2016_12_28_02267130488_006 ...","P"
2017,5,"APE 2016_12_28_02267130488_006 ...","P"

```

> Moreover, we can have access to the pdf associated to these document. This can be useful to extract addition text to be used for the task.

The categories have a hierarchy with:
1. a macro category
2. multiple sub-categories

```
CODICE;TITOLO;NOTA
A#ATTIVIT� DI GOVERNO, AFFARI GIURIDICO-ISTITUZIONALI, COMUNICAZIONE#null
A.010#Attivit� giuridico normativa, di studio e di programmazione di settore#null
A.010.010#Attivit� istruttoria e proposte di atti normativi#Comprende tutta la documentazione che supporta una proposta di legge, delibera o regolamento, inclusa l'attivit� di studio, i contributi consulenziali e i pareri (provenienti sia da soggetti esterni che da strutture regionali), che siano parte integrante della proposta normativa. Le proposte normative potranno avere anche un carattere specifico e non necessariamente riguardare tutta l'attivit� cui inerisce il titolo.
A.010.020#Notificazioni alla Unione europea#Comprende anche le notifiche prodotte dal Presidente della Regione all'Unione europea.
A.010.030#Analisi di impatto normativo#Comprende anche l'analisi di impatto della regolazione (AIER).

```

### Goal Definition

This is a case o hierarchical [1](https://en.wikipedia.org/wiki/Hierarchical_classifier) multi-label classification [1](https://en.wikipedia.org/wiki/Multi-label_classification), [2](http://scikit-learn.org/stable/modules/multiclass.html) for which one sample can be assigned to more than one class.
We are going to evaluate algorithms for:

1. macro-category,
2. multi label and
3. hierarchical Classification

## Steps

### Dataset Preprocessing  

Since we are going to apply deep-learning methods we need to transform the raw text into a numeric tensors. We are applying *text vectorization* to transform text into numeric tensors. In particular, we:

1. [segment text into words, and transform each word into a vector](./protocollo-vectorization-words.ipynb)
2. [segment text into words, remove stopwords, and trasnform each word into a vector](./protocollo-vectorization-words-stopwords.ipynb)
3. [segment text into characters, and transform each character into a vector](./protocollo-vectorization-chars.ipynb)

This will be done by using word embeddings.
Since we apply neural base methods we don't need to remove stop-words, but we can evaluate what is the impact of stopwords removal in the classification task.

### Split the Dataset

Basing on the size of the dataset we are going to split it into *training, validation and test set*.

### Algorithms selection and hyperparameters tuning


### Test the algorithms

### Results Discussion


# References
- [Evaluation Measures for Hierarchical Classification: a unified view and novel approaches](https://arxiv.org/abs/1306.6802)
- [HiNet: Hierarchical Classification with Neural Network](https://arxiv.org/abs/1705.11105)
