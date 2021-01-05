from flask import Flask, render_template, url_for, request, redirect, flash

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
        output += str(i.price) + '<br>'
        output += str(i.description) + '<br> <br>'

    return output


@app.route("/restaurant/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route("/restaurant/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu created successfully", "success")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        item.name = request.form['name']
        session.add(item)
        session.commit()
        flash("Menu item editted successfully", "success")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', item=item, restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu item deleted successfully", "success")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=item, menu_id=menu_id, restaurant_id=restaurant_id)


if __name__ == '__main__':
    app.secret_key = "123#@"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000 )