import argparse
import logging.config
import os
import json
from time import sleep
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from config import logger_config

logger = logging.getLogger("parse_tululu_logger")


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_id, filename, folder, timeout=10):
    url = "https://tululu.org/txt.php"
    payload = {'id': book_id}

    response = requests.get(url, params=payload, timeout=timeout)
    response.raise_for_status()

    check_for_redirect(response)

    book = response.text

    os.makedirs(folder, exist_ok=True)

    filename = ". ".join([str(book_id), sanitize_filename(filename)])
    book_path = os.path.join(folder, ".".join([filename, 'txt']))

    with open(book_path, 'w') as file:
        file.write(book)


def download_image(url, folder, timeout=10):
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    check_for_redirect(response)

    _, image_filename = os.path.split(urlsplit(url).path)

    os.makedirs(folder, exist_ok=True)

    image_path = os.path.join(folder, image_filename)

    with open(image_path, 'wb') as file:
        file.write(response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    book_title = soup.title.text.split(' - ')
    book_name = book_title[0]
    book_author = book_title[1].split(', ')[0]

    image_src = soup.select_one('.bookimage img')['src']
    book_image_url = urljoin(response.url, image_src)

    book_genres = [genre.text for genre in soup.select('span.d_book a')]

    book_comments = [comment.text for comment in soup.select('.texts span')]

    book_details = {
        'name': book_name,
        'author': book_author,
        'image_url': book_image_url,
        'genres': book_genres,
        'comments': book_comments,
    }

    return book_details


def create_parser():
    parser = argparse.ArgumentParser(
        prog='Parse books from tululu',
        description="A book parser for tululu.org website. "
                    "You can download books by specifying the range of book ids. "
                    "Books will be saved in the 'books' folder, books' covers in the 'images' folder."
                    "In the console, you will see the names and authors of the downloaded books.",
    )
    parser.add_argument('start_id',
                        help='You should specify the start id of the books range',
                        type=int,
                        default=1)
    parser.add_argument('end_id',
                        help='You should specify the end id of the books range',
                        type=int,
                        default=10)
    return parser


def get_books_by_ids(ids):
    logging.config.dictConfig(logger_config)
    logger.debug('Start parsing books')

    current_book_index = 0
    timeout = 10

    books_details = []

    while current_book_index < len(ids):
        current_book = ids[current_book_index]
        logger.debug(f'Start while, trу to download book with ID {current_book} (index {current_book_index})')
        try:
            url = f'https://tululu.org/b{current_book}/'
            book_page = requests.get(url, timeout=timeout)
            book_page.raise_for_status()

            check_for_redirect(book_page)

            book_details = parse_book_page(book_page)
            download_txt(current_book, book_details['name'], 'books', timeout)
            download_image(book_details['image_url'], 'images', timeout)
            books_details.append(book_details)
            logger.debug('Book was downloaded')
        except requests.exceptions.HTTPError:
            logger.error(f'Book with ID {current_book} is not found')
            current_book_index += 1
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            logger.error('Connection error')
            sleep(5)
        else:
            current_book_index += 1
            print('Название:', book_details['name'])
            print('Автор:', book_details['author'])
            print('')

    books_details_json = json.dumps(books_details, indent=4, ensure_ascii=False)
    with open('books_details.json', 'w', encoding='utf-8') as file:
        file.write(books_details_json)


if __name__ == '__main__':
    get_books_by_ids([1, 2])
