from datetime import datetime
from os import path

import requests

from file_utils import download_image, get_file_extension


def fetch_random_apod_images(image_folder, nasa_api_key):
    nasa_apod_image_url = 'https://api.nasa.gov/planetary/apod'
    images_quantity = 30
    params = {'count': images_quantity, 'api_key': nasa_api_key}
    response = requests.get(nasa_apod_image_url, params=params)
    response.raise_for_status()
    random_apods = response.json()
    for num, apod in enumerate(random_apods, 1):
        image_url = apod.get('hdurl')
        if not image_url:
            continue
        file_extension = get_file_extension(image_url)
        image_name = f'nasa{num}{file_extension}'
        try:
            download_image(image_url, path.join(image_folder, image_name))
        except requests.exceptions.HTTPError:
            print('Ошибка! Не удалось загрузить фотографию:', image_url)


def fetch_last_epic_images(image_folder, nasa_api_key):
    params = {'api_key': nasa_api_key}
    epic_images_url = f'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_images_url, params=params)
    response.raise_for_status()
    response_payload = response.json()
    for image in response_payload:
        file_image_name, epic_image_url = get_epic_image_name_and_url(image)
        try:
            download_image(epic_image_url, path.join(image_folder, file_image_name), params)
        except requests.exceptions.HTTPError:
            print('Ошибка! Не удалось загрузить фотографию:', epic_image_url)


def get_epic_image_name_and_url(image):
    file_extension = '.png'
    image_date, _ = image['date'].split()
    image_date = datetime.fromisoformat(image_date).date().strftime("%Y/%m/%d")
    image_name = image['image']
    image_name = f'{image_name}{file_extension}'
    image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}'
    return image_name, image_url
