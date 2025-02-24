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
import sys


class generateSpatioTransactional:
    """
    :Description Generate a transactional database with the given number of lines, average number of items per line, and total number of items

    :Attributes:
    numLines: int  
        - number of lines
    avgItemsPerLine: int
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
    def getPoint(x1, y1, x2, y2):

        return np.random.randint(x1, x2), np.random.randint(y1, y2)

    def __init__(self, numLines, avgItemsPerLine, numItems, x1, y1, x2, y2) -> None:
        """
        Initialize the transactional database with the given parameters

        Parameters:
        numLines: int - number of lines
        avgItemsPerLine: int - average number of items per line
        numItems: int - total number of items
        """

        self.numLines = numLines
        self.avgItemsPerLine = avgItemsPerLine
        self.numItems = numItems
        self.db = []
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        numPoints = (x2 - x1) * (y2 - y1)
        if numItems > numPoints:
            raise ValueError("Number of points is less than the number of lines * average items per line")
        
        self.itemPoint = {}
        usedPoints = set()

        for i in range(1, numItems + 1):
            # self.itemPoint[i] = (np.random.randint(x1, x2), np.random.randint(y1, y2))
            point = self.getPoint(x1, y1, x2, y2)
            while point in usedPoints:
                point = self.getPoint(x1, y1, x2, y2)
            self.itemPoint[i] = point
    
    @staticmethod
    def tuning(array, sumRes):
        """
        Tune the array so that the sum of the values is equal to sumRes

        :param array: numpy.ndarray of values of values

        :type array: numpy.ndarray of values

        :param sumRes: the sum of the values in the array to be tuned

        :type sumRes: int

        :return: list of values with the tuned values and the sum of the values in the array to be tuned and sumRes is equal to sumRes

        :rtype: numpy array
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
        

    def generateArray(self, nums, avg, maxItems):
        """
        Generate a random array of length n whose values average to m

        :param nums: number of values

        :type nums: int

        :param avg: average value

        :type avg: int

        :param maxItems: maximum value

        :type maxItems: int

        :return: random array

        :rtype: numpy array
        """

        # generate n random values
        values = np.random.randint(1, maxItems, nums)

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
        #db = set()

        values = self.generateArray(self.numLines, self.avgItemsPerLine, self.numItems)

        for value in values:
            line = np.random.choice(range(1, self.numItems + 1), value, replace=False)
            nline = [self.itemPoint[i] for i in line]
            # print(line, nline)
            # for i in range(len(line)):
            #     print(line[i], self.itemPoint[line[i]])
            #     line[i] = self.itemPoint[line[i]]
            self.db.append(nline)
            # self.db.append(line)

    def save(self, sep, filename) -> None:
        """
        Save the transactional database to a file
        :param sep: separator
        :type sep: str
        :param filename: name of the file
        :type filename: str

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
        

if __name__ == "__main__":
    # test the class
    db = generateSpatioTransactional(10, 5, 10, 1,5,5,10)
    db.create()
    db.save('\t','2.txt')
    print(db.getTransactions())

    obj = generateSpatioTransactional(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
    obj.create()
    #obj.save('\t',sys.argv[8])
    # print(obj.getTransactions())
    