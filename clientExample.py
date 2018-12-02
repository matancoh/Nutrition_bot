import EnginesClient
import time



engine = EnginesClient.FoodEngineClient()

res = engine.findProductByNameTopFive("pizza")
for product in res:
    print(product.name)

# measure time of find product
print("*********************************")
start = int(round(time.time() * 1000))
health = engine.findProductByIngredients(res[4].ingredients)
print(health.name)
end = int(round(time.time() * 1000))
print(end - start)

res = engine.findProductByName("twix")
print(res.name)

res = engine.findProductByIngredientsTopFive('nuts')
for product in res:
    print("Name:{}, Ingredients:{}".format(product.name, product.ingredients))
