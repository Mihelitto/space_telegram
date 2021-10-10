from time import sleep
from pathlib import Path
from os import path
from os import listdir
import random
import requests
from environs import Env
import telegram
from fetch_nasa import fetch_last_epic_images, fetch_random_apod_images
from fetch_spacex import fetch_spacex_launch

env = Env()
env.read_env()

image_folder = env.str('IMAGE_FOLDER', default='images')
tg_bot_token = env.str('TG_BOT_TOKEN')
tg_channel_id = env.str('TG_CHANNEL_ID')


def main():
    Path(image_folder).mkdir(parents=True, exist_ok=True)
    flight_number = 107

    try:
        fetch_random_apod_images()
        fetch_last_epic_images()
    except requests.exceptions.ConnectionError:
        print("Сайт nasa не отвечает.")
    except requests.exceptions.HTTPError:
        print("Ошибка! Не удалось получить список фотографий от nasa")

    try:
        fetch_spacex_launch(flight_number)
    except requests.exceptions.ConnectionError:
        print("Сайт spacex не отвечает.")
    except requests.exceptions.HTTPError:
        print("Ошибка! Не удалось получить список фотографий от spacex")

    image_names = listdir(image_folder)
    bot = telegram.Bot(token=tg_bot_token)

    while True:
        image_name = random.choice(image_names)
        image_names.remove(image_name)

        if not image_names:
            break

        with open(path.join(image_folder, image_name), 'rb') as image:
            bot.send_document(chat_id=tg_channel_id, document=image)
        sleep(60*60*24)


if __name__ == '__main__':
    main()
