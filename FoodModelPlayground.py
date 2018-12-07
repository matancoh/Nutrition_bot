import FoodEngine


engineNames = FoodEngine.FoodEngine('Name')
engineNames.loadEngine()
engineIngredients = FoodEngine.FoodEngine('Ingredients')
engineIngredients.loadEngine()


res = engineNames.search("pizza milk")
for id in res:
    print("name:{}, energy:{}".format(engineNames.products.get(id[1]).name,engineNames.products.get(id[1]).energy))



res = engineIngredients.search("sugar")
for id in res:
    print("name:{} , ing:{}".format(engineIngredients.products.get(id[1]).name,
                                    engineIngredients.products.get(id[1]).ingredients))



#res = engineIngredients.search("chop")
#for id in res:
#    print("name:{} , ing:{}".format(engineIngredients.products.get(id[1]).name,engineIngredients.products.get(id[1]).ingredients))






#temp
# import FoodEngine
# #engineNames = FoodEngine.FoodEngine('Name')
# #engineNames.load_data()
# #engineNames.build_inverted_index()
# #engineNames._createIdfToCorpus()
# #engineNames.saveEngine()
# #engineNames.loadEngine()
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
