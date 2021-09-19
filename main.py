import requests
from pathlib import Path
from urllib.parse import unquote, urlsplit
from os import path

IMAGE_FOLDER = 'images'


def download_image(image_url, image_name):
    response = requests.get(image_url)
    with open(image_name, 'bw') as file:
        file.write(response.content)


def fetch_spacex_last_launch(flight_number):
    url = f'https://api.spacexdata.com/v3/launches/{flight_number}'
    response = requests.get(url)
    launch = response.json()
    image_urls = launch["links"]["flickr_images"]
    for num, image_url in enumerate(image_urls):
        download_image(image_url, path.join(IMAGE_FOLDER, f'spacex{num}.jpg'))
        print(image_url)


def get_file_extension(link):
    file_path = unquote(urlsplit(link).path)
    return path.splitext(file_path)[1]


def main():
    Path(IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)
    flight_number = 107
    fetch_spacex_last_launch(flight_number)


if __name__ == '__main__':
    main()
