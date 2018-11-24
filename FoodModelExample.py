import FoodEngineClient


engineNames = FoodEngineClient.FoodEngineClient('Name')
engineNames.loadEngine()
engineIngredients = FoodEngineClient.FoodEngineClient('Ingredients')
engineIngredients.loadEngine()


res = engineIngredients.search("chop")
for id in res:
    print("name:{} , ing:{}".format(engineIngredients.products.get(id[1]).name,engineIngredients.products.get(id[1]).ingredients))

res = engineNames.search("milk")
for id in res:
    print(engineNames.products.get(id[1]).name)

#temp
#engineNames = FoodEngineClient.FoodEngineClient('Name')
#engineNames.load_data()
#engineNames.build_inverted_index()
#engineNames._createIdfToCorpus()
#engineNames.saveEngine()
#engineNames.loadEngine()
#engineIngredients = FoodEngineClient.FoodEngineClient('Ingredients')
#engineIngredients.load_data()
#engineIngredients.build_inverted_index()
#engineIngredients._createIdfToCorpus()
#engineIngredients.saveEngine()
#engineIngredients.loadEngine()

#res = engineIngredients.search("milk")
#for id in res:
#    print(engineIngredients.products.get(id[1]).name)
#engineIngredients.build_inverted_index()
#res = engineNames.search("milk")
#for id in res:
#    print(engineNames.products.get(id[1]).name)
#print(res.name)


#with open('{}{}.pkl'.format(FoodEngineClient.Paths.Engine_path, 'idfTermsIngredients'), 'wb') as output:
#    print("save idfTermsIngredients")
#    pickle.dump(engineIngredients.idfTerms, output)
