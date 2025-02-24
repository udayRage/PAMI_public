# 3pEclat is the fundamental approach to mine the partial periodic frequent patterns.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.periodicFrequentPattern.basic import PPP_ECLAT as alg
#
#             obj = alg.PPP_ECLAT(iFile, minPS, period)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of partial periodic patterns:", len(Patterns))
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
     Copyright (C)  2021 Rage Uday Kiran

"""



from PAMI.partialPeriodicPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
import pandas as pd
import numpy as np
from deprecated import deprecated

class PPP_ECLAT(_ab._partialPeriodicPatterns):
    """
    :Descripition:   3pEclat is the fundamental approach to mine the partial periodic frequent patterns.

    :Reference:   R. Uday Kirana,b,∗ , J.N. Venkateshd, Masashi Toyodaa , Masaru Kitsuregawaa,c , P. Krishna Reddy Discovering partial periodic-frequent patterns in a transactional database
                  https://www.tkl.iis.u-tokyo.ac.jp/new/uploads/publication_file/file/774/JSS_2017.pdf

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minPS: float:
                   Minimum partial periodic pattern...
    :param  period: float:
                   Minimum partial periodic...

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        self.iFile : file
            Name of the Input file or path of the input file
        self. oFile : file
            Name of the output file or path of the output file
        minPS: float or int or str
            The user can specify minPS either in count or proportion of database size.
            If the program detects the data type of minPS is integer, then it treats minPS is expressed in count.
            Otherwise, it will be treated as float.
            Example: minPS=10 will be treated as integer, while minPS=10.0 will be treated as float
        period: float or int or str
            The user can specify period either in count or proportion of database size.
            If the program detects the data type of period is integer, then it treats period is expressed in count.
            Otherwise, it will be treated as float.
            Example: period=10 will be treated as integer, while period=10.0 will be treated as float
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
        finalPatterns : dict
            it represents to store the patterns
        tidList : dict
            stores the timestamps of an item

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of frequent patterns will be loaded in to an  output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        creatingOneitemSets()
            Scan the database and store the items with their timestamps which are periodic frequent
        getPeriodAndSupport()
            Calculates the support and period for a list of timestamps.
        Generation()
            Used to implement prefix class equivalence method to generate the periodic patterns recursively

    **Executing the code on terminal:**
    ----------------------------------------
      .. code-block:: console


       Format:

       (.venv) $ python3 PPP_ECLAT.py <inputFile> <outputFile> <minPS> <period>

       Examples:

       (.venv) $ python3 PPP_ECLAT.py sampleDB.txt patterns.txt 0.3 0.4


    **Sample run of importing the code:**
    -----------------------------------------
    ...     code-block:: python

            from PAMI.periodicFrequentPattern.basic import PPP_ECLAT as alg

            obj = alg.PPP_ECLAT(iFile, minPS,period)

            obj.mine()

            Patterns = obj.getPatterns()

            print("Total number of partial periodic patterns:", len(Patterns))

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    ------------------
    The complete program was written by P.RaviKumar  under the supervision of Professor Rage Uday Kiran.\n

    """

    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _mapSupport = {}
    _itemsetCount = 0
    _writer = None
    _minPS = str()
    _period = str()
    _tidList = {}
    _lno = 0
    _Database = []
    _dbSize = None


    def _convert(self, value) -> Union[int, float]:
        """
        To convert the given user specified value
        :param value: user specified value

        :return: converted value
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

    def _getPeriodicSupport(self, timeStamps: list) -> int:
        """
        calculates the support and periodicity with list of timestamps.

        :param timeStamps : timestamps of a pattern
        :type timeStamps : list
        :return: list
        """
        timeStamps.sort()
        per = 0
        for i in range(len(timeStamps) - 1):
            j = i + 1
            if abs(timeStamps[j] - timeStamps[i]) <= self._period:
                per += 1
        return per
    
    # def _getPerSup(self, arr):
    #     arr = list(arr)
    #     arr.append(self._maxTS)
    #     arr.append(0)
    #     arr = np.sort(arr)
    #     arr = np.diff(arr)
    #
    #     locs = len(np.where(arr <= self._period)[0])
    #
    #     return locs

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, pd.DataFrame):
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
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self) -> None:
        """
        Main program start with extracting the periodic frequent items from the database and
        performs prefix equivalence to form the combinations and generates partial-periodic patterns.
        :return: None

        """
        self.mine()

    def _getPerSup(self, arr):
        arr = list(arr)
        arr = np.sort(arr)
        arr = np.diff(arr)
        locs = len(np.where(arr <= self._period)[0])

        return locs
    
    def _recursive(self, cands, items):
        for i in range(len(cands)):
            newCands = []
            nitems = {}
            for j in range(i + 1, len(cands)):
                intersection = items[cands[i]].intersection(items[cands[j]])
                perSup = self._getPerSup(intersection)
                if perSup >= self._minPS:
                    nCand = cands[i] + tuple([cands[j][-1]])
                    newCands.append(nCand)
                    nitems[nCand] = intersection
                    self._finalPatterns[nCand] = perSup
                # if len(intersection) >= self._min:
                #     perSup = self._getPerSup(intersection)
                #     ratio = perSup / (len(intersection) + 1)
                #     if ratio >= self._partialPeriodicPatterns__minPR:
                #         nCand = cands[i] + tuple([cands[j][-1]])
                #         newCands.append(nCand)
                #         nitems[nCand] = intersection
                #         self._finalPatterns[nCand] = [len(intersection), ratio]
            if len(newCands) > 1:
                self._recursive(newCands, nitems)


    def mine(self) -> None:
        """
        Main program start with extracting the periodic frequent items from the database and
        performs prefix equivalence to form the combinations and generates partial-periodic patterns.
        :return: None

        """
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._finalPatterns = {}


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

        self._period = self._convert(self._period)
        self._minPS = self._convert(self._minPS)

        cands = []
        nitems = {}

        for k, v in items.items():
            perSup = self._getPerSup(v)
            if perSup >= self._minPS:
                self._finalPatterns[k] = perSup
                cands.append(k)
                nitems[k] = v

        self._recursive(cands, nitems)

        temp = {}
        for k,v in self._finalPatterns.items():
            k = list(k)
            k = "\t".join(k)
            temp[k] = v
        self._finalPatterns = temp

        print("Partial Periodic Patterns were generated successfully using 3PEclat algorithm")
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
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
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

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
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
        dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'periodicSupport'])
        return dataframe

    def save(self, outFile: str) -> None:
        """Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, int]:
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        :return: None
        """
        print("Total number of Partial Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = PPP_ECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = PPP_ECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Partial Periodic Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        for i in [100, 200, 300, 400, 500]:
            _ap = PPP_ECLAT('/Users/tarunsreepada/Downloads/Temporal_T10I4D100K.csv', i, 5000, '\t')
            _ap.mine()
            print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
            _ap.save('/Users/tarunsreepada/Downloads/output.txt')
            print(_ap.getPatternsAsDataFrame())
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
