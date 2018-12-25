import FoodEngine
import User


class MenuProductsOptions:
    items =                {'breakfest':
                              {User.Taste.Omnivorous: [['quaker oat', 'low fat milk'], ['yogurt','granola'],['Corn flakes Kelloggs','low fat milk'], ['bread','yellow cheese', 'egg']],
                               User.Taste.Vegetarian : [['quaker oat', 'low fat milk'], ['yogurt','granola'],['Corn flakes Kelloggs','low fat milk'], ['bread','yellow cheese', 'egg']],
                               User.Taste.Vegan : [['quaker oat', 'soya beverage'], ['Corn flakes Kelloggs','soya beverage'], ['bread','hummus'] , ['bread','peanut butter']]},
                            'lunch' :
                              {User.Taste.Omnivorous: [['chicken breast', 'basmati rice', 'green salad'], ['turkey', 'basmati rice', 'green salad'], ['beef steak', 'basmati rice', 'green bean'],
                                                       ['chicken breast', 'quinoa','green salad'], ['turkey', 'quinoa','green salad'],['beef steak', 'quinoa','green bean'],
                                                       ['chicken breast', 'rice','green bean'], ['turkey', 'rice','green bean'],['beef steak', 'rice','green bean']],

                               User.Taste.Vegetarian: [['tofu', 'basmati rice', 'green salad'], ['salmon', 'basmati rice', 'green salad'], ['tuna  steak', 'basmati rice', 'green salad'],
                                                       ['tofu', 'quinoa','green salad'], ['salmon', 'quinoa','green salad'],['tuna steak', 'quinoa','green bean'],
                                                       ['tofu', 'rice','green bean'], ['salmon', 'rice','green bean'],['tuna steak', 'rice','green bean']],

                               User.Taste.Vegan: [['tofu', 'basmati rice', 'green salad'], ['corn schnitzel', 'basmati rice', 'green salad'],
                                                       ['tofu', 'quinoa','green salad'], ['corn schnitzel', 'quinoa','green bean'],
                                                       ['tofu', 'rice','green bean'], ['corn schnitzel', 'rice','green bean']]},
                            'dinner':
                              {User.Taste.Omnivorous: [['bread','pastrami','pesto'], ['bread','yellow chesse','pesto'], ['bread','tuna'], ['bread','tuna']],
                               User.Taste.Vegetarian: [['bread','yellow chesse','pesto'], ['bread','tuna'], ['bread','tuna']],
                               User.Taste.Vegan: [['bread', 'vegan cheddar'], []]},
                            'break':
                              {User.Taste.Omnivorous: [['yogurt'], ['Almonds'], ['peanuts'], ['energy bar']],
                               User.Taste.Vegetarian: [['yogurt'], ['Almonds'], ['peanuts'], ['energy bar']],
                               User.Taste.Vegan: [['Almonds'], ['peanuts'], ['energy bar']]},
                            'fruit': ['apples', 'PINEAPPLE', 'MEDJOOL DATES']
                            }

class ProductMeal(object):
    def __init__(self, _product, _amount):
        self.product = _product
        self.amount = _amount

class Meal(object):
    def __init__(self, _lstProducts):
        self.lstProducts = _lstProducts

class Menu(object):
    def __init__(self, _breakfest, _brakOne, _lunch, _breakTwo, _dinner):
        self.breakfest : Meal = _breakfest
        self.breakOne : Meal = _brakOne
        self.lunch : Meal = _lunch
        self.breakTwo : Meal = _breakTwo
        self.dinner : Meal = _dinner






