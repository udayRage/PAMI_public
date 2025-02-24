# UtilityDatabase is a code used to get stats of the database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.dbStats import UtilityDatabase as db
#
#             obj = db.UtilityDatabase(iFile, "\t")
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
from urllib.request import urlopen
import pandas as pd
from typing import Union
import PAMI.extras.graph.plotLineGraphFromDictionary as plt

class UtilityDatabase:
    """
    :Description:  UtilityDatabase is class to get stats of database.

    :Attributes:

        :param inputFile: file :
           input file path
        :param sep: str
            separator in file. Default is tab space.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.dbStats import UtilityDatabase as db

            obj = db.UtilityDatabase(iFile, "\t" )

            obj.save(oFile)

            obj.run()

            obj.printStats()

    """

    def __init__(self, inputFile: Union[str, pd.DataFrame], sep: str='\t') -> None:
        """
        :param inputFile: input file name or path
        :type inputFile: str
        :param sep: separator in file
        :type sep: str or
        :return: None
        """
        self.inputFile = inputFile
        self.database = {}
        self.lengthList = []
        self.utility = {}
        self.sep = sep
        self.Database,self.utilityValues = None,None

    def run(self) -> None:
        self.readDatabase()

    def creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.Database = []
        self.utilityValues = []
        if isinstance(self.inputFile, pd.DataFrame):
            if self.inputFile.empty:
                print("its empty..")
            i = self.inputFile.columns.values.tolist()
            if 'Transactions' in i:
                self.Database = self.inputFile['Transactions'].tolist()
            if 'Patterns' in i:
                self.Database = self.inputFile['Patterns'].tolist()
            if 'Utility' in i:
                self.utilityValues = self.inputFile['Utility'].tolist()

        if isinstance(self.inputFile, str):
            if self.inputFile.startswith("http://") or self.inputFile.startswith("https://"):
                data = urlopen(self.inputFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(":")]
                    transaction = [s for s in temp[0].split(self.sep)]
                    self.Database.append([x for x in transaction if x])
                    utilities = [int(s) for s in temp[2].split(self.sep)]
                    self.utilityValues.append([x for x in utilities if x])
            else:
                try:
                    with open(self.inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(":")]
                            transaction = [s for s in temp[0].split(self.sep)]
                            self.Database.append([x for x in transaction if x])
                            utilities = [int(s) for s in temp[2].split(self.sep)]
                            self.utilityValues.append([x for x in utilities if x])
                except IOError:
                    print("File Not Found")
                    quit()

    def readDatabase(self) -> None:
        """
        read database from input file and store into database and size of each transaction.
        """
        numberOfTransaction = 0
        self.creatingItemSets()
        for k in range(len(self.Database)):
            numberOfTransaction += 1
            transaction = self.Database[k]
            utilities = self.utilityValues[k]
            self.database[numberOfTransaction] = transaction
            for i in range(len(transaction)):
                self.utility[transaction[i]] = self.utility.get(transaction[i],0)
                self.utility[transaction[i]] += utilities[i]
        self.lengthList = [len(s) for s in self.database.values()]
        self.utility = {k: v for k, v in sorted(self.utility.items(), key=lambda x:x[1], reverse=True)}

    def getDatabaseSize(self) -> int:
        """
        get the size of database
        :return: size of database
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

    def getSparsity(self) -> float:
        # percentage of 0 dense dataframe
        """
        get the sparsity of database
        :return: sparsity of database in floating values
        :rtype: float
        """
        matrixSize = self.getDatabaseSize()*len(self.getSortedListOfItemFrequencies())
        return (matrixSize - sum(self.getSortedListOfItemFrequencies().values())) / matrixSize

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
        return {k: v for k, v in sorted(itemFrequencies.items(), key=lambda x:x[1], reverse=True)}
    
    def getFrequenciesInRange(self) -> dict:
        """
        This function is used to get the Frequencies in range
        :return: Frequencies In Range
        :rtype: dict
        """
        fre = self.getSortedListOfItemFrequencies()
        rangeFrequencies = {}
        maximum = max([i for i in fre.values()])
        values = [int(i*maximum/6) for i in range(1,6)]
        #print(maximum)
        va = len({key: val for key, val in fre.items() if 0 < val < values[0]})
        rangeFrequencies[va] = values[0]
        for i in range(1,len(values)):
            
            va = len({key: val for key, val in fre.items() if values[i] > val > values[i - 1]})
            rangeFrequencies[va] = values[i]
        return rangeFrequencies

    def getTransanctionalLengthDistribution(self) -> dict:
        """
        get transaction length
        :return: a dictionary of Transaction Length Distribution
        :rtype: dict
        """
        transactionLength = {}
        for length in self.lengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x:x[0])}

    def save(self, data, outputFile) -> None:
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

    def getTotalUtility(self) -> int:
        """
        get sum of utility
        :return: total utility
        :rtype: int
        """
        return sum(list(self.utility.values()))

    def getMinimumUtility(self) -> int:
        """
        get the minimum utility
        :return: integer value of minimum utility
        :rtype: int
        """
        return min(list(self.utility.values()))

    def getAverageUtility(self) -> float:
        """
        get the average utility
        :return: average utility
        :rtype: float
        """
        return sum(list(self.utility.values())) / len(self.utility)

    def getMaximumUtility(self) -> int:
        """
        get the maximum utility
        :return: integer value of maximum utility
        :rtype: int
        """
        return max(list(self.utility.values()))

    def getSortedUtilityValuesOfItem(self) -> dict:
        """
        get sorted utility value each item. key is item and value is utility of item
        :return: sorted dictionary utility value of item
        :rtype: dict
        """
        return self.utility
    
    def printStats(self) -> None:

        """
        This function is used to print the results
        """
        print(f'Database size : {self.getDatabaseSize()}')
        print(f'Number of items : {self.getTotalNumberOfItems()}')
        print(f'Minimum Transaction Size : {self.getMinimumTransactionLength()}')
        print(f'Average Transaction Size : {self.getAverageTransactionLength()}')
        print(f'Maximum Transaction Size : {self.getMaximumTransactionLength()}')
        print(f'Minimum utility : {self.getMinimumUtility()}')
        print(f'Average utility : {self.getAverageUtility()}')
        print(f'Maximum utility : {self.getMaximumUtility()}')
        print(f'Standard Deviation Transaction Size : {self.getStandardDeviationTransactionLength()}')
        print(f'Variance : {self.getVarianceTransactionLength()}')
        print(f'Sparsity : {self.getSparsity()}')
        
    
    def plotGraphs(self) -> None:
        
        itemFrequencies = self.getFrequenciesInRange()
        transactionLength = self.getTransanctionalLengthDistribution()
        plt.plotLineGraphFromDictionary(itemFrequencies, 100, 0, 'Frequency', 'no of items', 'frequency')
        plt.plotLineGraphFromDictionary(transactionLength, 100, 0, 'transaction length', 'transaction length', 'frequency')


if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            raise ValueError("Missing some of the input parameters. Format: python UtilityDatabase.py <fileName> <seperator (optional)>")

        iFile, separator = sys.argv[1], sys.argv[2]
        obj = UtilityDatabase(iFile, separator)
        obj.run()
        if obj.getDatabaseSize() > 0:
            obj.printStats()
            obj.plotGraphs()
        else:
            print("No data found in the database.")

    except ValueError as ve:
        print(f"ValueError: {ve}")

