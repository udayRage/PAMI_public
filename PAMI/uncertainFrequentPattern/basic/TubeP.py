# TUFP is one of the fundamental algorithm to discover top-k frequent patterns in a uncertain transactional database using CUP-Lists.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.uncertainFrequentPattern.basic import TUFP as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.TUFP(iFile, minSup)
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


from PAMI.uncertainFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Union
import pandas as pd
from deprecated import deprecated

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

    def __init__(self, item, probability) -> None:
        self.item = item
        self.probability = probability


class TUFP(_ab._frequentPatterns):
    """
    About this algorithm
    ====================

    :Description: It is one of the fundamental algorithm to discover top-k frequent patterns in a uncertain transactional database using CUP-Lists.

    :Reference:  Tuong Le, Bay Vo, Van-Nam Huynh, Ngoc Thanh Nguyen, Sung Wook Baik 5, "Mining top-k frequent patterns from uncertain databases",
                 Springer Science+Business Media, LLC, part of Springer Nature 2020, https://doi.org/10.1007/s10489-019-01622-1

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

        startTime : float
            To record the start time of the mining process

        endTime : float
            To record the completion time of the mining process

        Database : list
            To store the transactions of a database in list

        mapSupport : Dictionary
            To maintain the information of item and their frequency

        lno : int
            To represent the total no of transaction

        tree : class
            To represents the Tree class

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
        updateTransactions()
            Update the transactions by removing non-frequent items and sort the Database by item decreased support
        buildTree()
            After updating the Database, remaining items will be added into the tree by setting root node as null
        convert()
            to convert the user specified value
        mine()
            Mining process will start from this function

    Execution methods
    =================


    **Terminal command**


    .. code-block:: console

      Format:

      (.venv) $ python3 TUFP.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 TUFP.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup can be specified  in support count or a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            from PAMI.uncertainFrequentPattern.basic import TUFP as alg


            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.TUFP(iFile, minSup)

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
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _cupList = {}
    _topk = {}
    _minimum = 9999
    oFile = None

    def __init__(self, iFile, minSup, sep='\t'):
        super().__init__(iFile, minSup, sep)


    def _creatingItemSets(self) -> None:
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

    def _frequentOneItem(self) -> List[str]:
        """
        Takes the self.Database and calculates the support of each item in the dataset and assign the ranks to the items by decreasing support and returns the frequent items list

        :param self.Database : it represents the one self.Database in database
        :type self.Database : list
        """

        mapSupport = {}
        k = 0
        for i in self._Database:
            k += 1
            for j in i:
                if j.item not in mapSupport:
                    mapSupport[j.item] = j.probability
                    self._cupList[j.item] = {k:j.probability}
                else:
                    mapSupport[j.item] += j.probability
                    self._cupList[j.item].update({k: j.probability})
        plist = [k for k,v in sorted(mapSupport.items(), key=lambda x: x[1], reverse=True)]
        k = 0
        for x, in plist:
            k +=1
            if k >= self._minSup:
                break
            self._finalPatterns[x] = mapSupport[x]
        self._minimum = min(list(self._finalPatterns.values()))
        return plist

    @staticmethod
    def _convert(value: Union[int, float, str]) -> Union[int, float]:
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

    def _save(self, prefix: List[str], suffix: List[str], tidSetI: Dict[int, float]) -> None:
        """
        Saves the patterns that satisfy the periodic frequent property.

        :param prefix: the prefix of a pattern
        :type prefix: list
        :param suffix: the suffix of a patterns
        :type suffix: list
        :param tidSetI: the timestamp of a patterns
        :type tidSetI: dict
        """

        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        val = sum(tidSetI.values())
        #print(prefix, val)
        if len(self._finalPatterns) <= self._minSup:
            sample = str()
            for i in prefix:
                sample = sample + i + " "
            self._finalPatterns[sample] = val
        if len(self._finalPatterns) == self._minSup:
            if val > self._minimum:
                sample = str()
                for i in prefix:
                    sample = sample + i + " "
                index = list(self._finalPatterns.keys())[list(self._finalPatterns.values()).index(self._minimum)]
                del self._finalPatterns[index]
                self._finalPatterns[sample] = val
                self._minimum = min(list(self._finalPatterns.values()))
        #print(self.finalPatterns, self.minimum, self.minSup)


    def _Generation(self, prefix: List[str], itemSets: List[str], tidSets: List[Dict[int, float]]) -> None:
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
        for i in range(0, len(itemSets)):
            itemI = itemSets[i]
            if itemI is None:
                continue
            tidSetI = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetX = [itemI]
            for j in range(i+1, len(itemSets)):
                itemJ = itemSets[j]
                tidSetJ = tidSets[j]
                y = {key: tidSetJ[key] * tidSetI.get(key, 0) for key in tidSetJ.keys()}
                sum2 = sum(list(y.values()))
                #print(prefix, itemJ, y, sum2)
                #if sum2 >= self.minimum:
                self._save(prefix, [itemJ], y)
                classItemSets.append(itemJ)
                classTidSets.append(y)
            #print(itemI, tidSetI, classItemSets)
            newPrefix = list(set(itemSetX)) + prefix
            self._Generation(newPrefix, classItemSets, classTidSets)
            #self.save(prefix, list(set(itemSetX)), tidSetI)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Main method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patterns
        """
        self.mine()


    def mine(self) -> None:
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
            tidSetI = self._cupList[itemI]
            itemSetX = [itemI]
            itemSets = []
            tidSets = []
            for j in range(i+1, len(plist)):
                itemJ = plist[j]
                tidSetJ = self._cupList[itemJ]
                y1 = {key: tidSetJ[key] * tidSetI.get(key, 0)  for key in tidSetJ.keys()}
                self._save(itemSetX, [itemJ], y1)
                itemSets.append(itemJ)
                tidSets.append(y1)
            self._Generation(itemSetX, itemSets, tidSets)
        print("Top-K Frequent patterns were generated from uncertain databases successfully using TUFP algorithm")
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def getMemoryUSS(self) -> float:
        """

        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self) -> float:
        """

        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self) -> float:
        """

        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self) -> pd.DataFrame:
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, outFile: str) -> None:
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, float]:
        """

        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
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
            _ap = TUFP(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = TUFP(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        _Patterns = _ap.getPatterns()
        print("Total number of Patterns:", len(_Patterns))
        _ap.save(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        '''ap = TUFP("/home/apiiit-rkv/Desktop/uncertain/tubeSample", 10, ' ')
        ap.mine()
        Patterns = ap.getPatterns()
        print("Total number of Patterns:", len(Patterns))
        ap.save("patterns.txt")
        memUSS = ap.getMemoryUSS()
        print("Total Memory in USS:", memUSS)
        memRSS = ap.getMemoryRSS()
        print("Total Memory in RSS", memRSS)
        run = ap.getRuntime()
        print("Total ExecutionTime in ms:", run)'''
        print("Error! The number of input parameters do not match the total number of parameters provided")

