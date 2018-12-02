import pdb
from flask import Flask
from flask_assistant import Assistant, ask, tell, request

import logging
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
app = Flask(__name__)
assist = Assistant(app, route='/')


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
