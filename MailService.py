from smtplib import SMTP
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



with open('UserKeepLocal.txt','r') as f:
    user = f.readline()[:-1]
    password = f.readline()


def send_email(htmlMsg, emailAddress):
    sender = 'MTA.SADNA2018@gmail.com'
    to = emailAddress

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Awesome menu is waiting for you!!"
    msg['From'] = sender
    msg['To'] = to

    text = "Awesome menu is waiting for you!!"
    html = htmlMsg

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    server.sendmail(sender, to, msg.as_string())
    server.quit()


def getProductsOfMealForMsg(meals):
    msgMeal = ''
    for meal in meals:
        msgMeal = msgMeal + "<p> {} {} of: {}</p>".format(meal.amount, meal.product.serving.servingTool,meal.product.name).lower()

    return msgMeal

def sendMenuMailToClient(user, menu):
    with open(os.path.join('.','templates','mailMsgHtml.txt'), 'r') as msgfile:
        breakfest = getProductsOfMealForMsg(menu.breakfest.lstProducts)
        lunch = getProductsOfMealForMsg(menu.lunch.lstProducts)
        dinner = getProductsOfMealForMsg(menu.dinner.lstProducts)
        breakOne = getProductsOfMealForMsg(menu.breakOne.lstProducts)
        breakTwo = getProductsOfMealForMsg(menu.breakTwo.lstProducts)

        html = """\

                    {}

                    """.format(msgfile.read())

        htmlAfterFill = html.replace('gender', user.gender) \
            .replace('DATE', "{}".format(datetime.datetime.now().date())) \
            .replace('age', str(user.age)) \
            .replace('weight', str(user.weight)) \
            .replace('height', str(user.height)) \
            .replace('foodpreference', user.taste) \
            .replace('Exercisefrequency', user.activityLevel) \
            .replace('BreakfastP', breakfest) \
            .replace('InBetween1', breakOne) \
            .replace('LunchtP', lunch) \
            .replace('InBetween2', breakTwo) \
            .replace('DinnerP', dinner)

        send_email(htmlAfterFill, user.email)

