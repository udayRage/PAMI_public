# generateSequentialDatabase is a code used to generate sequential database.
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#     from PAMI.extras.generateDatabase import generateSequentialDatabase as db
#     obj = db(10,10, 5, 10)
#     obj.create()
#     obj.save('db.txt')
#     print(obj.getTransactions()) to get the transactional database as a pandas dataframe

# **Running the code from the command line**
# --------------------------------------------------------
#     python generateDatabase.py 10 5 10 db.txt
#     cat db.txt
#


__copyright__ = """
Copyright (C)  2024 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

#import math

import numpy as np
import pandas as pd
#import sys


class GeoReferentialSequentialDatabase:
    """
    :Description Generate a sequential database with the given number of lines, average number of items per line, and total number of items

    :Attributes:
    numSeq: int
        - number of sequences in database
    avgItemsetPerSeq:int
        - avarage number of itemset in one sequence
    avgItemsPeritemset: int
        - average number of items per itemset
    numItems: int
        - total kind of items
    maxItem: int(default:numItems)
        - maximum number of items per itemset
    maxItemset: int(default:avgItemsetPerSeq * 2)
        - maximum number of itemset per sequence
    seqSep: str
        - Separator for each item set

    :Methods:
        create:
            Generate the transactional database
        save:
            Save the sequential database to a file
        getTransactions:
            Get the sequential database




    """

    def __init__(self, numSeq, avgItemsetPerSeq, avgItemsPerItemset, numItems,x1=0,y1=0,x2=100,y2=100, maxItem=0, maxItemset=0,
                 seqSep="-1") -> None:
        """
        Initialize the transactional database with the given parameters

        """

        self.numSeq = numSeq
        self.avgItemsetPerSeq = avgItemsetPerSeq
        self.avgItemsPerItemset = avgItemsPerItemset
        self.numItems = numItems
        if maxItem == 0:
            self.maxItem = numItems
        else:
            self.maxItem = maxItem
        if maxItemset == 0:
            self.maxItemset = avgItemsetPerSeq * 2
        else:
            self.maxItemset = maxItemset
        self.seqSep = seqSep
        self.db = []
        numPoints = (x2 - x1) * (y2 - y1)
        if numItems > numPoints:
            raise ValueError("Number of points is less than the number of lines * average items per line")

        self.itemPoint = {}


        for i in (range(1, numItems + 1)):
            # self.itemPoint[i] = (np.random.randint(x1, x2), np.random.randint(y1, y2))
            point = self.getPoint(x1, y1, x2, y2)
            while point in self.itemPoint:
                point = self.getPoint(x1, y1, x2, y2)
            self.itemPoint[i] = point

    @staticmethod
    def getPoint(x1, y1, x2, y2):

        return np.random.randint(x1, x2), np.random.randint(y1, y2)

    @staticmethod
    def tuning(array, sumRes) -> list:
        """
        Tune the array so that the sum of the values is equal to sumRes

        :param array: list of values

        :type array: list

        :param sumRes: the sum of the values in the array to be tuned

        :type sumRes: int

        :return: list of values with the tuned values and the sum of the values in the array to be tuned and sumRes is equal to sumRes

        :rtype: list
        """

        while np.sum(array) != sumRes:
            # get index of largest value
            randIndex = np.random.randint(0, len(array))
            # if sum is too large, decrease the largest value
            if np.sum(array) > sumRes:
                array[randIndex] -= 1
            # if sum is too small, increase the smallest value
            else:
                #minIndex = np.argmin(array)
                array[randIndex] += 1
        return array

    def generateArray(self, nums, avg, maxItems) -> list:
        """
        Generate a random array of length nums whose values average to avg

        :param nums: number of values

        :type nums: int

        :param avg: average value

        :type avg: int

        :param maxItems: maximum value

        :type maxItems: int

        :return: random array

        :rtype: list
        """

        # generate n random values
        values = np.random.randint(1, maxItems, nums)
        sumRes = nums * avg

        values = self.tuning(values, sumRes)

        # if any value is less than 1, increase it and tune the array again
        while np.any(values < 1):
            for i in range(nums):
                if values[i] < 1:
                    values[i] += 1
            values = self.tuning(values, sumRes)

        while np.any(values > maxItems):
            for i in range(nums):
                if values[i] > maxItems:
                    values[i] -= 1
            values = self.tuning(values, sumRes)

        # if all values are same then randomly increase one value and decrease another
        while np.all(values == values[0]):
            values[np.random.randint(0, nums)] += 1
            values = self.tuning(values, sumRes)

        return values

    def create(self, item="") -> None:
        """
        :param item: list (default:generate random numItems items)
            item list to make database
        Generate the sequential database
        :return: None
        """
        if item == "":
            item=self.itemPoint

        #db = set()
        sequences = self.generateArray(self.numSeq, self.avgItemsetPerSeq - 1, self.maxItemset)

        for numItemset in sequences:
            seq = []
            values = self.generateArray(numItemset + 1, self.avgItemsPerItemset, self.maxItem)

            for value in values:
                line = list(set(np.random.choice(item, value, replace=False)))
                seq = seq + line
                seq = seq + [self.seqSep]
            seq.pop()

            self.db.append(seq)

    def save(self, filename, sep="\t") -> None:
        """
        Save the transactional database to a file

        :param sep: Separator

        :type sep: str

        :param filename: name of the file

        :type filename: str

        :return: None
        """

        with open(filename, 'w') as f:
            for line in self.db:
                f.write(sep.join(map(str, line)) + '\n')

    def getSequence(self) -> pd.DataFrame:
        """
        Get the sequential database

        :return: the sequential database

        :rtype: pd.DataFrame
        """
        df = pd.DataFrame(self.db)
        return df


if __name__ == "__main__":
    # test the class
    db = GeoReferentialSequentialDatabase(10, 5, 5, 10)
    db.create()
    db.save('db.txt')
    print(db.getSequence())
