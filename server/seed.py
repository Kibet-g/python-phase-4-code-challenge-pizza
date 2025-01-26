#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # Clear existing data
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Create Restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="address1")
    bistro = Restaurant(name="Sanjay's Pizza", address="address2")
    palace = Restaurant(name="Kiki's Pizza", address="address3")
    restaurants = [shack, bistro, palace]

    # Create Pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    # Create RestaurantPizza (join table entries)
    print("Creating restaurant_pizzas...")
    rp1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=1)
    rp2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4)
    rp3 = RestaurantPizza(restaurant=palace, pizza=california, price=5)
    restaurant_pizzas = [rp1, rp2, rp3]

    # Add and commit all data
    print("Seeding database...")
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding complete!")
