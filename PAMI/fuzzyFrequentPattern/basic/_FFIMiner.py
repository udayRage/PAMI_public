# Fuzzy Frequent  Pattern-Miner is desired to find all  frequent fuzzy patterns which is on-trivial and challenging problem
#
# to its huge search space.we are using efficient pruning techniques to reduce the search space.
#
# **Importing this algorithm into a python program**
# ---------------------------------------------------------
#
#             from PAMI.fuzzyFrequentPattern import FFIMiner as alg
#
#             obj = alg.FFIMiner("input.txt", 2)
#
#             obj.mine()
#
#             fuzzyFrequentPattern = obj.getPatterns()
#
#             print("Total number of Fuzzy Frequent Patterns:", len(fuzzyFrequentPattern))
#
#             obj.save("outputFile")
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

from PAMI.fuzzyFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated


class _FFList:
    """
    A class represent a Fuzzy List of an element

    :Attributes:

        item: int
            the item name

        sumIUtil: float
            the sum of utilities of a fuzzy item in database

        sumRUtil: float
            the sum of resting values of a fuzzy item in database

        elements: list
            a list of elements contain tid,Utility and resting values of element in each transaction

    :Methods:

        addElement(element)
            Method to add an element to this fuzzy list and update the sums at the same time.

        printElement(e)
            Method to print elements
    """

    def __init__(self, itemName: int) -> None:
        self.item = itemName
        self.sumIUtil = 0.0
        self.sumRUtil = 0.0
        self.elements = []

    def addElement(self, element) -> None:
        """
        A Method that add a new element to FFList

        :param element: an element to be added to FFList
        :type element: Element
        :return: None
        """
        self.sumIUtil += element.iUtils
        self.sumRUtil += element.rUtils
        self.elements.append(element)

    def printElement(self) -> None:
        """
        A method to print elements
        """
        for ele in self.elements:
            print(ele.tid, ele.iUtils, ele.rUtils)


class _Element:
    """
    A class represents an Element of a fuzzy list

    :Attributes:

        tid : int
            keep tact of transaction id

        iUtils: float
            the utility of a fuzzy item in the transaction

        rUtils : float
            the  resting value of a fuzzy item in the transaction
    """

    def __init__(self, tid: int, iUtil: float, rUtil: float) -> None:
        self.tid = tid
        self.iUtils = iUtil
        self.rUtils = rUtil


class _Pair:
    """
    A class to store item and it's quantity together
    """

    def __init__(self) -> None:
        self.item = 0
        self.quantity = 0


