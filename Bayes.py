#!/usr/local/bin/python
from __future__ import division

__author__ = 'Chris Wood'

import types

from Training import CategorySet
from Training import TestSet

class NaiveBayes(object):

    __categorySet = None
    __training = {}
    __priors = []
    __evidence = {}

    def __init__(self, categorySet):
        print "initializing"

        if not isinstance(categorySet, CategorySet):
            raise TypeError('Please specify a CategorySet')

        self.__training_set = None
        self.__priors = []
        self.__categorySet = categorySet

        for category in self.__categorySet.categories:
            self.__training[category] = {'prior': 0.0, 'documents': []}

    def train(self, trainingSet):
        print "training..."
        if not isinstance(trainingSet, TestSet):
            raise TypeError('Please specify a TestSet')

        self.__training_set = trainingSet
        self.__getDocuments()
        self.__calculatePriors()

    def __getDocuments(self):
        for categoryTestSet in self.__training_set.categoryTestSets:
            if categoryTestSet.category not in self.__categorySet.categories:
                raise StandardError('Invalid category' + categoryTestSet.category.name +
                                    '. This Bayesian instance does not include this category')

            category = categoryTestSet.category
            self.__training[category]['documents'] = categoryTestSet.getDocuments()

    def __calculatePriors(self):
        docCounts = map(lambda x: len(self.__training[x]['documents']), self.__training)
        totalDocuments = reduce(lambda x, y: x+y, docCounts)

        for category in self.__training:
            trainCat = self.__training[category]
            catDocCount = len(trainCat['documents'])
            trainCat['prior'] = catDocCount / totalDocuments

    def test(self, testSet):
        print "testing..."
        if not isinstance(testSet, TestSet):
            raise TypeError('Please specify a TestSet')

        correctly_classified = 0
        incorrectly_classified = 0

        for category_test_set in testSet.categoryTestSets:
            if category_test_set.category not in self.__categorySet.categories:
                raise StandardError('Invalid category' + category_test_set.category.name +
                    '. This Bayesian instance can not classify against this category')

            for document in category_test_set.getDocuments():

                # calculate against each class to determine the winner
                class_scores = {}

                for category_training_set in self.__training_set.categoryTestSets:
                    evidence = None

                    for token in document.getTokens():
                        token_count = 0
                        if token in category_training_set.get_vocabulary():
                            token_count = category_training_set.get_vocabulary()[token]

                        if evidence is None:
                            evidence = 1000*((token_count + 1) /
                                         (category_training_set.get_token_count() + self.__training_set.get_vocabulary_size()))
                        else:
                            evidence *= 1000*((token_count + 1) /
                                        (category_training_set.get_token_count() + self.__training_set.get_vocabulary_size()))

                    class_scores[category_training_set.category] = \
                        (self.__training[category_training_set.category]['prior'] * evidence)

                highest_scoring_category = None
                highest_score = 0.0
                for category in class_scores:
                    if class_scores[category] > highest_score:
                        highest_score = class_scores[category]
                        highest_scoring_category = category

                if highest_scoring_category == category_test_set.category:
                    correctly_classified += 1
                else:
                    incorrectly_classified += 1

        print "Correctly Classified %d of %d" % (correctly_classified,correctly_classified+incorrectly_classified)


    def classify(self):
        print "classifying..."
