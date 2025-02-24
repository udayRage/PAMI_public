# generateTransactionalDatabase is a code used to convert the database into Temporal database.
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#     from PAMI.extras.generateDatabase import generateTransactionalDatabase as db
#     obj = db(10, 5, 10)
#     obj.create()
#     obj.save('db.txt')
#     print(obj.getTransactions()) to get the transactional database as a pandas dataframe

# **Running the code from the command line**
# --------------------------------------------------------
#     python generateDatabase.py 10 5 10 db.txt
#     cat db.txt
#


__copyright__ = """
Copyright (C)  2021 Rage Uday Kiran

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

import numpy as np
import pandas as pd
#import time
import psutil, os, time, tqdm
#from matplotlib import pyplot as plt
import random
class GeoReferentialTransactionalDatabaseByTriangle:
    """
    :Description Generate a transactional database with the given number of lines, average number of items per line, and total number of items

    :Attributes:
    numLines: int
        - number of lines
    avgItemsPerTransaction: int
        - average number of items per line
    numItems: int
        - total number of items

    :Methods:
        create:
            Generate the transactional database
        save:
            Save the transactional database to a file
        getTransactions:
            Get the transactional database




    """
    @staticmethod
    def __tran_1(p):
        """
        To set a harf point
        :param
            p:list
            point(x,y)
        :return
            x1 :float
                new x-coordinate
            y1 :float
                new y-coordinate
        """
        x = p[0]
        y = p[1]
        x1 = 0.5 * x
        y1 = 0.5 * y

        return x1, y1

    def __tran_2(self, p):
        """
        to get harf point starts from center
        :param p:list
            point(x,y)
        :return:
            x1 :float
                new x-coordinate
            y1 :float
                new y-coordinate
        """
        x = p[0]
        y = p[1]
        x1 = 0.5 * x + self.maxDis/4
        y1 = 0.5 * y + self.maxDis/4
        return x1, y1

    def __tran_3(self, p):
        """
        To get a harf point start from top
        :param p:list
            point(x,y)
        :return:
            x1 :float
                new x-coordinate
            y1 :float
                new y-coordinate
        """
        x = p[0]
        y = p[1]
        x1 = 0.5 * x + self.maxDis/2
        y1 = 0.5 * y
        return x1, y1

    @staticmethod
    def __get_index():
        """
        To get index
        :return: int
            the number of point
        """
        prob = [0.333, 0.333, 0.333]
        r = random.random()
        c = 0
        sump = []
        for p in prob:
            c += p
            sump.append(c)
        for item, sp in enumerate(sump):
            if r <= sp:
                return item
        return len(prob) - 1

    def __tran(self, p):
        """
        To set transactioon
        :param p: list
            (point(x,y))
        :return:
            x:float
                new x-coordinates
            y:float
                new y-coordinate
        """
        trans = [self.__tran_1, self.__tran_2, self.__tran_3]
        tindex = self.__get_index()
        t = trans[tindex]
        x, y = t(p)
        return x, y

    def __draw(self, n):
        """
        To set points
        :param n: int
            the number of points
        :return:
        """
        x1 = 0
        y1 = 0
        for i in range(n):
            x1, y1 = self.__tran((x1, y1))
            self.__tx.append(x1)
            self.__ty.append(y1)
        return self.__tx, self.__ty

    def draw(self, n=5000):
        """
        To grow a graph
        :param n:int
            the number of point
        :return:float
            points
        """
        x, y = self.__draw(n)
        point=[(x[i],y[i])for i in range(n)]
        return point
    def __init__(self, databaseSize, avgItemsPerTransaction, numItems, maxDis, sep='\t') -> None:
        """
        Initialize the transactional database with the given parameters

        Parameters:
        databaseSize: int - number of lines
        avgItemsPerTransaction: int - average number of items per line
        numItems: int - total number of items
        """

        self.databaseSize = databaseSize
        self.avgItemsPerTransaction = avgItemsPerTransaction
        self.numItems = numItems
        self.db = []
        self.__tx = [0]
        self.__ty = [0]
        self.maxDis=maxDis
        self.seperator = sep

        numPoints = numItems*10

        self.itemPoint = {}

        self.itemPoint= self.draw(numPoints)
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()
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
            # if sum is too large, decrease the largest value
            if np.sum(array) > sumRes:
                maxIndex = np.argmax(array)
                array[maxIndex] -= 1
            # if sum is too small, increase the smallest value
            else:
                minIndex = np.argmin(array)
                array[minIndex] += 1
        return array

    def generateArray(self, nums, avg, maxItems) -> list:
        """
        Generate a random array of length n whose values average to m

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
        values = np.random.randint(1, avg*1.5, nums)

        sumRes = nums * avg

        self.tuning(values, sumRes)

        # if any value is less than 1, increase it and tune the array again
        while np.any(values < 1):
            for i in range(nums):
                if values[i] < 1:
                    values[i] += 1
            self.tuning(values, sumRes)

        while np.any(values > maxItems):
            for i in range(nums):
                if values[i] > maxItems:
                    values[i] -= 1
            self.tuning(values, sumRes)

        # if all values are same then randomly increase one value and decrease another
        while np.all(values == values[0]):
            values[np.random.randint(0, nums)] += 1
            self.tuning(values, sumRes)

        return values

    def create(self) -> None:
        """
        Generate the transactional database
        :return: None
        """
        self._startTime = time.time()
        #db = set()

        values = self.generateArray(self.databaseSize, self.avgItemsPerTransaction, self.numItems)

        for value in tqdm.tqdm(values):
            line = np.random.choice(range(1, self.numItems + 1), value, replace=False)
            nline = [self.itemPoint[i] for i in line]
            # print(line, nline)
            # for i in range(len(line)):
            #     print(line[i], self.itemPoint[line[i]])
            #     line[i] = self.itemPoint[line[i]]
            self.db.append(nline)
            # self.db.append(line)
        self._endTime = time.time()

    def save(self,filename, sep='\t') -> None:
        """
        Save the transactional database to a file

        :param filename: name of the file

        :type filename: str

        :param sep: seperator for the items

        :type sep: str

        :return: None
        """

        with open(filename, 'w') as f:
            for line in self.db:
                # f.write(','.join(map(str, line)) + '\n')
                line = list(map(str, line))
                f.write(sep.join(line) + '\n')

    def getTransactions(self) -> pd.DataFrame:
        """
        Get the transactional database

        :return: the transactional database

        :rtype: pd.DataFrame
        """
        df = pd.DataFrame(['\t'.join(map(str, line)) for line in self.db], columns=['Transactions'])
        return df

    def getRuntime(self) -> float:
        """
        Get the runtime of the transactional database

        :return: the runtime of the transactional database


        :rtype: float
        """
        return self._endTime - self._startTime

    def getMemoryUSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        return self._memoryUSS

    def getMemoryRSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryRSS = process.memory_info().rss
        return self._memoryRSS