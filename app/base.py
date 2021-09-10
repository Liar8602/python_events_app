import datetime
import requests
from app.event.models import Event
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()


def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()


def convert_date(date):
    date_format = '%Y-%m-%dT%H:%M:%S'
    date_update = datetime.datetime.strptime(date, date_format)
    return date_update


def direct_path(path):
    url = f'https://afisha.ru{path}'
    return url


def correct_text(data_descr):
    updated_text = data_descr.replace('<p>', '')
    text = updated_text.replace('</p>', '')
    return text


def get_description(path, category):
    url = path[1:]
    main_func = get_payload(url)
    if category == 'movie':
        data_descr = main_func['MovieCard']['Info']['Description']
    elif category == 'exhibition':
        if main_func['ExhibitionInfo']['DistributorInfo'] is None:
            data_descr = main_func['ExhibitionInfo']['Description']
        elif main_func['ExhibitionInfo']['Description'] == '':
            data_descr = main_func['ExhibitionInfo']['DistributorInfo']['Text']
        else:
            data_descr = None
    elif category == 'theatre':
        data_descr = main_func['PerformanceInfo']['Description']
    elif category == 'concert':
        if main_func['ConcertInfo']['DistributorInfo'] is None:
            data_descr = main_func['ConcertInfo']['Description']
        elif main_func['ConcertInfo']['Description'] == '' or main_func['ConcertInfo']['Description'] is None:
            data_descr = main_func['ConcertInfo']['DistributorInfo']['Text']
        else:
            data_descr = None
    if data_descr is not None:
        data_descr = correct_text(data_descr)
    return data_descr


def collect_details(category_lst, category, resource):
    tiles = [tile for item in category_lst for tile in item['Tiles']]
    all_events = []
    for tile in tiles:
        title = tile['Name']
        genre = tile['Badge']
        date_min = tile['ScheduleInfo']['MaxScheduleDate']
        date_max = tile['ScheduleInfo']['MinScheduleDate']
        if isinstance(date_min, str) and isinstance(date_max, str):
            date_start = convert_date(date_min)
            date_finish = convert_date(date_max)
        else:
            date_start, date_finish = None, None
        address = tile['Notice']['PlaceUrl']['Address']
        place = tile['Notice']['PlaceUrl']['Name']
        path = tile['Url']
        if tile['ScheduleInfo']['MinPrice'] is None:
            price = None
        else:
            price = tile['ScheduleInfo']['MinPrice']
        url = direct_path(path)
        description = tile['Verdict']  # краткая информация для main page
        img_path = tile['Image945x540']
        if img_path is None:
            img_url = None
        else:
            img_url = tile['Image945x540']['Url']
        text = get_description(path, category)  # для каждого события для карточки
        event = Event(title=title, genre=genre, date_start=date_start,
                      date_finish=date_finish, address=address, place=place,
                      price=price, url=url, description=description,
                      img_url=img_url, text=text, category_id=category,
                      resource_id=resource)
        all_events.append(event)
    try:
        s.bulk_save_objects(all_events)
        s.commit()
        s.close()
    except IntegrityError:
        s.rollback()
