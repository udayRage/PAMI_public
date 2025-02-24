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

from typing import Tuple, List, Union
import pandas as pd
import numpy as np
import random
import sys
import os

class generateTemporalDatabase:
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
    def __init__(self, numOfTransactions: int, avgLenOfTransactions: int, 
                 numItems: int, outputFile: str, percentage: int=50,
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

        self.numOfTransactions = numOfTransactions
        self.avgLenOfTransactions = avgLenOfTransactions
        self.numItems = numItems
        self.outputFile = outputFile
        self.df = None
        if percentage > 1:
            self.percentage = percentage / 100
        else:
            self.percentage = percentage
        self.sep = sep
        self.typeOfFile = typeOfFile.lower()

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
    
    def performCoinFlip(self, probability: float) -> bool:
        """
        Perform a coin flip with the given probability.
        :param probability: probability to perform coin flip
        :type probability: float
        :return: True if coin flip is performed, False otherwise
        :rtype: bool
        """
        result = np.random.choice([0, 1], p=[1 - probability, probability])
        return result == 1


    def tuning(self, array, sumRes) -> list:
        """
        Tune the array so that the sum of the values is equal to sumRes

        :param array: list of values

        :type array: list

        :param sumRes: target sum

        :type sumRes: int

        :return: list of values with the sum equal to sumRes after tuning

        :rtype: list
        """

        # first generate a random array of length n whose values average to m
        values = np.random.randint(1, self.numItems, len(array))

        while np.sum(values) != sumRes:
            # get index of largest value
            # if sum is too large, decrease the largest value
            if np.sum(values) > sumRes:
                maxIndex = np.argmax(values)
                values[maxIndex] -= 1
            # if sum is too small, increase the smallest value
            else:
                minIndex = np.argmin(values)
                values[minIndex] += 1

        # get location of all values greater than numItems
        
        for i in range(len(array)):
            array[i][1] = values[i]

        return array

    def createTemporalFile(self) -> None:
        """
        create Temporal database or dataframe depending on input
        :return: None
        """

        db = []
        lineSize = []
        for i in range(self.numOfTransactions):
            db.append([i])
            if self.performCoinFlip(self.percentage):
                lineSize.append([i,0])
        
        # make it so that sum of lineSize[1] equal to numTransactions * avgLenOfTransactions
        sumRes = self.numOfTransactions * self.avgLenOfTransactions
        self.tuning(lineSize, sumRes)

        for i in range(len(lineSize)):
            if lineSize[i][1] > self.numItems:
                raise ValueError("Error: Either increase numItems or decrease avgLenOfTransactions or modify percentage")
            line = np.random.choice(range(1, self.numItems + 1), lineSize[i][1], replace=False)
            db[lineSize[i][0]].extend(line)

        if self.typeOfFile == "database":
            with open(self.outputFile, "w") as outFile:
                for line in db:
                    outFile.write(self.sep.join(map(str, line)) + '\n')
            outFile.close()

        if self.typeOfFile == "dataframe":
            data = {
                'timestamp': [line[0] for line in db],
                'transactions': pd.Series([line[1:] for line in db])
            }
            self.df = pd.DataFrame(data)

        print("Temporal database created successfully")


if __name__ == '__main__':
    numOfTransactions_ = 100
    numItems_ = 20
    avgTransactionLength_ = 6
    outFileName_ = 'temporal_out.txt'
    sep_ = '\t'
    #frameOrBase = "database"

    temporalDB = generateTemporalDatabase(numOfTransactions_, avgTransactionLength_, numItems_, outFileName_)

    temporalDB.createTemporalFile()

    numOfTransactions1 = 100
    numItems1 = 15
    avgTransactionLength1 = 6
    outFileName1 = 'temporal_ot.txt'
    #sep = '\t'
    percent = 75
    frameOrBase = "dataframe"

    temporalDB = generateTemporalDatabase(numOfTransactions1, avgTransactionLength1, numItems1, outFileName1, percent, sep_, frameOrBase )
    temporalDB.createTemporalFile()
    print(temporalDB.getDatabaseAsDataFrame())

    obj = generateTemporalDatabase(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    obj.createTemporalFile()
