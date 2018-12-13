import sys
sys.path.append('/home/vmedu/Nutrition_bot')
import re
from flask import Flask
from EnginesClient import FoodEngineClient
from flask_assistant import Assistant, ask, tell, request
import logging


############### REGULAR EXPRESSIONS#####################
CALORIES_EXP = re.compile("how many calories in a[n]? (.*)")




#####################################################
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
app = Flask(__name__)
assist = Assistant(app, route='/')

class Speech:
    GET_PARAM = "The {} for {} are {}"
    ASK_PARAM = "for which food you want get {}?"


EngineClient = FoodEngineClient()
############### PRODUCT ATTRIBUTE ###################
@assist.action('ask_calories')
def ask_calories():
    speech = Speech.ASK_PARAM.format('calories')
    return ask(speech)

@assist.action('get_calories')
def get_calories(name):
    query = CALORIES_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'calories')
    return ask(speech)

@assist.action('ask_fat')
def ask_fat():
    speech = Speech.ASK_PARAM.format('fat')
    return ask(speech)

@assist.action('get_fat')
def get_fat(name):
    speech = getProductAttrByParam(name, 'fat')
    return ask(speech)

@assist.action('ask_sugar')
def ask_sugar():
    speech = Speech.ASK_PARAM.format('sugar')
    return ask(speech)

@assist.action('get_sugar')
def get_sugar(name):
    speech = getProductAttrByParam(name, 'sugar')
    return ask(speech)

@assist.action('ask_protein')
def ask_protein():
    speech = Speech.ASK_PARAM.format('protein')
    return ask(speech)

@assist.action('get_protein')
def get_protein(name):
    speech = getProductAttrByParam(name, 'protein')
    return ask(speech)

@assist.action('ask_carbohydrate')
def ask_carbohydrate():
    speech = Speech.ASK_PARAM.format('carbohydrate')
    return ask(speech)

@assist.action('get_carbohydrate')
def get_carbohydrate(name):
    speech = getProductAttrByParam(name, 'carbohydrate')
    return ask(speech)

@assist.action('ask_sodium')
def ask_sodium():
    speech = Speech.ASK_PARAM.format('sodium')
    return ask(speech)

@assist.action('get_sodium')
def get_sodium(name):
    speech = getProductAttrByParam(name, 'sodium')
    return ask(speech)


def getProductAttrByParam(name ,productAttr):
    res =  EngineClient.findProductByName(name)
    speech = Speech.GET_PARAM.format(productAttr, name, res.get(productAttr))
    return speech
############### PRODUCT ATTRIBUTE ###################




####################### AMIT FIRST TEST #################

@assist.action('greeting')
def greet_and_start():
    #pdb.set_trace()
    speech = "Hey! Are you male or female?"
    return ask(speech)

@assist.action("give-gender")
def ask_for_color(gender):
    if gender == 'male':
        gender_msg = 'Sup bro!'
    else:
        gender_msg = 'Haay gurl!'

    speech = gender_msg + ' What is your favorite color?'
    return ask(speech)



@assist.action('give-color', mapping={'color': 'sys.color'})
def ask_for_season(color):
    speech = 'Ok, {} is an okay color I guess'.format(color)
    return ask(speech)

@assist.action('ask-allergies')
def ask_for_allergies():
    speech = "Hey, what are your allergies?"
    return ask(speech)

@assist.action('give-allergies')
def give_allergies(allergie):
    speech = "ok so you are allergic to  {}".format(allergie)
    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)
