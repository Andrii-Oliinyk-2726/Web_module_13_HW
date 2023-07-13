import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project_v2.settings")
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient("mongodb://localhost")

db = client.hw10_v2

authors = db.authors.find()

for author in authors:
    # print(author['fullname'])
    # Author.objects.get_or_create(
    #     fullname=author['fullname'],
    #     date_born=author['date_born'],
    #     location_born=author['location_born'],
    #     bio=author['bio'],
    # )
    try:
        obj = Author.objects.get(
            fullname=author['fullname'],
            date_born=author['date_born'],
            location_born=author['location_born'],
            bio=author['bio'],
        )
        print("AAAA", obj)
        # obj.save()
    except Author.DoesNotExist:
        obj = Author(
            fullname=author['fullname'],
            date_born=author['date_born'],
            location_born=author['location_born'],
            bio=author['bio']
        )
        print("QQQ", obj)
        obj.save()

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        author = db.authors.find_one({"_id": quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)


