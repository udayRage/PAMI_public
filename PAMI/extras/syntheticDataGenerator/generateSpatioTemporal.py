# generateTemporalDatabase is a code used to convert the database into Temporal database.
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#
#             from PAMI.extras.generateDatabase import generateTemporalDatabase as db
#
#             obj = db.generateTemporalDatabase(100, 10, 6, oFile, %, "\t")
#
#             obj.save()
#
#             obj.getFileName("outputFileName") # to create a file
#
#             obj.getDatabaseAsDataFrame("outputFileName") # to convert database into dataframe
#
#             obj.createTemporalFile("outputFileName") # to get outputfile
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

#from typing import Tuple, List, Union
import pandas as pd
import numpy as np
#import random
import sys
#import os

class generateSpatioTemporal:
    """
    :Description:   generateTemporalDatabase creates a temporal database and outputs a database or a frame depending on input

    :Attributes:
        :param numOfTransactions: int
            number of transactions
        :param avgLenOfTransactions: int
            average length of transactions
        :param numItems: int
            number of items
        :param outputFile: str
            output file name
        :param percentage: int
            percentage of coinToss for TID of temporalDatabase
        :param sep: str
            seperator for database output file
        :param typeOfFile: str
            specify database or dataframe to get corresponding output

    :Methods:
        getFileName():
            returns filename
        createTemporalFile():
            creates temporal database file or dataframe
        getDatabaseAsDataFrame:
            returns dataframe
        performCoinFlip():
            Perform a coin flip with the given probability
        tuning():
            Tune the arrayLength to match avgLenOfTransactions
        createTemporalFile():
            create Temporal database or dataframe depending on input

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.generateDatabase import generateTemporalDatabase as db

            numOfTransactions = 100
            numItems = 15
            avgTransactionLength = 6
            outFileName = 'temporal_ot.txt'
            sep = '\t'
            percent = 75
            frameOrBase = "dataframe" # if you want to get dataframe as output
            frameOrBase = "database" # if you want to get database/csv/file as output

            temporalDB = db.generateTemporalDatabase(numOfTransactions, avgTransactionLength, numItems, outFileName, percent, sep, frameOrBase )
            temporalDB.createTemporalFile()
            print(temporalDB.getDatabaseAsDataFrame())

    """

    @staticmethod
    def getPoint(x1, y1, x2, y2):
        return np.random.randint(x1, x2), np.random.randint(y1, y2)

    def __init__(self, numOfTransactions: int, avgLenOfTransactions: float,
                 numItems: int, outputFile: str, x1, y1, x2, y2, percentage: float=50.0,
                 sep: str='\t', typeOfFile: str="Database") -> None:
        
        """
        :Description:   Initialize the generateTemporalDatabase class

        :Attributes:
            :param numOfTransactions: int
                number of transactions
            :param avgLenOfTransactions: int
                average length of transactions
            :param numItems: int
                number of items
            :param outputFile: str
                output file name
            :param percentage: int
                percentage of coinToss for TID of temporalDatabase
            :param sep: str
                seperator for database output file
            :param typeOfFile: str
                specify database or dataframe to get corresponding output

        :Methods:
            getFileName():
                returns filename
            createTemporalFile():
                creates temporal database file or dataframe
            getDatabaseAsDataFrame:
                returns dataframe
            performCoinFlip():
                Perform a coin flip with the given probability
            tuning():
                Tune the arrayLength to match avgLenOfTransactions
            createTemporalFile():
                create Temporal database or dataframe depending on input
        
        """

        self.df = None
        self.numOfTransactions = numOfTransactions
        self.avgLenOfTransactions = avgLenOfTransactions
        self.numItems = numItems
        self.outputFile = outputFile
        if percentage > 1:
            self.percentage = percentage / 100
        else:
            self.percentage = percentage
        self.sep = sep
        self.typeOfFile = typeOfFile.lower()
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

    def getFileName(self) -> str:
        """
        return filename
        :return: filename
        :rtype: str
        """
        return self.outputFile

    def getDatabaseAsDataFrame(self) -> pd.DataFrame:
        """
        return dataframe
        :return: dataframe
        :rtype: pd.DataFrame
        """
        return self.df
    
    @staticmethod
    def performCoinFlip(probability: float) -> bool:
        """
        Perform a coin flip with the given probability.
        :param probability: probability to perform coin flip
        :type probability: float
        :return: True if coin flip is performed, False otherwise
        :rtype: bool
        """
        result = np.random.choice([0, 1], p=[1 - probability, probability])
        return result == 1


    @staticmethod
    def tuning(array, sumRes):
        """
        Tune the array so that the sum of the values is equal to sumRes

        :param array: numpy.ndarray of values

        :type array: numpy.ndarray

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
        

    def generateArray(self, nums, maxItems, sumRes):
        """
        Generate a random array of length n whose values average to m

        :param nums: number of values

        :type nums: int

        :param maxItems: maximum value

        :type maxItems: int

        :param sumRes: Resultant sum

        :type sumRes: int

        :return: random array

        :rtype: list
        """

        # generate n random values
        values = np.random.randint(1, maxItems, nums)

        # sumRes = nums * avg

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

    def createTemporalFile(self) -> None:
        """
        create Temporal database or dataframe depending on input
        :return: None
        """

        lines = [i for i in range(self.numOfTransactions) if self.performCoinFlip(self.percentage)]
        values = self.generateArray(len(lines), self.numItems, int(self.avgLenOfTransactions * self.numOfTransactions))
        # print(values, sum(values), self.avgLenOfTransactions * self.numOfTransactions, sum(values)/self.numOfTransactions)
        # print(lines)

        form = list(zip(lines, values))

        database = [None for _ in range(self.numOfTransactions)]

        for i in range(len(form)):
            database[form[i][0]] = np.random.choice(range(1, self.numItems + 1), form[i][1], replace=False).tolist()
            database[form[i][0]] = [str(self.itemPoint[i]) for i in database[form[i][0]]]
            database[form[i][0]] = self.sep.join(database[form[i][0]])

        self.df = pd.DataFrame({'TS': [i+1 for i in range(self.numOfTransactions)], 'Transactions': database})

    def getTransactions(self):
        # self.df change header name to Transactions
        return self.df

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
            for row in self.df.iterrows():
                # f.write(str(row[1]['TS']) + sep + row[1]['Transactions'] + '\n')
                # line = list(map(str, line))
                line = row[1]['Transactions']
                if line is not None:
                    f.write(str(row[1]['TS']) + sep + line.replace('\t', sep) + '\n')
                else:
                    f.write(str(row[1]['TS']) + sep + '\n')


if __name__ == '__main__':
    numOfTransactions_ = 100
    numItems_ = 20
    avgTransactionLength_ = 6
    outFileName = '1.txt'
    sep_ = '\t'

    temporalDB = generateSpatioTemporal(numOfTransactions_, avgTransactionLength_, numItems_, outFileName,1,1,10,10)

    temporalDB.createTemporalFile()
    temporalDB.save(sep_, outFileName)
    print(temporalDB.getTransactions())



    obj = generateSpatioTemporal(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    obj.createTemporalFile()
    obj.getFileName()
