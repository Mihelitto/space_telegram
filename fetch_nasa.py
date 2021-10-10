from os import path
from datetime import datetime
import requests
from environs import Env
from utils import download_image, get_file_extension

env = Env()
env.read_env()

image_folder = env.str('IMAGE_FOLDER', default='images')
nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')


def fetch_random_apod_images():
    nasa_apod_image_url = 'https://api.nasa.gov/planetary/apod'
    images_quantity = 30
    params = {'count': images_quantity, 'api_key': nasa_api_key}
    response = requests.get(nasa_apod_image_url, params=params)
    response.raise_for_status()
    random_apods = response.json()
    for num, apod in enumerate(random_apods, 1):
        try:
            image_url = apod['hdurl']
        except KeyError:
            print('Не удалось получить ссылку на фотографию.')
            print(apod)
            continue
        file_extension = get_file_extension(image_url)
        image_name = f'nasa{num}{file_extension}'
        try:
            download_image(image_url, path.join(image_folder, image_name))
            print(image_url, 'Загружена')
        except requests.exceptions.HTTPError:
            print("Ошибка! Не удалось загрузить фотографию:", image_url)


def fetch_last_epic_images():
    params = {'api_key': nasa_api_key}
    epic_images_url = f'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(epic_images_url, params=params)
    response.raise_for_status()
    response_payload = response.json()
    for image in response_payload:
        file_image_name, epic_image_url = get_epic_image_name_and_url(image)
        try:
            download_image(epic_image_url, path.join(image_folder, file_image_name), params)
            print(epic_image_url, 'Загружена')
        except requests.exceptions.HTTPError:
            print("Ошибка! Не удалось загрузить фотографию:", epic_image_url)


def get_epic_image_name_and_url(image):
    file_extension = '.png'
    image_date, _ = image['date'].split()
    image_date = datetime.fromisoformat(image_date).date()
    image_name = image['image']
    epic_image_name = f'{image_name}{file_extension}'
    epic_image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date.year}/{image_date.month:02d}/{image_date.day:02d}/png/{image_name}.png?api_key={nasa_api_key}'
    return epic_image_name, epic_image_url
