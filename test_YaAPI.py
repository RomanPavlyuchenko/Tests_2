import pytest
import requests
import json


class TestYaDiskAPI:
    @pytest.fixture(scope='module')
    def _setup_token(self):
        token = ''
        with open('token.json') as token_file:
            token = json.load(token_file).get('token')
        return token

    @pytest.fixture
    def setup_data(self, _setup_token):
        folder_name = 'test'
        data = {
            'headers': {

                    'Content-type': 'application/json',
                    'Authorization': 'OAuth {}'.format(_setup_token)
            },
            'params': {
                'path': folder_name
            },
            'name': folder_name

        }
        return data

    @pytest.fixture
    def url(self):
        return 'https://cloud-api.yandex.net/v1/disk/resources/'

    def test_get_directories(self, url, setup_data):
        params = {
            'path': '/'
        }
        response = requests.get(url, headers=setup_data['headers'], params=params)
        assert response.status_code == 200

    def test_create_directory_positive(self, url, setup_data):
        # pre_response = requests.get(url, headers=setup_data['headers'], params=setup_data['params'])
        # if pre_response.status_code == 200:
        #     pre_response = requests.delete(url, headers=setup_data['headers'], params=setup_data['params'])
        #     if pre_response.status_code != 204:
        #         pass
        # elif pre_response.status_code == 404:
        #     pass

        # по коду ответа на создание
        response = requests.put(url, headers=setup_data['headers'], params=setup_data['params'])
        assert response.status_code == 201

        # по коду ответа на наличие созданной папки на диске
        response = requests.get(url, headers=setup_data['headers'], params=setup_data['params'])
        assert response.status_code == 200

        # по наличию папки в списке папок на диске
        response = requests.get(url, headers=setup_data['headers'], params={'path': '/'})
        items = [i['name'] for i in response.json()['_embedded']['items']]
        assert setup_data['name'] in items

        # teardown
        requests.delete(url, headers=setup_data['headers'], params=setup_data['params'])

    def test_create_directory_400(self, url, setup_data):
        respone = requests.put(url, headers=setup_data['headers'])
        assert respone.status_code == 400

    def test_create_directory_401(self, url, setup_data):
        response = requests.put(url, params=setup_data['params'])
        assert response.status_code == 401

    def test_create_directory_404(self, url, setup_data):
        requests.put(url, headers=setup_data['headers'], params=setup_data['params'])

        response = requests.put(url, headers=setup_data['headers'], params=setup_data['params'])
        assert response.status_code == 409

        requests.delete(url, headers=setup_data['headers'], params=setup_data['params'])
