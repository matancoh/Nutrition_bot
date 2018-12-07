#!/usr/local/bin/python3
import sys
print(sys.executable)
print(sys.version)
import EnginesClient
from flask import Flask, request, jsonify
app = Flask(__name__)

engine = EnginesClient.FoodEngineClient()

@app.route('/api/productByName/<name>', methods=['GET'])
def product_by_name(name):
    res = engine.findProductByName(name)
    return jsonify(res.name)

@app.route('/api/getIngredientsForProduct/<name>', methods=['GET'])
def getIngredientsForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.ingredients)

@app.route('/api/getEnergyForProduct/<name>', methods=['GET'])
def getEnergyForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.energy)

@app.route('/api/getProteinForProduct/<name>', methods=['GET'])
def getProteinForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.protein)

@app.route('/api/getFatForProduct/<name>', methods=['GET'])
def getProteinForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.fat)

@app.route('/api/getCarbohydrateForProduct/<name>', methods=['GET'])
def getCarbohydrateForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.carbohydrate)

@app.route('/api/getSugarsForProduct/<name>', methods=['GET'])
def getSugarsForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.sugars)

@app.route('/api/getSodiumForProduct/<name>', methods=['GET'])
def getSodiumForProduct(name):
    res = engine.findProductByName(name)
    return jsonify(res.sodium)

@app.route('/api/product/<id>', methods=['GET'])
def product_by_id(id):
    res = engine.getProductById(id)
    return jsonify(res)
