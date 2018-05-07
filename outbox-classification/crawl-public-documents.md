# Crawl Public Documents from Regione Toscana

The goal of this document is to describe how to crawl the public documents from [Regione Toscana Atti](http://www.regione.toscana.it/bancadati/atti/).
This page allow us to search across the documents produced by Regione Toscana.

![search page](./imgs/regione-toscana-search.png "Search Page")

Unfortunately, there isn't a clear why to download via api this documents.
But we noted that there is a json based API, and thus we are going to write a script to download all this data.

Each document has a detail page from which we can download the pdf documents.

![detail page](./imgs/regione-toscana-detail-doc.png "Detail Page")

## Url Analysis

- endpoint: http://www.regione.toscana.it/bancadati/search?
- type of document: site=atti
- client: client=fend_json
- output: output=xml_no_dtd
- fields: getfields=*
- ulang=it
- ie=UTF-8
- proxystylesheet=fend_json
- start=0
- num=10
- filter=0
- rc=1
- q=inmeta%3AID_TIPO_PRATICA%3DMON+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid
- sort=meta%3ACODICE_PRATICA%3AD

> example "atti giunta"
> http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start=0&num=10&filter=0&rc=1&q=inmeta%3AID_TIPO_PRATICA%3DAD+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AD

> example "atti presidente"
> http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start=0&num=10&filter=0&rc=1&q=inmeta%3AID_TIPO_PRATICA%3DPG+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AD

> example "atti dei dirigenti"
> http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start=0&num=10&filter=0&rc=1&q=inmeta%3AID_TIPO_PRATICA%3DMON+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AD

> example "tutti gli atti"
> http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start=0&num=10&filter=0&rc=1&q=inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AD
