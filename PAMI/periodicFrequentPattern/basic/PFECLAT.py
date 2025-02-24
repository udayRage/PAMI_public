# PFECLAT is the fundamental approach to mine the periodic-frequent patterns.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.periodicFrequentPattern.basic import PFECLAT as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             maxPer = 20 # can also be specified between 0 and 1
#
#             obj = alg.PFECLAT(iFile, minSup, maxPer)
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))
#
#             obj.save("periodicFrequentPatterns")
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

import pandas as pd
from deprecated import deprecated
import numpy as np

from PAMI.periodicFrequentPattern.basic import abstract as _ab


class PFECLAT(_ab._periodicFrequentPatterns):
    """
    **About this algorithm**

    :**Description**:   PFECLAT is the fundamental approach to mine the periodic-frequent patterns.

    :**Reference**:   P. Ravikumar, P.Likhitha, R. Uday kiran, Y. Watanobe, and Koji Zettsu, "Towards efficient discovery of
                      periodic-frequent patterns in columnar temporal databases", 2021 IEA/AIE.

    :**Parameters**:    - **iFile** (*str or URL or dataFrame*) -- *Name of the Input file to mine complete set of frequent patterns.*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of frequent patterns.*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.*
                        - **maxPer** (*int or float or str*) -- *The user can specify maxPer either in count or proportion of database size. It controls the maximum number of transactions in which any two items within a pattern can reappear.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **finalPatterns** (*dict*) -- *Storing the complete set of patterns in a dictionary variable.*
                        - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **Database** (*list*) -- *To store the transactions of a database in list.*
                        - **mapSupport** (*Dictionary*) -- *To maintain the information of item and their frequency.*
                        - **lno** (*int*) -- *It represents the total no of transactions*
                        - **tree** (*class*) -- *it represents the Tree class.*
                        - **itemSetCount** (*int*) -- *it represents the total no of patterns.*
                        - **tidList** (*dict*) -- *stores the timestamps of an item.*
                        - **hashing** (*dict*) -- *stores the patterns with their support to check for the closed property.*

    :**Methods**:       - **mine()** -- *Mining process will start from here.*
                        - **getPatterns()** -- *Complete set of patterns will be retrieved with this function.*
                        - **save(oFile)** -- *Complete set of periodic-frequent patterns will be loaded in to a output file.*
                        - **getPatternsAsDataFrame()** -- *Complete set of periodic-frequent patterns will be loaded in to a dataframe.*
                        - **getMemoryUSS()** -- *Total amount of USS memory consumed by the mining process will be retrieved from this function.*
                        - **getMemoryRSS()** -- *Total amount of RSS memory consumed by the mining process will be retrieved from this function.*
                        - **getRuntime()** -- *Total amount of runtime taken by the mining process will be retrieved from this function.*
                        - **creatingOneItemSets()** -- *Scan the database and store the items with their timestamps which are periodic frequent.*
                        - **getPeriodAndSupport()** -- *Calculates the support and period for a list of timestamps.*
                        - **Generation()** -- *Used to implement prefix class equivalence method to generate the periodic patterns recursively*

    **Execution methods**

    **Terminal command**

    .. code-block:: console

       Format:

       (.venv) $ python3 PFECLAT.py <inputFile> <outputFile> <minSup> <maxPer>

       Example usage:

       (.venv) $ python3 PFECLAT.py sampleDB.txt patterns.txt 10.0 20.0

    .. note:: minSup will be considered in percentage of database transactions


    **Calling from a python program**

    .. code-block:: python

            from PAMI.periodicFrequentPattern.basic import PFECLAT as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            maxPer = 20 # can also be specified between 0 and 1

            obj = alg.PFECLAT(iFile, minSup, maxPer)

            obj.mine()

            periodicFrequentPatterns = obj.getPatterns()

            print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))

            obj.save("periodicFrequentPatterns")

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**

    The complete program was written by P. Likhitha  and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

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
    _memoryUSS = float()
    _memoryRSS = float()

    def _convert(self, value) -> float:
        """
        To convert the given user specified value

        :param value: user specified value
        :type value: int or float or str
        :return: converted value
        :rtype: int or float
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

    def _creatingItemSets(self) -> None:
        """

        Storing the complete transactions of the database/input file in a database variable

        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            data, ts = [], []
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
                    self._Database.append(tr)
                else:
                    self._Database.append([str(ts[i])])

        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        self.mine()

    def _getMaxPer(self, arr, maxTS):
        arr = np.append(list(arr), [0, maxTS])
        arr = np.sort(arr)
        arr = np.diff(arr)

        return np.max(arr)

    def mine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """
        self._startTime = _ab._time.time()
        self._finalPatterns = {}
        #frequentSets = self._creatingItemSets()

        items = {}
        maxTS = 0
        for line in self._Database:
            index = int(line[0])
            maxTS = max(maxTS, index)
            for item in line[1:]:
                if tuple([item]) not in items:
                    items[tuple([item])] = set()
                items[tuple([item])].add(index)

        self._dbSize = maxTS

        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        minSup = self._minSup
        maxPer = self._maxPer


        items = {k: v for k, v in items.items() if len(v) >= minSup}
        items = {k: v for k, v in sorted(items.items(), key = lambda x: len(x[1]), reverse = True)}

        keys = []
        for item in list(items.keys()):
            per = self._getMaxPer(items[item], maxTS)
            if per <= maxPer:
                keys.append(item)
                self._finalPatterns[item] = [len(items[item]), per, set(items[item])]

        while keys:
            newKeys = []
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    if keys[i][:-1] == keys[j][:-1] and keys[i][-1] != keys[j][-1]:
                        # print(keys[i], keys[j])
                        newKey = tuple(keys[i] + (keys[j][-1],))
                        intersect = items[keys[i]].intersection(items[keys[j]])
                        per = self._getMaxPer(intersect, maxTS)
                        sup = len(intersect)
                        if sup >= minSup and per <= maxPer:
                            items[newKey] = intersect
                            newKeys.append(newKey)
                            self._finalPatterns[newKey] = [sup, per, set(intersect)]
                    else:
                        break
            keys = newKeys

        newPattern = {}
        for k, v in self._finalPatterns.items():
            newPattern["\t".join([str(x) for x in k])] = v

        self._finalPatterns = newPattern

        # self._generateEclat(frequentSets)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Periodic-Frequent patterns were generated successfully using PFECLAT algorithm ")

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
        Complete set of periodic-frequent patterns will be loaded in to a output file

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
            _ap = PFECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = PFECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        print("Total number of Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

    