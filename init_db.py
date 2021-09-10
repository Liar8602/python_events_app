from app.base import s
from app.models import Category, Resource


def get_or_create_category(name):
    try:
        category = s.query(Category).get(name=name)
    except:
        category = Category(name=name)
        s.add(category)
        s.commit()
    return category


def get_or_create_resource(name):
    try:
        resource = s.query(Resource).get(name=name)
    except:
        resource = Resource(name=name)
        s.add(resource)
        s.commit()
    return resource
