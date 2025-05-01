from tqdm import tqdm

import os
import json
import requests

token = ''

def search_dogs(breed_dog, token_user):
    """Creating a folder with images on yandex.disk using the API"""

    if uploading_images(breed_dog):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'{breed_dog}'}
        headers = {'Authorization': f'{token_user}'}
        requests.get(url, params=params, headers=headers)

        files_image = os.listdir(f'images/{breed_dog}')


        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'{breed_dog}'}
        headers = {'Authorization': f'{token_user}'}
        requests.put(url, params=params, headers=headers)

        for i in tqdm(files_image):
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                    params={'path': f'{breed_dog}/{i}'}, headers=headers)
            upload_url = response.json()['href']
            with open(f'images/{breed_dog}/{i}', 'rb') as f:
                requests.put(upload_url, files={'file': f})


def uploading_images(breed):
    """Uploading images using the API https://dog.ceo/dog-api/ """
    name_list_breeds = []

    # request all breeds on the website
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url).json()
    url_breeds_list = response['message']

    # search for the requested breed
    if breed in url_breeds_list:
        # we form a list depending on whether the given breed is sub-breed.
        if len(url_breeds_list[breed]) == 0:
            url_breed = f'https://dog.ceo/api/breed/{breed}/images'
            breed_image = requests.get(url_breed).json()['message']
            name_list_breeds.extend(breed_image)
        else:
            for name in tqdm(url_breeds_list[breed]):
                url_breed = f'https://dog.ceo/api/breed/{breed}/{name}/images'
                breed_image = requests.get(url_breed).json()['message']
                name_list_breeds.extend(breed_image)

        # completing task №4 "Сохранять информацию по фотографиям в json-файл с результатами."
        data_file_json = {'file_name': name_list_breeds}
        with open('result.json', 'w') as f:
            json.dump(data_file_json, f)

        # uploads images to disk
        if not os.path.isdir(f'images/{breed}'):
            os.mkdir(f'images/{breed}')
        for i in name_list_breeds:
            filename = i.split('/')[-1]
            response = requests.get(i)
            with open(f'images/{breed}/{breed}_{filename}', 'wb') as f:
                f.write(response.content)

        return True
    else:
        print('This dog breed is not listed in the database')
        return False



search_dogs('akita', token)

