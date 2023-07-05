# Book Parser
This is a Python script that allows you to parse and download books from 
the tululu.org website. It retrieves book details, downloads the book in text format,
and saves the book cover image.

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
To parse and download books, run the script with the following command:
```
python parse_tululu.py start_id end_id
```
Replace start_id with the starting book ID and end_id with the ending book ID.
The script will parse the books within the specified range.

## Example
```
python parse_tululu.py 1 10
```
This will parse and download books with IDs from 1 to 10.
The books will be saved in the books folder and the book covers in the images folder.
The script will display the names and authors of the downloaded books in the console.


**Notes:** 
- This script requires an active internet connection to access 
the tululu.org website and download the books.
- The script will not download books that are absent on the website so in the books folder you may
find fewer books than the specified range.