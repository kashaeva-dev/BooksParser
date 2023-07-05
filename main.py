import requests
import os
from contextlib import suppress
from pathvalidate import sanitize_filename

from bs4 import BeautifulSoup


def get_book(book_id):

    url = "https://tululu.org/txt.php"

    payload = {'id': book_id}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    check_for_redirect(response)

    return response.text


def download_txt(id, filename, folder):
    book = get_book(id)
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = sanitize_filename(filename)
    book_file = ".".join([filename, 'txt'])
    book_path = os.path.join(folder, book_file)


    with open(book_path, 'w') as file:
        file.write(book)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_details(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    book_details = soup.title.text.split(', ')[0]
    name, author = book_details.split(' - ')

    return name, author


def main():
    for id in range(1, 11):
        with suppress(requests.HTTPError):
            print(id)
            filename, _ = get_book_details(id)
            download_txt(id, filename, 'books')


if __name__=="__main__":
    main()
