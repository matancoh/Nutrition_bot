import sys
sys.path.append('/home/vmedu/Nutrition_bot')
import re
from flask import Flask
from EnginesClient import FoodEngineClient
from flask_assistant import Assistant, ask, tell, request
from flask_assistant import context_manager
import logging


############### REGULAR EXPRESSIONS#####################
CALORIES_EXP = re.compile("how [many|much]+ calories ?are in [a|an]+ (.*)")
FAT_EXP = re.compile("how [many|much]+ fat ?is in [a|an] (.*)")
SUGAR_EXP = re.compile("how [many|much]+ sugar ?is in [a|an]+ (.*)")
PROTEIN_EXP = re.compile("how [many|much]+ protein|proteins ?are in [a|an]+ (.*)")
CARBS_EXP = re.compile("how [many|much]+ carbs|carbohydrates ?are in [a|an]+ (.*)")
SODIUM_EXP = re.compile("how [many|much]+ sodium ?is in [a|an]+ (.*)")


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
def get_fat():
    query = FAT_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(name, 'fat')
    return ask(speech)

@assist.action('ask_sugar')
def ask_sugar():
    speech = Speech.ASK_PARAM.format('sugar')
    return ask(speech)

@assist.action('get_sugar')
def get_sugar():
    query = SUGAR_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'sugar')
    return ask(speech)

@assist.action('ask_protein')
def ask_protein():
    speech = Speech.ASK_PARAM.format('protein')
    return ask(speech)

@assist.action('get_protein')
def get_protein():
    query = PROTEIN_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'protein')
    return ask(speech)

@assist.action('ask_carbohydrate')
def ask_carbohydrate():
    speech = Speech.ASK_PARAM.format('carbohydrate')
    return ask(speech)

@assist.action('get_carbohydrate')
def get_carbohydrate():
    query = CARBS_EXP.findall(assist.request['result']['resolvedQuery'])
    print(query[0])
    speech = getProductAttrByParam(query[0], 'carbohydrate')
    return ask(speech)

@assist.action('ask_sodium')
def ask_sodium():
    speech = Speech.ASK_PARAM.format('sodium')
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

@assist.action('start-allergies')
def start_allergies():
    context_manager.add('allergies')
    speech = "sure, to what food you are allergic to?"
    #return ask(speech)
    return event('get_allergy')

@assist.action('get-allergy')
def get_allergy(allergy):
    context_manager.set('allergies','allergy',allergy)
    print("amit, Done....")
    return tell("thanks! :)")
  
# @assist.promt_for('allergy', intent_name='')
# def promt_allergy(allergy):
    # spee
    

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
