import requests
import os


def get_book(book_id):

    url = "https://tululu.org/txt.php"

    payload = {'id': book_id}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.text


def save_book(filename, book):
    if not os.path.exists('books'):
        os.makedirs('books')

    book_file = ".".join([filename, 'txt'])
    book_path = "/".join(['books', book_file])

    with open(book_path, 'w') as file:
        file.write(book)


def main():
    for id in range(1, 11):
        book = get_book(id)
        save_book(str(id), book)


if __name__=="__main__":
    main()
