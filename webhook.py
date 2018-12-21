import sys
sys.path.append('/home/vmedu/Nutrition_bot')
import re
from flask import Flask
from EnginesClient import FoodEngineClient
from flask_assistant import Assistant, ask, tell, request, event, build_item
from flask_assistant import context_manager
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

class Speech:
    GET_PARAM = "The {} for {} are {}"
    ASK_PARAM = "for which food you want get {}?"


EngineClient = FoodEngineClient()
############### ASK ###################
@assist.action('ask_calories')
# def ask_calories():
    # speech = Speech.ASK_PARAM.format('calories')
    # return ask(speech)
    
# @assist.action('ask_fat')
# def ask_fat():
    # speech = Speech.ASK_PARAM.format('fat')
    # return ask(speech)

# @assist.action('ask_sugar')
# def ask_sugar():
    # speech = Speech.ASK_PARAM.format('sugar')
    # return ask(speech)

# @assist.action('ask_protein')
# def ask_protein():
    # speech = Speech.ASK_PARAM.format('protein')
    # return ask(speech)

# @assist.action('ask_carbohydrate')
# def ask_carbohydrate():
    # speech = Speech.ASK_PARAM.format('carbohydrate')
    # return ask(speech)

# @assist.action('ask_sodium')
# def ask_sodium():
    # speech = Speech.ASK_PARAM.format('sodium')
    # return ask(speech)
###################################################################3


@assist.action('get_calories')
def get_calories(product):
    #query = CALORIES_EXP.findall(assist.request['result']['resolvedQuery'])
    print(product])
    #speech = getProductAttrByParam(query[0], 'calories')
    speech = getProductAttrByParam(product, 'calories')
    
    return ask(speech)


@assist.action('get_fat')
def get_fat():
    query = FAT_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(name, 'fat')
    return ask(speech)



@assist.action('get_sugar')
def get_sugar():
    query = SUGAR_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'sugar')
    return ask(speech)



@assist.action('get_protein')
def get_protein():
    query = PROTEIN_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'protein')
    return ask(speech)


@assist.action('get_carbohydrate')
def get_carbohydrate():
    query = CARBS_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'carbohydrate')
    return ask(speech)



@assist.action('get_sodium')
def get_sodium():
    query = SODIUM_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'sodium')
    return ask(speech)


def getProductAttrByParam(name ,productAttr):
    res =  EngineClient.findProductByName(name)
    speech = Speech.GET_PARAM.format(productAttr, name, res.get(productAttr))
    return speech
############### PRODUCT ATTRIBUTE ###################




####################### ALLERGIES #################


@assist.action('start-allergies')
def start_allergies():
    context_manager.add('allergies')
    ALLERGIES = {}
    speech = "sure, to what food you are allergic to?"
    
    return ask(speech)

@assist.context('allergies')
@assist.action('get-allergies')
def get_allergies(allergan):
    print(allergan)
    context_manager.set('allergies','allergy',allergan)
    ALLERGIES['allergy'] = allergan
    speech = "Ok, and what food you would like to check?"
    return ask(speech)

@assist.context('allergies')
@assist.action('get-food')
def get_food(product):
    #TODO: need to check here what is happening if they have two allergies
    product = EngineClient.findProductByName(product)
    allergans_in_product = EngineClient.checkAllergies(product)
    allergy  = ALLERGIES['allergy']
    if allergy in allergans_in_product:
        speech = "This food is not safe for you"
    else:
        speech = "I couldn't find any allergans in this food related to your allergies"
    return tell(speech)

if __name__ == '__main__':
    app.run(debug=True)
