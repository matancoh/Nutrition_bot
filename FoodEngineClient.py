from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import math
import csv
import string
import itertools
import numpy as np
import heapq
import pickle
import os

block_size = 100000
block_path = '.\\blocks\\'
block_names_path = '.\\blocks_names\\'
mainBlockPath = '.\\main block\\'
mergedBlockFileName = r'mergedBlockFile.json'
blockFileName = r"block_%s.json"


class Paths:
    FOOD_DB = '.\\Food DB\\'
    ProductsCsv = FOOD_DB + 'Products.csv'
    NutrientCsv = FOOD_DB + 'Nutrient.csv'
    Engine_path = '.\\Engine\\'


TEXT = "text"
SIZE_OF_RESULTS = 5


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


class FoodEngineClient(object):
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

        for product in products_rows:
            data[product['NDB_Number']] = self.addToProductsDict(product)  # Add to dict all new products

        for nutrientProduct in nutrient_rows:
            data[nutrientProduct['NDB_No']] = self.addNutrientToProduct(data[nutrientProduct['NDB_No']],
                                                                        nutrientProduct)
        for productId in data:
            product = data.get(productId)
            if product.energy is not None:
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

            for word in tokens:
                # If our inverted dict doesn't have this word, initiazlize a new key
                if word not in temp_inverted:
                    temp_inverted[word] = {}
                    # insert the index to the inverted dict

                # add tf to inverted index
                if index not in temp_inverted[word]:
                    temp_inverted[word][index] = 1
                else:
                    temp_inverted[word][index] = temp_inverted[word][index] + 1

        self.inverted_index = temp_inverted
        # do idf to all terms and create weight matrix
        # self._createTfIdfToCorpus()

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
            # incase on or more terms are not in the inverted there is no need to continue
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


    def getIngredientsByProductName(self, productName):
        return self.products[productName]

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


    def _createTfIdfVectorForTerm(self, term, row, matrix, docsSet):
        for doc in self.inverted_index[term]:  # do log(tf)*idf for every term
            if doc in docsSet:
                index = docsSet.index(doc)
                matrix[row][index] = (1 + math.log10(self.inverted_index[term][doc])) * self.idfTerms[term]

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

        return np.asmatrix(queryVector)

    def _inverseDocFreq(self, termList: list):  # create idf for corpus
        termListIdf = {}
        for term in termList:
            if term in self.inverted_index:
                termListIdf[term] = math.log10(self.products.__len__() / self.inverted_index[term].__len__())
            else:
                termListIdf[term] = 0
        self.idfTerms = termListIdf

    def _createSetOfDocs(self, termsList):  # create set of union docs for list of terms
        docsSet = set()
        for term in termsList:
            if term in self.inverted_index:
                docsSet.update(self.inverted_index[term])
        return docsSet

    def search(self, query):  # search and return the 5 top docs that much similar to query
        queryTermsList = self.index(query, tokenization_function)  # get the terms from query
        docsSet = self._createSetOfDocs(queryTermsList)
        queryVector = self._createVectorTfIdfForQuery(queryTermsList)  # create vector from terms

        docsSet = list(docsSet)
        scores = []

        #create empty matrix
        matrix = [[0 for x in range(docsSet.__len__())]
                 for y in range(queryTermsList.__len__())]

        #create matrix for the docSets
        row = 0  # counter of terms
        for term in queryTermsList:  # fill the matrix
            self._createTfIdfVectorForTerm(term , row, matrix, docsSet)
            row = row + 1


        weightMatrix = np.asmatrix(matrix)
        # check cosine of query and doc, for every doc on docs set
        for doc in docsSet:
            docVector: np.matrix = weightMatrix[:, docsSet.index(doc)]
            score = self._cosine(queryVector.transpose(), docVector)[0, 0]
            if len(scores) < SIZE_OF_RESULTS:
                heapq.heappush(scores, (score, doc))
            else:
                if(scores[0][0] < score):
                    heapq.heappop(scores)
                    heapq.heappush(scores, (score, doc))

        return scores

    def likeThis(self, docId):  # search and return the 5 top docs that much similar to the doc that user enter
        scores = []
        result = list()

        # check cosine of docId that user enter and doc, for every doc on docs set
        for doc in self.products:
            if (doc != docId):
                score = self._cosine(self.weightMatrix[:, docId - 1], self.weightMatrix[:, doc - 1])[0, 0]
                heapq.heappush(scores, (score, doc))

        for index in range(SIZE_OF_RESULTS):  # insert the top 5 results
            if scores.__len__() > 0:
                result.append(scores.pop()[1])

        return result

    def _cosine(self, vec1, vec2):  # calculate cosine
        score = (vec1.transpose() * vec2 / ((np.linalg.norm(vec1)) * np.linalg.norm(vec2)))
        return score

    def loadEngine(self):
        with open('{}{}.pkl'.format(Paths.Engine_path, 'products'), 'rb') as input:
            print("load products".format(self.type))
            self.products = pickle.load(input)

        with open('{}{}.pkl'.format(Paths.Engine_path, 'engine{}'.format(self.type)), 'rb') as input:
            print("load engine {}".format(self.type))
            self.inverted_index = pickle.load(input)

        with open('{}{}.pkl'.format(Paths.Engine_path, 'idfTerms{}'.format(self.type)), 'rb') as input:
            print("load idf {}".format(self.type))
            self.idfTerms = pickle.load(input)


    def saveEngine(self):
        if not os.path.exists(Paths.Engine_path):
            os.makedirs(Paths.Engine_path)

        with open('{}{}.pkl'.format(Paths.Engine_path, 'products'),'wb') as output:
            print("save products".format(self.type))
            pickle.dump(self.products, output)

        with open('{}{}.pkl'.format(Paths.Engine_path, 'engine{}'.format(self.type)), 'wb') as output:
            print("save engine {}".format(self.type))
            pickle.dump(self.inverted_index, output)

        with open('{}{}.pkl'.format(Paths.Engine_path, 'idfTerms{}'.format(self.type)),'wb') as output:
            print("save idf {}".format(self.type))
            pickle.dump(self.idfTerms, output)
