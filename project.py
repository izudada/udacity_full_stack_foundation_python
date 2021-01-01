from flask import Flask, render_template, url_for, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Restaurant, Base, MenuItem
 
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
def AllMenu():
    first_restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = first_restaurant.id)
    
    output = ''
    output += 'For ' + first_restaurant.name + '<br> <br>' 
    for i in items:
        output += i.name
        output += '<br>' 
        output += i.price + '<br>'
        output += i.description + '<br> <br>'

    return output


@app.route("/restaurant/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route("/restaurant/<int:restaurant_id>/new/", methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return "page to edit a menu item. Task 2 complete!"


@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/")
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000 )