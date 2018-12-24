from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import operator
import math
import csv
import string
import itertools
import heapq
import pickle
import os


class Paths:
    FOOD_DB = os.path.join('.', 'Food DB')
    ProductsCsv = os.path.join(FOOD_DB, 'Products.csv')
    NutrientCsv = os.path.join(FOOD_DB, 'Nutrient.csv')
    ServingSizeCsv = os.path.join(FOOD_DB, 'Serving_Size.csv')
    Engine_path = os.path.join('.', 'Engine')

TEXT = "text"
SIZE_OF_RESULTS = 5
SIZE_OF_SEARCH_RESULTS = 5000
SIZE_OF_RESULTS_HEALTH = 100


class Unit:
    Milliliter = 'ml'
    Gram = 'g'

class Serving(object):
    def __init__(self, amount, unit: Unit, servingTool, servingAmount):
        self.amount = amount
        self.unit = unit
        self.servingTool = servingTool
        self.servingAmount = servingAmount

class Product(object):
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.manufacturer = None
        self.ingredients = None
        self.protein = None
        self.fat = None
        self.carbohydrate = None
        self.energy = None
        self.sugars = None
        self.sodium = None
        self.fatSaturated = None
        self.serving: Serving = None


    def get(self, attrName):
            return {
                'id': self.id,
                'name': self.name,
                'manufacturer': self.manufacturer,
                'ingredients': self.ingredients,
                'protein': self.protein,
                'fat': self.fat,
                'carbohydrate': self.carbohydrate,
                'calories': self.energy,
                'sugar': self.sugars,
                'sodium': self.sodium,
                'fatSaturated' : self.fatSaturated
            }[attrName]

def tokenization_function(raw_text):
    # lower case
    raw_text = raw_text.lower()

    # create translate table
    translator = raw_text.maketrans('', '', string.punctuation)

    # remove punctuation and split to words
    word_tokens = word_tokenize(raw_text.translate(translator))

    # remove stop words
    stop_words = set(stopwords.words('english'))

    filtered_text = [word for word in word_tokens if not word in stop_words]

    # stemming
    ps = PorterStemmer()
    tokenized_words = [ps.stem(word) for word in filtered_text]

    return tokenized_words


