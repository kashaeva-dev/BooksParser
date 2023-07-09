import argparse
import os
import logging.config
from urllib.parse import urljoin, urlsplit
from time import sleep

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from config import logger_config

logger = logging.getLogger("book_parser_logger")


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

    book_title = soup.title.text.split(', ')[0].split(' - ')
    book_name = " - ".join(book_title[:-1])
    book_author = book_title[-1]

    image_src = soup.find('div', class_='bookimage').find('img')['src']
    book_image_url = urljoin(response.url, image_src)

    book_genre = soup.find('span', class_='d_book').find('a').text

    comments = soup.find_all('div', class_='texts')
    book_comments = [comment.find('span').text for comment in comments]

    book_details = {
        'name': book_name,
        'author': book_author,
        'image_url': book_image_url,
        'genre': book_genre,
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


def main():
    logging.config.dictConfig(logger_config)
    logger.debug('Start parsing books')

    parser = create_parser()
    user_input = parser.parse_args()
    start_id = user_input.start_id
    end_id = user_input.end_id

    current_book = start_id
    timeout = 10

    while current_book < end_id + 1:
        logger.debug(f'Start while, trу to download book with ID {current_book}')
        try:
            url = f'https://tululu.org/b{current_book}/'
            book_page = requests.get(url, timeout=timeout)
            book_page.raise_for_status()

            check_for_redirect(book_page)

            book_details = parse_book_page(book_page)
            download_txt(current_book, book_details['name'], 'books', timeout)
            download_image(book_details['image_url'], 'images', timeout)

            logger.debug('Book was downloaded')
        except requests.exceptions.HTTPError:
            logger.error(f'Book with ID {current_book} is not found')
            current_book += 1
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            logger.error('Connection error')
            sleep(5)
        else:
            current_book += 1
            print('Название:', book_details['name'])
            print('Автор:', book_details['author'])
            print('')


if __name__ == "__main__":
    main()
