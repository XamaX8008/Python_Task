import argparse
import itertools
import os
import pathlib
import re
import signal
import sys
import time
import urllib.request
import threading
from typing import Optional
from urllib.error import URLError, HTTPError

exit_event = threading.Event()


def load_content(url: str) -> Optional[bytes]:
    try:
        return urllib.request.urlopen(url, timeout=10).read().decode("UTF-8")
    except (HTTPError, URLError):
        return None


def links_search(page_number: int):
    start_link = 'http://habr.com'
    page_content = load_content(f"http://habr.com/ru/all/page{page_number}/")
    links_from_article = re.findall(r'href="(.*?)" data-article-link',
                                    page_content)
    list_links = [start_link + i for i in links_from_article]

    return list_links


def normalize_name(name):
    name = name.replace(' ', '_')
    name = name.replace(':', '.')
    name = name.replace('?', '.')
    name = name.replace('\\', '.')
    name = name.replace('/', '.')
    name = name.replace('*', '.')
    name = name.replace('"', '_')
    name = name.replace('<', '_')
    name = name.replace('>', '_')
    name = name.replace('|', '_')
    return name


def search_article_name(page_content):
    tmp_page_name = re.findall(
        r'<h1 lang="ru" class="tm-article-snippet__title '
        r'tm-article-snippet__title_h1"><span>(.*?)</span></h1>',
        page_content)

    if tmp_page_name:
        page_name = tmp_page_name[0]
    else:
        page_name = 'name not found'

    page_name = normalize_name(page_name)
    return page_name


def photo_search(page):
    page_content = load_content(page)
    list_links_to_photos = re.findall(
        r'img src="(https://habrastorage.org/.*?)"', page_content)

    page_name = search_article_name(page_content)

    return {page_name: list_links_to_photos}


def download_photos(dict_links, out_dir):
    if len(list(dict_links.values())[0]) != 0:
        page_name = list(dict_links.keys())[0]
        page_path = os.path.join(out_dir, page_name)

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        if not os.path.exists(page_path):
            os.mkdir(page_path)

        for link in dict_links[page_name]:
            picture_data = urllib.request.urlopen(link, timeout=20).read()
            filename = link.split("/")[-1]
            file = open(page_path + f"/{filename}", "wb")
            file.write(picture_data)
            file.close()
    else:
        print("На странице нет фото")


def signal_handler(signal, frame):
    print("Interrupt!")
    exit_event.set()


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    threads_list = []
    signal.signal(signal.SIGINT, signal_handler)
    links_list = links_search(1)
    page_number = 1

    while len(links_list) < articles:
        page_number += 1
        links_page = links_search(page_number)
        links_list = list(itertools.chain(links_list, links_page))

    for i in range(articles):
        dict_links = photo_search(links_list[i])

        if exit_event.is_set():
            [threads.join() for thread in threads_list]
            sys.exit()

        if threading.activeCount() - 1 < threads:
            thread = threading.Thread(target=download_photos,
                                      args=(dict_links, out_dir))
            thread.start()
            threads_list.append(thread)
        else:
            while threading.active_count() - 1 == threads:
                time.sleep(0.1)
            else:
                thread = threading.Thread(target=download_photos,
                                          args=(dict_links, out_dir))
                thread.start()
                threads_list.append(thread)

    for thread in threads_list:
        thread.join()


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [ARTICLES_NUMBER] THREAD_NUMBER OUT_DIRECTORY',
        description='Habr parser',
    )
    parser.add_argument(
        '-n', type=int, default=25, help='Number of articles to be processed',
    )
    parser.add_argument(
        'threads', type=int, help='Number of threads to be run',
    )
    parser.add_argument(
        'out_dir', type=pathlib.Path, help='Directory to download habr images',
    )
    args = parser.parse_args()

    run_scraper(args.threads, args.n, args.out_dir)


if __name__ == '__main__':
    main()
