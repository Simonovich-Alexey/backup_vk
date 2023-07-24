import json
import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm


class VKClient:
    OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id, count):
        self.token = token
        self.user_id = user_id
        self.photo_params = []
        self.list_likes = []
        self.get_photos_params(count)
        self.get_photo_likes()
        self.give_file_name()

    def get_token_vk(self):
        params = {
            'client_id': 51707794,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': 'photos',
            'response_type': 'token'
        }
        oauth_url = requests.get(self.OAUTH_BASE_URL, params=params)
        print(oauth_url.url)

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def _build_url(self, api_method):
        return f"{self.API_BASE_URL}/{api_method}"

    def get_photos_params(self, count):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile'})
        try:
            response = requests.get(self._build_url('photos.get'), params=params)
            data_json = response.json().get('response').get('items')[:count]
            photo_params = tqdm(data_json)
            for i in photo_params:
                photo_params.set_description("Search foto: ")
                photos_id = i.get('id')
                photos_date = datetime.utcfromtimestamp(i.get('date')).strftime('%d-%m-%Y')
                sorted_size = sorted(i.get('sizes'), key=lambda x: x.get('height'))
                photos_url = sorted_size[-1].get('url')
                photos_size = sorted_size[-1].get('type')
                photos_dict = {'id': photos_id, 'date': photos_date, 'link': photos_url, 'size': photos_size}
                self.photo_params.append(photos_dict)
        except AttributeError:
            print('Проверте свой ID и TOKEN')

    def get_photo_likes(self):
        params = self.get_common_params()
        photo_params = tqdm(self.photo_params)
        for count, value in enumerate(photo_params):
            photo_params.set_description("Add likes: ")
            time.sleep(0.25)
            params.update({'type': 'photo', 'owner_id': self.user_id, 'item_id': value.get('id')})
            response = requests.get(self._build_url('likes.getList'), params=params)
            likes = response.json().get('response').get('count')
            self.photo_params[count].update({'likes': likes})
            self.list_likes.append(likes)

    def give_file_name(self):
        for count, value in enumerate(self.photo_params):
            if self.list_likes.count(value.get('likes')) > 1:
                name_img = f"{str(value.get('likes'))}-{value.get('date')}"
                self.photo_params[count].update({'file_name': name_img})
            else:
                self.photo_params[count].update({'file_name': value.get('likes')})

    def get_file_json(self):
        data_json = []
        for i in self.photo_params:
            file_dict = {'file_name': i.get('file_name'), 'size': i.get('size')}
            data_json.append(file_dict)
        with open('file-info.json', 'w') as file:
            json.dump(data_json, file, indent=2)


class YaUploader(VKClient):
    API_URL_YA = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, user_id, token_yd, count=5):
        super().__init__(token, user_id, count)
        self.token_yd = token_yd
        self.check_folder()
        self.upload()
        self.upload_json()

    def get_common_headers(self):
        return {"Authorization": "OAuth " + self.token_yd}

    def create_folder(self):
        params = {'path': '/vk-backup'}
        requests.put(self.API_URL_YA, headers=self.get_common_headers(), params=params)

    def check_folder(self):
        params = {'path': '/vk-backup'}
        response = requests.get(self.API_URL_YA, headers=self.get_common_headers(), params=params)
        if not response.json().get('name'):
            self.create_folder()

    def upload_json(self):
        self.get_file_json()
        params = {'path': '/vk-backup/file-info.json', 'overwrite': True}
        response = requests.get(self.API_URL_YA + '/upload', headers=self.get_common_headers(), params=params)
        data = response.json().get('href')
        with open('file-info.json') as file:
            requests.post(data, files={'file': file})

    def upload(self):
        photo_params = tqdm(self.photo_params)
        for value in photo_params:
            photo_params.set_description("Upload: ")
            path = f'/vk-backup/{value.get("file_name")}.jpg'
            params = {'path': path, 'url': value.get('link')}
            requests.post(self.API_URL_YA + '/upload', headers=self.get_common_headers(), params=params)


if __name__ == '__main__':
    load_dotenv()

    TOKEN_YD = os.getenv('TOKEN_YD')
    TOKEN_VK = os.getenv('TOKEN_VK')
    USER_ID = os.getenv('USER_ID')
    APP_ID = os.getenv('APP_ID')

    user_one = YaUploader(TOKEN_VK, 15777557, TOKEN_YD, 30)
    # user_one.get_token_vk()
