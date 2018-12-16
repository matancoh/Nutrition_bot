import FoodEngine


class HealthStatus:
    HealtyFood = 'Healty Food'
    HighSuger = 'High Suger'
    HighSodium = 'High Sodium'
    HighFatSaturated = 'High Fat Saturated'

class Allergy:
    Celiac = {'name': 'Celiac','ingredients': ['wheat', 'barley', 'rye', 'oatmeal', 'oat', 'flour']}
    Lactose = {'name': 'Lactose', 'ingredients': ['milk', 'LACTOSE', 'MILKFAT']}
    Peanuts = {'name': 'Lactose', 'ingredients': ['peanut', 'PEANUTS']}
    Nuts = {'name': 'Lactose', 'ingredients': ['nut', 'walnut', 'filbert','ALMONDS','Pecan', 'coconut','pistachios','PECANS']}
    Soya = {'name': 'Lactose', 'ingredients': ['soya', 'soy']}

class FoodEngineClient(object):
    def __init__(self):
        self.ingredientsIREngine = self.loadEngine('Ingredients')
        self.nameIREngine = self.loadEngine('Name')

    def loadEngine(self, nameOfEngine):
        engine = FoodEngine.FoodEngine(nameOfEngine)
        engine.loadEngine()
        return engine

    def findProductByName(self, name):
        products = self.nameIREngine.search(name)
        topProduct = self.nameIREngine.get(products[products.__len__()- 1][1])
        return topProduct

    def findProductByIngredients(self, Ingredients):
        products = self.ingredientsIREngine.search(Ingredients)
        topProduct = self.ingredientsIREngine.get(products[products.__len__()- 1][1])
        return topProduct

    def getProductById(self,id):
        product = self.nameIREngine.products[id]
        return product

    def getHealtyFood(self, name):
        # if res == None than the food is healthy
        res : FoodEngine.Product = None
        product = self.findProductByName(name)
        productStatus = self.getHealthStatus(product)

        if HealthStatus.HealtyFood in productStatus:
            return None
        else:
            productsId = self.ingredientsIREngine.search(product.ingredients, numberOfResults = FoodEngine.SIZE_OF_RESULTS_HEALTH)
            for productTuple in productsId:
                productCurr : FoodEngine.Product = self.nameIREngine.get(productTuple[1])
                if (productCurr.id != product.id):
                    foodStatus = self.getHealthStatus(productCurr)
                    res = self.compareProducts(foodStatus, productCurr, res)
            return res

    def compareProducts(self, foodStatus, productCurr, res):
        if (res == None) and (HealthStatus.HealtyFood in foodStatus):
            res = productCurr
        elif (res != None) and float(productCurr.fatSaturated) < float(res.fatSaturated) and float(
                productCurr.sugars) < float(res.sugars) and float(productCurr.sodium) < float(res.sodium) and (HealthStatus.HealtyFood in foodStatus):
            res = productCurr
        return res

    def getHealthStatus(self, product: FoodEngine.Product):
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
        self.addAllergy(Allergy.Celiac, ingredientsTerms, res)
        self.addAllergy(Allergy.Lactose, ingredientsTerms, res)
        self.addAllergy(Allergy.Peanuts, ingredientsTerms, res)
        self.addAllergy(Allergy.Nuts, ingredientsTerms, res)
        self.addAllergy(Allergy.Soya, ingredientsTerms, res)
        return res

    def addAllergy(self, allergy, ingredientsTerms, res):
        for term in allergy['ingredients']:
            termAfterTokenization = FoodEngine.tokenization_function(term)
            if termAfterTokenization[0] in ingredientsTerms:
                if allergy.get('name') not in res:
                    res.append(allergy.get('name'))


