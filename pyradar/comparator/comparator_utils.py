#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matías Herranz <matiasherranz@gmail.com>
# Joaquín Tita <joaquintita@gmail.com>
#
# hhttps://github.com/PyRadar/pyradar
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.


"""
Code forked from: https://github.com/ocelma/python-recsys/
"""
from math import sqrt
from scipy.stats import pearsonr

from operator import itemgetter
from numpy import nan

ROUND_FLOAT = 6


class Evaluation(object):
    """
    Base class for Evaluation

    It has the basic methods to load ground truth and test data.
    Any other Evaluation class derives from this base class.

    :param data: A list of tuples, containing the real and the predicted value.
                 E.g: [(3, 2.3), (1, 0.9), (5, 4.9), (2, 0.9), (3, 1.5)]
    :type data: list
    """
    def __init__(self, data=None):
        # data is a list of tuples.
        # E.g: [(3, 2.3), (1, 0.9), (5, 4.9), (2, 0.9), (3, 1.5)]
        if data:
            self._ground_truth, self._test = map(itemgetter(0), data), \
                                             map(itemgetter(1), data)
        else:
            self._ground_truth = []
            self._test = []

    def __repr__(self):
        gt = str(self._ground_truth)
        test = str(self._test)
        return 'GT  : %s\nTest: %s' % (gt, test)
        #return str('\n'.join((str(self._ground_truth), str(self._test))))

    def load_test(self, test):
        """
        Loads a test dataset

        :param test: a list of predicted values. E.g: [2.3, 0.9, 4.9, 0.9, 1.5]
        :type test: list
        """
        if isinstance(test, list):
            self._test = list(test)
        else:
            self._test = test

    def get_test(self):
        """
        :returns: the test dataset (a list)
        """
        return self._test

    def load_ground_truth(self, ground_truth):
        """
        Loads a ground truth dataset

        :param ground_truth: a list of real values (aka ground truth).
                             E.g: [3.0, 1.0, 5.0, 2.0, 3.0]
        :type ground_truth: list
        """
        if isinstance(ground_truth, list):
            self._ground_truth = list(ground_truth)
        else:
            self._ground_truth = ground_truth

    def get_ground_truth(self):
        """
        :returns: the ground truth list
        """
        return self._ground_truth

    def load(self, ground_truth, test):
        """
        Loads both the ground truth and the test lists. The two lists must have
        the same length.

        :param ground_truth: a list of real values (aka ground truth).
                             E.g: [3.0, 1.0, 5.0, 2.0, 3.0]
        :type ground_truth: list
        :param test: a list of predicted values. E.g: [2.3, 0.9, 4.9, 0.9, 1.5]
        :type test: list
        """
        self.load_ground_truth(ground_truth)
        self.load_test(test)

    def add(self, rating, rating_pred):
        """
        Adds a tuple <real rating, pred. rating>

        :param rating: a real rating value (the ground truth)
        :param rating_pred: the predicted rating
        """
        if rating is not nan and rating_pred is not nan:
            self._ground_truth.append(rating)
            self._test.append(rating_pred)

    def add_test(self, rating_pred):
        """
        Adds a predicted rating to the current test list

        :param rating_pred: the predicted rating
        """
        if rating_pred is not nan:
            self._test.append(rating_pred)

    def compute(self):
        """
        Computes the evaluation using the loaded ground truth and test lists
        """
#        import ipdb; ipdb.set_trace()
        if self._ground_truth is None:
            raise ValueError('Ground Truth dataset is empty!')
        if self._test is None:
            raise ValueError('Test dataset is empty!')


# Predictive-Based Metrics
class MAE(Evaluation):
    """
    Mean Absolute Error

    :param data: a tuple containing the Ground Truth data, and the Test data
    :type data: <list, list>
    """
    def __init__(self, data=None):
        super(MAE, self).__init__(data)

    def compute(self, r=None, r_pred=None):
        if r and r_pred:
            return round(abs(r - r_pred), ROUND_FLOAT)

        if not len(self._ground_truth) == len(self._test):
            raise ValueError('Ground truth and Test datasets have different'\
                             'sizes!')

        #Compute for the whole test set
        super(MAE, self).compute()
        sum = 0.0
        for i in range(0, len(self._ground_truth)):
            r = self._ground_truth[i]
            r_pred = self._test[i]
            sum += abs(r - r_pred)
        return round(abs(float(sum / len(self._test))), ROUND_FLOAT)


class RMSE(Evaluation):
    """
    Root Mean Square Error

    :param data: a tuple containing the Ground Truth data, and the Test data
    :type data: <list, list>
    """
    def __init__(self, data=None):
        super(RMSE, self).__init__(data)

    def compute(self, r=None, r_pred=None):
        if r and r_pred:
            return round(sqrt(abs((r - r_pred) * (r - r_pred))), ROUND_FLOAT)

        if not len(self._ground_truth) == len(self._test):
            raise ValueError('Ground truth and Test datasets have'\
                             'different sizes!')

        #Compute for the whole test set
        super(RMSE, self).compute()
        sum = 0.0
        for i in range(0, len(self._ground_truth)):
            r = self._ground_truth[i]
            r_pred = self._test[i]
            sum += abs((r - r_pred) * (r - r_pred))
        return round(sqrt(abs(float(sum / len(self._test)))), ROUND_FLOAT)


#Correlation-Based Metrics
class Pearson(Evaluation):
    """
    Pearson correlation

    :param data: a tuple containing the Ground Truth data, and the Test data
    :type data: <list, list>
    """
    def __init__(self, data=None):
        super(Pearson, self).__init__(data)

    def compute(self):
        super(Pearson, self).compute()
        return round(pearsonr(self._ground_truth, self._test)[0], ROUND_FLOAT)
