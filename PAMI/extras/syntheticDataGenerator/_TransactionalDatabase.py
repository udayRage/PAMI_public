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
import sys


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

        numLines: int
            Number of lines
        avgItemsPerLine: int
            Average number of items per line
        numItems: int
            Total number of items

    :Methods:

        create: 
            Generate the transactional database
        save: 
            Save the transactional database to a user-specified file
        getTransactions: 
            Get the transactional database


    **Methods to execute code on terminal**
    ---------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 TransactionalDatabase_old.py <numLines> <avgItemsPerLine> <numItems>

      Example Usage:

      (.venv) $ python3 TransactionalDatabase_old.py 50.0 10.0 100



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

    @staticmethod
    def _generateArray(nums, avg):
        """
        Generate a random array of length n whose values average to m

        :param nums: number of values
        :type nums: int
        :param avg: average value
        :type avg: int


        Returns:
        values: list - random array
        """

        # generate n random values
        values = np.random.randint(1, avg * 2, nums)
        sums = np.sum(values)
        weights = values / sums

        # Calculate sumRes
        sumRes = nums * avg

        # Adjust values based on weights and sumRes
        new_values = np.round(sumRes * weights).astype(int)

        # if all transactions have 0 items, add 1 item to each transaction
        for loc in np.where(new_values < 1)[0]:
            new_values[loc] += 1

        difference = sumRes - np.sum(new_values)
        if difference > 0:
            for i in range(difference):
                index = np.random.randint(0, len(new_values))
                new_values[index] += 1
        else:
            for i in range(abs(difference)):
                index = np.random.randint(0, len(new_values))
                new_values[index] -= 1

        return values

    def create(self) -> None:
        """
        Generate the transactional database with the given input parameters.
        Returns: None
        """

        values = self._generateArray(self.databaseSize, self.avgItemsPerTransaction)

        self.db = []
        for i in range(self.databaseSize):
            self.db.append(np.random.choice(range(1, self.numItems + 1), values[i], replace=False))

    def save(self, filename) -> None:
        """
        Save the transactional database to a file

        :param filename: name of the file
        :type filename: str
        """

        with open(filename, 'w') as f:
            for line in self.db:
                f.write(str(self.sep).join(map(str, line)) + '\n')

    def getTransactions(self, sep = "\t") -> pd.DataFrame:
        """
        Get the transactional database in dataFrame format

        Returns:
        db: pd.dataFrame - transactional database
        """
        column = "Transactions"
        db = pd.DataFrame(columns=[column])
        db[column] = [sep.join(map(str, line)) for line in self.db]
        return db
        

if __name__ == "__main__":

    if len(sys.argv) == 5:
        obj = TransactionalDatabase(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        obj.create()
        obj.save(sys.argv[4])
    if len(sys.argv) == 6:
        obj = TransactionalDatabase(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
        obj.create()
        obj.save(sys.argv[5])
    else:
        raise ValueError("Invalid number of arguments. Args: <numLines> <avgItemsPerLine> <numItems> <filename> or Args: <numLines> <avgItemsPerLine> <numItems> <sep> <filename>")
    