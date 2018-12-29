import sys
sys.path.append('/home/vmedu/Nutrition_bot')
import re
from flask import Flask
from EnginesClient import FoodEngineClient
from flask_assistant import context_manager
from flask_assistant import Assistant, ask, tell, request, event, build_item
import logging
import pdb
import User
import time
from multiprocessing.pool import ThreadPool

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
userHealthyRes = ''
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


####################### ALLERGIES #################


@assist.action('start-allergies')
def start_allergies():
    context_manager.add('await_for_food', lifespan=10)
    speech = "sure, what is your allergy?"
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
    if context is None:
        speech = "sorry, can you please remind me what is your allergy?"
        return ask(speech)
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
####################################################################

######################## healtier ############################
@assist.action('get-healthy')
def get_healthy(product):
    EngineClient.getHealtyFood(product)
    speech = "I'm looking for healthier food, in the mean time, can you tell me what is the color of an apple?"
    return ask(speech)
    
@assist.action('retrive-healthy')
def retrive_healthy(color):
    time.sleep(3)
    context = context_manager.get('healthy')
    product = context.parameters['product']
    res = EngineClient.getHealtyResult()
    if res == 'WAIT':
        time.sleep(3)
        res = EngineClient.getHealtyResult()
    if res == 'WAIT':
        speech = "umm I think I saw an apple in that color once. but any way, I'm sorry I couldn't find it please try with another product"
    if res is None:
        speech = "umm I think I saw an apple in that color once. but any way, I'm Sorry, I couldn't find healtier food than {product}".format(product=product)
    elif res == False:
        speech = "umm I think I saw an apple in that color once. but Sorry, I'm not familiar with this product, please try another"
    elif res == True:
        speech = "umm I think I saw an apple in that color once, but any way {product} is healthy".format(product=product)
    else:
        #is value is necessary here?
        healthier_product_name = res.get('name')
        speech = "umm I think I saw an apple in that color once. any way I found that {healtier} is healtier than {product}".format(healtier=healthier_product_name, product=product)
    return ask(speech)

@assist.action('get-mail')
def get_mail():
    context = context_manager.get('get-age-followup')
    
    age = context.parameters['age']['amount']
    prefernce = context.parameters['food-perference']
    gender = context.parameters['gender']
    weight = context.parameters['unit-weight']['amount']
    height = context.parameters['unit-length']['amount']
    email = context.parameters['email']
    activity = context.parameters['activity-level']
    user = User.User(gender=gender, age=age, weight=weight,
                     height=height, taste=prefernce, activityLevel=activity,
                     email=email)
    menu = EngineClient.createMenuAndSendMail(user)
    
    speech = "thank you"
    return ask(speech)
    
if __name__ == '__main__':
    app.run(debug=True)
