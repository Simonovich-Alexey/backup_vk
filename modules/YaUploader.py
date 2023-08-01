import requests
import time
from tqdm import tqdm
from modules.VKClient import VKClient


class YaUploader(VKClient):
    API_URL_YA = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, user_id, token_yd, count=5):
        super().__init__(token, user_id, count)
        self.token_yd = token_yd
        self.check_folder()
        self.upload()

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
        # self.get_file_json()
        params = {'path': '/vk-backup/file-info.json', 'overwrite': True}
        response = requests.get(self.API_URL_YA + '/upload', headers=self.get_common_headers(), params=params)
        data = response.json().get('href')
        with open('file-info.json') as file:
            requests.post(data, files={'file': file})

    def upload(self):
        photo_params = tqdm(self.photo_params)
        for value in photo_params:
            photo_params.set_description("Upload: ")
            time.sleep(2)
            path = f'/vk-backup/{value.get("file_name")}.jpg'
            params = {'path': path, 'url': value.get('link')}
            requests.post(self.API_URL_YA + '/upload', headers=self.get_common_headers(), params=params)
