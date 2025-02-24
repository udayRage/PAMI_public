# Stable periodic pattern mining aims to discover all interesting patterns in a temporal database using three constraints minimum support,
# maximum period and maximum liability, that have support no less than the user-specified minimum support  constraint and liability no
# greater than maximum liability.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.stablePeriodicFrequentPattern.basic import basic as alg
#
#             obj = alg.SPPEclat("../basic/sampleTDB.txt", 5, 3, 3)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of Stable Periodic Frequent Patterns:", len(Patterns))
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
import pandas as pd
from deprecated import deprecated

from PAMI.stablePeriodicFrequentPattern.basic import abstract as _ab

class SPPEclat(_ab._stablePeriodicFrequentPatterns):
    """
    :Description:   Stable periodic pattern mining aims to dicover all interesting patterns in a temporal database using three contraints minimum support,
                    maximum period and maximum lability, that have support no less than the user-specified minimum support  constraint and lability no
                    greater than maximum lability.

    :Reference:   Fournier-Viger, P., Yang, P., Lin, J. C.-W., Kiran, U. (2019). Discovering Stable Periodic-Frequent Patterns in Transactional Data. Proc.
                  32nd Intern. Conf. on Industrial, Engineering and Other Applications of Applied Intelligent Systems (IEA AIE 2019), Springer LNAI, pp. 230-244

    :param  iFile: str :
                   Name of the Input file to mine complete set of stable periodic Frequent Pattern.
    :param  oFile: str :
                   Name of the output file to store complete set of stable periodic Frequent Pattern.
    :param  minSup: float or int or str :
                    The user can specify minSup either in count or proportion of database size.
                    If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
                    Otherwise, it will be treated as float.
                    Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
    :param  itemSup: int or float :
                    Frequency of an item
    :param maxLa: float :
                  minimum loss of a pattern
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
        maxLa : int or float or str
            The user can specify maxLa either in count or proportion of database size.
            If the program detects the data type of maxLa is integer, then it treats maxLa is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxLa=10 will be treated as integer, while maxLa=10.0 will be treated as float
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
        creatingItemSets()
            Scan the database and store the items with their timestamps which are periodic frequent
        calculateLa()
            Calculates the support and period for a list of timestamps.
        Generation()
            Used to implement prefix class equivalence method to generate the periodic patterns recursively



    **Methods to execute code on terminal**
    -----------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 basic.py <inputFile> <outputFile> <minSup> <maxPer> <maxLa>

       Example usage:

       (.venv) $ python3 basic.py sampleDB.txt patterns.txt 10.0 4.0 2.0


               .. note:: constraints will be considered in percentage of database transactions

    **Importing this algorithm into a python program**
    ---------------------------------------------------
    ... code-block:: python

                    from PAMI.stablePeriodicFrequentPattern.basic import basic as alg

                    obj = alg.PFPECLAT("../basic/sampleTDB.txt", 5, 3, 3)

                    obj.mine()

                    Patterns = obj.getPatterns()

                    print("Total number of Stable Periodic Frequent Patterns:", len(Patterns))

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
             The complete program was written by  P.Likhitha under the supervision of Professor Rage Uday Kiran.

       """
    _iFile = " "
    _oFile = " "
    _minSup = str()
    _maxPer = str()
    _maxLa = float()
    _sep = " "
    _SPPList = {}
    _itemList = []
    _last = int()
    _finalPatterns = {}
    _tsList = {}
    _startTime = float()
    _endTime = float()
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []

    def __init__(self, inputFile, minSup, maxPer, maxLa, iFile, maxLA, sep='\t'):
        super().__init__(iFile, minSup, maxPer, maxLA, sep)
        self._iFile = inputFile
        self._minSup = minSup
        self._maxPer = maxPer
        self._maxLa = maxLa
        self._sep = sep

    def _creatingItemsets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
            if 'Patterns' in i:
                self._Database = self._iFile['Patterns'].tolist()
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

    def _convert(self, value):
        """
        to convert the type of user specified minSup value

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

    def _createSPPList(self):
        """
        to convert the single length stable periodic patterns
        """
        tidLast = {}
        la = {}
        self._SPPList = {}
        self._tsList = {}
        for transaction in self._Database:
            ts = int(transaction[0])
            for item in transaction[1:]:
                if item not in self._SPPList:
                    la[item] = max(0, ts - self._maxPer)
                    self._SPPList[item] = [1, la[item]]
                    self._tsList[item] = [ts]
                else:
                    s = self._SPPList[item][0] + 1
                    la[item] = max(0, la[item] + ts - tidLast.get(item) - self._maxPer)
                    self._SPPList[item] = [s, max(la[item], self._SPPList[item][1])]
                    self._tsList[item].append(ts)
                tidLast[item] = ts
            self._last = ts
        for item in self._SPPList:
            la[item] = max(0, la[item] + self._last - tidLast[item] - self._maxPer)
            self._SPPList[item][1] = max(la[item], self._SPPList[item][1])
        self._SPPList = {k: v for k, v in self._SPPList.items() if v[0] >= self._minSup and v[1] <= self._maxLa}
        self._SPPList = {k: v for k, v in sorted(self._SPPList.items(), key=lambda x: x[1][0], reverse=True)}
        self._Generation(list(self._SPPList), set())

    def _Generation(self, GPPFList, CP):
        """
        To generate the patterns using depth-first search
        """
        for i in range(len(GPPFList)):
            item = GPPFList[i]
            CP1 = CP | {item}
            if CP != set():
                self._tsList['\t'.join(CP1)] = list(set(self._tsList['\t'.join(CP)]) & set(self._tsList[item]))
            la = self._calculateLa(self._tsList['\t'.join(CP1)])
            support = len(self._tsList['\t'.join(CP1)])
            if la <= self._maxLa and len(self._tsList['\t'.join(CP1)]) >= self._minSup:
                #CP = CP1
                self._finalPatterns['\t'.join(CP1)] = [support, la]
                if i+1 < len(GPPFList):
                    self._Generation(GPPFList[i+1:], CP1)

    def _calculateLa(self, tsList):
        """
        To calculate the liability of a patterns based on its timestamps
        """
        previous = 0
        la = 0
        tsList = sorted(tsList)
        laList = []
        for ts in tsList:
            la = max(0, la + ts - previous - self._maxPer)
            laList.append(la)
            previous = ts
            
        la = max(0, la + self._last - previous - self._maxPer)
        laList.append(la)
        maxla = max(laList)
        return maxla

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Method to start the mining of patterns
        """
        self.mine()

    def mine(self):
        """
        Method to start the mining of patterns
        """
        self._startTime = _ab._time.time()
        self._creatingItemsets()
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        self._maxLa = self._convert(self._maxLa)
        self._finalPatterns = {}
        #print(self._minSup, self._maxPer, self._maxLa)
        self._createSPPList()
        self._endTime = _ab._time.time()
        self._memoryUSS = float()
        self._memoryRSS = float()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Stable Periodic Frequent patterns were generated successfully using basic algorithm ")


    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self._endTime - self._startTime

    def getPatterns(self):
        """
        Function to return the set of stable periodic-frequent patterns after completion of the mining process

        :return: returning stable periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def save(self, outFile):
        """
        Complete set of periodic-frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatternsAsDataFrame(self):
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Stable Periodic  Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())

if __name__ == '__main__':
    _ap = str()
    if len(_ab._sys.argv) == 6 or len(_ab._sys.argv) == 7:
        if len(_ab._sys.argv) == 7:
            _ap = SPPEclat(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6])
        if len(_ab._sys.argv) == 6:
            _ap = SPPEclat(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        _ap.mine()
        _ap.mine()
        print("Total number of Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
