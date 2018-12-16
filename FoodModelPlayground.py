import FoodEngine


# engineNames = FoodEngine.FoodEngine('Name')
# engineNames.loadEngine()
# engineIngredients = FoodEngine.FoodEngine('Ingredients')
# engineIngredients.loadEngine()
#
#
# res = engineNames.search("pizza milk")
# for id in res:
#     print("name:{}, energy:{}".format(engineNames.products.get(id[1]).name,engineNames.products.get(id[1]).energy))
#
#
#
# res = engineIngredients.search("sugar")
# for id in res:
#     print("name:{} , ing:{}".format(engineIngredients.products.get(id[1]).name,
#                                     engineIngredients.products.get(id[1]).ingredients))



#res = engineIngredients.search("chop")
#for id in res:
#    print("name:{} , ing:{}".format(engineIngredients.products.get(id[1]).name,engineIngredients.products.get(id[1]).ingredients))




#
#
# # temp
# import FoodEngine
# engineNames = FoodEngine.FoodEngine('Name')
# engineNames.load_data()
# engineNames.build_inverted_index()
# engineNames._createIdfToCorpus()
# engineNames.saveEngine()
# engineNames.loadEngine()
# engineIngredients = FoodEngine.FoodEngine('Ingredients')
# engineIngredients.load_data()
# engineIngredients.build_inverted_index()
# engineIngredients._createIdfToCorpus()
# engineIngredients.saveEngine()
# engineIngredients.loadEngine()

#res = engineIngredients.search("milk")
#engineIngredients.inverted_index['milk'].__len__()
#for id in res:
#    print(engineIngredients.products.get(id[1]).name)
#engineIngredients.build_inverted_index()

#with open('{}{}.pkl'.format(FoodEngineClient.Paths.Engine_path, 'idfTermsIngredients'), 'wb') as output:
#    print("save idfTermsIngredients")
#    pickle.dump(engineIngredients.idfTerms, output)


# import EnginesClient
# import time
#
#
# engine = EnginesClient.FoodEngineClient()
#
# res = engine.findProductByNameTopFive("creme brulee")
# for product in res:
#     print(product.name)

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
#
import EnginesClient
# import time
engine = EnginesClient.FoodEngineClient()

product = engine.findProductByName('pasta')
res = engine.checkAllergies(product)
print(res)
# start = int(round(time.time() * 1000))
# healty = engine.getHealtyFood(product.name)
# status = engine.getHealthStatus(product)
# end = int(round(time.time() * 1000))
# if healty != None:
#     print("{} - Name:{}, Ingredients:{}".format(end-start, healty.name, healty.ingredients))
# else:
#     print("{} - The food is ok".format(end - start))
#
#
#


