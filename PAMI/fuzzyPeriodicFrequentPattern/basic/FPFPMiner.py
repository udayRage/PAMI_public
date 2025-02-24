# Fuzzy Periodic Frequent Pattern Miner is desired to find all fuzzy periodic frequent patterns which is
# on-trivial and challenging problem to its huge search space.we are using efficient pruning
# techniques to reduce the search space.
#
# Sample run of importing the code:
# ----------------------------------------
#
#             from PAMI.fuzzyPeriodicFrequentPattern.basic import FPFPMiner as alg
#
#             obj =alg.FPFPMiner("input.txt",2,3)
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Fuzzy Periodic Frequent Patterns:", len(periodicFrequentPatterns))
#
#             obj.save("output.txt")
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


from PAMI.fuzzyPeriodicFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated


class _FFList:
    """
    A class represent a Fuzzy List of an element
    :Attributes:

        item : int
            the item name
        sumLUtil : float
            the sum of utilities of a fuzzy item in database
        sumRUtil : float
            the sum of resting values of a fuzzy item in database
        elements : list
            list of elements contain tid,Utility and resting values of element in each transaction
        maxPeriod : int
            it represents the max period of a item

    :Methods:

        addElement(element)
            Method to add an element to this fuzzy list and update the sums at the same time.
        printElement(e)
            Method to print elements

    """

    def __init__(self, itemName: str) -> None:
        self.item = itemName
        self.sumLUtil = 0.0
        self.sumRUtil = 0.0
        self.elements = []
        self.maxPeriod = 0

    def addElement(self, element) -> None:
        """
        A Method that add a new element to FFList

        :param element: an element to be added to FFList
        :type element: Element
        :return: None
        """
        self.sumLUtil += element.lUtils
        self.sumRUtil += element.rUtils
        self.elements.append(element)
        self.maxPeriod = max(self.maxPeriod, element.period)

    def printElement(self) -> None:
        """
        A Method to Print elements in the FFList
        :return: None
        """
        for ele in self.elements:
            print(ele.tid, ele.lUtils, ele.rUtils, ele.period)


class _Element:
    """
        A class represents an Element of a fuzzy list

        :Attributes:

        tid : int
            keep tact of transaction id
        lUtils: float
            the utility of a fuzzy item in the transaction
        rUtils : float
            the resting value of a fuzzy item in the transaction
        period: int
            represent the period of the element
    """

    def __init__(self, tid: int, iUtil: float, rUtil: float, period: int) -> None:
        self.tid = tid
        self.lUtils = iUtil
        self.rUtils = rUtil
        self.period = period


class _Pair:
    """
    A class to store item name and quantity together.
    """

    def __init__(self) -> None:
        self.item = 0
        self.quantity = 0


