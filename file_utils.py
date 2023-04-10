from os import path
from urllib.parse import unquote, urlsplit

import requests


def download_image(image_url, image_name, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    with open(image_name, 'bw') as file:
        file.write(response.content)


def get_file_extension(link):
    file_path = unquote(urlsplit(link).path)
    _, extension = path.splitext(file_path)
    return extension
