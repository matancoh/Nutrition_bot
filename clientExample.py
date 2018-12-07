# import EnginesClient
# import time
#
#
# engine = EnginesClient.FoodEngineClient()
#
res = engine.findProductByNameTopFive("creme brulee")
for product in res:
    print(product.name)

# # measure time of find product
# print("*********************************")
#
#
# res = engine.findProductByNameTopFive("pizza")
# for product in res:
#     print("Name:{}, energy:{}".format(product.name, product.energy))
#
#
# res = engine.findProductByName("pizza")
# print("Name:{}, energy:{} , ingredients:{}".format(res.name, res.energy, res.ingredients))
#
# start = int(round(time.time() * 1000))
# health = engine.findProductByIngredientsTopFive(res.ingredients)
# for product in health:
#     print(product.name)
# end = int(round(time.time() * 1000))
# print(end - start)
#
# res = engine.findProductByIngredientsTopFive('nuts')
# for product in res:
#     print("Name:{}, Ingredients:{}".format(product.name, product.ingredients))
#
#

import EnginesClient
import time
engine = EnginesClient.FoodEngineClient()
start = int(round(time.time() * 1000))
pasta = engine.findProductByName('pasta')
healty = engine.getMostHealtyFood("pasta")
end = int(round(time.time() * 1000))
print("Name:{}, Ingredients:{}".format(healty.name, healty.ingredients))