#import random as _rd
#import sys as _sys
import time
import os
import psutil
import numpy as np
import tqdm
import pandas as pd


class GeoReferentialTemporalDatabaseByTriangle:
    """
    This class create synthetic geo-referential temporal database.

    :Attribute:

        totalTransactions : int
            No of transactions
        noOfItems : int or float
            No of items
        avgTransactionLength : str
            The length of average transaction
        outputFile: str
            Name of the output file.

    :Methods:

        GeoReferentialTemporalDatabase(outputFile)
            Create geo-referential temporal database and store into outputFile

    **Credits:**
    ---------------
             The complete program was written by  P.Likhitha   under the supervision of Professor Rage Uday Kiran.

    """

    def __init__(
            self,
            databaseSize: int,
            avgItemsPerTransaction: int,
            numItems: int,
            maxDis:int=1,
            sep: str = '\t',
            occurrenceProbabilityOfSameTimestamp: float = 0,
            occurrenceProbabilityToSkipSubsequentTimestamp: float = 0,
    ) -> None:
        self.db = None
        self.databaseSize = databaseSize
        self.avgItemsPerTransaction = avgItemsPerTransaction
        self.numItems = numItems
        self.__tx = [0]
        self.__ty = [0]
        self.maxDis = maxDis
        self.seperator = sep
        self.occurrenceProbabilityOfSameTimestamp = occurrenceProbabilityOfSameTimestamp
        self.occurrenceProbabilityToSkipSubsequentTimestamp = occurrenceProbabilityToSkipSubsequentTimestamp
        self.current_timestamp=int()
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()
        numPoints = numItems * 10

        self.itemPoint = {}

        self.itemPoint = self.draw(numPoints)

    @staticmethod
    def performCoinFlip(probability: float) -> bool:
        """
        Perform a coin flip with the given probability.

        :param probability: Probability of the coin landing heads (i.e., the event occurring).
        :return: True if the coin lands heads, False otherwise.
        """
        result = np.random.choice([0, 1], p=[1 - probability, probability])
        return result

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
        Generate the Temporal database
        :return: None
        """
        self._startTime = time.time()
        #db = set()

        values = self.generateArray(self.databaseSize, self.avgItemsPerTransaction, self.numItems)
        
        for i in range(self.databaseSize):
            # Determine the timestamp
            if self.performCoinFlip(self.occurrenceProbabilityOfSameTimestamp):
                timestamp = self.current_timestamp
            else:
                if self.performCoinFlip(self.occurrenceProbabilityToSkipSubsequentTimestamp)==1:
                    self.current_timestamp += 2
                else:
                    self.current_timestamp += 1
                timestamp = self.current_timestamp

            self.db.append([timestamp])  # Start the transaction with the timestamp

            

        # For each transaction, generate items
        for i in tqdm.tqdm(range(self.databaseSize)):

            items = np.random.choice(range(1, self.numItems + 1), values[i], replace=False)
            nline = [self.itemPoint[i] for i in items]
            self.db[i].extend(nline)

        self._endTime = time.time()
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def save(self,filename, sep='\t') -> None:
        """
        Save the Temporal database to a file

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
        Get the Temporal database

        :return: the Temporal database

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

        return self._memoryUSS

    def getMemoryRSS(self) -> float:

        return self._memoryRSS
# if __name__ == "__main__":
#     _ap = str()
#     _ap = createSyntheticGeoreferentialTemporal(100000, 870, 10)
#     _ap.GeoreferentialTemporalDatabase("T10_geo_temp.txt")
# else:
#     print("Error! The number of input parameters do not match the total number of parameters provided")