class FFIMiner(_ab._fuzzyFrequentPattenrs):
    """
    :Description:   Fuzzy Frequent  Pattern-Miner is desired to find all  frequent fuzzy patterns which is on-trivial and challenging problem
                    to its huge search space.we are using efficient pruning techniques to reduce the search space.

    :Reference:   Lin, Chun-Wei & Li, Ting & Fournier Viger, Philippe & Hong, Tzung-Pei. (2015).
                  A fast Algorithm for mining fuzzy frequent itemsets. Journal of Intelligent & Fuzzy Systems. 29.
                  2373-2379. 10.3233/IFS-151936.
                  https://www.researchgate.net/publication/286510908_A_fast_Algorithm_for_mining_fuzzy_frequent_itemSets

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param fuzFile: str :
                    The user can specify fuzFile.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : string
            Name of the input file to mine complete set of fuzzy  frequent patterns

        fmFile : string
            Name of the fuzzy membership file to mine complete set of fuzzy  frequent patterns

        oFile : string
            Name of the oFile file to store complete set of fuzzy  frequent patterns

        minSup : float
            The user given minimum support

        memoryRSS : float
            To store the total amount of RSS memory consumed by the program

        startTime:float
            To record the start time of the mining process

        endTime:float
            To record the completion time of the mining process

        itemsCnt: int
            To record the number of fuzzy spatial itemSets generated

        mapItemSum: map
            To keep track of sum of Fuzzy Values of items

        joinsCnt: int
            To keep track of the number of ffi-list that was constructed

        BufferSize: int
            represent the size of Buffer

        itemSetBuffer list
            to keep track of items in buffer

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
        convert(value)
            To convert the given user specified value
        compareItems(o1, o2)
            A Function that sort all ffi-list in ascending order of Support
        FSFIMining(prefix, prefixLen, FSFIM, minSup)
            Method generate ffi from prefix
        construct(px, py)
            A function to construct Fuzzy itemSet from 2 fuzzy itemSets
        findElementWithTID(uList, tid)
            To find element with same tid as given
        WriteOut(prefix, prefixLen, item, sumIUtil)
            To Store the patten


    **Executing the code on terminal :**
    ------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 FFIMiner.py <inputFile> <outputFile> <minSup> <separator>

      Example Usage:

      (.venv) $ python3  FFIMiner.py sampleTDB.txt output.txt 6

    .. note:: minSup will be considered in percentage of database transactions


    **Sample run of importing the code:**
    ------------------------------------------
    .. code-block:: python

            from PAMI.fuzzyFrequentPattern import FFIMiner as alg

            obj = alg.FFIMiner("input.txt", 2)

            obj.mine()

            fuzzyFrequentPattern = obj.getPatterns()

            print("Total number of Fuzzy Frequent Patterns:", len(fuzzyFrequentPattern))

            obj.save("outputFile")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    **Credits:**
    ---------------
            The complete program was written by B.Sai Chitra under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _fuzFile = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _sep = "\t"

    def __init__(self, iFile: str, minSup: float, sep: str="\t") -> None:
        super().__init__(iFile, minSup, sep)
        self._startTime = 0
        self._endTime = 0
        self._itemsCnt = 0
        self._mapItemSum = {}
        self._joinsCnt = 0
        self._BufferSize = 200
        self._itemSetBuffer = []
        self._transactions = []
        self._fuzzyValues = []
        self._finalPatterns = {}
        self._dbLen = 0

    def _compareItems(self, o1: _FFList, o2: _FFList) -> int:
        """
        A Function that sort all ffi-list in ascending order of Support

        :param o1: First FFI-list
        :type o1: _FFList
        :param o2: Second FFI-list
        :type o1: _FFList
        :return: Comparision Value
        :rtype: int
        """
        compare = self._mapItemSum[o1.item] - self._mapItemSum[o2.item]
        if compare == 0:
            if o1.item < o2.item:
                return -1
            elif o1.item > o2.item:
                return 1
            else:
                return 0
        else:
            return compare

    def _convert(self, value) -> Union[int, float]:
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
            value = (self._dbLen * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbLen * value)
            else:
                value = int(value)
        return value

    def _creatingItemsets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._transactions, self._fuzzyValues, self._Database = [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValues = self._iFile['fuzzyValues'].tolist()
            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    parts[0] = parts[0].strip()
                    parts[1] = parts[1].strip()
                    items = parts[0].split(self._sep)
                    quantities = parts[1].split(self._sep)
                    self._transactions.append([x for x in items])
                    self._fuzzyValues.append([float(x) for x in quantities])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            items = parts[0].split(self._sep)
                            quantities = parts[1].split(self._sep)
                            self._transactions.append([x for x in items])
                            self._fuzzyValues.append([float(x) for x in quantities])
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        fuzzy-Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self) -> None:
        """
        fuzzy-Frequent pattern mining process will start from here
        """
        self._startTime = _ab._time.time()
        self._creatingItemsets()
        for line in range(len(self._transactions)):
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            self._dbLen += 1
            for i in range(0, len(items)):
                item = items[i]
                if item in self._mapItemSum:
                    self._mapItemSum[item] += quantities[i]
                else:
                    self._mapItemSum[item] = quantities[i]
        listOfffilist = []
        mapItemsToFFLIST = {}
        #self._minSup = self._convert(self._minSup)
        # minSup = self.minSup
        for item1 in self._mapItemSum.keys():
            item = item1
            if self._mapItemSum[item] >= self._minSup:
                fuList = _FFList(item)
                mapItemsToFFLIST[item] = fuList
                listOfffilist.append(fuList)
        listOfffilist.sort(key=_ab._functools.cmp_to_key(self._compareItems))
        tid = 0
        for line in range(len(self._transactions)):
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            revisedTransaction = []
            for i in range(0, len(items)):
                pair = _Pair()
                pair.item = items[i]
                pair.quantity = quantities[i]
                item = pair.item
                if self._mapItemSum[item] >= self._minSup:
                    if pair.quantity > 0:
                        revisedTransaction.append(pair)
            revisedTransaction.sort(key=_ab._functools.cmp_to_key(self._compareItems))
            for i in range(len(revisedTransaction) - 1, -1, -1):
                pair = revisedTransaction[i]
                remainUtil = 0
                for j in range(len(revisedTransaction) - 1, i, -1):
                    remainUtil += revisedTransaction[j].quantity
                remainingUtility = remainUtil
                if mapItemsToFFLIST.get(pair.item) is not None:
                    FFListOfItem = mapItemsToFFLIST[pair.item]
                    element = _Element(tid, pair.quantity, remainingUtility)
                    FFListOfItem.addElement(element)
            tid += 1
        self._FFIMining(self._itemSetBuffer, 0, listOfffilist, self._minSup)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def _FFIMining(self, prefix, prefixLen, FSFIM, minSup):
        """
        Generates ffi from prefix

        :param prefix: the prefix patterns of ffi
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
        :param FSFIM: the Fuzzy list of prefix itemSets
        :type FSFIM: list
        :param minSup: the minimum support of
        :type minSup: int or float
        """
        for i in range(0, len(FSFIM)):
            X = FSFIM[i]
            if X.sumIUtil >= minSup:
                self._WriteOut(prefix, prefixLen, X.item, X.sumIUtil)
            if X.sumRUtil >= minSup:
                exULs = []
                for j in range(i + 1, len(FSFIM)):
                    Y = FSFIM[j]
                    exULs.append(self._construct(X, Y))
                    self._joinsCnt += 1
                self._itemSetBuffer.insert(prefixLen, X.item)
                self._FFIMining(self._itemSetBuffer, prefixLen + 1, exULs, minSup)

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

    def _construct(self, px, py) -> _FFList:
        """
        A function to construct a new Fuzzy itemSet from 2 fuzzy itemSets

        :param px:the itemSet px
        :type px:ffi-List
        :param py:itemSet py
        :type py:ffi-List
        :return :the itemSet of pxy(px and py)
        :rtype :ffi-List
        """
        pxyUL = _FFList(py.item)
        for ex in px.elements:
            ey = self._findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            eXY = _Element(ex.tid, min([ex.iUtils, ey.iUtils], key=lambda x: float(x)), ey.rUtils)
            pxyUL.addElement(eXY)
        return pxyUL

    def _findElementWithTID(self, uList, tid) -> _Element:
        """
        To find element with same tid as given

        :param uList: fuzzyList
        :type uList: ffi-List
        :param tid: transaction id
        :type tid: int
        :return: element  tid as given
        :rtype: element if exit or None
        """
        List_ = uList.elements
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

    def _WriteOut(self, prefix: list, prefixLen: int, item: int, sumIUtil: float) -> None:
        """
        To Store the patten

        :param prefix: prefix of itemSet
        :type prefix: list
        :param prefixLen: length of prefix
        :type prefixLen: int
        :param item: the last item
        :type item: int
        :param sumIUtil: sum of utility of itemSet
        :type sumIUtil: float
        :return: None
        """
        self._itemsCnt += 1
        res = ""
        for i in range(0, prefixLen):
            res += str(prefix[i])  + "\t"
        res += str(item)
        res1 = str(sumIUtil)
        self._finalPatterns[res] = res1

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def getPatterns(self) -> dict:
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile) -> dict:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: dictionary of frequent patterns
        :rtype: dict
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Fuzzy Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = FFIMiner('/Users/tarunsreepada/Downloads/Fuzzy_T10I4D100K.csv', 400, '\t')
        # _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
        for k,v in _ap.getPatterns().items():
            print(k,v)

