import requests
from bs4 import BeautifulSoup
import sys, os
import threading


def thread_function(name, urls):
    print(f'Thread {name} started')
    for url in urls:
        links = get_links(url)
        print(os.getpid(), len(links), url)


def get_links(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    return [v['href'] for v in soup.find_all('a', href=True) if v['href'].startswith('http')]


def main():
    num_threads = int(sys.argv[1])
    urls = sys.argv[2:]
    threads = []

    for index in range(num_threads):
        print(f'Create and start thread {index}')
        x = threading.Thread(target=thread_function, args=(index,urls,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
        print(f'Thread {index} done')
    

if __name__ == '__main__':
    main()
