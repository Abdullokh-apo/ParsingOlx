import json
import os

import requests
from bs4 import BeautifulSoup


def get_data(url):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.128 Safari/537.36 '
    }

    project_data_list = []

    iteration_count = 25
    print(f'Всего страниц {iteration_count}')

    for item in range(1,26):
        req = requests.get(url + f'?page={item}', headers)

        folder_name = f'data/data_{item}'

        if os.path.exists(folder_name):
            print('Папка уже существует')
        else:
            os.mkdir(folder_name)

        with open(f'{folder_name}/projects_{item}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        with open(f'{folder_name}/projects_{item}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        articles = soup.find_all('div', class_='offer-wrapper')

        project_urls = []
        for article in articles:
            project_url = article.find('td', class_='photo-cell').find('a').get('href')
            project_urls.append(project_url)

        for project_url in project_urls:
            req = requests.get(project_url, headers)

            project_name = project_url.split('/')[-1]

            with open(f'{folder_name}/page_{project_name}.html', 'w', encoding='utf-8') as file:
                file.write(req.text)

            with open(f'{folder_name}/page_{project_name}.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            project_data = soup.find('div', class_='content')

            try:
                project_title = project_data.find('div', class_='offer-titlebox').find('h1').text
            except Exception:
                project_title = 'Товар без названия!'

            try:
                project_price = project_data.find('div', class_='offer-titlebox__price').find('strong').text
            except Exception:
                project_price = 'Цена товара не указана'

            try:
                project_discription = project_data.find('div', class_='clr lheight20 large').text
            except Exception:
                project_discription = 'Товар не описан'

            try:
                project_img = project_data.find('div', class_='descgallery__image').find('img').get('src')
            except Exception:
                project_img = 'Фото товара отсутвует'

            project_data_list.append(
                {
                    'Название товара': project_title.strip(),
                    'Цена товара': project_price,
                    'Описание товара': project_discription.strip(),
                    'Фото товара': project_img,
                }
            )
        iteration_count -=1
        print(f'Страница #{item} завершена, осталось страниц {iteration_count}')

        if iteration_count == 0:
            print('Сбор данных завершена!!!')
    with open('projects_data.json', 'w', encoding='utf-8') as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)


get_data('https://www.olx.uz/elektronika/telefony/?page=')
