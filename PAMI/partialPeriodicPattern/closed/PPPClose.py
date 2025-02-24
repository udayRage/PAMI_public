

# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.partialPeriodicPattern.closed import PPPClose as alg
#
#             obj = alg.PPPClose("../basic/sampleTDB.txt", "2", "6")
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
#
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



import sys as _sys
import validators as _validators
from urllib.request import urlopen as _urlopen
from PAMI.partialPeriodicPattern.closed import abstract as _abstract
import pandas as pd
from deprecated import deprecated

class PPPClose(_abstract._partialPeriodicPatterns):
    """
    :Description:

    PPPClose algorithm is used to discover the closed partial periodic patterns in temporal databases.
    It uses depth-first search.

    :Reference: R. Uday Kiran1 , J. N. Venkatesh2 , Philippe Fournier-Viger3 , Masashi Toyoda1 , P. Krishna Reddy2 and Masaru Kitsuregawa
                 https://www.tkl.iis.u-tokyo.ac.jp/new/uploads/publication_file/file/799/PAKDD.pdf

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  period: float:
                   Minimum partial periodic...
    :param  periodicSupport: float:
                   Minimum partial periodic...

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : str
            Input file name or path of the input file
        oFile : str
            Name of the output file or path of the input file
        periodicSupport: int or float or str
            The user can specify periodicSupport either in count or proportion of database size.
            If the program detects the data type of periodicSupport is integer, then it treats periodicSupport is expressed in count.
            Otherwise, it will be treated as float.
            Example: periodicSupport=10 will be treated as integer, while periodicSupport=10.0 will be treated as float
        period: int or float or str
            The user can specify period either in count or proportion of database size.
            If the program detects the data type of period is integer, then it treats period is expressed in count.
            Otherwise, it will be treated as float.
            Example: period=10 will be treated as integer, while period=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default separator is tab space or \t.
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
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function

    **Executing the code on terminal:**
    -------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 PPPClose.py <inputFile> <outputFile> <periodicSupport> <period>

       Examples:

       (.venv) $ python3 PPPClose.py sampleTDB.txt patterns.txt 0.3 0.4


    **Sample run of the imported code:**
    --------------------------------------
    .. code-block:: python

            from PAMI.partialPeriodicPattern.closed import PPPClose as alg

            obj = alg.PPPClose("../basic/sampleTDB.txt", "2", "6")

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
    --------------
        The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.\n

    """

    _periodicSupport = float()
    _period = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _Database = []
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

    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        if isinstance(self._iFile, _abstract._pd.DataFrame):
            timeStamp, data = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                timeStamp = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            for i in range(len(data)):
                tr = [timeStamp[i]]
                tr = tr + data[i]
                self._Database.append(tr)
            self._lno = len(self._Database)
        if isinstance(self._iFile, str):
            if _validators.url(self._iFile):
                data = _urlopen(self._iFile)
                for line in data:
                    self._lno += 1
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            self._lno += 1
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def _OneLengthPartialItems(self):
        """
        To scan the database and extracts the 1-length periodic-frequent items

        :return: Returns the 1-length periodic-frequent items
        """
        self._mapSupport = {}
        self._tidList = {}
        self._period = self._convert(self._period)
        for line in self._Database:
            n = int(line[0])
            for i in range(1, len(line)):
                si = line[i]
                if self._mapSupport.get(si) is None:
                    self._mapSupport[si] = [1, 0, n]
                    self._tidList[si] = [n]
                else:
                    self._mapSupport[si][0] += 1
                    period = abs(n - self._mapSupport[si][2])
                    if period <= self._period:
                        self._mapSupport[si][1] += 1
                    self._mapSupport[si][2] = n
                    self._tidList[si].append(n)
        for x, y in self._mapSupport.items():
            period = abs(self._lno - self._mapSupport[x][2])
            if period <= self._period:
                self._mapSupport[x][1] += 1
        self._periodicSupport = self._convert(self._periodicSupport)
        self._mapSupport = {k: v[1] for k, v in self._mapSupport.items() if v[1] >= self._periodicSupport}
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
        :param val: support and period of itemSet
        :param hashcode: the key generated in calculate() method for every itemSet

        :return: true if itemSet with same support present in dictionary(hashing) or else returns false
        """
        if self._hashing.get(hashcode) is None:
            return False
        for i in self._hashing[hashcode]:
            itemSetX = i
            if val == self._hashing[hashcode][itemSetX] and set(itemSetX).issuperset(itemSet):
                return True
        return False

    def _getPeriodicSupport(self, timeStamps):
        """
        Calculates the period and support of timeStamps

        :param: timeStamps: timeStamps of itemSet
        :return: period and support
        """
        timeStamps.sort()
        sup = 0
        for j in range(len(timeStamps) - 1):
            per = abs(timeStamps[j + 1] - timeStamps[j])
            if per <= self._period:
                sup += 1
        return sup

    def _save(self, prefix, suffix, tidSetX):
        """
        Saves the generated pattern which satisfies the closed property

        :param prefix: the prefix part of itemSet
        :param suffix: the suffix part of itemSet
        :param tidSetX: the timeStamps of the generated itemSet
        :return: saves the closed periodic-frequent pattern
        """
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        prefix = list(set(prefix))
        prefix.sort()
        val = self._getPeriodicSupport(tidSetX)
        if val >= self._periodicSupport:
            hashcode = self._calculate(tidSetX)
            if self._contains(prefix, val, hashcode) is False:
                self._itemSetCount += 1
                sample = str()
                for i in prefix:
                    sample = sample + i + "\t"
                self._finalPatterns[sample] = val
            if hashcode not in self._hashing:
                self._hashing[hashcode] = {tuple(prefix): val}
            else:
                self._hashing[hashcode][tuple(prefix)] = val

    def _processEquivalenceClass(self, prefix, itemSets, tidSets):
        """

        :param prefix: Prefix class of an itemSet
        :param itemSets: suffix items in periodicFrequentItems that satisfies the periodicSupport condition
        :param tidSets: timeStamps of items in itemSets respectively
        :return: closed periodic patterns with length more than 2
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
            if len(y1) >= self._periodicSupport:
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
                if len(y) < self._periodicSupport:
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
        self.mine()

    def mine(self):
        """
        Mining process will start from here
        """
        self._startTime = _abstract._time.time()
        self._creatingItemSets()
        self._hashing = {}
        self._finalPatterns = {}
        periodicFrequentItems = self._OneLengthPartialItems()
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
                if len(y1) < self._periodicSupport:
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
        self._endTime = _abstract._time.time()
        process = _abstract._psutil.Process(_abstract._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Closed periodic frequent patterns were generated successfully using PPPClose algorithm ")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

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
            data.append([a.replace('\t', ' '), b])
            dataFrame = _abstract._pd.DataFrame(data, columns=['Patterns', 'periodicSupport'])
        return dataFrame

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        print("Total number of  Closed Partial Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_sys.argv) == 5 or len(_sys.argv) == 6:
        if len(_sys.argv) == 6:
            _ap = PPPClose(_sys.argv[1], _sys.argv[3], _sys.argv[4], _sys.argv[5])
        if len(_sys.argv) == 5:
            _ap = PPPClose(_sys.argv[1], _sys.argv[3], _sys.argv[4])
        _ap.mine()
        print("Total number of  Patterns:", len(_ap.getPatterns()))
        _ap.save(_sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

