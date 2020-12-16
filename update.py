from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

def findveggies():
    for veggieBurger in veggieBurgers:
        print(veggieBurger.id)
        print(veggieBurger.price)
        print(veggieBurger.restaurant.name)
        print("\n")

def findveggies2():
    for veggieBurger in veggieBurgers:
        if veggieBurger.price != '$6.00':
            veggieBurger.price = '$6.00'
            session.add(veggieBurger)
            session.commit()

PandaVeggieBurger = session.query(MenuItem).filter_by(id = 20).one()
# print(PandaVeggieBurger.price)

PandaVeggieBurger.price = '$6.00'
session.add(PandaVeggieBurger)
session.commit()


findveggies2()
findveggies()