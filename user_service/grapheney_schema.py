from graphene import ObjectType, Field, String, Int, List
from models import Customer, db

class CustomerType(ObjectType):
  id = Int(required=True)
  name = String(required=True)
  address = String()

class Query(ObjectType):
  customers = List(CustomerType, description="List of all customers")
  customer = Field(CustomerType, id=Int(required=True), description="Get a customer by ID")

  def resolve_customers(self, info):
    return Customer.query.all()

  def resolve_customer(self, info, id):
    return Customer.query.get(id)

class Mutation(ObjectType):
  createCustomer = Field(CustomerType, data=String(required=True), description="Create a new customer")
  updateCustomer = Field(CustomerType, id=Int(required=True), data=String(), description="Update a customer")
  deleteCustomer = Field(String, id=Int(required=True), description="Delete a customer")

  def mutate_createCustomer(self, info, data):
    customer = Customer(name=data)
    db.session.add(customer)
    db.session.commit()
    return customer

  def mutate_updateCustomer(self, info, id, data):
    customer = Customer.query.get(id)
    customer.name = data
    db.session.commit()
    return customer

  def mutate_deleteCustomer(self, info, id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return "Customer deleted"
