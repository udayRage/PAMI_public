# VBFTMine is one of the fundamental algorithm to discover fault-tolerant frequent patterns in an uncertain transactional database based on bitset representation.
#
# **Importing this algorithm into a python program**
#
#             import PAMI.uncertainFaultTolerantFrequentPattern.basic.VBFTMine as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             itemSup = 2  # can also be specified between 0 and 1
#
#             minLength = 3 # can also be specified between 0 and 1
#
#             faultTolerance = 2 # can also be specified between 0 and 1
#
#             obj = alg.VBFTMine(iFile, minSup, itemSup, minLength, faultTolerance)
#
#             obj.mine()
#
#             faultTolerantFrequentPattern = obj.getPatterns()
#
#             print("Total number of Fault Tolerant Frequent Patterns:", len(faultTolerantFrequentPattern))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternInDataFrame()
#
#             memUSS = obj.getMemoryUSS()
#
#             print("Total Memory in USS:", memUSS)
#
#             memRSS = obj.getMemoryRSS()
#
#             print("Total Memory in RSS", memRSS)
#
#             run = obj.getRuntime()
#
#             print("Total ExecutionTime in seconds:", run)
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

import pandas as pd
from deprecated import deprecated

import numpy as _np
from PAMI.faultTolerantFrequentPattern.basic import abstract as _ab

