import FoodEngine
import Menu
import User
import MailService
from random import randint
import time, threading


class HealthStatus:
    HealtyFood = 'Healty Food'
    HighSuger = 'High Suger'
    HighSodium = 'High Sodium'
    HighFatSaturated = 'High Fat Saturated'

class Allergy:
    Celiac = {'name': 'celiac','ingredients': ['wheat', 'barley', 'rye', 'oatmeal', 'oat', 'flour']}
    Lactose = {'name': 'lactose', 'ingredients': ['milk', 'lactose', 'milkfat']}
    Peanuts = {'name': 'peanuts', 'ingredients': ['peanut', 'peanuts']}
    Nuts = {'name': 'nuts', 'ingredients': ['nut', 'walnut', 'filbert','almond','Pecan', 'coconut','pistachios','pecans']}
    Soya = {'name': 'soy', 'ingredients': ['soya', 'soy']}

class FoodEngineClient(object):
    def __init__(self):
        self.ingredientsIREngine = self.loadEngine('Ingredients')
        self.nameIREngine = self.loadEngine('Name')
        self.healtyFoodResult = ''

    def loadEngine(self, nameOfEngine):
        engine = FoodEngine.FoodEngine(nameOfEngine)
        engine.loadEngine()
        return engine

    def findProductByName(self, name):
        try:
            products = self.nameIREngine.search(name)
            topProduct = self.nameIREngine.get(products[products.__len__()- 1][1])
            return topProduct
        except Exception as e:
            print(e)
            return None

    def findProductByIngredients(self, Ingredients):
        try:
            products = self.ingredientsIREngine.search(Ingredients)
            topProduct = self.ingredientsIREngine.get(products[products.__len__()- 1][1])
            return topProduct
        except Exception as e:
            print(e)
            return None

    def getProductById(self,id):
        product = self.nameIREngine.products[id]
        return product

    def getHealtyResult(self):
        if(self.healtyFoodResult != ''):
            return self.healtyFoodResult
        else:
            return "WAIT"


    def getHealtyFood(self, name):
        self.healtyFoodResult = ''
        t = threading.Thread(target= FoodEngineClient._getHealtyFoodHelper, args=(self, name))
        t.start()

    def _getHealtyFoodHelper(self, name):
        # if res == None than the food is healthy
        res = None
        product = self.findProductByName(name)

        if product == None:
            self.healtyFoodResult = False

        productStatus = self.getHealthStatus(product)

        if HealthStatus.HealtyFood in productStatus:
            self.healtyFoodResult = True
        else:
            ingredientsStr = ''
            ingredients = product.ingredients.split(',')
            for curr in range(0, int(ingredients .__len__() / 4)):
                ingredientsStr = ingredientsStr +" " + ingredients[curr]

            productsId = self.ingredientsIREngine.search(ingredientsStr , numberOfResults = FoodEngine.SIZE_OF_RESULTS_HEALTH)
            for productTuple in productsId:
                productCurr = self.nameIREngine.get(productTuple[1])
                if (productCurr.id != product.id):
                    foodStatus = self.getHealthStatus(productCurr)
                    res = self.compareProducts(foodStatus, productCurr, res)
            self.healtyFoodResult = res

    def compareProducts(self, foodStatus, productCurr, res):
        if (res == None) and (HealthStatus.HealtyFood in foodStatus):
            res = productCurr
        elif (res != None) and float(productCurr.fatSaturated) < float(res.fatSaturated) and float(
                productCurr.sugars) < float(res.sugars) and float(productCurr.sodium) < float(res.sodium) and (HealthStatus.HealtyFood in foodStatus):
            res = productCurr
        return res

    def getHealthStatus(self, product):
        res = []
        isHighSodium = float(product.sodium) >= 400.0
        isHighSugar = float(product.sugars) >= 10.0
        isHighFatSaturated = float(product.fatSaturated) >= 4.0

        # check if health parameter
        if isHighSodium:
            res.append(HealthStatus.HighSodium)
        if isHighFatSaturated:
            res.append(HealthStatus.HighFatSaturated)
        if isHighSugar:
            res.append(HealthStatus.HighSuger)
        # if have good in any paramater food is healty
        if res.__len__() == 0:
            res.append(HealthStatus.HealtyFood)
        return res

    def checkAllergies(self, product):
        res = []
        # if res == None than the food is healthy
        ingredientsTerms = FoodEngine.tokenization_function(product.ingredients)
        self._addAllergy(Allergy.Celiac, ingredientsTerms, res)
        self._addAllergy(Allergy.Lactose, ingredientsTerms, res)
        self._addAllergy(Allergy.Peanuts, ingredientsTerms, res)
        self._addAllergy(Allergy.Nuts, ingredientsTerms, res)
        self._addAllergy(Allergy.Soya, ingredientsTerms, res)
        return res

    def _addAllergy(self, allergy, ingredientsTerms, res):
        for term in allergy['ingredients']:
            termAfterTokenization = FoodEngine.tokenization_function(term)
            if termAfterTokenization[0] in ingredientsTerms:
                if allergy.get('name') not in res:
                    res.append(allergy.get('name'))


    def createMenuAndSendMail(self, user):
        t = threading.Thread(target=FoodEngineClient._createMenuAndSendMailHelper, args=(self, user))
        t.start()

    def _createMenuAndSendMailHelper(self, user):
        menu = self._createMenu(user)
        MailService.sendMenuMailToClient(user, menu)

    def _createMenu(self, user):
        totalCalories = self._calculateCalories(user.activityLevel, user.age, user.gender, user.height, user.weight)

        breakfestCalories = int(totalCalories / 4)
        lunchCalories = int(totalCalories / 3)
        dinnerCalories = int(totalCalories / 4)
        breakCalories = int(totalCalories - breakfestCalories  - lunchCalories - dinnerCalories) / 2

        breakfest = self._createMeal('breakfest', breakfestCalories, user.taste)
        breakOne = self._createMeal('break', breakCalories, user.taste)
        lunch = self._createMeal('lunch', lunchCalories, user.taste)
        breakTwo= self._createMeal('break', breakCalories, user.taste)
        dinner = self._createMeal('dinner', dinnerCalories, user.taste)

        return Menu.Menu(breakfest, breakOne, lunch, breakTwo, dinner)


    def _createMeal(self, typeOfMeal, totalCaloriesForMeal, taste):
        products = self._getProductsForMeal(taste, typeOfMeal)
        servingAmount = self._calculateServingAmount(products, totalCaloriesForMeal)
        sumOfCaloriesForMeal = self._calculateTotalCaloriesForMeal(products, servingAmount)

        productMealLst = list()
        if sumOfCaloriesForMeal < totalCaloriesForMeal:
            productMealLst.append(self._addFruit())

        for product in products:
            productMealLst.append(Menu.ProductMeal(product, servingAmount))
        return Menu.Meal(productMealLst)

    def _addFruit(self):
        options = Menu.MenuProductsOptions.items['fruit']
        randomProduct = int(randint(0, options .__len__() - 1))
        productsName = options[randomProduct]
        product = self.findProductByName(productsName)

        return Menu.ProductMeal(product, 1)

    def _calculateTotalCaloriesForMeal(self, products, servingAmount):
        sumOfCaloriesForMeal = 0
        for product in products:
            sumOfCaloriesForMeal = sumOfCaloriesForMeal + (float(product.serving.amount) / 100 * float(product.energy)) * float(servingAmount)
        return sumOfCaloriesForMeal

    def _calculateServingAmount(self, products, totalCaloriesForMeal):
        sumOfCaloriesForMeal = 0
        servingAmount = 0
        while sumOfCaloriesForMeal <= totalCaloriesForMeal:
            servingAmount = servingAmount + 1
            sumOfCaloriesForMeal = self._calculateTotalCaloriesForMeal(products, servingAmount)
        servingAmount = servingAmount - 1
        return servingAmount

    def _getProductsForMeal(self, taste, typeOfMeal):
        Menu.MenuProductsOptions.items[typeOfMeal][taste]
        randomProduct = int(randint(0, Menu.MenuProductsOptions.items[typeOfMeal][taste].__len__() - 1))
        productsName = Menu.MenuProductsOptions.items[typeOfMeal][taste][randomProduct]
        products = list()
        for product in productsName:
            products.append(self.findProductByName(product))
        return products

    def _calculateCalories(self, activityLevel, age, gender, height, weight):
        bmr = (10 * weight) + (6.25 * height) - (5 * age)
        if gender == User.Gender.Male:
            bmr = bmr + 5
        elif gender == User.Gender.Female:
            bmr = bmr - 161
        if activityLevel == User.ActivityLevel.Low:
            pal = 1.53
        elif activityLevel == User.ActivityLevel.Medium:
            pal = 1.76
        elif activityLevel == User.ActivityLevel.High:
            pal = 2.25
        return bmr * pal * 0.9


