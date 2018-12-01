import EnginesClient


engine = EnginesClient.FoodEngineClient()

res = engine.findProductByNameTopFive("pizza")
for product in res:
    print(product.name)

res = engine.findProductByName("mars")
print(res.name)

res = engine.findProductByIngredientsTopFive('nuts')
for product in res:
    print("Name:{}, Ingredients:{}".format(product.name, product.ingredients))
