from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurants = association_proxy("restaurant_pizzas", "restaurant")
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")



    # add serialization rules
    serialize_rules = ('-restaurant_pizzas',)


    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship

    restaurants = association_proxy("restaurant_pizzas", "pizza")
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")

    

    # add serialization rules
    serialize_rules = ('-restaurant_pizzas',)


    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)

    # add serilazation rules
    serialize_rules = ('-restaurant', '-pizza',) 

    # add validation
    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        if value > 30:
            raise ValueError("Price must be less than or equal to 30")
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
