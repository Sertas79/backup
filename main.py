from tqdm import tqdm

import os
import json
import requests

token = 'y0__xDZmbmJARjblgMg8_XI-xI-S3IcjJ1mxMM7EbAPv0zDxancVg'

def search_dogs(breed_dog, token_user):
    """Creating a folder with images on yandex.disk using the API"""

    if uploading_images(breed_dog):
        files_image = os.listdir(f'images/{breed_dog}')
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'{breed_dog}'}
        headers = {'Authorization': f'{token_user}'}
        responses = requests.put(url, params=params, headers=headers)
        if responses.status_code != 201:
            print(f'Ошибка запроса 1: {responses.status_code}')
            return False

        for i in tqdm(files_image):
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                    params={'path': f'{breed_dog}/{i}'}, headers=headers)
            upload_url = response.json()['href']
            with open(f'images/{breed_dog}/{i}', 'rb') as f:
                responses = requests.put(upload_url, files={'file': f})
                if responses.status_code != 201:
                    print(f'Ошибка запроса: {responses.status_code}')
                    return False
    return False


def uploading_images(breed):
    """Uploading images using the API https://dog.ceo/dog-api/ """
    name_list_breeds = []

    # request all breeds on the website
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Ошибка запроса: {response.status_code}')
        return False
    url_breeds_list = response.json()['message']

    # search for the requested breed
    if breed in url_breeds_list:
        # we form a list depending on whether the given breed is sub-breed.
        if len(url_breeds_list[breed]) == 0:
            url_breed = f'https://dog.ceo/api/breed/{breed}/images'
            breed_image = requests.get(url_breed)
            if breed_image.status_code != 200:
                print(f'Ошибка запроса при получении всех пород(подпород): '
                      f'{breed_image.status_code}')
                return False
            name_list_breeds.extend(breed_image.json()['message'])
        else:
            for name in tqdm(url_breeds_list[breed]):
                url_breed = f'https://dog.ceo/api/breed/{breed}/{name}/images'
                breed_image = requests.get(url_breed).json()['message']
                if breed_image.status_code != 200:
                    print(f'Ошибка запроса при получении всех пород: '
                          f'{breed_image.stutus_code}')
                    return False
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
            if response.status_code != 200:
                print(f'Ошибка запроса: {response.status_code}')
                return False
            with open(f'images/{breed}/{breed}_{filename}', 'wb') as f:
                f.write(response.content)

        return True
    else:
        print('This dog breed is not listed in the database')
        return False



search_dogs('akita', token)

