from smtplib import SMTP
import Menu
import User
import os

recipients = ['MTA.SADNA2018@gmail.com']#, , 'zimerman@gmail.com', 'meidan89@gmail.com']


with open('UserKeepLocal.txt','r') as f:
    user = f.readline()[:-1]
    password = f.readline()


def send_email(message, status, emailAddress):
    fromaddr = 'MTA.SADNA2018@gmail.com'
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user , password)
    server.sendmail(fromaddr, emailAddress, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

def getProductsOfMealForMsg(meals):
    msgMeal = ''
    for meal in meals:
        msgMeal = msgMeal + "            - {} {} of: {}\n".format(meal.amount, meal.product.serving.servingTool,meal.product.name).lower()

    return msgMeal

def sendMenuMailToClient(user : User, menu: Menu.Menu):
    with open(os.path.join('.','templates','mailMsg.txt'), 'r') as myfile:
        breakfest = getProductsOfMealForMsg(menu.breakfest.lstProducts)
        lunch = getProductsOfMealForMsg(menu.lunch.lstProducts)
        dinner = getProductsOfMealForMsg(menu.dinner.lstProducts)
        breakOne = getProductsOfMealForMsg(menu.breakOne.lstProducts)
        breakTwo = getProductsOfMealForMsg(menu.breakTwo.lstProducts)

        data = myfile.read().replace('<fullname>',user.name)\
            .replace('<gender>', user.gender)\
            .replace('<age>', str(user.age)) \
            .replace('<weight>', str(user.weight)) \
            .replace('<height>', str(user.height)) \
            .replace('<foodpreference>', user.taste) \
            .replace('<Exercisefrequency>', user.activityLevel) \
            .replace('<Breakfast>', breakfest) \
            .replace('<BetweenFirst>', breakOne) \
            .replace('<Lunch>', lunch) \
            .replace('<BetweenSecond>', breakTwo) \
            .replace('<Dinner>', dinner)

        send_email(data,"Hi {}, Awesome menu is waiting for you!!".format(user.name), user.email)

