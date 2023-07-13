import argparse
import logging.config
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import logger_config
from parse_tululu import get_books_by_ids

logger = logging.getLogger("parse_tululu_category_logger")

def get_books_ids(start_page=1, end_page=10):
    base_url = 'https://tululu.org/l55/'
    book_ids = []
    for page in range(start_page, end_page):
        url = urljoin(base_url, str(page))
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        book_ids.extend([tag['href'].strip('/b') for tag in soup.select('.d_book .bookimage a')])

    return book_ids


def create_parser():
    parser = argparse.ArgumentParser(
        prog='Parse books from tululu',
        description="A science fiction book parser for tululu.org website. "
                    "You can download science fiction books by specifying the range of science fiction books pages. "
                    "Books will be saved in the 'books' folder, books' covers in the 'images' folder."
                    "In the console, you will see the names and authors of the downloaded books.",
    )
    parser.add_argument('--start_page',
                        help='You should specify the start page of the books range',
                        type=int,
                        default=1)
    parser.add_argument('--end_page',
                        help='You should specify the end page of the books range',
                        type=int,
                        )
    return parser


def main():
    logging.config.dictConfig(logger_config)

    parser = create_parser()
    args = parser.parse_args()

    if args.start_page < 1:
        logger.error('Start page should be greater than 0')
        exit()

    if args.end_page is None:
        args.end_page = args.start_page

    if args.end_page < args.start_page:
        logger.error('End page should be greater than start page')
        exit()

    if args.end_page > 701:
        logger.error('End page should be equal to or less than 701')
        exit()

    ids = get_books_ids(args.start_page, args.end_page +1)
    get_books_by_ids(ids)


if __name__ == "__main__":
    main()
