import requests
from bs4 import BeautifulSoup

def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('main').find('header').find('h1')
    title_text = title_tag.text
    print(title_text)

    picture_url = soup.find('img', class_='attachment-post-image')['src']
    print(picture_url)
    print("")

    post_text_strings = []
    text_content = soup.find('div', class_='entry-content').text.split('\n')
    for string in text_content:
        if string != 'Additional Reading:':
            post_text_strings.append(string)
        else:
            break
    print("\n".join(post_text_strings))


if __name__ == '__main__':
    main()
