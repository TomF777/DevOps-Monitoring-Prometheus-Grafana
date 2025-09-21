# imports
import json
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

# configuration
app = Flask(__name__)
metrics = PrometheusMetrics.for_app_factory()
metrics.init_app(app)


products = [
 { 'id': 1, 'name': 'headphones' },
 { 'id': 2, 'name': 'laptop' },
 { 'id': 3, 'name': 'smartwatch' },
 { 'id': 4, 'name': 'bag' }
]

next_product_id = len(products) + 1


def get_product(id):
 return next((e for e in products if e['id'] == id), None)

def product_is_valid(product):
    for key in product.keys():
        if key != 'name':
            return False
    return True

@app.route('/')
def root():
    return "Flask App"

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ 'error': 'Product does not exist'}), 404
    return jsonify(product)


@app.route('/products', methods=['POST'])
def create_product():
    global next_product_id
    product = json.loads(request.data)
    if not product_is_valid(product):
        return jsonify({ 'error': 'Invalid product properties.' }), 400

    product['id'] = next_product_id
    next_product_id += 1
    products.append(product)

    return '', 201, { 'location': f'/products/{product["id"]}' }


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ 'error': 'Product does not exist.' }), 404

    updated_product = json.loads(request.data)
    if not product_is_valid(updated_product):
        return jsonify({ 'error': 'Invalid product properties.' }), 400

    product.update(updated_product)
    return jsonify(products)


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    global products
    product = get_product(id)
    if product is None:
        return jsonify({ 'error': 'Product does not exist.' }), 404

    products = [e for e in products if e['id'] != id]
    return jsonify(product), 200


if __name__ == '__main__':
   app.run(port=5000, host = "0.0.0.0", debug=False)
