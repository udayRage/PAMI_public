# UVEclat is one of the fundamental algorithm to discover frequent patterns in an uncertain transactional database using PUF-Tree.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.uncertainFrequentPattern.basic import UVECLAT as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.UVEclat(iFile, minSup)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternsAsDataFrame()
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

import operator as _operator
from PAMI.uncertainFrequentPattern.basic import abstract as _ab
import deprecated

_minSup = float()
_finalPatterns = {}


class _Item:
    """
    A class used to represent the item with probability in transaction of dataset

    :Attributes:

        item : int or word
          Represents the name of the item

        probability : float
          Represent the existential probability(likelihood presence) of an item
    """

    def __init__(self, item, probability):
        self.item = item
        self.probability = probability


class UVEclat(_ab._frequentPatterns):
    """
    About this algorithm
    ====================

    :Description: It is one of the fundamental algorithm to discover frequent patterns in an uncertain transactional database using PUF-Tree.

    :Reference:  Carson Kai-Sang Leung, Lijing Sun: "Equivalence class transformation based mining of frequent itemsets from uncertain data",
                 SAC '11: Proceedings of the 2011 ACM Symposium on Applied ComputingMarch, 2011, Pages 983–984,
                 https://doi.org/10.1145/1982185.1982399

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file

        oFile : file
            Name of the output file or path of the output file

        minSup : float or int or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float

        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.

        memoryUSS : float
            To store the total amount of USS memory consumed by the program

        memoryRSS : float
            To store the total amount of RSS memory consumed by the program

        startTime:float
            To record the start time of the mining process

        endTime:float
            To record the completion time of the mining process

        Database : list
            To store the transactions of a database in list

        mapSupport : Dictionary
            To maintain the information of item and their frequency

        lno : int
            To represent the total no of transaction

        tree : class
            To represent the Tree class

        itemSetCount : int
            To represents the total no of patterns

        finalPatterns : dict
            To store the complete patterns

    :Methods:
        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        storePatternsInFile(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsInDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        creatingItemSets(fileName)
            Scans the dataset and stores in a list format
        frequentOneItem()
            Extracts the one-length frequent patterns from database

    Execution methods
    =================


    **Terminal command**


    .. code-block:: console

      Format:

      (.venv) $ python3 uveclat.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 uveclat.py sampleDB.txt patterns.txt 3

    .. note:: minSup can be specified  in support count or a value between 0 and 1.


    **Calling from a python program**
    ---------------------------------------------------
    .. code-block:: python

            from PAMI.uncertainFrequentPattern.basic import UVECLAT as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.UVEclat(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getmemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    Credits
    =======

             The complete program was written by   P.Likhitha   under the supervision of Professor Rage Uday Kiran.
    """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _finalPatterns = {}
    _iFile = " "
    oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _tidList = {}
    _rank = {}

    def _creatingItemSets(self):
        """
        Scans the dataset
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            uncertain, data = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
            if 'uncertain' in i:
                uncertain = self._iFile['uncertain'].tolist()
            for k in range(len(data)):
                tr = []
                for j in range(len(data[k])):
                    product = _Item(data[k][j], uncertain[k][j])
                    tr.append(product)
                self._Database.append(tr)

            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    tr = []
                    for i in temp:
                        i1 = i.index('(')
                        i2 = i.index(')')
                        item = i[0:i1]
                        probability = float(i[i1 + 1:i2])
                        product = _Item(item, probability)
                        tr.append(product)
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            tr = []
                            for i in temp:
                                i1 = i.index('(')
                                i2 = i.index(')')
                                item = i[0:i1]
                                probability = float(i[i1 + 1:i2])
                                product = _Item(item, probability)
                                tr.append(product)
                            self._Database.append(tr)
                except IOError:
                    print("File Not Found")

    def _frequentOneItem(self):
        """
        Takes the self.Database and calculates the support of each item in the dataset and assign the ranks to the items by decreasing support and returns the frequent items list
        """
        mapSupport = {}
        k = 0
        for i in self._Database:
            k += 1
            for j in i:
                if j.item not in mapSupport:
                    mapSupport[str(j.item)] = j.probability
                    self._tidList[str(j.item)] = {k: j.probability}
                else:
                    mapSupport[str(j.item)] += j.probability
                    self._tidList[str(j.item)].update({k: j.probability})
        mapSupport = {k: v for k, v in mapSupport.items() if v >= self._minSup}
        plist = dict( sorted(mapSupport.items(), key=_operator.itemgetter(1),reverse=True))
        return list(plist.keys())

    @staticmethod
    def _check(i, x):
        """
        To check the presence of item or pattern in transaction

        :param x: it represents the pattern
        :type x : list
        :param i : represents the uncertain self.Database
        :type i : list
        """

        # This method taken a transaction as input and returns the tree
        for m in x:
            k = 0
            for n in i:
                if m == n.item:
                    k += 1
            if k == 0:
                return 0
        return 1

    @staticmethod
    def _convert(value):
        """
        To convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type minSup value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = float(value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        return value

    def _removeFalsePositives(self):
        """
        To remove the false positive patterns generated in frequent patterns

        :return: patterns with accurate probability
        """
        global _finalPatterns
        periods = {}
        for i in self._Database:
            for x, y in _finalPatterns.items():
                if len(x) == 1:
                    periods[x] = y
                else:
                    s = 1
                    check = self._check(i, x)
                    if check == 1:
                        for j in i:
                            if j.item in x:
                                s *= j.probability
                        if x in periods:
                            periods[x] += s
                        else:
                            periods[x] = s
        for x, y in periods.items():
            if y >= self._minSup:
                sample = str()
                for i in x:
                    sample = sample + i + "\t"
                self._finalPatterns[sample] = y

    @staticmethod
    def _Intersection(tidSetx, tidSetY):
        """
        This function is used to find the intersection

        :param tidSetx: the timestamp of a patterns
        :type tidSetx: dict
        :param tidSetY: the timestamp of a patterns
        :type tidSetY: dict
        """
        tids = []
        support = []
        tidDict = {}
        for x, y in tidSetx.items():
            for x1, y1 in tidSetY.items():
                if x == x1:
                    tids.append(x)
                    support.append(y * y1)
                    tidDict.update({x: y * y1})
        return tidDict

    def _calculateExpSup(self, tidList):
        """
        This function is used to calculate support of tidList

        :param tidList: timestamp of a list.
        :type tidList: List
        """
        return sum(tidList.values())

    def _save(self, prefix, suffix, tidSetI):
        """
        Saves the patterns that satisfy the periodic frequent property.

        :param prefix: the prefix of a pattern
        :type prefix: list
        :param suffix: the suffix of a patterns
        :type suffix: list
        :param tidSetI: the timestamp of a patterns
        :type tidSetI: dict
        """

        global _finalPatterns
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        val = self._calculateExpSup(tidSetI)
        _finalPatterns[tuple(prefix)] = val

    def _Generation(self, prefix, itemSets, tidSets):
        """
        Equivalence class is followed  and checks for the patterns generated for periodic-frequent patterns.

        :param prefix:  main equivalence prefix
        :type prefix: periodic-frequent item or pattern
        :param itemSets: patterns which are items combined with prefix and satisfying the periodicity and frequent with their timestamps
        :type itemSets: list
        :param tidSets: timestamps of the items in the argument itemSets
        :type tidSets: list
        """
        if len(itemSets) == 1:
            i = itemSets[0]
            tidI = tidSets[0]
            self._save(prefix, [i], tidI)
            return
        for i in range(len(itemSets)):
            itemI = itemSets[i]
            if itemI is None:
                continue
            tidSetI = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetX = [itemI]
            for j in range(i + 1, len(itemSets)):
                itemJ = itemSets[j]
                tidSetJ = tidSets[j]
                y = self._Intersection(tidSetI, tidSetJ)
                if self._calculateExpSup(y) >= self._minSup:
                    classItemSets.append(itemJ)
                    classTidSets.append(y)
            newPrefix = list(set(itemSetX)) + prefix
            self._Generation(newPrefix, classItemSets, classTidSets)
            self._save(prefix, list(set(itemSetX)), tidSetI)

    def mine(self):
        """
        Main method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patterns
        """
        global _minSup
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        _minSup = self._minSup
        plist = self._frequentOneItem()
        for i in range(len(plist)):
            itemI = plist[i]
            tidSetI = self._tidList[itemI]
            itemSetX = [itemI]
            itemSets = []
            tidSets = []
            for j in range(i+1, len(plist)):
                itemJ = plist[j]
                tidSetJ = self._tidList[itemJ]
                y1 = self._Intersection(tidSetI, tidSetJ)
                if self._calculateExpSup(y1) >= self._minSup:
                    itemSets.append(itemJ)
                    tidSets.append(y1)
            self._Generation(itemSetX, itemSets, tidSets)
            self._save(None, itemSetX, tidSetI)
        self._removeFalsePositives()
        print("Frequent patterns were generated from uncertain databases successfully using PUF algorithm")
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

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

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, oFile):
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param oFile: name of the output file
        :type oFile: csv file
        """
        self.oFile = oFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
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
        print("Total number of  Uncertain Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = UVEclat(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = UVEclat(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        print("Total number of Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
