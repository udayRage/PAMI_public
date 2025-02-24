#This code is used to calculate multiple minimum support of items in the the given database. Output can be stored in file or as as dataframe.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.calculateMISValues import usingSD as db
#
#             obj = db.usingSD(iFile, 16, "\t")
#
#             obj.getPatterns("outputFileName") # To create patterns as dataframes
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
import sys as _sys
import pandas as _pd
import validators as _validators
import statistics as _statistics
from urllib.request import urlopen as _urlopen

class usingSD:
    """

    :Description: This code is used to calculate multiple minimum support of items in the the given database. Output can be stored in file or as as dataframe.

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param sd: int :
                   SD of items to mine complete set of frequent patterns.
    :param  threshold: int :
                   The user can specify threshold either in count or proportion of database size. If the program detects the data type of threshold is integer, then it treats threshold is expressed in count.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.calculateMISValues import usingSD as db

            obj = db.usingSD(iFile, 16, "\t")

            obj.getPatterns("outputFileName") # To create patterns in dataframe

            obj.save(oFile)
    """

    _iFile: str = ' '
    _sd: int = int()
    _sep: str = str()
    _threshold: int = int()
    _finalPatterns: dict = {}


    def __init__(self, iFile: str, threshold: int, sep: str):
        self._iFile = iFile
        self._threshold = threshold
        self._sep = sep
        self._oFile = str

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        self._mapSupport = {}
        if isinstance(self._iFile, _pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()

        if isinstance(self._iFile, str):
            if _validators.url(self._iFile):
                data = _urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            self._lno += 1
                            splitter = [i.rstrip() for i in line.split(self._sep)]
                            splitter = [x for x in splitter if x]
                            self._Database.append(splitter)
                except IOError:
                    print("File Not Found")

    def _creatingFrequentItems(self) -> tuple:
        """
        This function creates frequent items from _database.
        :return: frequentTidData that stores frequent items and their tid list.
        :rtype: tuple
        """
        tidData = {}
        self._lno = 0
        for transaction in self._Database:
            self._lno = self._lno + 1
            for item in transaction:
                if item not in tidData:
                    tidData[item] = [self._lno]
                else:
                    tidData[item].append(self._lno)
        mini = min([len(k) for k in tidData.values()])
        sd = _statistics.stdev([len(k) for k in tidData.values()])
        frequentTidData = {k: len(v) - sd for k, v in tidData.items()}
        return mini, frequentTidData

    def calculateMIS(self) -> None:
        self._creatingItemSets()
        mini, frequentItems = self._creatingFrequentItems()
        for x, y in frequentItems.items():
            if y < self._threshold:
                self._finalPatterns[x] = mini
            else:
                self._finalPatterns[x] = y

    def getDataFrame(self) -> _pd.DataFrame:
        """
        Storing Items and its respective calculated minimum support values in a dataframe
        :return: returning Items and its respective calculated minimum support values in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataFrame = _pd.DataFrame(data, columns=['Items', 'MIS'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete Items and its respective calculated minimum support values will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x + "\t" + str(y)
            writer.write("%s \n" % patternsAndSupport)

if __name__ == '__main__':
    cd = usingSD(_sys.argv[1],int(_sys.argv[2]),_sys.argv[3])
    cd.calculateMIS()
    cd.save(_sys.argv[4])
