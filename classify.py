#!/usr/local/bin/python
from Bayes import NaiveBayes
from Training import *

categories = CategorySet([
    Category(name='positive'),
    Category(name='negative')
])

positiveTraining = CategoryTestSet(categories.get(0))
positiveTraining.testfile = 'data/pos_train_data.txt'

negativeTraining = CategoryTestSet(categories.get(1))
negativeTraining.testfile = 'data/neg_train_data.txt'

training = TestSet()
training.addCategoryTestSet(positiveTraining)
training.addCategoryTestSet(negativeTraining)

# build training set
bayes = NaiveBayes(categories)
bayes.train(training)

# test classifier

bayes.test(training)

positiveTest = CategoryTestSet(categories.get(0))
positiveTest.testfile = 'data/pos_test_data.txt'

negativeTest = CategoryTestSet(categories.get(1))
negativeTest.testfile = 'data/neg_test_data.txt'

test = TestSet()
test.addCategoryTestSet(positiveTest)
test.addCategoryTestSet(negativeTest)

bayes.test(test)
