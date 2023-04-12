import random
from os import listdir
from os import path
from pathlib import Path
from time import sleep

import requests
import telegram
from environs import Env

from fetch_nasa import fetch_last_epic_images, fetch_random_apod_images
from fetch_spacex import fetch_spacex_launch


def upload_image(tg_bot_token, tg_channel_id, image_folder, image_name):
    bot = telegram.Bot(token=tg_bot_token)
    with open(path.join(image_folder, image_name), 'rb') as image:
        bot.send_document(chat_id=tg_channel_id, document=image)


def main():
    env = Env()
    env.read_env()

    image_folder = env.str('IMAGE_FOLDER', default='images')
    nasa_api_key = env.str('NASA_API_KEY', default='DEMO_KEY')
    tg_bot_token = env.str('TG_BOT_TOKEN')
    tg_channel_id = env.str('TG_CHANNEL_ID')

    seconds_in_day = 86400

    Path(image_folder).mkdir(parents=True, exist_ok=True)
    flight_number = 107

    try:
        fetch_random_apod_images(image_folder, nasa_api_key)
        fetch_last_epic_images(image_folder, nasa_api_key)
    except requests.exceptions.ConnectionError:
        print('Сайт nasa не отвечает.')
    except requests.exceptions.HTTPError:
        print('Ошибка! Не удалось получить список фотографий от nasa')

    try:
        fetch_spacex_launch(flight_number, image_folder)
    except requests.exceptions.ConnectionError:
        print('Сайт spacex не отвечает.')
    except requests.exceptions.HTTPError:
        print('Ошибка! Не удалось получить список фотографий от spacex')

    image_names = listdir(image_folder)

    while True:
        if not image_names:
            break
        image_name = random.choice(image_names)
        image_names.remove(image_name)

        upload_image(tg_bot_token, tg_channel_id, image_folder, image_name)
        sleep(seconds_in_day)


if __name__ == '__main__':
    main()