class FoodEngine(object):
    def __init__(self, _type):
        self.products = None
        self.type = _type
        self.inverted_index = {}
        self.idfTerms = None

    def load_data(self):
        data = {}
        dataAfterFilter ={}

        fProducts = open(Paths.ProductsCsv, encoding='utf-8')
        products_rows = csv.DictReader(fProducts)

        fNutrient = open(Paths.NutrientCsv, encoding='utf-8')
        nutrient_rows = csv.DictReader(fNutrient)

        fServingSize = open(Paths.ServingSizeCsv, encoding='utf-8')
        servingSize_rows = csv.DictReader(fServingSize)

        for product in products_rows:
            data[product['NDB_Number']] = self.addToProductsDict(product)  # Add to dict all new products

        for nutrientProduct in nutrient_rows:
            data[nutrientProduct['NDB_No']] = self.addNutrientToProduct(data[nutrientProduct['NDB_No']],
                                                                                nutrientProduct)
        for product in servingSize_rows:
            productId = product['\ufeffNDB_No']

            if(data[productId] != None):
                data[productId].serving = Serving(product['Serving_Size'], product['Serving_Size_UOM'],
                                        product['Household_Serving_Size'], product['Household_Serving_Size_UOM'])

        for productId in data:
            product = data.get(productId)
            if (product.energy is not None) and (product.sugars is not None) and (product.sodium is not None) \
                    and (product.fatSaturated is not None):
                dataAfterFilter[product.id] = product

        self.products = dataAfterFilter

    def addNutrientToProduct(self, product, nutrient):
        if (nutrient['Nutrient_name'] == 'Protein'):
            product.protein = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Total lipid (fat)'):
            product.fat = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Energy'):
            product.energy = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Carbohydrate, by difference'):
            product.carbohydrate = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Sodium, Na'):
            product.sodium = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Sugars, total'):
            product.sugars = nutrient['Output_value']
        elif (nutrient['Nutrient_name'] == 'Fatty acids, total saturated'):
            product.fatSaturated = nutrient['Output_value']

        return product

    def addToProductsDict(self, product):
        newProduct = Product(product['NDB_Number'])  # set with uniqeID
        newProduct.manufacturer = product['manufacturer']
        newProduct.name = product['long_name']
        newProduct.ingredients = product['ingredients_english']

        return newProduct

    def build_inverted_index(self):

        temp_inverted = {}

        for index, raw_text in self.products.items():
            if self.type =='Name':
                tokens = self.index(raw_text.name, tokenization_function)  # Get tokenized words
            elif self.type =='Ingredients':
                tokens = self.index(raw_text.ingredients, tokenization_function)  # Get tokenized words

            if self.type == 'Ingredients':
                counter = tokens.__len__()
            else:
                counter = 1



            for word in tokens:
                # If our inverted dict doesn't have this word, initiazlize a new key
                if word not in temp_inverted:
                    temp_inverted[word] = {}
                    # insert the index to the inverted dict

                # add tf to inverted index
                if index not in temp_inverted[word]:
                    if counter == 1:
                        temp_inverted[word][index] = 1
                    else:
                        temp_inverted[word][index] = counter * 10
                        counter = counter - 1
                else:
                    temp_inverted[word][index] = temp_inverted[word][index] + 1
        self.inverted_index = temp_inverted

    def index(self, document_text, tokenization_function):
        terms = tokenization_function(document_text)
        return terms

    # implement and query between 2 terms
    def intersection(self, term1, term2):
        term1_after_tokenize = tokenization_function(term1)
        term2_after_tokenize = tokenization_function(term2)
        p1, p2 = 0, 0

        # the current version supports only one tokenized word intersection (or one word after normalization)
        if not len(term1_after_tokenize) == 1 or not len(term2_after_tokenize) == 1:
            return []
        index1 = self.inverted_index.get(term1_after_tokenize[0])
        index2 = self.inverted_index.get(term2_after_tokenize[0])

        # making sure both words are in the inverted index
        if not index1 or not index2:
            # increase on or more terms are not in the inverted there is no need to continue
            return []

        res_indexes = []
        while p1 < len(index1) and p2 < len(index2):
            if index1[p1] < index2[p2]:
                p1 += 1
            elif index1[p1] > index2[p2]:
                p2 += 1
            else:
                res_indexes.append(index1[p1])
                p1 += 1
                p2 += 1

        return res_indexes

    # implement or query between 2 terms
    def union(self, term1, term2):
        term1_after_tokenize = tokenization_function(term1)
        term2_after_tokenize = tokenization_function(term2)

        # the current version supports only one tokenized word intersection (or one word after normalization)
        if not len(term1_after_tokenize) == 1 or not len(term2_after_tokenize) == 1:
            return []

        index1 = self.inverted_index.get(term1_after_tokenize[0])
        index2 = self.inverted_index.get(term2_after_tokenize[0])

        # making sure one of the words are in the inverted index
        if not index1 and not index2:
            return []

        lst = index1 + index2
        return list(set(lst))


    def get(self, productId):
        product = None
        try:
            product = self.products[productId]
        except:
            print('cannot find product:{}'.format(productId))

        return product


    def _sizeOfDic(self):
        print(f'THE SIZE OF THE DICTIONARY IS: {len(self.inverted_index)}')
        return len(self.inverted_index)

    def _sliceDicFunc(self, number_to_slice=10):
        return dict(itertools.islice(self.inverted_index.items(), number_to_slice))

    def showFirstsTermsAndSize(self):
        self._sizeOfDic()
        topTerms = self._sliceDicFunc()

        for term in topTerms:
            print(term)

    def _createIdfToCorpus(self):  # create weight matrix of tf*idf for all corpus
        self._inverseDocFreq(self.inverted_index.keys()) # create idf for corpus


    def _createTfIdfVectorForTerm(self, term, row, matrix, productsSet):
        for product in self.inverted_index[term]:  # do log(tf)*idf for every term
            if product in productsSet:
                index = productsSet.index(product)
                matrix[row][index] = (1 + math.log10(self.inverted_index[term][product])) * self.idfTerms[term]

    def _createVectorTfIdfForQuery(self, termList):  # create vector for query
        termFreq = {}
        queryVector = list()

        # create term frequency for query
        for term in termList:
            if term in termFreq:
                termFreq[term] = termFreq[term] + 1
            else:
                termFreq[term] = 1

        # do tf*idf for query
        for term in termFreq:
            queryVector.append((1 + math.log10(termFreq[term])) * self.idfTerms[term])

        return queryVector

    def _inverseDocFreq(self, termList: list):  # create idf for corpus
        termListIdf = {}
        for term in termList:
            if term in self.inverted_index:
                termListIdf[term] = math.log10(self.products.__len__() / self.inverted_index[term].__len__())
            else:
                termListIdf[term] = 0
        self.idfTerms = termListIdf

    def _createSetOfDocs(self, termsList):  # create set of union docs for list of terms
        productsIdSet = set()
        sizeOfBatch = int(SIZE_OF_SEARCH_RESULTS / termsList.__len__())

        for term in termsList:
            productsIdDic = {}
            sortedProducts = {}
            if term in self.inverted_index:
                productsIdDic = self.inverted_index[term].copy()
                sortedProducts = sorted(productsIdDic.items(), key=operator.itemgetter(1), reverse=True)
            for index in range(sizeOfBatch):
                if index == sortedProducts.__len__() - 1:
                    break
                else:
                    productsIdSet.add(sortedProducts[index][0])

        return productsIdSet

    def search(self, query, numberOfResults = SIZE_OF_RESULTS):  # search and return the 5 top docs that much similar to query
        queryTermsList = self.index(query, tokenization_function)  # get the terms from query
        productsSet = self._createSetOfDocs(queryTermsList)
        queryVector = self._createVectorTfIdfForQuery(queryTermsList)  # create vector from terms

        productsSet = list(productsSet)
        scores = []

        #create empty matrix
        matrix = [[0 for x in range(productsSet.__len__())]
                 for y in range(queryTermsList.__len__())]

        for productId in self.products:
            product = self.products[productId]
            if product.name.upper() == query.upper():
                scores.append((1.0, productId))
                return scores

        #create matrix for the products
        row = 0  # counter of terms
        for term in queryTermsList:  # fill the matrix
            self._createTfIdfVectorForTerm(term , row, matrix, productsSet)
            row = row + 1

        for product in productsSet:
            productVector = list()
            for word in range(matrix.__len__()):
                productVector.append(matrix[word][productsSet.index(product)])
            score = self._cosine(queryVector, productVector)
            if len(scores) < numberOfResults:
                heapq.heappush(scores, (score, product))
            else:
                if(scores[0][0] < score):
                    heapq.heappop(scores)
                    heapq.heappush(scores, (score, product))

        return scores

    def _cosine(self, vec1, vec2):  # calculate cosine
        dotProduct = 0
        for index in range(vec1.__len__()):
            dotProduct = dotProduct + vec1[index] * vec2[index]
        if dotProduct != 0:
            score = dotProduct / (self.normal(vec1) * self.normal(vec2))
        else:
            score = 0
        return score

    def normal(self, vec):
        sigma = 0

        for index in range(vec.__len__()):
            sigma = sigma + math.pow(vec[index], 2)
        res = math.sqrt(sigma)
        return res


    def loadEngine(self):
        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'products')), 'rb') as input:
            print("load products".format(self.type))
            self.products = pickle.load(input)

        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'engine{}'.format(self.type))), 'rb') as input:
            print("load engine {}".format(self.type))
            self.inverted_index = pickle.load(input)

        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'idfTerms{}'.format(self.type))), 'rb') as input:
            print("load idf {}".format(self.type))
            self.idfTerms = pickle.load(input)


    def saveEngine(self):
        if not os.path.exists(Paths.Engine_path):
            os.makedirs(Paths.Engine_path)

        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'products')),'wb') as output:
            print("save products".format(self.type))
            pickle.dump(self.products, output)

        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'engine{}'.format(self.type))), 'wb') as output:
            print("save engine {}".format(self.type))
            pickle.dump(self.inverted_index, output)

        with open('{}.pkl'.format(os.path.join(Paths.Engine_path, 'idfTerms{}'.format(self.type))),'wb') as output:
            print("save idf {}".format(self.type))
            pickle.dump(self.idfTerms, output)
