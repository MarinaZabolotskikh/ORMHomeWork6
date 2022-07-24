import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from models import create_tables,Publisher, Shop, Book, Stock, Sale

DSN = ''
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publ = input("Введите данные издателя: ")
query = session.query(Shop)
query = query.join(Stock, Stock.id_shop == Shop.id)
query = query.join(Book, Book.id == Stock.id_book)
query = query.join(Publisher, Publisher.id == Book.id_publisher)

try:
    publ = int(publ)
    res = query.filter(Publisher.id == publ)
except ValueError:
    res = query.filter(Publisher.name.like(publ))
for shops in res.all():
    print(shops)

session.close()