class VBFTMine(_ab._faultTolerantFrequentPatterns):
    """
    About this algorithm
    ====================
    
    :Description:  VBFTMine is one of the fundamental algorithm to discover fault tolerant frequent patterns in an uncertain transactional database based on
                   bitset representation.
                   This program employs apriori property (or downward closure property) to  reduce the search space effectively.

    :Reference:   Koh, JL., Yo, PW. (2005). An Efficient Approach for Mining Fault-Tolerant Frequent Patterns Based on Bit Vector Representations.
            In:   Zhou, L., Ooi, B.C., Meng, X. (eds) Database Systems for Advanced Applications. DASFAA 2005. Lecture Notes in Computer Science,
                  vol 3453. Springer, Berlin, Heidelberg. https://doi.org/10.1007/11408079_51

    :param  iFile: str :
                   Name of the Input file to mine complete set of uncertain Fault Tolerant FrequentFrequent Patterns
    :param  oFile: str :
                   Name of the output file to store complete set of uncertain Fault Tolerant FrequentFrequent Patterns
    :param  minSup: float or int or str :
                   The user can specify minSup either in count or proportion of database size.
                   If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
                   Otherwise, it will be treated as float.
                   Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
    :param  itemSup: int or float :
                    Frequency of an item
    :param minLength: int
                    minimum length of a pattern
    :param faultTolerance: int :
                    The ability of a pattern mining algorithm to handle errors or inconsistencies in the data without completely failing or producing incorrect results.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        startTime : float
          To record the start time of the mining process

        endTime : float
          To record the completion time of the mining process

        finalPatterns : dict
          Storing the complete set of patterns in a dictionary variable

        memoryUSS : float
          To store the total amount of USS memory consumed by the program

        memoryRSS : float
          To store the total amount of RSS memory consumed by the program

        Database : list
          To store the transactions of a database in list


    Execution methods
    =================

    **Terminal command**


    .. code-block:: console

       Format:

       (.venv) $ python3 VBFTMine.py <inputFile> <outputFile> <minSup> <itemSup> <minLength> <faultTolerance>

       Examples usage:

       (.venv) $ python3 VBFTMine.py sampleDB.txt patterns.txt 10.0 3.0 3 1

    .. note:: minSup will be considered in times of minSup and count of database transactions


    **Calling from a python program**

    .. code-block:: python
    
            import PAMI.faultTolerantFrequentPattern.basic.VBFTMine as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            itemSup = 2  # can also be specified between 0 and 1

            minLength = 3 # can also be specified between 0 and 1

            faultTolerance = 2 # can also be specified between 0 and 1

            obj = alg.VBFTMine(iFile, minSup, itemSup, minLength, faultTolerance)

            obj.mine()

            faultTolerantFrequentPattern = obj.getPatterns()

            print("Total number of Fault Tolerant Frequent Patterns:", len(faultTolerantFrequentPattern))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    Credits
    =======

           The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    _minSup = float()
    _itemSup = float()
    _minLength = int()
    _faultTolerance = int()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _plist = []
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}

    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()

            for k in temp:
                self._Database.append(set(k))
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(set(temp))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            for i in temp:
                                if i not in self._plist:
                                    self._plist.append(i)
                            self._Database.append(set(temp))
                except IOError:
                    print("File Not Found")
                    quit()

    def _convert(self, value):
        """
        To convert the user specified minSup value

        :param value: user specified minSup value
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def _Count(self, tids):
        """
        Count the occurrences of 1s in the given list of transaction IDs.

        :param tids: List of transaction IDs.
        :type tids: List[int]
        :return: Count of occurrences of 1s in the list.
        :rtype: int
        """
        count = 0
        for i in tids:
            if i == 1:
                count += 1
        return count

    def _save(self, prefix, suffix, tidsetx):
        """
        Save the pattern with its support count if it meets the fault tolerance criteria.

        :param prefix: Prefix part of the pattern.
        :type prefix: list
        :param suffix: Suffix part of the pattern.
        :type suffix: list
        :param tidsetx: Transaction IDs associated with the pattern.
        :type tidsetx: list
        :return: None
        """
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        prefix = list(set(prefix))
        prefix.sort()
        val = self._Count(tidsetx)
        if len(prefix) > self._faultTolerance:
            self._finalPatterns[tuple(prefix)] = val

    def _processEquivalenceClass(self, prefix, itemsets, tidsets):
        """
        Process the equivalence class to generate frequent patterns.

        :param prefix: Prefix part of the pattern.
        :type prefix: list.
        :param itemsets: List of itemsets in the equivalence class.
        :type itemsets: list.
        :param tidsets: List of transaction IDs associated with each itemset.
        :type tidsets: list
        :return: None
        """
        if len(itemsets) == 1:
            i = itemsets[0]
            tidi = tidsets[0]
            self._save(prefix, [i], tidi)
            return
        for i in range(len(itemsets)):
            itemx = itemsets[i]
            if itemx is None:
                continue
            tidsetx = tidsets[i]
            classItemsets = []
            classtidsets = []
            itemsetx = [itemx]
            for j in range(i + 1, len(itemsets)):
                itemj = itemsets[j]
                tidsetj = tidsets[j]
                y = list(_np.array(tidsetx) & _np.array(tidsetj))
                total = self._Count(y)
                if total >= self._minSup:
                    classItemsets.append(itemj)
                    classtidsets.append(y)
            if len(classItemsets) > 0:
                newprefix = list(set(itemsetx)) + prefix
                self._processEquivalenceClass(newprefix, classItemsets, classtidsets)
            self._save(prefix, list(set(itemsetx)), tidsetx)

    def _oneLengthFrequentItems(self):
        """
        To calculate the one Length items
        """
        Vector = {}
        items = []
        for i in self._Database:
            for j in self._plist:
                count = 0
                if j in i:
                    count = 1
                if j in Vector:
                    Vector[j].append(count)
                else:
                    Vector[j] = [count]
        for x, y in Vector.items():
            v = self._Count(y)
            if v >= self._itemSup:
                items.append(x)
        return Vector, items

    @deprecated(
        "It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._itemSup = self._convert(self._itemSup)
        self._minLength = int(self._minLength)
        self._faultTolerance = int(self._faultTolerance)
        Vector, plist = self._oneLengthFrequentItems()
        for i in range(len(plist)):
            itemx = plist[i]
            tidsetx = Vector[itemx]
            itemsetx = [itemx]
            itemsets = []
            tidsets = []
            for j in range(i + 1, len(plist)):
                itemj = plist[j]
                tidsetj = Vector[itemj]
                y1 = list(_np.array(tidsetx) | _np.array(tidsetj))
                total = self._Count(y1)
                if total >= self._minSup:
                    itemsets.append(itemj)
                    tidsets.append(y1)
            if len(itemsets) > 0:
                self._processEquivalenceClass(itemsetx, itemsets, tidsets)
            self._save(None, itemsetx, tidsetx)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Fault-Tolerant Frequent patterns were generated successfully using VBFTMine algorithm ")

    def getMemoryUSS(self):
        """

        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """

        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """

        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            s = str()
            for i in a:
                s = s + i + ' '
            data.append([s, b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        # dataFrame = dataFrame.replace(r'\r+|\n+|\t+',' ', regex=True)
        return dataFrame

    def save(self, outFile):
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s = str()
            for i in x:
                s = s + i + '\t'
            s1 = s.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """

        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 7 or len(_ab._sys.argv) == 8:
        if len(_ab._sys.argv) == 8:
            _ap = VBFTMine(_ab._sys.argv[1], _ab._sys.argv[3],  _ab._sys.argv[4],
                            _ab._sys.argv[5], _ab._sys.argv[6], _ab._sys.argv[7],)
        if len(_ab._sys.argv) == 7:
            _ap = VBFTMine(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6])
        _ap.mine()
        _ap.mine()
        print("Total number of Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = VBFTMine('/Users/Likhitha/Downloads/fault/sample4.txt', 5, 3, 2, 1, ' ')
        _ap.mine()
        _ap.printResults()
        print(_ap.getPatternsAsDataFrame())
        print("Error! The number of input parameters do not match the total number of parameters provided")
