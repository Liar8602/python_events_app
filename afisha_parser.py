import requests
from bs4 import BeautifulSoup as bs

URL = 'https://www.afisha.ru/ufa/schedule_cinema/?view=list'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }
DOMAIN = 'https://www.afisha.ru'


def get_request(url, params=None):
    try:
        result = requests.get(url, headers=HEADERS, params=params)
        result.raise_for_status()
        return result
    except(requests.RequestException, ValueError):
        return False

def links_dict(html):
    soup = bs(html, 'html.parser')
    links = []
    for link in soup.find_all('a', class_='new-list__item-link'):
        links.append(DOMAIN + link.get('href'))
    return links


def get_pages_count(html):
    soup = bs(html, 'html.parser')
    pages = soup.find_all('a', class_='_3GZQg')
    if pages:
        return int(pages[-1].get_text())
    else:
        return 1


def events_data(html):
    data_dict = links_dict(html)
    final_data = []
    for link in data_dict:
        events = get_request(link)
        if events.status_code == 200:
            final_data.append(get_content(events.text, link))
        else:
            continue
        return final_data


def get_content(events, link):
    soup = bs(events, 'html.parser')
    movies = soup.find('div', class_='_16qgW')
    movie_dict = {}
    movie_dict.update({
        'name': soup.find('div', class_='_3kkV1 dbGiX').get_text(),
        'description': movies.find('div', class_='new-list__item-verdict').get_text(),
        'link': link
    })
    return movie_dict


def parse():
    html = get_request(URL)
    if html.status_code == 200:
        actions = []
        count = get_pages_count(html.text)
        for page in range(2):
            print(f'Осталось {count - page}.', end="")
            html = get_request(URL, params={'page': page})
            actions.extend(events_data(html.text))
    else:
        print('Error')

if __name__ == '__main__':
    parse()
