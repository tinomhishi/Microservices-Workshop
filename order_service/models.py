from database import BASE, engine
from sqlalchemy import Column, Integer, String, Float, text


# Declaring a model for orders
# Inherits from the Base class, 
# The declarative base created using declarative_base from SQLAlchemy.
# This establishes the connection between the model and the database table

class Order(BASE):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    address = Column(String)
    customer_id = Column(Integer)
    customer_name = Column(String)

# create tables in database
BASE.metadata.create_all(bind=engine)