import sys
sys.path.append('/home/vmedu/Nutrition_bot')
import re
from flask import Flask
from EnginesClient import FoodEngineClient
from flask_assistant import context_manager
from flask_assistant import Assistant, ask, tell, request, event, build_item
import logging
import pdb

############### REGULAR EXPRESSIONS#####################
CALORIES_EXP = re.compile("how [many|much]+ calories ?are in [a|an]+ (.*)")
FAT_EXP = re.compile("how [many|much]+ fat ?is in [a|an] (.*)")
SUGAR_EXP = re.compile("how [many|much]+ sugar ?is in [a|an]+ (.*)")
PROTEIN_EXP = re.compile("how [many|much]+ protein|proteins ?are in [a|an]+ (.*)")
CARBS_EXP = re.compile("how [many|much]+ carbs|carbohydrates ?are in [a|an]+ (.*)")
SODIUM_EXP = re.compile("how [many|much]+ sodium ?is in [a|an]+ (.*)")


#####################################################

############### CONSTS #####################

ALLERGIES = {}

#####################################################
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
app = Flask(__name__)
assist = Assistant(app, route='/')

att_speech =  {'calories': "{product} has {result} calories",
  'sugar': "{product} has {result} grams of sugar in it",
  'carbohydrates': "{product} has {result} grams of carbohydrates in it",
  'protein': "{product} has {result} grams of proteins in it",
  'fat': "{product} has {result} grams of fat",
  'sodium': "{product} has {result} grams of sodium"}

class Speech:
    GET_PARAM = "The {} for {} are {}"
    ASK_PARAM = "for which food you want get {}?"

# Initiate EngineClient
EngineClient = FoodEngineClient()

@assist.action('get_calories')
def get_calories(product, attr):
    #query = CALORIES_EXP.findall(assist.request['result']['resolvedQuery'])
    print(product, attr)
    
    #TODO: seperate to two checks, and reply with the relevant info (attr or product)
    if not product or not attr:
        speech = "couldn't understand please try with another product"
        return ask(speech)
    result = getProductAttrByParam(product, attr)
    #speech = getProductAttrByParam(product, 'calories')
    speech = att_speech[attr].format(product=product, result=result)
    return ask(speech)


def getProductAttrByParam(name ,productAttr):
    res =  EngineClient.findProductByName(name)
    #speech = Speech.GET_PARAM.format(productAttr, name, res.get(productAttr))
    return round(float(res.get(productAttr)))
############### PRODUCT ATTRIBUTE ###################




####################### ALLERGIES #################


@assist.action('start-allergies')
def start_allergies():
    context_manager.add('await_for_food')
    speech = "sure, to what food you are allergic to?"
    return ask(speech)


@assist.action('get-allergies')
def get_allergies(allergan):
    context_manager.set('await_for_food','allergy',allergan)
    if not allergan:
        speech = "I couldn't understand that, please repeat"
        return ask(speech)
    speech = "Ok, and what food you would like to check?"
    return ask(speech)


@assist.action('get-food')
def get_food(product):
    context = context_manager.get('await_for_food')
    product = context.parameters['product']
    allergy = context.parameters['allergan']
    #TODO: need to check here what is happening if they have two allergies
    product = EngineClient.findProductByName(product)
    allergans_in_product = EngineClient.checkAllergies(product)
    if allergy in allergans_in_product:
        speech = "This food is not safe for you"
    else:
        speech = "I couldn't find any allergans in this food related to your allergies"
    return ask(speech)
######################################################

######################## healtier ############################
@assist.action('get-healthy')
def get_healthy(product):
    res = engine.getHealtyFood(product)
    if res is None:
        speech = "{product} is healthy enough".format(product=product)
    else:
        #is value is necessary here?
        healthier_product_name = res.get('name')
        speech = "I found that {healtier} is healtier than {product}".format(healtier=healthier_product_name, product=product)
    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)
