import logging.config
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import logger_config
from parse_tululu import get_books_by_ids

logger = logging.getLogger("parse_tululu_category_logger")

def get_books_ids():
    base_url = 'https://tululu.org/l55/'
    book_ids = []
    for page in range(1, 2):
        url = urljoin(base_url, str(page))
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        book_ids.extend([tag['href'].strip('/b') for tag in soup.select('.d_book .bookimage a')])

    return book_ids


def main():
    logging.config.dictConfig(logger_config)

    ids = get_books_ids()
    get_books_by_ids(ids)


if __name__ == "__main__":
    main()
