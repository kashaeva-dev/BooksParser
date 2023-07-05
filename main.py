import requests
import os
from contextlib import suppress
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit

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

    filename = ". ".join([str(id), sanitize_filename(filename)])
    book_file = ".".join([filename, 'txt'])
    book_path = os.path.join(folder, book_file)


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


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    book_details = dict()
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


def main():
    for id in range(1, 11):
        with suppress(requests.HTTPError):
            book_details = parse_book_page(id)
            is_downloaded = download_txt(id, book_details['name'], 'books')
            download_image(book_details['image_url'], 'images')
            show_book_details(book_details, is_downloaded)


if __name__=="__main__":
    main()
