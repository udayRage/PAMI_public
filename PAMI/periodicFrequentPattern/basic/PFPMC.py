# PFPMC is the fundamental approach to mine the periodic-frequent patterns.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.periodicFrequentPattern.basic import PFPMC as alg
#
#             obj = alg.PFPMC("../basic/sampleTDB.txt", "2", "5")
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))
#
#             obj.save("patterns")
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
     Copyright (C)  2021 Rage Uday Kiran

"""

from PAMI.periodicFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated
from itertools import groupby as _groupby
from operator import itemgetter as _itemgetter
from PAMI.periodicFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator


class PFPMC(_ab._periodicFrequentPatterns):
    """
    :Description:   PFPMC is the fundamental approach to mine the periodic-frequent patterns.

    :Reference: (has to be added)

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  minSup: str:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  maxPer: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        minSup : int or float or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        maxPer : int or float or str
            The user can specify maxPer either in count or proportion of database size.
            If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxPer=10 will be treated as integer, while maxPer=10.0 will be treated as float
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
            it represents the total no of transactions
        tree : class
            it represents the Tree class
        itemSetCount : int
            it represents the total no of patterns
        finalPatterns : dict
            it represents to store the patterns
        tidList : dict
            stores the timestamps of an item
        hashing : dict
            stores the patterns with their support to check for the closed property

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of periodic-frequent patterns will be loaded in to an output file
        getPatternsAsDataFrame()
            Complete set of periodic-frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        creatingOneItemSets()
            Scan the database and store the items with their timestamps which are periodic frequent
        getPeriodAndSupport()
            Calculates the support and period for a list of timestamps.
        Generation()
            Used to implement prefix class equivalence method to generate the periodic patterns recursively


    **Methods to execute code on terminal**
    ------------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 PFPMC.py <inputFile> <outputFile> <minSup> <maxPer>

       Example usage:

       (.venv) $ python3 PFPMC.py sampleDB.txt patterns.txt 10.0 4.0


               .. note:: minSup and maxPer will be considered in percentage of database transactions

    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

                from PAMI.periodicFrequentPattern.basic import PFPMC as alg

                obj = alg.PFPMC("../basic/sampleTDB.txt", "2", "5")

                obj.mine()

                periodicFrequentPatterns = obj.getPatterns()

                print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))

                obj.save("patterns")

                Df = obj.getPatternsAsDataFrame()

                memUSS = obj.getMemoryUSS()

                print("Total Memory in USS:", memUSS)

                memRSS = obj.getMemoryRSS()

                print("Total Memory in RSS", memRSS)

                run = obj.getRuntime()

                print("Total ExecutionTime in seconds:", run)

    **Credits:**
    ----------------

    The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    _iFile = " "
    _oFile = " "
    _sep = " "
    _dbSize = None
    _Database = None
    _minSup = str()
    _maxPer = str()
    _tidSet = set()
    _finalPatterns = {}
    _startTime = None
    _endTime = None
    _lastTid = int()
    _memoryUSS = float()
    _memoryRSS = float()

    # def _getPeriodic(self, tids: set) -> int:
    #     """
    #     To get  Periodic frequent patterns
    #
    #     :param tids: represents the timestamp of a transaction
    #     :type tids: set
    #     :return: None
    #     """
    #     tids = list(tids)
    #     tids.sort()
    #     temp = self._maxPer + 1
    #     diffs = []
    #     if self._lastTid in tids:
    #         tids.remove(self._lastTid)
    #     for k, g in _groupby(enumerate(tids), lambda ix: ix[0] - ix[1]):
    #         diffs.append(len(list(map(_itemgetter(1), g))))
    #     if len(diffs) < 1:
    #         return temp
    #     return max(diffs) + 1

    # def _getPeriodic(self, tids: set):
    #
    #     tids = list(tids)
    #     tids.sort()
    #     temp = self._maxPer + 1
    #     if self._lastTid in tids:
    #         tids.remove(self._lastTid)
    #     diffs = []
    #     # find the longest consecutive period
    #
    #     count = 0
    #     for i in range(len(tids) - 1):
    #         if tids[i + 1] == tids[i] + 1:
    #             count += 1
    #         else:
    #             diffs.append(count)
    #             count = 0
    #     if len(diffs) < 1:
    #         return temp
    #     return max(diffs) + 1

    def _getPeriodic(self, tids: set):
        tids = list(tids)
        tids.sort()
        temp = self._maxPer + 1
        if self._lastTid in tids:
            tids.remove(self._lastTid)
        diffs = []
        tempPer = 0
        period = 0
        for i in range(len(tids) - 1):
            if tids[i+1] - tids[i] == 1:
                tempPer += 1
            else:
                period = max(period, tempPer + 1)
                if period > self._maxPer:
                    return temp
                tempPer = 0

        return period

    def _convert(self, value) -> float:
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbSize * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbSize * value)
            else:
                value = int(value)
        return value

    def _creatingOneItemSets(self) -> list:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: list
        """
        plist = []
        Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            ts, data = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                ts = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            for i in range(len(data)):
                if data[i]:
                    tr = [str(ts[i])] + [x for x in data[i].split(self._sep)]
                    Database.append(tr)
                else:
                    Database.append([str(ts[i])])
                    
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()
        tid = 0
        itemsets = {}  # {key: item, value: list of tids}
        periodicHelper = {}  # {key: item, value: [period, last_tid]}
        for line in Database:
            tid = int(line[0])
            self._tidSet.add(tid)
            for item in line[1:]:
                if item in itemsets:
                    itemsets[item].add(tid)
                else:
                    itemsets[item] = {tid}

        maxNos = [int(x[0]) for x in Database]
        self._lno = max(maxNos)

        self._dbSize = len(Database)
        self._lastTid = max(self._tidSet)
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        del Database
        candidates = []
        for item, tids in itemsets.items():
            diff = self._tidSet.difference(tids)
            per = self._getPeriodic(diff)
            sup = len(tids)
            if sup >= self._minSup and per <= self._maxPer:
                candidates.append(item)
                self._finalPatterns[item] = [sup, per, diff]
        return candidates

    def _generateDiffsetEclat(self, candidates: list) -> None:
        new_freqList = []
        for i in range(0, len(candidates)):
            item1 = candidates[i]
            i1_list = item1.split()
            for j in range(i + 1, len(candidates)):
                item2 = candidates[j]
                i2_list = item2.split()
                if i1_list[:-1] == i2_list[:-1]:
                    union_DiffSet = self._finalPatterns[item2][2].union(self._finalPatterns[item1][2])
                    sorted(union_DiffSet)
                    union_supp = self._dbSize - len(union_DiffSet)
                    period = self._getPeriodic(union_DiffSet)
                    if union_supp >= self._minSup and period <= self._maxPer:
                        newKey = item1 + "\t" + i2_list[-1]
                        self._finalPatterns[newKey] = [union_supp, period, union_DiffSet]
                        new_freqList.append(newKey)
                else:
                    break

        if len(new_freqList) > 0:
            self._generateDiffsetEclat(new_freqList)

    def mine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """
        # print(f"Optimized {type(self).__name__}")
        self._startTime = _ab._time.time()
        self._finalPatterns = {}
        frequentSets = self._creatingOneItemSets()
        self._generateDiffsetEclat(frequentSets)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Periodic-Frequent patterns were generated successfully using PFPDiffset ECLAT algorithm ")

    def startMine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """
        self.mine()
        # # print(f"Optimized {type(self).__name__}")
        # self._startTime = _ab._time.time()
        # self._finalPatterns = {}
        # frequentSets = self._creatingOneItemSets()
        # self._generateDiffsetEclat(frequentSets)
        # self._endTime = _ab._time.time()
        # process = _ab._psutil.Process(_ab._os.getpid())
        # self._memoryRSS = float()
        # self._memoryUSS = float()
        # self._memoryUSS = process.memory_full_info().uss
        # self._memoryRSS = process.memory_info().rss
        # print("Periodic-Frequent patterns were generated successfully using PFPDiffset ECLAT algorithm ")

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

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataframe

    def save(self, outFile: str) -> None:
        """
        Complete set of periodic-frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y[0]) + ":" + str(y[1])
            #s1 = x.replace(' ', '\t') + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatterns(self) -> dict:
        """
        Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        :return: None
        """
        print("Total number of Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = PFPMC(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = PFPMC(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
