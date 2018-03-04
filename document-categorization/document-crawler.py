
# coding: utf-8

# In[38]:


import urllib3
import json
import random
import time
import os
import logging


# In[39]:


logger = logging.getLogger('crawler_application')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('crawler.log')
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# In[40]:


out_folder = 'regione-toscana'
file_name = 'regione-toscana-result-{:d}-{:d}.json'


# In[41]:


if not os.path.exists(out_folder):
    os.makedirs(out_folder)


# In[42]:


http_pool = urllib3.PoolManager()


# In[43]:


url_base = "http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start={:d}&num={:d}&filter=0&rc=1&q=inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AD"


# In[46]:


def download_data(start, num):
    logger.info("start {}, num {}".format(start,num))
    sleep_time = random.randint(10,30)
    logger.debug('sleeping {} seconds'.format(sleep_time))
    time.sleep(random.randint(5,20))
    
    output_name = out_folder + "/" + file_name.format(start, start + num)
    url = url_base.format(start, num)
    logger.info('requesting url {}'.format(url))
    res = http_pool.request('GET', url, retries=1)
    logger.info('got status {} for url {}'.format(res.status, url))
    
    num_res = 0
    
    if res.status is 200:
        json_data = json.loads(res.data.decode('utf-8'))
        if 'RES' in json_data['GSP']:
            num_res = len(json_data['GSP']['RES']['R'])
            with open(output_name, 'w') as f:
                f.write(res.data.decode('utf-8'))
                logger.info('saved result in {}'.format(output_name))
        else:
            logger.error('no results skipped {} \n {}'.format(url, json_data))
    else:
        logger.error('status {} skipped {}'.format(res.status, url))
    
    status = res.status
    res.close()
    return num_res
    


# In[47]:


start = 1000
num = 100

num_records = 1
counter = 0

while num_records > 0:
    num_records = download_data(start, num)
    counter += num_records
    start += num
    logger.info('extracted {} records'.format(counter))


# In[24]:


#json_data['GSP']['RES']['R'][1]

