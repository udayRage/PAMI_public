# Transactional Database is a class used to get stats of database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.dbStats import TransactionalDatabase as db
#
#             obj = db.TransactionalDatabase(iFile, "\t")
#
#             obj.save(oFile)
#
#             obj.run()
#
#             obj.printStats()
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
import sys
import statistics
import pandas as pd
import validators
import numpy as np
from urllib.request import urlopen
from typing import List, Dict, Tuple, Set, Union, Any, Generator
import PAMI.extras.graph.plotLineGraphFromDictionary as plt


class TransactionalDatabase:
    """
    :Description:  TransactionalDatabase is class to get stats of database.

    :Attributes:

        :param inputFile: file :
            input file path
        :param sep: str
            separator in file. Default is tab space.

    :Methods:

        run()
            execute readDatabase function
        readDatabase()
            read database from input file
        getDatabaseSize()
            get the size of database
        getMinimumTransactionLength()
            get the minimum transaction length
        getAverageTransactionLength()
            get the average transaction length. It is sum of all transaction length divided by database length.
        getMaximumTransactionLength()
            get the maximum transaction length
        getStandardDeviationTransactionLength()
            get the standard deviation of transaction length
        getSortedListOfItemFrequencies()
            get sorted list of item frequencies
        getSortedListOfTransactionLength()
            get sorted list of transaction length
        save(data, outputFile)
            store data into outputFile
        getMinimumPeriod()
            get the minimum period
        getAveragePeriod()
            get the average period
        getMaximumPeriod()
            get the maximum period
        getStandardDeviationPeriod()
            get the standard deviation period
        getNumberOfTransactionsPerTimestamp()
            get number of transactions per time stamp. This time stamp range is 1 to max period.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.dbStats import TransactionalDatabase as db

            obj = db.TransactionalDatabase(iFile, "\t")

            obj.save(oFile)

            obj.run()

            obj.printStats()

    """

    def __init__(self, inputFile: Union[str, pd.DataFrame], sep: str='\t') -> None:
        """
        :param inputFile: input file name or path
        :type inputFile: str
        :param sep: separator
        :type sep: str
        :return: None
        """
        self.inputFile = inputFile
        self.lengthList = []
        self.sep = sep
        self.database = {}
        self.itemFrequencies = {}

    def run(self) -> None:
        self.readDatabase()

    def readDatabase(self) -> None:
        """
        read database from input file and store into database and size of each transaction.
        """
        # self.creatingItemSets()
        numberOfTransaction = 0
        if isinstance(self.inputFile, pd.DataFrame):
            if self.inputFile.empty:
                print("its empty..")
            i = self.inputFile.columns.values.tolist()
            if 'tid' in i and 'Transactions' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
            if 'tid' in i and 'Patterns' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
        if isinstance(self.inputFile, str):
            if validators.url(self.inputFile):
                data_ = urlopen(self.inputFile)
                for line in data_:
                    numberOfTransaction += 1
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self.sep)]
                    temp = [x for x in temp if x]
                    self.database[numberOfTransaction] = temp
            else:
                try:
                    with open(self.inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            numberOfTransaction += 1
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self.sep)]
                            temp = [x for x in temp if x]
                            self.database[numberOfTransaction] = temp
                except IOError:
                    print("File Not Found")
                    quit()
        self.lengthList = [len(s) for s in self.database.values()]

    def getDatabaseSize(self) -> int:
        """
        get the size of database
        :return: dataset size
        :rtype: int
        """
        return len(self.database)

    def getTotalNumberOfItems(self) -> int:
        """
        get the number of items in database.
        :return: number of items
        :rtype: int
        """
        return len(self.getSortedListOfItemFrequencies())

    def getMinimumTransactionLength(self) -> int:
        """
        get the minimum transaction length
        :return: minimum transaction length
        :rtype: int
        """
        return min(self.lengthList)

    def getAverageTransactionLength(self) -> float:
        """
        get the average transaction length. It is sum of all transaction length divided by database length.
        :return: average transaction length
        :rtype: float
        """
        totalLength = sum(self.lengthList)
        return totalLength / len(self.database)

    def getMaximumTransactionLength(self) -> int:
        """
        get the maximum transaction length
        :return: maximum transaction length
        :rtype: int
        """
        return max(self.lengthList)

    def getStandardDeviationTransactionLength(self) -> float:
        """
        get the standard deviation transaction length
        :return: standard deviation transaction length
        :rtype: float
        """
        return statistics.pstdev(self.lengthList)

    def getVarianceTransactionLength(self) -> float:
        """
        get the variance transaction length
        :return: variance transaction length
        :rtype: float
        """
        return statistics.variance(self.lengthList)

    def getNumberOfItems(self) -> int:
        """
        get the number of items in database.
        :return: number of items
        :rtype: int
        """
        return len(self.getSortedListOfItemFrequencies())

    def convertDataIntoMatrix(self) -> np.ndarray:
        singleItems = self.getSortedListOfItemFrequencies()
        # big_array = np.zeros((self.getDatabaseSize(), len(self.getSortedListOfItemFrequencies())))
        itemsets = {}
        for i in self.database:
            for item in singleItems:
                if item in itemsets:
                    if item in self.database[i]:
                        itemsets[item].append(1)
                    else:
                        itemsets[item].append(0)
                else:
                    if item in self.database[i]:
                        itemsets[item] = [1]
                    else:
                        itemsets[item] = [0]
        # new = pd.DataFrame.from_dict(itemsets)
        data_ = list(itemsets.values())
        an_array = np.array(data_)
        return an_array

    def getSparsity(self) -> float:
        """
        get the sparsity of database. sparsity is percentage of 0 of database.
        :return: database sparsity
        :rtype: float
        """
        big_array = self.convertDataIntoMatrix()
        n_zeros = np.count_nonzero(big_array == 0)
        return n_zeros / big_array.size

    def getDensity(self) -> float:
        """
        get the sparsity of database. sparsity is percentage of 0 of database.
        :return: database sparsity
        :rtype: float
        """
        big_array = self.convertDataIntoMatrix()
        n_zeros = np.count_nonzero(big_array != 0)
        return n_zeros / big_array.size

    def getSortedListOfItemFrequencies(self) -> dict:
        """
        get sorted list of item frequencies
        :return: item frequencies
        :rtype: dict
        """
        itemFrequencies = {}
        for tid in self.database:
            for item in self.database[tid]:
                itemFrequencies[item] = itemFrequencies.get(item, 0)
                itemFrequencies[item] += 1
        self.itemFrequencies = {k: v for k, v in sorted(itemFrequencies.items(), key=lambda x: x[1], reverse=True)}
        return self.itemFrequencies
    
    def getFrequenciesInRange(self) -> dict:
        fre = self.getSortedListOfItemFrequencies()
        rangeFrequencies = {}
        maximum = max([i for i in fre.values()])
        values = [int(i*maximum/6) for i in range(1,6)]
        va = len({key: val for key, val in fre.items() if 0 < val < values[0]})
        rangeFrequencies[va] = values[0]
        for i in range(1,len(values)):
            va = len({key: val for key, val in fre.items() if values[i] > val > values[i - 1]})
            rangeFrequencies[va] = values[i]
        return rangeFrequencies

    def getTransanctionalLengthDistribution(self) -> dict:
        """
        Get transaction length
        :return: a dictionary with transaction length as keys and their total length as values
        :rtype: dict
        """
        transactionLength = {}
        for length in self.lengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def save(self, data_: dict, outputFile: str) -> None:
        """
        store data into outputFile
        :param data_: input data
        :type data_: dict
        :param outputFile: output file name or path to store
        :type outputFile: str
        :return: None
        """
        with open(outputFile, 'w') as f:
            for key, value in data_.items():
                f.write(f'{key}\t{value}\n')
                   
    def printStats(self) -> None:
        print(f'Database size (total no of transactions) : {self.getDatabaseSize()}')
        print(f'Number of items : {self.getNumberOfItems()}')
        print(f'Minimum Transaction Size : {self.getMinimumTransactionLength()}')
        print(f'Average Transaction Size : {self.getAverageTransactionLength()}')
        print(f'Maximum Transaction Size : {self.getMaximumTransactionLength()}')
        print(f'Standard Deviation Transaction Size : {self.getStandardDeviationTransactionLength()}')
        print(f'Variance in Transaction Sizes : {self.getVarianceTransactionLength()}')
        print(f'Sparsity : {self.getSparsity()}')
  
    def plotGraphs(self) -> None:
        # itemFrequencies = self.getFrequenciesInRange()
        transactionLength = self.getTransanctionalLengthDistribution()
        plt.plotLineGraphFromDictionary(self.itemFrequencies, 100, 0, 'Frequency', 'No of items', 'frequency')
        plt.plotLineGraphFromDictionary(transactionLength, 100, 0, 'transaction length', 'transaction length', 'frequency')


if __name__ == '__main__':
    data = {'tid': [1, 2, 3, 4, 5, 6, 7],

            'Transactions': [['a', 'd', 'e'], ['b', 'a', 'f', 'g', 'h'], ['b', 'a', 'd', 'f'], ['b', 'a', 'c'],
                             ['a', 'd', 'g', 'k'],

                             ['b', 'd', 'g', 'c', 'i'], ['b', 'd', 'g', 'e', 'j']]}

    # data = pd.DataFrame.from_dict('transactional_T10I4D100K.csv')
    import PAMI.extras.graph.plotLineGraphFromDictionary as plt
    import pandas as pd
    # obj = TransactionalDatabase(data)
    obj = TransactionalDatabase(sys.argv[1], sys.argv[2])
    #obj = TransactionalDatabase(pd.DataFrame(data))
    obj.run()
    obj.printStats()
    obj.plotGraphs()



