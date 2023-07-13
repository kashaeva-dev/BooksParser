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
        description="A science fiction books parser for tululu.org website. "
                    "You can download science fiction books by specifying range of pages with science fiction books. "
                    "Books will be saved in the 'books' folder, books' covers in the 'images' folder."
                    "You can specify the destination folder for these folders with the --dest_folder argument."
                    "A json file with books' info will be saved in the destination folder too."
                    "You can also skip downloading of books' images or texts with --skip_imgs or --skip_txt flags."
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
    parser.add_argument('--dest_folder',
                        help='You can specify folder the books will be downloaded to',
                        default='tululu_books',
                        )
    parser.add_argument('--skip_imgs',
                        action='store_true',
                        help="If specified the images won't be downloaded",
                        )
    parser.add_argument('--skip_txt',
                        action='store_true',
                        help="If specified the texts of the books won't be downloaded",
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

    ids = get_books_ids(args.start_page, args.end_page + 1)
    get_books_by_ids(ids, args.dest_folder, args.skip_imgs, args.skip_txt)


if __name__ == "__main__":
    main()
