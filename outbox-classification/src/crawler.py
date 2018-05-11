import requests
import json
import logging
import utils
import argparse
import time

act_types = {
    'atti_dirigenti': 'DMON',
    'atti_presidente': 'DPG',
    'atti_giunta': 'DAD'
}


base_url = "http://www.regione.toscana.it/bancadati/search?site=atti&client=fend_json&output=xml_no_dtd&getfields=*&ulang=it&ie=UTF-8&proxystylesheet=fend_json&start={:d}&num={:d}&filter=0&rc=1&q=inmeta%3AID_TIPO_PRATICA%3{}+AND+inmeta%3ADATA_ATTO%3A{}-01-01..{}-12-31+AND+inmeta%3ANUMERO%3A{}..{}+AND+inmeta%3AALLEGATO_DESCRIZIONE%3Dvoid&sort=meta%3ACODICE_PRATICA%3AA"

log = logging.getLogger('RegioneToscanaCrawler')


class RegioneToscanaCrawler(object):

    __file_name = 'data-result-type_{}-year_{:d}-from_{:d}-to_{:d}.json'

    def __init__(self, act_type, output_path, years):
        self._act_type = act_type
        self._output_path = output_path
        self._years = years

        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler('{}/crawler-{}.log'.format(output_path, act_type))
        ch = logging.StreamHandler()

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        log.addHandler(fh)
        log.addHandler(ch)


    def __download_data(self, url, out_path):
        """download a url and save it in the out_path
        :url the: url to download the records
        :out_path: the path were the file is saved
        :return: the number records extracted
        """
        r = requests.get(url)
        log.info('processing url {}'.format(url))
        time.sleep(0.5)
        if r.status_code is 200:
            data = utils.extract_data(r.json())
            if len(data) > 0:
                log.info('saving file {}'.format(out_path))
                with open(out_path, 'w') as f:
                    json.dump(data, f)
                return len(data)
            else:
                log.error('no data for url {}'.format(url))
        else:
            log.error('go respone {} for url {}'.format(r.status_code, url))
        r.close()
        return 0

    def __process_year(self, year):
        """extracts all the records for the given year
        """
        log.info('processing year {}'.format(year))
        counter = 0
        num_records = 1
        start = 0
        num = 200
        from_number = 0
        to_number = 200
        
        while num_records > 0:
            log.info('starting extraction from {} to {} for year {}'.format(from_number, to_number, year))
            url = base_url.format(
                start,
                num,
                self._act_type,
                year,
                year,
                from_number,
                to_number
            )
            out_path = self._output_path + "/" + RegioneToscanaCrawler.__file_name.format(
                self._act_type,
                year,
                from_number,
                to_number
            )
            num_records = self.__download_data(url, out_path)
            counter += num_records
            from_number = to_number
            to_number += num
            
        log.info('extracted {} records for year {}'.format(counter, year))


    def start(self):
        for year in self._years:
            self.__process_year(year)

if __name__ == '__main__':
    acts = ' '.join(act_types.keys())
    parser = argparse.ArgumentParser(description="Regione Toscana Crawler")
    parser.add_argument('-from_year',help="the year to start", type=int)
    parser.add_argument('-to_year', help="the year to end", type=int)
    parser.add_argument('-save_path', help="the folder to save the data", type=str)
    parser.add_argument('-act_type', help='one value from {}'.format(acts))

    print(parser.error)

    opts = parser.parse_args()
    act_type = act_types[opts.act_type]

    years = list(range(opts.from_year, opts.to_year))
    crawler = RegioneToscanaCrawler(act_type,opts.save_path, years)
    crawler.start()