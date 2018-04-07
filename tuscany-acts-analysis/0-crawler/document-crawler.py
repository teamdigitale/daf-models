
# coding: utf-8

# In[2]:


import urllib3
import json
import random
import time
import os
import logging


# # Crawl official documents from Tuscany Region

# Setup the loggers

# In[3]:


log = logging.getLogger('crawler_application')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('crawler.log')
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(fh)
log.addHandler(ch)


# Define output folder, output filename pattern

# In[4]:


out_folder = 'regione-toscana'

act_types = {
    'atti_dirigenti': 'DMON',
    'atti_presidente': 'DPG',
    'atti_giunta': 'DAD'
}

file_name = 'regione-toscana-result-type_{}-year_{:d}-from_{:d}-to_{:d}.json'
query = "http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start={:d}&num={:d}&filter=0&rc=1&q=inmeta%3AID_TIPO_PRATICA%3{}+AND+inmeta%3ADATA_ATTO%3A{}-01-01..{}-12-31+AND+inmeta%3ANUMERO%3A{}..{}+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AA"


# In[5]:


if not os.path.exists(out_folder):
    os.makedirs(out_folder)


# In[6]:


http_pool = urllib3.PoolManager()


# In[7]:


year = 2017
start = 0
num = 200
from_number = 0
to_number = 200


# In[8]:


example = query.format(start, num, act_types['atti_giunta'], year, year, from_number, to_number)


# In[9]:


example


# In[10]:


def download_data(start, num, act_name, year, from_number, to_number):

    log.info("start {}, num {}, act_name {}, year {}, from_number {}, to_number {}".format(
        start,num, act_name, year, from_number, to_number))
    sleep_time = random.randint(2,5)
    log.debug('sleeping {} seconds'.format(sleep_time))
    time.sleep(random.randint(5,20))

    url = query.format(start, num + 1, act_types[act_name], year, year, from_number, to_number)
    log.info('requesting url {}'.format(url))
    res = http_pool.request('GET', url, retries=1)
    log.info('got status {} for url {}'.format(res.status, url))

    num_res = 0

    if res.status is 200:
        json_data = json.loads(res.data.decode('utf-8'))
        if 'RES' in json_data['GSP']:
            num_res = len(json_data['GSP']['RES']['R'])

            out_file_name = out_folder + "/" + file_name.format(act_name, year, from_number, to_number)

            with open(out_file_name, 'w') as f:
                f.write(res.data.decode('utf-8'))
                log.info('saved result in {}'.format(out_file_name))
        else:
            log.error('no results skipped {} \n {}'.format(url, json_data))
    else:
        log.error('status {} skipped {}'.format(res.status, url))

    res.close()
    return num_res



# In[11]:


# download_data(start, num, 'atti_giunta', year, from_number, to_number)


# In[12]:


years = list(range(2002,2019))
print(years)


# In[13]:


for act_name in act_types.keys():
    counter = 0
    for year in years:
        log.info('start crawling document of type {} for the year {}'.format(act_name, year))
        num_records = 1
        start = 0
        num = 200
        from_number = 0
        to_number = 200
        while num_records > 0:
            num_records = download_data(start, num, act_name, year, from_number, to_number)
            counter += num_records
            from_number = to_number
            to_number += num
        log.info('end crawling document of type {} for the year {} total number {}'.format(act_name, year, counter))


# In[ ]:


#json_data['GSP']['RES']['R'][1]


# In[ ]:


http_pool.clear()
