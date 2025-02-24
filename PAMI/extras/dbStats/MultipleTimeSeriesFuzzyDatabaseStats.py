# MultipleTimeSeriesFuzzyDatabaseStats is class to get stats of multiple time series fuzzy database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.dbStats import MultipleTimeSeriesFuzzyDatabaseStats as db
#
#             obj = db.MultipleTimeSeriesDatabaseStats(iFile, "\t")
#
#             obj.run()
#
#             obj.printStats()
#
#             obj.save(oFile)
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
import statistics
import pandas as pd
import validators
import numpy as np
from urllib.request import urlopen
import sys
import PAMI.extras.graph.plotLineGraphFromDictionary as plt


class MultipleTimeSeriesFuzzyDatabaseStats:
    """
    :Description:  MultipleTimeSeriesDatabaseStats is class to get stats of multiple time series fuzzy database.

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
        getTotalNumberOfItems()
            get the total number of items in a database
        getMinimumTransactionLength()
            get the minimum transaction length
        getAverageTransactionLength()
            get the average transaction length. It is sum of all transaction length divided by database length.
        getMaximumTransactionLength()
            get the maximum transaction length
        getStandardDeviationTransactionLength()
            get the standard deviation of transaction length
        convertDataIntoMatrix()
            Convert the database into matrix form to calculate the sparsity and density of a database
        getSparsity()
            get sparsity value of database
        getDensity()
            get density value of database
        getSortedListOfItemFrequencies()
            get sorted list of item frequencies
        getSortedListOfTransactionLength()
            get sorted list of transaction length
        save(data, outputFile)
            store data into outputFile
        printStats()
            To print all the stats of the database
        plotGraphs()
            To plot all the graphs of frequency disctribution of items and transaction length distribution in database
   

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.dbStats import MultipleTimeSeriesFuzzyDatabaseStats as db

            obj = db.MultipleTimeSeriesFuzzyDatabaseStats(iFile, "\t")

            obj.run()

            obj.save(oFile)

            obj.printStats()

    """

    def __init__(self, inputFile: str, sep: str='\t'):
        """
        :param inputFile: input file name or path
        :type inputFile: str
        :param sep: separator
        :type sep: str
        """
        self.inputFile = inputFile
        self.lengthList = []
        self.sep = sep
        self.database = {}
        self.itemFrequencies = {}
        self._transactions, self._fuzzyValues, self._Database, self._ts = [], [], [], []

    def run(self) -> None:
        self.readDatabase()

    def readDatabase(self) -> None:
        """
        read database from input file and store into database and size of each transaction.
        """
        self._transactions, self._fuzzyValues, self._Database, self._ts = [], [], [], []
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
                data = urlopen(self.inputFile)
                for line in data:
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
                            line = line.strip()
                            parts = line.split(":")
                            numberOfTransaction += 1
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            parts[2] = parts[2].strip()
                            times = parts[0].split(self.sep)
                            items = parts[1].split(self.sep)
                            quantities = parts[2].split(self.sep)
                            #print(times, items, quantities)
                            _time = [x for x in times if x]
                            items = [x for x in items if x]
                            quantities = [float(x) for x in quantities if x]
                            tempList = []
                            for k in range(len(_time)):
                                ite = "(" + _time[k] + "," + items[k] + ")"
                                tempList.append(ite)
                            self._ts.append([x for x in times])
                            self._transactions.append([x for x in tempList])
                            self._fuzzyValues.append([x for x in quantities])
                            self.database[numberOfTransaction] = tempList
                except IOError:
                    print("File Not Found")
                    quit()
        self.lengthList = [len(s) for s in self._transactions]

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
        data = list(itemsets.values())
        an_array = np.array(data)
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
        for line in range(len(self._transactions)):
            times = self._ts[line]
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            for i in range(0, len(items)):
                item = items[i]
                if item in itemFrequencies:
                    itemFrequencies[item] += quantities[i]
                else:
                    itemFrequencies[item] = quantities[i]
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
        get transaction length
        :return: transactional length
        :rtype: dict
        """
        transactionLength = {}
        for length in self.lengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def save(self, data: dict, outputFile: str) -> None:
        """
        store data into outputFile
        :param data: input data
        :type data: dict
        :param outputFile: output file name or path to store
        :type outputFile: str
        :return: None
        """
        with open(outputFile, 'w') as f:
            for key, value in data.items():
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
    import PAMI.extras.graph.plotLineGraphFromDictionary as plt
    import pandas as pd
    obj = MultipleTimeSeriesFuzzyDatabaseStats(sys.argv[1])
    obj.run()
    obj.printStats()
    obj.plotGraphs()
