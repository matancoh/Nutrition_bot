#!/usr/local/bin/python3
import sys
print(sys.executable)
print(sys.version)
import EnginesClient
from flask import Flask, request, jsonify



app = Flask(__name__)

engines = None


@app.route('/api/productByName/<name>', methods=['GET'])
def product_by_name(name):
    if engines is None:
        engine = EnginesClient.FoodEngineClient()

    res = engine.findProductByName(name)
    return jsonify(res.name)


@app.route('/api/topFiveProducts/<name>', methods=['POST'])
def product_by_name_top_five(name):
    if engines is None:
        engine = EnginesClient.FoodEngineClient()

    res = engine.findProductByNameTopFive(name)
    return jsonify(res)

@app.route('/api/product/<id>', methods=['POST'])
def product_by_id(id):
    if engines is None:
        engine = EnginesClient.FoodEngineClient()

    res = engine.getProductById(id)
    return jsonify(res)


