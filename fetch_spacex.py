from os import path
from environs import Env
import requests
from utils import download_image

env = Env()
env.read_env()

image_folder = env.str('IMAGE_FOLDER', default='images')


def fetch_spacex_launch(flight_number):
    url = f'https://api.spacexdata.com/v3/launches/{flight_number}'
    response = requests.get(url)
    response.raise_for_status()
    launch = response.json()
    image_urls = launch["links"]["flickr_images"]
    for num, image_url in enumerate(image_urls):
        try:
            download_image(image_url, path.join(image_folder, f'spacex{num}.jpg'))
            print(image_url, 'Загружена')
        except requests.exceptions.HTTPError:
            print("Ошибка! Не удалось загрузить фотографию:", url)
