__author__ = 'cwood'

import types
import re


class CategorySet(object):
    def __init__(self, categories):
        if not isinstance(categories, types.ListType) and not isinstance(categories, types.TupleType):
            raise TypeError('Expected a list of type Category')
        else:
            for category in categories:
                if not isinstance(category, Category):
                    raise TypeError('Expected a list of type Category')
        self._categories = categories

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    def get(self, index):
        return self._categories[index]



class Category(object):
    # def __init__(self, name, trainingData='', testData=''):
    def __init__(self, name):
        self.name = name
        # self.trainingData = trainingData
        # self.testData = testData

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __attrs(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Category) and self.__attrs() == other.__attrs()

    def __hash__(self):
        return hash(self.__attrs())


class TestSet(object):
    def __init__(self):
        self._categoryTestSets = []
        self._vocabulary = {}

    @property
    def categoryTestSets(self):
        return self._categoryTestSets

    def addCategoryTestSet(self, categoryTestSet):
        self._categoryTestSets.append(categoryTestSet)
        self._update_vocabulary(categoryTestSet)

    def get_vocabulary(self):
        return self._vocabulary

    def get_vocabulary_size(self):
        return len(self._vocabulary)

    def _update_vocabulary(self, category_test_set):
        for token in category_test_set.get_vocabulary():
            if token not in self._vocabulary:
                self._vocabulary[token] = category_test_set.get_vocabulary()[token]
            else:
                self._vocabulary[token] = self._vocabulary[token] + category_test_set.get_vocabulary()[token]


class CategoryTestSet(object):
    def __init__(self, category):
        if not isinstance(category, Category):
            raise TypeError('Expected a category of type Category')
        self._category = category
        self._documents = []
        self._vocabulary = {}
        self._token_count = 0
        self._testfile = None

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def testfile(self):
        return self._testfile

    @testfile.setter
    def testfile(self, value):
        self._testfile = value
        self._set_documents()

    def get_vocabulary(self):
        return self._vocabulary

    def get_token_count(self):
        return self._token_count

    def getDocuments(self):
        return self._documents

    def _set_documents(self):
        self._vocabulary = {}
        self._token_count = 0
        self._documents = []
        f = open(self.testfile, 'r')

        for document in f.readlines():
            my_doc = Document(document)

            self._documents.append(my_doc)
            self._token_count += len(my_doc.getTokens())

            for token in my_doc.getTokens():
                if token not in self._vocabulary:
                    self._vocabulary[token] = 0
                self._vocabulary[token] += my_doc.getTokens()[token]

        f.close()

class Document:
    def __init__(self, contents):
        self._contents = contents
        self._tokens = {}
        for token in re.findall(r"\w+|[^\w\s]", self._contents, re.UNICODE):
            if token not in self._tokens:
                self._tokens[token] = 0
            self._tokens[token] += 1

    def getTokens(self):
        return self._tokens

    def getContents(self):
        return self._contents
