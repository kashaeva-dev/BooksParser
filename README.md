# Book Parser
This is a Python script that allows you to parse and download science fiction books from 
the [tululu.org](https://tululu.org/) website. It retrieves book details, downloads the book in text format,
and saves the book cover image.

You can download science fiction books by specifying the range of pages with science fiction books.
There are 701 pages and about 25 books per page.
Books will be saved in the `books` folder, books' covers in the `images` folder.
You can specify the destination folder for these folders with the `--dest_folder` argument.
A json file with books' info will be saved in the destination folder too.
By default `tululu_books` is the destination folder.
You can also skip downloading of books' images or texts with `--skip_imgs` or `--skip_txt` flags.
In the console, you will see the names and authors of the downloaded books.

## Installation
Clone the repository:
```shell
git clone https://github.com/kashaeva-dev/BooksParser
```
Create a virtual environment:
```
python -m venv env
```
Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage
To parse and download books from the first 5 pages run the script with the following command:
```
python parse_tululu.py --start_page 1 --end_page 5
```
The scrips will parse books from the first 5 pages. 
The script will display the names and authors of the downloaded books in the console.
The books will be saved to the books folder and the book covers to the images folder,
books' description will be saved to `book_details.json`. All these files will be saved in the `tululu_books` folder,
which is destination folder by default.

You can specify the destination folder for the books and images with the --dest_folder argument:
```
python parse_tululu.py --start_page 1 --end_page 5 --dest_folder my_folder
```
Now all the data will be saved in the `my_folder` folder.

You can also skip downloading of books' images or texts with --skip_imgs or --skip_txt flags:
```
python parse_tululu.py --start_page 1 --end_page 5 --skip_imgs --skip_txt
```
The script will parse books from the first 5 pages and **will only save their description** to `book_details.json`
file in the `tululu_books` folder.
The script will parse the books within the specified pages' range.


**Notes:** 
- This script requires an active internet connection to access 
the [tululu.org](https://tululu.org/) website and download the books.
- The script will not download books that are absent on the website so in the books folder you may
find fewer books than the specified range.
- You can find book IDs that are absent on the website in the ```book_parser.log``` file.
