import requests
import pprint
from datetime import datetime


class VKClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id, count):
        self.token = token
        self.user_id = user_id
        self.convert_user_id()
        self.photo_params = []
        self.albums = {}
        self.list_likes = []
        self.get_photos_params(count, self.get_album())
        self.give_file_name()

    def get_common_params(self):
        return {
            'access_token': self.token,
            'owner_id': self.user_id,
            'v': '5.131'
        }

    def _build_url(self, api_method):
        return f"{self.API_BASE_URL}/{api_method}"

    def convert_user_id(self):
        if isinstance(self.user_id, str):
            params = self.get_common_params()
            params.update({'user_ids': self.user_id})
            response = requests.get(self._build_url('users.get'), params=params)
            data = response.json()
            self.user_id = data.get('response')[0].get('id')

    def get_album(self):
        params = self.get_common_params()
        params.update({'need_system': 1})
        response = requests.get(self._build_url('photos.getAlbums'), params=params)
        data = response.json()
        for i in data.get('response').get('items'):
            name_album = i.get('title')
            id_album = i.get('id')
            self.albums.update({name_album: id_album})
        pprint.pprint(self.albums)
        number = input('ВЫБЕРЕТЕ И ВСТАВТЕ НОМЕР, ИНТЕРЕСУЮЩЕГО ВАС АЛЬБОМА: ')
        return number

    def get_photos_params(self, count, album):
        params = self.get_common_params()
        params.update({'album_id': album, 'extended': 1, 'rev': 1})
        try:
            response = requests.get(self._build_url('photos.get'), params=params)
            data_json = response.json().get('response').get('items')[:count]
            for i in data_json:
                photos_id = i.get('id')
                photos_date = datetime.utcfromtimestamp(i.get('date')).strftime('%d-%m-%Y')
                sorted_size = sorted(i.get('sizes'), key=lambda x: x.get('height'))
                photos_url = sorted_size[-1].get('url')
                photos_size = sorted_size[-1].get('type')
                photos_likes = i.get('likes').get('count')
                photos_dict = {'id': photos_id, 'date': photos_date, 'link': photos_url,
                               'size': photos_size, 'likes': photos_likes}
                self.photo_params.append(photos_dict)
                self.list_likes.append(photos_likes)
        except AttributeError:
            print('Проверьте свой ID и TOKEN')

    def give_file_name(self):
        for count, value in enumerate(self.photo_params):
            if self.list_likes.count(value.get('likes')) > 1:
                name_img = f"{str(value.get('likes'))}-{value.get('date')}"
                self.photo_params[count].update({'file_name': name_img})
            else:
                self.photo_params[count].update({'file_name': value.get('likes')})


def get_token_vk():
    oauth_base_url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': 51707794,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'page',
        'scope': 'photos',
        'response_type': 'token'
    }
    oauth_url = requests.get(oauth_base_url, params=params)
    print(oauth_url.url)
