import requests
import csv
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = 'https://myshows.me'
SEARCH_URL = 'https://myshows.me/search/all/'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# запрашиваем страницу, возвращаем объект bs4
def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    return None


# собираем ссылки на сериалы
def get_tvshow_url():
    links = set()
    page = 1001

    while len(links) < 24288:
        url = f'{SEARCH_URL}?page={page}'
        soup = get_soup(url)
        if not soup:
            break
        
        catalog = soup.select_one('div.ShowsCatalog__tiles')
        if not catalog:
            break
        
        show_links = catalog.select('a[href^="/view/"]')
        for link in show_links:
            full_url = BASE_URL + link.get('href')
            links.add(full_url)
        
        print(f'Страница {page} обработана, собрано {len(links)} ссылок')
        page += 1
        # time.sleep(1)

        if not show_links:
            break
    return list(links)


# извлекаем данные из страницы
def parse_tvshow_page(url):
    soup = get_soup(url)
    if not soup:
        return None
    
    try:
        # название
        title = soup.select_one('h1').text.strip()
        # описание
        description_tag = soup.select_one("div.HtmlContent p")
        description = description_tag.text.strip() if description_tag else "N/A"
        # постер
        image_tag = soup.select_one("div.PicturePoster-picture img")
        image_url = image_tag["src"] if image_tag else "N/A"

        info_rows = soup.select("tr.info-row")
        # жанры
        genres = "N/A"
        if len(info_rows) > 2:  # проверяем, что есть минимум 3 строки
            genre_tags = info_rows[2].select("td.info-row__value span")  # берем третий info-row, т.к в нем хранится информация о жанрах
            genres = ", ".join([g.text.strip() for g in genre_tags]) if genre_tags else "N/A"
        # дата выхода
        date = "N/A"
        if len(info_rows) > 0:  # Проверяем, есть ли строки
            date_text = info_rows[0].select_one("td.info-row__value").text.strip()  # берем первую строку т.к. там информация о дате
            date = date_text.split(" - ")[0].strip() if date_text else 'N/A'  # работает
    except AttributeError:
        return None

    return [url, image_url, title, description, genres, date]


# сохраняем в csv
def save_to_csv(data):
    with open('tvshows.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['page_url', 'image_url', 'title', 'description', 'genres', 'date'])
        writer.writerows(data)


# собираем все функции воедино
def main():
    print('Собираем ссылки на сериалы...')
    tvshow_links = get_tvshow_url()

    print('Начинаем парсить сериалы...')
    data = []
    for i, link in enumerate(tqdm(tvshow_links, desc='Парсим сериалы'), 1):
        result = parse_tvshow_page(link)
        if result:
            data.append(result)

        # time.sleep(1)
    
    print('Сохранение данных')
    save_to_csv(data)
    print('Данные сохранены')


# запуск
if __name__=='__main__':
    main()
