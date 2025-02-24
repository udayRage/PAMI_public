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


class generateTransactional:
    """
    :Description Generate a transactional database with the given number of lines, average number of items per line, and total number of items

    :Attributes:
    numLines: int  
        - number of lines
    avgItemsPerLine: float
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

    def __init__(self, numLines, avgItemsPerLine, numItems) -> None:
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
    
    @staticmethod
    def tuning(array, sumRes) -> np.ndarray:
        """
        Tune the array so that the sum of the values is equal to sumRes

        :param array: list of values

        :type array: numpy.ndarray

        :param sumRes: the sum of the values in the array to be tuned

        :type sumRes: int

        :return: list of values with the tuned values and the sum of the values in the array to be tuned and sumRes is equal to sumRes

        :rtype: numpy.ndarray
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
        

    def generateArray(self, nums, avg, maxItems) -> np.ndarray:
        """
        Generate a random array of length n whose values average to m

        :param nums: number of values

        :type nums: int

        :param avg: average value

        :type avg: int

        :param maxItems: maximum value

        :type maxItems: int

        :return: random array

        :rtype: numpy.ndarray
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
        self.db = set()

        values = self.generateArray(self.numLines, self.avgItemsPerLine, self.numItems)

        for value in values:
            line = np.random.choice(range(1, self.numItems + 1), value, replace=False)
            self.db.append(line)

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
                f.write(sep.join(map(str, line)) + '\n')

    def getTransactions(self) -> pd.DataFrame:
        """
        Get the transactional database

        :return: the transactional database

        :rtype: pd.DataFrame
        """
        # df = pd.DataFrame(self.db)
        temp = ["\t".join(map(str, line)) for line in self.db]
        df = pd.DataFrame(temp, columns=["Transactions"])
        return df
        

if __name__ == "__main__":
    # test the class
    db = generateTransactional(10, 5, 10)
    db.create()
    db.save("\t", '4.txt')
    print(db.getTransactions())

    obj = generateTransactional(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    obj.create()
    #obj.save(sys.argv[4])
    # print(obj.getTransactions())
    