import os
import pprint

import requests
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm


class VkApiClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.photo_params = []
        self.get_photos_params()
        # self.get_photo_likes()
        self.give_name()

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def _build_url(self, api_method):
        return f"{self.API_BASE_URL}/{api_method}"

    def get_photos_params(self):
        params = self.get_common_params()
        try:
            params.update({'owner_id': self.user_id, 'album_id': 'profile'})
            response = requests.get(self._build_url('photos.get'), params=params)
            item_photo = response.json().get('response').get('items')
            for i in item_photo:
                photos_id = i.get('id')
                photos_date = datetime.utcfromtimestamp(i.get('date')).strftime('%d-%m-%Y')
                photos_link = i.get('sizes')[-1].get('url')
                photos_size = i.get('sizes')[-1].get('type')
                photos_dict = {'id': photos_id, 'date': photos_date, 'link': photos_link, 'size': photos_size}
                self.photo_params.append(photos_dict)
        except AttributeError:
            print('Проверте свой ID и TOKEN')

    def give_name(self):
        list_likes = []
        for j in self.photo_params:
            list_likes.append(j.get('likes'))
        for count, i in enumerate(self.photo_params):
            if list_likes.count(i.get('likes')) > 1:
                name_img = f"{str(i.get('likes'))}-{i.get('date')}"
                self.photo_params[count].update({'name_img': name_img})
            else:
                self.photo_params[count].update({'name_img': i['likes']})

    def get_photo_likes(self):
        params = self.get_common_params()
        for count, i in enumerate(self.photo_params):
            params.update({'type': 'photo', 'owner_id': self.user_id, 'item_id': i.get('id')})
            response = requests.get(self._build_url('likes.getList'), params=params)
            likes = response.json().get('response').get('count')
            self.photo_params[count].update({'likes': likes})


class YaUploader(VkApiClient):
    API_URL_YA = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, user_id, token_yd):
        super().__init__(token, user_id)
        self.token_yd = token_yd
        self.get_disk()

    def get_disk(self):
        params = {'path': '/vk-backup'}
        headers = {"Authorization": "OAuth " + self.token_yd}
        response = requests.get(self.API_URL_YA, headers=headers, params=params)
        if not response.json().get('name'):
            self.create_folder()

    def create_folder(self):
        params = {'path': '/vk-backup'}
        headers = {"Authorization": "OAuth " + self.token_yd}
        requests.put(self.API_URL_YA, headers=headers, params=params)

    def upload(self):
        headers = {"Authorization": "OAuth " + self.token_yd}
        if len(self.photo_params) > 1:
            photo_params = tqdm(self.photo_params)
            for i in photo_params:
                photo_params.set_description("Upload: ")
                path = f'/vk-backup/{i.get("name_img")}.jpg'
                params = {'path': path, 'url': i.get('link')}
                requests.post(self.API_URL_YA + '/upload', headers=headers, params=params)


if __name__ == '__main__':
    load_dotenv()

    TOKEN_YD = os.getenv('TOKEN_YD')
    TOKEN_VK = os.getenv('TOKEN_VK')
    USER_ID = os.getenv('USER_ID')
    APP_ID = os.getenv('APP_ID')

    # OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
    # params = {
    #     'client_id': 51707794,
    #     'redirect_uri': 'https://oauth.vk.com/blank.html',
    #     'display': 'page',
    #     'scope': ['photos'],
    #     'response_type': 'token'
    # }
    #
    # oauth_url = requests.get(OAUTH_BASE_URL, params=params)
    # print(oauth_url.url)

    user_one = YaUploader(TOKEN_VK, 15777557, TOKEN_YD)

    user_one.upload()
