#  CPFPMiner algorithm is used to discover the closed periodic frequent patterns in temporal databases.
#  It uses depth-first search.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.periodicFrequentPattern.closed import CPFPMiner as alg
#
#             obj = alg.CPFPMiner("../basic/sampleTDB.txt", "2", "6")
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(periodicFrequentPatterns))
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

from PAMI.periodicFrequentPattern.closed import abstract as _ab

class CPFPMiner(_ab._periodicFrequentPatterns):
    """
    About this algorithm
    ====================

    :Description:   CPFPMiner algorithm is used to discover the closed periodic frequent patterns in temporal databases.
                    It uses depth-first search.

    :Reference:   P. Likhitha et al., "Discovering Closed Periodic-Frequent Patterns in Very Large Temporal Databases"
                  2020 IEEE International Conference on Big Data (Big Data), 2020, https://ieeexplore.ieee.org/document/9378215

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  minSup: float:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  maxPer: float:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : str
            Input file name or path of the input file
        oFile : str
            Name of the output file or path of the input file
        minSup: int or float or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        maxPer: int or float or str
            The user can specify maxPer either in count or proportion of database size.
            If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxPer=10 will be treated as integer, while maxPer=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        finalPatterns: dict
            Storing the complete set of patterns in a dictionary variable
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of frequent patterns will be loaded in to an output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function


    Execution methods
    =================


    **Terminal command**


    .. code-block:: console

       Format:

       (.venv) $  python3 CPFPMiner.py <inputFile> <outputFile> <minSup> <maxPer>

       Example:

       (.venv) $ python3 CPFPMiner.py sampleTDB.txt patterns.txt 0.3 0.4

     .. note:: minSup will be considered in percentage of database transactions
        
        
    **Calling from a python program**

    .. code-block:: python

                    from PAMI.periodicFrequentPattern.closed import CPFPMiner as alg
        
                    obj = alg.CPFPMiner("../basic/sampleTDB.txt", "2", "6")
        
                    obj.mine()
        
                    periodicFrequentPatterns = obj.getPatterns()
        
                    print("Total number of Frequent Patterns:", len(periodicFrequentPatterns))
        
                    obj.save("patterns")
        
                    Df = obj.getPatternsAsDataFrame()
        
                    memUSS = obj.getMemoryUSS()
        
                    print("Total Memory in USS:", memUSS)
        
                    memRSS = obj.getMemoryRSS()
        
                    print("Total Memory in RSS", memRSS)
        
                    run = obj.getRuntime()
        
                    print("Total ExecutionTime in seconds:", run)
        
    **Credits:**
    ------------------
    The complete program was written by  P.Likhitha under the supervision of Professor Rage Uday Kiran.
    """

    _minSup = float()
    _maxPer = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _transaction = []
    _hashing = {}
    _mapSupport = {}
    _itemSetCount = 0
    _maxItemId = 0
    _tableSize = 10000
    _tidList = {}
    _lno = 0

    def __init__(self, iFile, minSup, maxPer, sep='\t'):
        super().__init__(iFile, minSup, maxPer, sep)
        self._finalPatterns = {}
    
    def _convert(self, value):
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._lno * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._lno * value)
            else:
                value = int(value)
        return value

    def _scanDatabase(self):
        """
        To scan the database and extracts the 1-length periodic-frequent items

        :return:   Returns the 1-length periodic-frequent items
        """
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
                tr = [ts[i][0]]
                tr = tr + data[i]
                Database.append(tr)

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
        self._tidList = {}
        self._mapSupport = {}
        for line in Database:
            self._lno += 1
            s = line
            n = int(s[0])
            for i in range(1, len(s)):
                si = s[i]
                if self._mapSupport.get(si) is None:
                    self._mapSupport[si] = [1, abs(0 - n), n]
                    self._tidList[si] = [n]
                else:
                    self._mapSupport[si][0] += 1
                    self._mapSupport[si][1] = max(self._mapSupport[si][1], abs(n - self._mapSupport[si][2]))
                    self._mapSupport[si][2] = n
                    self._tidList[si].append(n)
        for x, y in self._mapSupport.items():
            self._mapSupport[x][1] = max(self._mapSupport[x][1], abs(self._lno - self._mapSupport[x][2]))
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        self._mapSupport = {k: [v[0], v[1]] for k, v in self._mapSupport.items() if
                           v[0] >= self._minSup and v[1] <= self._maxPer}
        periodicFrequentItems = {}
        self._tidList = {k: v for k, v in self._tidList.items() if k in self._mapSupport}
        for x, y in self._tidList.items():
            t1 = 0
            for i in y:
                t1 += i
            periodicFrequentItems[x] = t1
        periodicFrequentItems = [key for key, value in sorted(periodicFrequentItems.items(), key=lambda x: x[1])]
        return periodicFrequentItems

    def _calculate(self, tidSet):
        """
        To calculate the weight if pattern based on the respective timeStamps

        :param tidSet: timeStamps of the pattern
        :return: the calculated weight of the timeStamps
        """
        hashcode = 0
        for i in tidSet:
            hashcode += i
        if hashcode < 0:
            hashcode = abs(0 - hashcode)
        return hashcode % self._tableSize

    def _contains(self, itemSet, val, hashcode):
        """
        To check if the key(hashcode) is in dictionary(hashing) variable

        :param itemSet: generated periodic-frequent itemSet
        :param val: support and periodicity of itemSet
        :param hashcode: the key generated in calculate() method for every itemSet

        :return: true if itemSet with same support present in dictionary(hashing) or else returns false
        """
        if self._hashing.get(hashcode) is None:
            return False
        for i in self._hashing[hashcode]:
            itemSetX = i
            if val[0] == self._hashing[hashcode][itemSetX][0] and set(itemSetX).issuperset(itemSet):
                return True
        return False

    def _getPeriodAndSupport(self, timeStamps):
        """
        Calculates the periodicity and support of timeStamps

        :param timeStamps: timeStamps of itemSet
        :return: periodicity and support
        """
        timeStamps.sort()
        cur = 0
        per = 0
        sup = 0
        for j in range(len(timeStamps)):
            per = max(per, timeStamps[j] - cur)
            if per > self._maxPer:
                return [0, 0]
            cur = timeStamps[j]
            sup += 1
        per = max(per, self._lno - cur)
        return [sup, per]

    def _save(self, prefix, suffix, tidSetX):
        """
        Saves the generated pattern which satisfies the closed property
        Parameters:
        -----------
            prefix: the prefix part of itemSet
            suffix: the suffix part of itemSet
            tidSetX: the timeStamps of the generated itemSet

        Returns:
        --------
            saves the closed periodic-frequent pattern

        """
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        prefix = list(set(prefix))
        prefix.sort()
        val = self._getPeriodAndSupport(tidSetX)
        if val[0] >= self._minSup and val[1] <= self._maxPer:
            hashcode = self._calculate(tidSetX)
            if self._contains(prefix, val, hashcode) is False:
                self._itemSetCount += 1
                sample = str()
                for i in prefix:
                    sample = sample + i + " "
                self._finalPatterns[sample] = val
            if hashcode not in self._hashing:
                self._hashing[hashcode] = {tuple(prefix): val}
            else:
                self._hashing[hashcode][tuple(prefix)] = val

    def _processEquivalenceClass(self, prefix, itemSets, tidSets):
        """
        identifies and saves closed periodic patterns of length more than 2 in a dataset, by processing equivalence classes of item sets that satisfy a minimum support condition.
        :param prefix: Prefix class of an itemSet
        :param itemSets: suffix items in periodicFrequentItems that satisfies the minSup condition
        :param tidSets: timeStamps of items in itemSets respectively
        :return:  closed periodic patterns with length more than 2
        """
        if len(itemSets) == 1:
            i = itemSets[0]
            tidList = tidSets[0]
            self._save(prefix, [i], tidList)
            return
        if len(itemSets) == 2:
            itemI = itemSets[0]
            tidSetI = tidSets[0]
            itemJ = itemSets[1]
            tidSetJ = tidSets[1]
            y1 = list(set(tidSetI).intersection(tidSetJ))
            if len(y1) >= self._minSup:
                suffix = []
                suffix += [itemI, itemJ]
                suffix = list(set(suffix))
                self._save(prefix, suffix, y1)
            if len(y1) != len(tidSetI):
                self._save(prefix, [itemI], tidSetI)
            if len(y1) != len(tidSetJ):
                self._save(prefix, [itemJ], tidSetJ)
            return
        for i in range(len(itemSets)):
            itemX = itemSets[i]
            if itemX is None:
                continue
            tidSetX = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetX = [itemX]
            for j in range(i + 1, len(itemSets)):
                itemJ = itemSets[j]
                if itemJ is None:
                    continue
                tidSetJ = tidSets[j]
                y = list(set(tidSetX).intersection(tidSetJ))
                if len(y) < self._minSup:
                    continue
                if len(tidSetX) == len(tidSetJ) and len(y) == len(tidSetX):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    itemSetX.append(itemJ)
                elif len(tidSetJ) > len(tidSetX) == len(y):
                    itemSetX.append(itemJ)
                elif len(tidSetX) > len(tidSetJ) and len(y) == len(tidSetJ):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    classItemSets.append(itemJ)
                    classTidSets.append(y)
                else:
                    classItemSets.append(itemJ)
                    classTidSets.append(y)
            if len(classItemSets) > 0:
                newPrefix = list(set(itemSetX)) + prefix
                self._processEquivalenceClass(newPrefix, classItemSets, classTidSets)
            self._save(prefix, list(set(itemSetX)), tidSetX)

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Mining process will start from here
        """
        self._startTime = _ab._time.time()
        self._finalPatterns = {}
        self._hashing = {}
        periodicFrequentItems = self._scanDatabase()
        for i in range(len(periodicFrequentItems)):
            itemX = periodicFrequentItems[i]
            if itemX is None:
                continue
            tidSetX = self._tidList[itemX]
            itemSetX = [itemX]
            itemSets = []
            tidSets = []
            for j in range(i + 1, len(periodicFrequentItems)):
                itemJ = periodicFrequentItems[j]
                if itemJ is None:
                    continue
                tidSetJ = self._tidList[itemJ]
                y1 = list(set(tidSetX).intersection(tidSetJ))
                if len(y1) < self._minSup:
                    continue
                if len(tidSetX) == len(tidSetJ) and len(y1) is len(tidSetX):
                    periodicFrequentItems.insert(j, None)
                    itemSetX.append(itemJ)
                elif len(tidSetX) < len(tidSetJ) and len(y1) is len(tidSetX):
                    itemSetX.append(itemJ)
                elif len(tidSetX) > len(tidSetJ) and len(y1) is len(tidSetJ):
                    periodicFrequentItems.insert(j, None)
                    itemSets.append(itemJ)
                    tidSets.append(y1)
                else:

                    itemSets.append(itemJ)
                    tidSets.append(y1)
            if len(itemSets) > 0:
                self._processEquivalenceClass(itemSetX, itemSets, tidSets)
            self._save([], itemSetX, tidSetX)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Closed periodic frequent patterns were generated successfully using CPFPMiner algorithm ")

    def mine(self):
        """
        Mining process will start from here
        """
        self._startTime = _ab._time.time()
        self._finalPatterns = {}
        self._hashing = {}
        periodicFrequentItems = self._scanDatabase()
        for i in range(len(periodicFrequentItems)):
            itemX = periodicFrequentItems[i]
            if itemX is None:
                continue
            tidSetX = self._tidList[itemX]
            itemSetX = [itemX]
            itemSets = []
            tidSets = []
            for j in range(i + 1, len(periodicFrequentItems)):
                itemJ = periodicFrequentItems[j]
                if itemJ is None:
                    continue
                tidSetJ = self._tidList[itemJ]
                y1 = list(set(tidSetX).intersection(tidSetJ))
                if len(y1) < self._minSup:
                    continue
                if len(tidSetX) == len(tidSetJ) and len(y1) is len(tidSetX):
                    periodicFrequentItems.insert(j, None)
                    itemSetX.append(itemJ)
                elif len(tidSetX) < len(tidSetJ) and len(y1) is len(tidSetX):
                    itemSetX.append(itemJ)
                elif len(tidSetX) > len(tidSetJ) and len(y1) is len(tidSetJ):
                    periodicFrequentItems.insert(j, None)
                    itemSets.append(itemJ)
                    tidSets.append(y1)
                else:

                    itemSets.append(itemJ)
                    tidSets.append(y1)
            if len(itemSets) > 0:
                self._processEquivalenceClass(itemSetX, itemSets, tidSets)
            self._save([], itemSetX, tidSetX)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Closed periodic frequent patterns were generated successfully using CPFPMiner algorithm ")

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.replace(' ', '\t').strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Closed Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())
        

if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = CPFPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = CPFPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Closed Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
