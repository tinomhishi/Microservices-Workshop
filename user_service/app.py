from flask import Flask, jsonify, request, abort
from prometheus_flask_exporter import PrometheusMetrics
from flask_graphql import GraphQLView

import grapheney_schema


from models import db, Customer
from serializer import CustomerSchema

# import dotenv
graphql_view = GraphQLView(schema=grapheney_schema, graphiql=True)  # Enable GraphiQL interface

# USER = dotenv.get("USER")
# PWD = dotenv.get("PWD")
# DATABASE = dotenv.get("DATABASE")

USER = 'user_service'
PWD = 'user_service'
DATABASE = 'user_service'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PWD}@localhost/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.add_url_rule('/graphql', view_func=graphql_view)
metrics = PrometheusMetrics(app)

# Initialize SQLAlchemy
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    
path_prefix = "/api/v1"

# Routes
@app.route(f"{path_prefix}/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    return jsonify(customer_schema.dump(customers))

@app.route(f"{path_prefix}/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_schema = CustomerSchema()
    return jsonify(customer_schema.dump(customer))

@app.route(f"{path_prefix}/customers", methods=["POST"])
def create_customer():
    data = request.json
    print(f'>>>>>>>!!!>>>>>{data}')
    customer = Customer(name=data["name"], address=data.get("address", ""))
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "address": customer.address
    }), 201

@app.route(f"{path_prefix}/customers/<int:customer_id>", methods=["PATCH"])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_schema = CustomerSchema(partial=True)
    updated_customer = customer_schema.load(request.json, instance=customer, partial=True)
    data = request.json
    if "name" in data:
        customer.name = data["name"]
    if "email" in data:
        customer.email = data["email"]
    db.session.commit()
    return jsonify(customer_schema.dump(updated_customer)), 200

@app.route(f"{path_prefix}/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
