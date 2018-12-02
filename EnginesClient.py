import FoodEngine

class FoodEngineClient(object):
    def __init__(self):
        self.ingredientsIREngine = self.loadEngine('Ingredients')
        self.nameIREngine = self.loadEngine('Name')

    def loadEngine(self, nameOfEngine):
        engine = FoodEngine.FoodEngine(nameOfEngine)
        engine.loadEngine()
        return engine

    def findProductByNameTopFive(self, name):
        res = list()
        products = self.nameIREngine.search(name)

        for product in products:
            res.append(self.nameIREngine.get(product[1]))
        return res

    def findProductByIngredientsTopFive(self, Ingredients):
        res = list()
        products = self.ingredientsIREngine.search(Ingredients)

        for product in products:
            res.append(self.ingredientsIREngine.get(product[1]))
        return res

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