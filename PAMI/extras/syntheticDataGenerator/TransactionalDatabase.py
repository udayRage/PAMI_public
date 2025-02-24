# TransactionalDatabase is a collection of transactions. It only considers the data in  transactions and ignores the metadata.
#
#  **Importing this algorithm into a python program**
#  --------------------------------------------------------
#     from PAMI.extras.syntheticDataGenerator import TransactionalDatabase as db
#
#     obj = db(10, 5, 10)
#
#     obj.create()
#
#     obj.save('db.txt')
#
#     print(obj.getTransactions())
#
import numpy as np
import pandas as pd
import sys, psutil, os, time

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


class TransactionalDatabase:
    """
        :Description: TransactionalDatabase is a collection of transactions. It only considers the data in  transactions and ignores the metadata.
        :Attributes:

            dataBaseSize: int
                Number of Transactions in a database
            avgItemsPerTransaction: int
                Average number of items per transaction
            itemsNo: int
                Total number of items
            memoryUSS : float
                To store the total amount of USS memory consumed by the program
            memoryRSS : float
                        To store the total amount of RSS memory consumed by the program
            startTime : float
                        To record the start time of the mining process
            endTime : float
                        To record the completion time of the mining process

        :Methods:

            create:
                Generate the transactional database
            save:
                Save the transactional database to a user-specified file
            getTransactions:
                Get the transactional database
            getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
            getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
            getRuntime()
                Total amount of runtime taken by the mining process will be retrieved from this function

        **Methods to execute code on terminal**
        ---------------------------------------------

        .. code-block:: console

          Format:

          (.venv) $ python3 TransactionalDatabase.py <dataBaseSize> <avgItemsPerTransaction> <itemsNo>

          Example Usage:

          (.venv) $ python3 TransactionalDatabase.py 50.0 10.0 100


        **Importing this algorithm into a python program**
        --------------------------------------------------------
            from PAMI.extras.syntheticDataGenerator import TransactionalDatabase as db

            obj = db.TransactionalDatabase(10, 5, 10)

            obj.create()

            obj.save('db.txt')

            print(obj.getTransactions())


        """

    def __init__(self, databaseSize, avgItemsPerTransaction, numItems,sep = "\t") -> None:

        """
        Initialize the transactional database with the given parameters

        :param databaseSize: total number of transactions in the database
        :type databaseSize: int
        :param avgItemsPerTransaction: average number of items per transaction
        :type avgItemsPerTransaction: int
        :param numItems: total number of items
        :type numItems: int
        :param sep: separator to distinguish the items in a transaction
        :type sep: str
        """

        self.databaseSize = databaseSize
        self.avgItemsPerTransaction = avgItemsPerTransaction
        self.numItems = numItems
        self.sep = sep
        self.db = []
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()


    @staticmethod
    def _generateArray(databaseSize, avgItemsPerTransaction):

        #generating random numbers with size of dataBaseSize
        transactionSize = np.random.rand(databaseSize)

        #sum of the values in the transactionSize array - sumTransactions
        sumTransactions = np.sum(transactionSize)

        #weights of the values in the array - transactionSize
        weights = transactionSize/sumTransactions

        #sumResultant -> whose average is equal to averageItemsPerTransaction's value
        sumResultant = avgItemsPerTransaction*databaseSize

        #Getting new values whose average is averageItemsPerTransaction
        newValues = np.round(weights*sumResultant)

        #changing the values in numpy array to int
        valuesInt = newValues.astype(int)

        #finding if there are any 0's in the array
        indexZero = np.where(valuesInt==0)[0]

        #Adding +1 to the transactions which have 0
        if len(indexZero)==0:
            return valuesInt
        else:
            for i in indexZero:
                valuesInt[i]+=1

        return valuesInt

    def create(self):
        self._startTime = time.time()
        noofItemsperTrans = self._generateArray(self.databaseSize, self.avgItemsPerTransaction)
        for i in range(self.databaseSize):
            self.db.append(np.random.choice(range(1,self.numItems+1), noofItemsperTrans[i], replace=False))

        self._endTime = time.time()

    def save(self, filename):
        with open(filename, 'w') as f:
            for line in self.db:
                f.write(str(self.sep).join(map(str, line)) + '\n')


    def getTransactions(self):
        transactions = []
        for line in self.db:
            transactions.append(line)

        dataFrame = pd.DataFrame([transactions], index=['Transactions']).T
        return dataFrame


    def getMemoryUSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        return self._memoryUSS

    def getMemoryRSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryRSS = process.memory_info().rss
        return self._memoryRSS

    def getRuntime(self) -> float:
        return self._endTime - self._startTime

if __name__ == "__main__":

    if len(sys.argv) == 5:
        obj = TransactionalDatabase(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        obj.create()
        obj.save(sys.argv[4])
        print("Total Memory in USS:", obj.getMemoryUSS())
        print("Total Memory in RSS", obj.getMemoryRSS())
        print("Total ExecutionTime in ms:", obj.getRuntime())
    elif len(sys.argv) == 6:
        obj = TransactionalDatabase(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
        obj.create()
        obj.save(sys.argv[5])
        print("Total Memory in USS:", obj.getMemoryUSS())
        print("Total Memory in RSS", obj.getMemoryRSS())
        print("Total ExecutionTime in ms:", obj.getRuntime())
    elif len(sys.argv) == 4:
        obj = TransactionalDatabase(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        obj.create()
        print("Total Memory in USS:", obj.getMemoryUSS())
        print("Total Memory in RSS", obj.getMemoryRSS())
        print("Total ExecutionTime in ms:", obj.getRuntime())
    else:
        raise ValueError(
            "Invalid number of arguments. Args: <databaseSize> <avgItemsPerTransaction> <noOfItems> <filename> or Args: <databaseSize> <avgItemsPerTransaction> <noOfItems> <sep> <filename>")