class FPFPMiner(_ab._fuzzyPeriodicFrequentPatterns):
    """
    :Description:   Fuzzy Periodic Frequent Pattern Miner is desired to find all fuzzy periodic frequent patterns which is
                    on-trivial and challenging problem to its huge search space.we are using efficient pruning
                    techniques to reduce the search space.

    :Reference:   R. U. Kiran et al., "Discovering Fuzzy Periodic-Frequent Patterns in Quantitative Temporal Databases,"
                  2020 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE), Glasgow, UK, 2020, pp.
                  1-8, doi: 10.1109/FUZZ48607.2020.9177579.

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of fuzzy spatial frequent patterns
        oFile : file
               Name of the oFile file to store complete set of fuzzy spatial frequent patterns
        minSup : float
            The user given support
        period: int
            periodicity of an element
        memoryRSS : float
                To store the total amount of RSS memory consumed by the program
        startTime:float
               To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        itemsCnt: int
            To record the number of fuzzy spatial itemSets generated
        mapItemsLowSum: map
            To keep track of low region values of items
        mapItemsMidSum: map
            To keep track of middle region values of items
        mapItemsHighSum: map
            To keep track of high region values of items
        mapItemSum: map
            To keep track of sum of Fuzzy Values of items
        mapItemRegions: map
            To Keep track of fuzzy regions of item
        jointCnt: int
            To keep track of the number of FFI-list that was constructed
        BufferSize: int
            represent the size of Buffer
        itemBuffer list
            to keep track of items in buffer
        maxTID: int
            represent the maximum tid of the database
        lastTIDs: map
            represent the last tid of fuzzy items
        itemsToRegion: map
            represent items with respective regions

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
        convert(value):
            To convert the given user specified value
        FSFIMining( prefix, prefixLen, fsFim, minSup)
            Method generate FFI from prefix
        construct(px, py)
            A function to construct Fuzzy itemSet from 2 fuzzy itemSets
        findElementWithTID(UList, tid)
            To find element with same tid as given
        WriteOut(prefix, prefixLen, item, sumIUtil,period)
            To Store the patten

    **Executing the code on terminal :**
    ----------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 FPFPMiner.py <inputFile> <outputFile> <minSup> <maxPer> <sep>

      Example Usage:

      (.venv) $ python3  FPFPMiner.py sampleTDB.txt output.txt 2 3

    .. note:: minSup will be considered in percentage of database transactions


    **Sample run of importing the code:**
    --------------------------------------

        from PAMI.fuzzyPeriodicFrequentPattern.basic import FPFPMiner as alg

        obj =alg.FPFPMiner("input.txt",2,3)

        obj.mine()

        periodicFrequentPatterns = obj.getPatterns()

        print("Total number of Fuzzy Periodic Frequent Patterns:", len(periodicFrequentPatterns))

        obj.save("output.txt")

        memUSS = obj.getMemoryUSS()

        print("Total Memory in USS:", memUSS)

        memRSS = obj.getMemoryRSS()

        print("Total Memory in RSS", memRSS)

        run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)

    **Credits:**
    --------------
            The complete program was written by Sai Chitra.B under the supervision of Professor Rage Uday Kiran.

    """
    _startTime = float()
    _endTime = float()
    _minSup = float()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _sep = " "
    _Database = []
    _transactions = []
    _fuzzyValues = []
    _ts = []

    def __init__(self, iFile: Union[str, _ab._pd.DataFrame], minSup: Union[int, float], period: Union[int, float], sep: str="\t") -> None:
        super().__init__(iFile, minSup, period, sep)
        self._oFile = ""
        self._BufferSize = 200
        self._itemSetBuffer = []
        self._mapItemSum = {}
        self._finalPatterns = {}
        self._joinsCnt = 0
        self._itemsCnt = 0
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._dbLen = 0

    def _compareItems(self, o1, o2) -> int:
        """
        A Function that sort all FFI-list in ascending order of Support

        :param o1: First FFI-list

        :type o1: _FFList

        :param o2: Second FFI-list

        :type o1: _FFList

        :return: Comparision Value

        :rtype: int
        """
        compare = self._mapItemSum[o1.item] - self._mapItemSum[o2.item]
        if compare == 0:
            return int(o1.item) - int(o2.item)
        else:
            return compare

    def _convert(self, value) -> float:
        """
        To convert the given user specified value

        :param value: user specified value

        :type value: int or float or str

        :return: converted value

        :rtype: float
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbLen * value)
        if type(value) is str:
            if '.' in value:
                value = (self._dbLen * value)
            else:
                value = int(value)
        return value

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable

        :return: None
        """
        data, self._transactions, self._fuzzyValues, ts = [], [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                self._ts = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                self._transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValues = self._iFile['fuzzyValues'].tolist()
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                count = 0
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    parts[0] = parts[0].strip()
                    parts[1] = parts[1].strip()
                    items = parts[0].split(self._sep)
                    quantities = parts[1].split(self._sep)
                    self._ts.append(int(items[0]))
                    self._transactions.append([x for x in items[1:]])
                    self._fuzzyValues.append([float(x) for x in quantities])
                    count += 1
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        count = 0
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            items = parts[0].split(self._sep)
                            quantities = parts[1].split(self._sep)
                            self._ts.append(int(items[0]))
                            self._transactions.append([x for x in items[1:]])
                            self._fuzzyValues.append([float(x) for x in quantities])
                            count += 1
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Fuzzy periodic Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self) -> None:
        """
        Fuzzy periodic Frequent pattern mining process will start from here
        """
        maxTID = 0
        lastTIDs = {}
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._finalPatterns = {}
        tid = int()
        for line in range(len(self._transactions)):
            tid = int(self._ts[line])
            self._dbLen += 1
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            if tid < maxTID:
                maxTID = tid
            for i in range(0, len(items)):
                item = items[i]
                if item in self._mapItemSum:
                    self._mapItemSum[item] += quantities[i]
                else:
                    self._mapItemSum[item] = quantities[i]
        listOfFFIList = []
        mapItemsToFFLIST = {}
        # self._minSup = self._convert(self._minSup)
        self._minSup = float(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        for item1 in self._mapItemSum.keys():
            item = item1
            if self._mapItemSum[item] >= self._minSup:
                fUList = _FFList(item)
                k = tuple([item])
                mapItemsToFFLIST[k] = fUList
                listOfFFIList.append(fUList)
                lastTIDs[item] = tid
        listOfFFIList.sort(key=_ab._functools.cmp_to_key(self._compareItems))
        for line in range(len(self._transactions)):
            tid = int(self._ts[line])
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            revisedTransaction = []
            for i in range(0, len(items)):
                pair = _Pair()
                pair.item = items[i]
                item = pair.item
                pair.quantity = quantities[i]
                if self._mapItemSum[item] >= self._minSup:
                    if pair.quantity > 0:
                        revisedTransaction.append(pair)
            revisedTransaction.sort(key=_ab._functools.cmp_to_key(self._compareItems))
            for i in range(len(revisedTransaction) - 1, -1, -1):
                pair = revisedTransaction[i]
                remainUtil = 0
                for j in range(len(revisedTransaction) - 1, i - 1, -1):
                    remainUtil += revisedTransaction[j].quantity
                if pair.quantity > remainUtil:
                    remainingUtility = pair.quantity
                else:
                    remainingUtility = remainUtil
                if mapItemsToFFLIST.get(tuple([pair.item])) is not None:
                    FFListOfItem = mapItemsToFFLIST[tuple([pair.item])]
                    if len(FFListOfItem.elements) == 0:
                        element = _Element(tid, pair.quantity, remainingUtility, 0)
                    else:
                        if lastTIDs[pair.item] == tid:
                            element = _Element(tid, pair.quantity, remainingUtility, maxTID - tid)
                        else:
                            lastTid = FFListOfItem.elements[-1].tid
                            curPer = tid - lastTid
                            element = _Element(tid, pair.quantity, remainingUtility, curPer)
                    FFListOfItem.addElement(element)
        self._FPFPMining(self._itemSetBuffer, 0, listOfFFIList)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def _FPFPMining(self, prefix, prefixLen, fsFim):

        """
        Generates FPFP from prefix

        :param prefix: the prefix patterns of FPFP
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
        :param fsFim: the Fuzzy list of prefix itemSets
        :type fsFim: list
        """
        for i in range(0, len(fsFim)):
            X = fsFim[i]
            if X.sumLUtil >= self._minSup and X.maxPeriod <= self._maxPer:
                self._WriteOut(prefix, prefixLen, X.item, X.sumLUtil, X.maxPeriod)
            if X.sumRUtil >= self._minSup:
                exULs = []
                for j in range(i + 1, len(fsFim)):
                    Y = fsFim[j]
                    exULs.append(self._construct(X, Y))
                    self._joinsCnt += 1
                self._itemSetBuffer.insert(prefixLen, X.item)
                self._FPFPMining(self._itemSetBuffer, prefixLen + 1, exULs)

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

    def _construct(self, px: _FFList, py: _FFList) -> _FFList:
        """
        A function to construct a new Fuzzy item set from 2 fuzzy itemSets

        :param px:the item set px
        :type px:FFI-List
        :param py:item set py
        :type py:FFI-List
        :return :the item set of pxy(px and py)
        :rtype :FFI-List
        """
        pxyUL = _FFList(py.item)
        prev = 0
        for ex in px.elements:
            ey = self._findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            eXY = _Element(ex.tid, min([ex.lUtils, ey.lUtils], key=lambda x: float(x)), ey.rUtils, ex.tid - prev)
            pxyUL.addElement(eXY)
            prev = ex.tid
        return pxyUL

    def _findElementWithTID(self, UList, tid) -> _Element:
        """
        To find element with same tid as given

        :param UList: fuzzy list
        :type UList: FFI-List
        :param tid:transaction id
        :type tid: int
        :return: element eith tid as given
        :rtype: element if exist or None
        """
        List_ = UList.elements
        first = 0
        last = len(List_) - 1
        while first <= last:
            mid = (first + last) >> 1
            if List_[mid].tid < tid:
                first = mid + 1
            elif List_[mid].tid > tid:
                last = mid - 1
            else:
                return List_[mid]
        return None

    def _WriteOut(self, prefix: List[int], prefixLen: int, item: int, sumLUtil: float, period: int) -> None:
        """
        To Store the patten

        :param prefix: prefix of itemSet
        :type prefix: list
        :param prefixLen: length of prefix
        :type prefixLen: int
        :param item: the last item
        :type item: int
        :param sumLUtil: sum of utility of itemSet
        :type sumLUtil: float
        :param period: represent the period of itemSet
        :type period: int
        :return: None
        """
        self._itemsCnt += 1
        res = ""
        for i in range(0, prefixLen):
            res += str(prefix[i]) +  "\t"
        res += str(item)
        #res1 = str(sumLUtil) + " : " + str(period)
        self._finalPatterns[res] = [sumLUtil, period]

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def getPatterns(self) -> Dict[str, str]:
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile: str) -> None:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % patternsAndSupport)

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Fuzzy Periodic-Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:  # to  include a user specified separator
            _ap = FPFPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:  # to consider "\t" as a separator
            _ap = FPFPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = FPFPMiner('sample.txt', 1, 10, ' ')
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")

