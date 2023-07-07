import argparse
import os
import logging.config
from contextlib import suppress
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from config import logger_config

logger = logging.getLogger("book_parser_logger")


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_id, filename, folder):
    url = "https://tululu.org/txt.php"
    payload = {'id': book_id}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    check_for_redirect(response)

    book = response.text

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = ". ".join([str(book_id), sanitize_filename(filename)])
    book_path = os.path.join(folder, ".".join([filename, 'txt']))

    with open(book_path, 'w') as file:
        file.write(book)

    return True


def download_image(url, folder):
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    _, image_filename = os.path.split(urlsplit(url).path)

    if not os.path.exists(folder):
        os.makedirs(folder)

    image_path = os.path.join(folder, image_filename)

    with open(image_path, 'wb') as file:
        file.write(response.content)


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    book_details = {}
    book_details['name'], book_details['author'] = soup.title.text.split(', ')[0].split(' - ')

    image_src = soup.find('div', class_='bookimage').find('img')['src']
    book_details['image_url'] = urljoin('https://tululu.org/', image_src)

    book_details['genre'] = soup.find('span', class_='d_book').find('a').text

    comments = soup.find_all('div', class_='texts')
    book_details['comments'] = [comment.find('span').text for comment in comments]

    return book_details


def show_book_details(book_details, is_downloaded):
    if is_downloaded:
        print('Название:', book_details['name'])
        print('Автор:', book_details['author'])
        print('')


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
    for book_id in range(start_id, end_id + 1):
        try:
            book_details = parse_book_page(book_id)
            is_downloaded = download_txt(book_id, book_details['name'], 'books')
            download_image(book_details['image_url'], 'images')
        except requests.HTTPError:
            logger.error(f'Book with id {book_id} is not found')
            continue
        show_book_details(book_details, is_downloaded)



if __name__ == "__main__":
    main()
