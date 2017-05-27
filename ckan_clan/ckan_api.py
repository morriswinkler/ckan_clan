import urllib3
import json
import csv
import io

class CkanApi(object):
    def __init__(self, api_key, demo=False):
        # urrlib3 pool
        self.http = urllib3.PoolManager()

        # api endpoint
        self.api_url = 'http://beta.ckan.org/api/3/'

        self.api_key = api_key

        if demo:
            # fetch against demo api
            self.api_url = 'http://demo.ckan.org/api/3/'

    @property
    def list_datasets(self):
        endpoint = 'action/package_list'

        response = self.http.request('GET', self.api_url + endpoint)

        assert response.status == 200
        response_dict = json.loads(response.data)
        assert response_dict['success'] is True
        return response_dict['result']

    def get_dataset(self, set_name):
        endpoint = 'action/package_show?id=' + set_name

        json_resp = self.http.request('GET', self.api_url + endpoint)

        assert json_resp.status == 200
        response_dict = json.loads(json_resp.data)
        assert response_dict['success'] is True

        csv_resp = self.http.urlopen('GET', response_dict['result']['resources'][0]['url'])
        assert csv_resp.status == 200

        csv_str = csv_resp.data.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_str))
        return csv_reader

    def count_datasets(self):
        endpoint = 'action/package_list'

        response = self.http.request('GET', self.api_url + endpoint)

        assert response.status == 200
        response_dict = json.loads(response.data)
        assert response_dict['success'] is True

        result = {'total': len(response_dict['result']), 'empty_urls': 0, 'foreign_urls': 0}

        for set_name in response_dict['result']:

            endpoint = 'action/package_show?id=' + set_name
            response = self.http.request('GET', self.api_url + endpoint)
            response_dict = json.loads(response.data)
            assert response_dict['success'] is True

            if response_dict['result']['resources'][0]['url'] == '':
                result['empty_urls'] += 1
            if response_dict['result']['resources'][0]['url'].startswith('http://beta.ckan.org'):
                result['foreign_urls'] += 1

        return result
