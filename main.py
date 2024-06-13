import requests
import time
import json
from tqdm import tqdm
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
access_token = config['Vkontakte']['access_token']


class VK:
   def __init__(self, access_token, my_id, version='5.199'):
       self.token = access_token
       self.id = my_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def utils_resolveScreenName(self):
       url = 'https://api.vk.com/method/utils.resolveScreenName'
       params = {'screen_name': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()['response']['object_id']

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id,
                 'fields': 'screen_name'}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def vk_download(self, offset=0, count=5):
       if my_id.isdigit() == True:
           response = requests.get('https://api.vk.com/method/photos.get', params={
               'owner_id': self.id,
               'access_token': self.token,
               'offset': offset,
               'count': count,
               'album_id': 'profile',
               'extended': 1,
               'photo_sizes': 1,
               'v': self.version
               })
       else:
           response = requests.get('https://api.vk.com/method/photos.get', params={
               'owner_id': f'{vk.utils_resolveScreenName()}',
               'access_token': self.token,
               'offset': offset,
               'count': count,
               'album_id': 'profile',
               'extended': 1,
               'photo_sizes': 1,
               'v': self.version
           })
       return response.json()


   def do_data(self):
       data = vk.vk_download()
       return data

   def get_photo_url(self):
       list_ph = []
       for photos in vk.do_data()['response']['items']:
           photo_url = photos['sizes'][-1]['url']
           list_ph.append(photo_url)
       return list_ph


   def get_file_name(self):
       likes = 0
       dict_j = {}
       dict_j['file_name'] = ''
       dict_j['size'] = ''
       list_photo_name = []
       for photos in vk.do_data()['response']['items']:
           for i in tqdm(range(vk.do_data()['response']['count'])):
               time.sleep(0.5)
           photo_url = photos['sizes'][-1]['url']
           name_photo = photos['likes']['count']
           date_photo = datetime.fromtimestamp(photos['date'])
           date_photo = str(date_photo)
           date_photo = date_photo.split(' ')[0]
           size_photo = photos['sizes'][-1]['type']
           if name_photo == likes:
               name_photo = str(name_photo) + str(date_photo)
           elif name_photo != likes:
               likes = name_photo
           file_name = photo_url.split('?')[0]
           file_name1 = file_name.split('/')[-1]
           file_name2 = str(name_photo) + file_name1[11:15]
           list_photo_name.append(file_name2)
           dict_j['file_name'] = file_name2
           dict_j['size'] = size_photo
           with open('save_file.json', 'a') as f:
               json.dump(dict_j, f)
       return list_photo_name


def start():
    try:
        my_id = input('Введите ID пользователя ВКонтакте: ')
        vk = VK(access_token, my_id)
        screen_name = vk.users_info()['response'][0]['screen_name']
        id1 = str(vk.users_info()['response'][0]['id'])

        if my_id == screen_name or my_id == id1:
            print('Фото будут загружены из профиля пользователя с именем: ')
            print(vk.users_info()['response'][0]['first_name'])


    except IndexError:
        print('Неверный ID, попробуйте снова')
    except UnboundLocalError:
        print('Неверный ID, попробуйте снова')
        my_id = id1
    return my_id

my_id = start()
vk = VK(access_token, my_id)

token_ya = input('Введите токен с Полигона Яндекс.Диска: ')



class Yandex:
   def __init__(self, token_ya):
       self.token = token_ya

   def do_folder(self):
       params = {'path': 'Kursovaya_rabota'}
       headers = {'Authorization': 'OAuth ' + self.token}
       response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                               params=params,
                               headers=headers)
       return 'Папка на Яндекс Диске создана :)'

   def download_photos(self):
       a = vk.get_file_name()
       b = vk.get_photo_url()

       for file_name, url_photo in zip(a, b):
           params = {'path': f'Kursovaya_rabota/{file_name}', 'url': f'{url_photo}'}
           headers = {'Authorization': 'OAuth ' + self.token}
           response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                               params=params,
                               headers=headers)
       return "Мы уже загрузили твои фото в папку, проверяй"


ya = Yandex(token_ya)




if __name__ == '__main__':
    # print(vk.users_info())
    # print(vk.utils_resolveScreenName())
    print(ya.do_folder())
    print(ya.download_photos())
    with open('save_file.json') as f:
        res = f.read()
    print(res)