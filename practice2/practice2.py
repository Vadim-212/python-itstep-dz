import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def get_links(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    urls = [v['href'] for v in soup.find_all('a', href=True) if v['href'].startswith('http')]
    urls = [urlparse(i).netloc for i in urls]
    unique_urls = []
    for i in urls: 
        if i not in unique_urls: 
            unique_urls.append(i) 
    counted_urls = []
    url_counter = 0
    for url in unique_urls:
        for u in urls:
            if url == u:
                url_counter += 1
        counted_urls.append((url_counter, url))
        url_counter = 0
    counted_urls.sort(key=sortByUrlCount, reverse=True)
    return counted_urls


def sortByUrlCount(inputItem: tuple):
    return inputItem[0]


if __name__ == "__main__":
    url = 'https://google.com/'
    urls = get_links(url)
    for url in urls:
        print(f'{url[0]:<5} {url[1]}')