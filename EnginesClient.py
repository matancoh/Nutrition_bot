import FoodEngine

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

    def getMostHealtyFood(self, name):
        res = None
        product = self.findProductByName(name)
        productsId = self.ingredientsIREngine.search(product.ingredients, numberOfResults = FoodEngine.SIZE_OF_RESULTS_HEALTH)

        for productTuple in productsId:
            productCurr = self.nameIREngine.get(productTuple[1])
            if (productCurr.id != product.id) and (name.upper() not in productCurr.name.upper()):
                if res == None:
                    res = productCurr
                elif productCurr.energy < res.energy:
                        res = productCurr
        return res


