from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Customer

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ("id", "name", "address")
