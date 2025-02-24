# PPF_DFS is algorithm to mine the partial periodic frequent patterns.
#
# **Importing this algorithm into a python program**
#
#           from PAMI.partialPeriodicFrequentPattern.basic import PPF_DFS as alg
#
#           iFile = 'sampleTDB.txt'
#
#           minSup = 0.25 # can be specified between 0 and 1
#
#           maxPer = 300 # can  be specified between 0 and 1
#
#           minPR = 0.7 # can  be specified between 0 and 1
#
#           obj = alg.PPF_DFS(iFile, minSup, maxPer, minPR, sep)
#
#           obj.mine()
#
#           frequentPatterns = obj.getPatterns()
#
#           print("Total number of Frequent Patterns:", len(frequentPatterns))
#
#           obj.save(oFile)
#
#           Df = obj.getPatternInDataFrame()
#
#           memUSS = obj.getMemoryUSS()
#
#           print("Total Memory in USS:", memUSS)
#
#           memRSS = obj.getMemoryRSS()
#
#           print("Total Memory in RSS", memRSS)
#
#           run = obj.getRuntime()
#
#           print("Total ExecutionTime in seconds:", run)
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

from abc import ABC

from PAMI.partialPeriodicFrequentPattern.basic.abstract import *
import deprecated
import numpy as np
import pandas as pd


