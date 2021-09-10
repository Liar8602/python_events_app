from app import create_app
from app.base import get_payload, collect_details
from init_db import get_or_create_category, get_or_create_resource


app = create_app()

with app.app_context():
    resource = 'https://afisha.ru'
    categories = [('concert', 'concerts'), ('movie', 'cinema'),
                  ('theatre', 'theatre'), ('exhibition', 'exhibitions')]
    for category_name, category_link in categories:
        data = get_payload(f'ufa/{category_link}/')['Widget']['CardsCarousels']
        result = collect_details(data, category_name, resource)
        get_or_create_category(category_name)
        get_or_create_resource(resource)
