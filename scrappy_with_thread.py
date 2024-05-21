import concurrent.futures
import random

from logs import logger
import requests
import csv
from bs4 import BeautifulSoup
import time

popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
MAX_THREADS = 10

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def extract_movie_details(movie_link: str):
    time.sleep(random.uniform(0, 0.2))

    content = requests.get(url=movie_link, headers=headers).content

    data_soup = BeautifulSoup(content, 'html.parser')

    if data_soup is not None:
        title = None
        date = None

        movie_data = data_soup.find("section", attrs={'class': 'ipc-page-section'})

        if movie_data is not None:
            title = movie_data.find('h1', attrs={
                'data-testid': 'hero__pageTitle'
            }).get_text()

            date = movie_data.find('ul', attrs={
                'class': 'ipc-inline-list'
            }).find('a', attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text()

        rating = movie_data.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).find('span',
                                                                                                                attrs={
                                                                                                                    'class': 'sc-bde20123-1 cMEQkK'
                                                                                                                }).get_text()

        plot = movie_data.find('p', attrs={'data-testid': 'plot'}).find('span', attrs={
            'data-testid': 'plot-xs_to_m'}).get_text()

        with open('movies.csv', mode='a') as file:
            movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if all([title, date, rating, plot]):
                logger.info(f"writing: {title}, {date}, {rating}, {plot}")
                movie_writer.writerow([title, date, rating, plot])


def extract_movies(movie_links: list):
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool:
        pool.map(extract_movie_details, movie_links)


def main():
    start_time = time.time()

    content = requests.get(url=popular_movies_url, headers=headers).content

    soup = BeautifulSoup(content, 'html.parser')

    movies_list = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul', attrs={
        'class': 'ipc-metadata-list'
    })

    movie_items = movies_list.find_all('li', attrs={'class': 'ipc-metadata-list-summary-item'})

    movie_links = ["https://imdb.com" + movie.find('a')['href'] for movie in movie_items]

    extract_movies(movie_links)

    end_time = time.time()

    logger.info(f" tempo de espera aproximado: {end_time - start_time}")


if __name__ == '__main__':
    main()