class PPF_DFS(partialPeriodicPatterns, ABC):
    """
    **About this algorithm**

    :**Description**:   PPF_DFS is algorithm to mine the partial periodic frequent patterns.

    :**References**:    (Has to be added)

    :**parameters**:    - **iFile** (*str*) -- *Name of the Input file to mine complete set of correlated patterns.*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of correlated patterns.*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.*
                        - **minPR** (*str*) -- *Controls the maximum number of transactions in which any two items within a pattern can reappear.*
                        - **maxPer** (*str*) -- *Controls the maximum number of transactions in which any two items within a pattern can reappear.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **minSup** (*int*) -- *The user given minSup.*
                        - **maxPer** (*int*) -- *The user given maxPer.*
                        - **minPR** (*int*) -- *The user given minPR.*
                        - **finalPatterns** (*dict*) -- *It represents to store the pattern.*

    :**Methods**:       - **mine()** -- *Mining process will start from here.*
                        - **Generation(prefix, itemsets, tidsets)** -- *Used to implement prefix class equibalence method to generate the periodic patterns recursively.*
                        - **getPartialPeriodicPatterns()** -- *Complete set of patterns will be retrieved with this function.*
                        - **storePatternsInFile(ouputFile)** -- *Complete set of frequent patterns will be loaded in to an output file.*
                        - **getPatternsAsDataFrame()** -- *Complete set of frequent patterns will be loaded in to an output file.*
                        - **getMemoryUSS()** -- *Total amount of USS memory consumed by the mining process will be retrieved from this function.*
                        - **getMemoryRSS()** -- *Total amount of RSS memory consumed by the mining process will be retrieved from this function.*
                        - **getRuntime()** -- *Total amount of runtime taken by the mining process will be retrieved from this function.*


    **Execution methods**

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 PPF_DFS.py <inputFile> <outputFile> <minSup> <maxPer> <minPR>

      Example Usage:

      (.venv) $ python3 PPF_DFS.py sampleTDB.txt output.txt 0.25 300 0.7

    .. note:: minSup can be specified in support count or a value between 0 and 1.

    **Calling from a python program**

    .. code-block:: python

            from PAMI.partialPeriodicFrequentPattern.basic import PPF_DFS as alg

            iFile = 'sampleTDB.txt'

            minSup = 0.25 # can be specified between 0 and 1

            maxPer = 300 # can  be specified between 0 and 1

            minPR = 0.7 # can  be specified between 0 and 1

            obj = alg.PPF_DFS(inputFile, minSup, maxPer, minPR, sep)

            obj.mine()

            partialPeriodicFrequentPatterns = obj.getPatterns()

            print("Total number of partial periodic Patterns:", len(partialPeriodicFrequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDf()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits**

    The complete program was written by Nakamura and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """

    __path = ' '
    _partialPeriodicPatterns__iFile = ' '
    _partialPeriodicPatterns__oFile = ' '
    _partialPeriodicPatterns__sep = str()
    _partialPeriodicPatterns__minSup = str()
    _partialPeriodicPatterns__maxPer = str()
    _partialPeriodicPatterns__minPR = str()
    __tidlist = {}
    __last = 0
    __lno = 0
    __mapSupport = {}
    _partialPeriodicPatterns__finalPatterns = {}
    __runTime = float()
    _partialPeriodicPatterns__memoryUSS = float()
    _partialPeriodicPatterns__memoryRSS = float()
    _partialPeriodicPatterns__startTime = float()
    _partialPeriodicPatterns__endTime = float()
    __Database = []
    _maxTS = None
    _dbSize = None
    oFile = None


    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable

        :return: None
        """
        self._Database = []
        if isinstance(self._partialPeriodicPatterns__iFile, pd.DataFrame):
            data, ts = [], []
            if self._partialPeriodicPatterns__iFile.empty:
                print("its empty..")
            i = self._partialPeriodicPatterns__iFile.columns.values.tolist()
            if 'TS' in i:
                ts = self._partialPeriodicPatterns__iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._partialPeriodicPatterns__iFile['Transactions'].tolist()
            for i in range(len(data)):
                if data[i]:
                    tr = [str(ts[i])] + [x for x in data[i].split(self._partialPeriodicPatterns__sep)]
                    self._Database.append(tr)
                else:
                    self._Database.append([str(ts[i])])

        if isinstance(self._partialPeriodicPatterns__iFile, str):
            if validators.url(self._partialPeriodicPatterns__iFile):
                data = urlopen(self._partialPeriodicPatterns__iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._partialPeriodicPatterns__iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()
                    

    def _partialPeriodicPatterns__getPerSup(self, tids):
        """
        calculate ip of a pattern

        :param tids: tid list of the pattern
        :type tids: list
        :return: ip
        """
        # print(lno)
        tids = list(set(tids))
        tids.sort()
        per = 0
        sup = 0
        cur = 0
        if len(tids) == 0:
            return 0
        if abs(0 - tids[0]) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        for j in range(len(tids) - 1):
            i = j + 1
            per = abs(tids[i] - tids[j])
            if per <= self._partialPeriodicPatterns__maxPer:
                sup += 1
        if abs(tids[len(tids) - 1] - self.__last) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        if sup == 0:
            return 0
        return sup


    def __convert(self, value):
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type
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


    def startMine(self):
        self.mine()

    def _getPerSup(self, arr):
        """
        This function takes the arr as input and returns locs as output

        :param arr: an array contains the items.
        :type arr: array
        :return: locs
        """
        arr = list(arr)
        arr.append(self._maxTS)
        arr.append(0)
        arr = list(set(arr))
        arr = np.sort(arr)
        arr = np.diff(arr)

        locs = len(np.where(arr <= self._partialPeriodicPatterns__maxPer)[0])

        return locs
    
    def __recursive(self, cands, items):
        """
        This method processes candidate patterns, generates new candidates by intersecting
        itemsets, and filters them based on minimum support and periodic support ratio.
        If new candidates are found, the method recursively calls itself.

        :param cands: List of current candidate patterns.
        :type cands: List of tuple
        :param items: Dictionary where keys are candidate patterns and values are sets of transaction indices in which the pattern occurs.
        :type items: dict
        :return: None
        """

        for i in range(len(cands)):
            newCands = []
            nitems = {}
            for j in range(i + 1, len(cands)):
                intersection = items[cands[i]].intersection(items[cands[j]])
                if len(intersection) >= self._partialPeriodicPatterns__minSup:
                    perSup = self._getPerSup(intersection)
                    ratio = perSup / (len(intersection) + 1)
                    nCand = cands[i] + tuple([cands[j][-1]])
                    newCands.append(nCand)
                    nitems[nCand] = intersection
                    if ratio >= self._partialPeriodicPatterns__minPR:
                        self._partialPeriodicPatterns__finalPatterns[nCand] = [len(intersection), ratio]
            if len(newCands):
                self.__recursive(newCands, nitems)


    def mine(self):
        """
        Main program start with extracting the periodic frequent items from the database and
        performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.
        """
        self._partialPeriodicPatterns__startTime = time.time()
        self._creatingItemSets()
        self._partialPeriodicPatterns__finalPatterns = {}
        
        items = {}
        tids = set()
        maxTS = 0
        for line in self._Database:
            index = int(line[0])
            tids.add(index)
            maxTS = max(maxTS, index)
            for item in line[1:]:
                if tuple([item]) not in items:
                    items[tuple([item])] = set()
                items[tuple([item])].add(index)

        self._maxTS = maxTS

        self._dbSize = maxTS

        self._partialPeriodicPatterns__minSup = self.__convert(self._partialPeriodicPatterns__minSup)
        self._partialPeriodicPatterns__maxPer = self.__convert(self._partialPeriodicPatterns__maxPer)
        self._partialPeriodicPatterns__minPR = float(self._partialPeriodicPatterns__minPR)

        cands = []
        nitems = {}

        for k, v in items.items():
            if len(v) >= self._partialPeriodicPatterns__minSup:
                perSup = self._getPerSup(v)
                cands.append(k)
                nitems[k] = v
                ratio = perSup / (len(v) + 1)
                if ratio >= self._partialPeriodicPatterns__minPR:
                    self._partialPeriodicPatterns__finalPatterns[k] = [len(v), ratio]

        self.__recursive(cands, nitems)

        temp = {}
        for k,v in self._partialPeriodicPatterns__finalPatterns.items():
            k = list(k)
            k = "\t".join(k)
            temp[k] = v
        self._partialPeriodicPatterns__finalPatterns = temp

        self._partialPeriodicPatterns__endTime = time.time()
        self.__runTime = self._partialPeriodicPatterns__endTime - self._partialPeriodicPatterns__startTime
        process = psutil.Process(os.getpid())
        self._partialPeriodicPatterns__memoryUSS = float()
        self._partialPeriodicPatterns__memoryRSS = float()
        self._partialPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._partialPeriodicPatterns__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__runTime

    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        # print("Storing the patterns in a dataframe")
        dataFrame = {}
        data = []
        for a, b in self._partialPeriodicPatterns__finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodic Ratio'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        with open(self.oFile, 'w') as f:
            for x, y in self._partialPeriodicPatterns__finalPatterns.items():
                # print(list(x), y)
                f.write(x + ":" + str(y[0]) + ":" + str(y[1]) + "\n")

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._partialPeriodicPatterns__finalPatterns


    def printResults(self):
        """
        this function is used to print the results
        """
        print("Total number of Partial Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in s:", self.getRuntime())

if __name__ == '__main__':
    ap = str()
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        if len(sys.argv) == 7:
            ap = PPF_DFS(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        if len(sys.argv) == 6:
            ap = PPF_DFS(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
        ap.mine()
        print("Total number of Frequent Patterns:", len(ap.getPatterns()))
        ap.save(sys.argv[2])
        print("Total Memory in USS:", ap.getMemoryUSS())
        print("Total Memory in RSS", ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

