#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
import os

# App setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Routes
class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict() for restaurant in restaurants], 200


class RestaurantByID(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(
            only=("id", "name", "address", "restaurant_pizzas.pizza")
        ), 200

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204


class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict() for pizza in pizzas], 200


class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            restaurant_id = data["restaurant_id"]
            pizza_id = data["pizza_id"]
            price = data["price"]
        except KeyError:
            return {"errors": ["Missing required fields"]}, 400

        try:
            restaurant_pizza = RestaurantPizza(
                restaurant_id=restaurant_id, pizza_id=pizza_id, price=price
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(
                only=(
                    "id",
                    "price",
                    "restaurant_id",
                    "pizza_id",
                    "pizza.name",
                    "pizza.ingredients",
                    "restaurant.id",
                    "restaurant.name",
                    "restaurant.address",
                )
            ), 201
        except ValueError as e:
            return {"errors": [str(e)]}, 400


# Register resources
api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantByID, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
