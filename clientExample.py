import EnginesClient
import time



engine = EnginesClient.FoodEngineClient()

res = engine.findProductByNameTopFive("pizza")
for product in res:
    print(product.name)

res = engine.findProductByName("mars")
print(res.name)

# measure time of find product
start = int(round(time.time() * 1000))
health = engine.findProductByIngredients(res.ingredients)
end = int(round(time.time() * 1000))
print(end - start)



res = engine.findProductByIngredientsTopFive('nuts')
for product in res:
    print("Name:{}, Ingredients:{}".format(product.name, product.ingredients))
