# CMine algorithms aims to discover the coverage patterns in transactional databases.
#
# **Importing this algorithm into a python program**
# ----------------------------------------------------
#
#
#             from PAMI.coveragePattern.basic import CMine as alg
#
#             obj = alg.CMine(iFile, minRF, minCS, maxOR, seperator)
#
#             obj.mine()
#
#             coveragePattern = obj.getPatterns()
#
#             print("Total number of coverage Patterns:", len(coveragePattern))
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




from PAMI.coveragePattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecation import deprecated


class CMine(_ab._coveragePatterns):
    """
    About this algorithm
    ====================

    :Description:  CMine algorithms aims to discover the coverage patterns in transactional databases.

    :Reference:    Bhargav Sripada, Polepalli Krishna Reddy, Rage Uday Kiran:
                   Coverage patterns for efficient banner advertisement placement. WWW (Companion Volume) 2011: 131-132
                   __https://dl.acm.org/doi/10.1145/1963192.1963259

    :param  iFile: str :
                   Name of the Input file to mine complete set of coverage patterns
    :param  oFile: str :
                   Name of the output file to store complete set of coverage patterns
    :param  minRF: str:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  minCS: str:
                   Controls the minimum number of transactions in which at least one time within a pattern must appear in a database.
    :param  maxOR: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

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

      (.venv) $ python3 CMine.py <inputFile> <outputFile> <minRF> <minCS> <maxOR> <'\t'>

      Example Usage:

      (.venv) $ python3 CMine.py sampleTDB.txt patterns.txt 0.4 0.7 0.5 '\t'

    .. note: At the fixed minCS value, it can also be observed that the number of patterns increases as maxOR value increases.

    **Calling from a python program**

    .. code-block:: python

            from PAMI.coveragePattern.basic import CMine as alg

            obj = alg.CMine(iFile, minRF, minCS, maxOR, seperator)

            obj.mine()

            coveragePattern = obj.getPatterns()

            print("Total number of coverage Patterns:", len(coveragePattern))

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

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

    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _minCS = str()
    _minRF = str()
    _maxOR = str()
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}
    _lno = 0


    @staticmethod
    def _convert(value) -> Union[int, float]:
        """
        To convert the user specified minSup value

        :param value: user specified minSup value
        :return: converted type
        :rtype: Union[int, float]
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = value
        if type(value) is str:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        return value

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        self._mapSupport = {}
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()

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
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            self._lno += 1
                            splitter = [i.rstrip() for i in line.split(self._sep)]
                            splitter = [x for x in splitter if x]
                            self._Database.append(splitter)
                except IOError:
                    print("File Not Found")

    def creatingCoverageItems(self) -> Dict[str, List[str]]:
        """
        This function creates coverage items from _database.

        :return: coverageTidData that stores coverage items and their tid list.
        :rtype: dict
        """
        tidData = {}
        self._lno = 0
        for transaction in self._Database:
            self._lno = self._lno + 1
            for item in transaction[1:]:
                if item not in tidData:
                    tidData[item] = [self._lno]
                else:
                    tidData[item].append(self._lno)
        coverageTidData = {k: v for k, v in tidData.items() if len(v) / len(self._Database) >= self._minRF}
        coverageTidData = dict(sorted(coverageTidData.items(), reverse=True, key=lambda x: len(x[1])))
        return coverageTidData

    def tidToBitset(self,item_set: Dict[str, int]) -> Dict[str, int]:
        """
        This function converts tid list to bitset.

        :param item_set:
        :return: Dictionary
        :rtype: dict[str,int]
        """
        bitset = {}

        for k,v in item_set.items():
            bitset[k] = 0b1
            bitset[k] = (bitset[k] << int(v[0])) | 0b1
            for i in range(1,len(v)):
                diff = int(v[i]) - int(v[i-1])
                bitset[k] = (bitset[k] << diff) | 0b1
            bitset[k] = (bitset[k] << (self._lno - int(v[i])))
        return bitset

    def genPatterns(self,prefix: Tuple[str, int],tidData: List[Tuple[str, int]]) -> None:
        """
        This function generate coverage pattern about prefix.

        :param prefix: String
        :param tidData: list
        :return: None
        """
        # variables to store coverage item set and
        item_set = prefix[0]

        # Get the length of tidData
        length = len(tidData)
        for i in range(length):
            tid = prefix[1] & tidData[i][1]
            tid1 = prefix[1] | tidData[i][1]
            andCount = bin(tid).count("1") - 1
            orCount = bin(tid1).count("1") - 1
            if orCount/len(self._Database) >= self._minCS and andCount / len(str(prefix[1])) <= self._maxOR:
                coverageItem_set = item_set + '\t' + tidData[i][0]
                if orCount / len(self._Database) >= self._minRF:
                    self._finalPatterns[coverageItem_set] = andCount
                self.genPatterns((coverageItem_set,tid),tidData[i+1:length])

    def generateAllPatterns(self,coverageItems: Dict[str, int]) -> None:
        """
        This function generates all coverage patterns.

        :param coverageItems: coverage items
        :return: None
        """
        tidData = list(coverageItems.items())
        length = len(tidData)
        for i in range(length):
            #print(i,tidData[i][0])
            self.genPatterns(tidData[i],tidData[i+1:length])

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """ Main method to start """

        self.mine()

    def mine(self) -> None:
        """ Main method to start """

        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        self._creatingItemSets()
        self._minCS = self._convert(self._minCS)
        self._minRF =  self._convert(self._minRF)
        self._maxOR = self._convert(self._maxOR)
        coverageItems = self.creatingCoverageItems()
        self._finalPatterns = {k: len(v) for k, v in coverageItems.items()}
        coverageItemsBitset = self.tidToBitset(coverageItems)
        self.generateAllPatterns(coverageItemsBitset)
        self.save('output.txt')
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Coverage patterns were generated successfully using CMine  algorithm")

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
        Storing final coverage patterns in a dataframe

        :return: returning coverage patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete set of coverage patterns will be loaded in to an output file

        :param outFile: name of the outputfile
        :type outFile: file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def getPatterns(self) -> Dict[str, int]:
        """
        Function to send the set of coverage patterns after completion of the mining process

        :return: Dictionary of patterns and their support counts.
        :rtype: Dict[str, int]
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the result
        """
        print("Total number of Coverage Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__=="__main__":
    _ap = str()
    if len(_ab._sys.argv) == 7 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 7:
            _ap = CMine(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6])
        if len(_ab._sys.argv) == 6:
            _ap = CMine(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        _ap.mine()
        _ap.mine()
        print("Total number of coverage Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
