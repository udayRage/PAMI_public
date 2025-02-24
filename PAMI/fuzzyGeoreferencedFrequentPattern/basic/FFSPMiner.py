# Fuzzy Frequent Spatial Pattern-Miner is desired to find all Spatially frequent fuzzy patterns
# which is on-trivial and challenging problem to its huge search space.we are using efficient pruning
# techniques to reduce the search space.
#
# **Importing this algorithm into a python program**
# ---------------------------------------------------------
# .. code-block:: python
#
#             from PAMI.fuzzyGeoreferencedFrequentPattern import FFSPMiner as alg
#
#             obj = alg.FFSPMiner("input.txt", "neighbours.txt", 2)
#
#             obj.mine()
#
#             fuzzySpatialFrequentPatterns = obj.getPatterns()
#
#             print("Total number of fuzzy frequent spatial patterns:", len(fuzzySpatialFrequentPatterns))
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

from PAMI.fuzzyGeoreferencedFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated


class _FFList:
    """
    A class represent a Fuzzy List of an element

    :Attributes:

         item : int
             the item name
         sumIUtil : float
             the sum of utilities of a fuzzy item in database
         sumRUtil : float
             the sum of resting values of a fuzzy item in database
         elements : list
             a list of elements contain tid,Utility and resting values of element in each transaction

    :Methods:

        addElement(element)
            Method to add an element to this fuzzy list and update the sums at the same time.
        printElement(e)
            Method to print elements

    """

    def __init__(self, itemName: str) -> None:
        self.item = itemName
        self.sumIUtil = 0.0
        self.sumRUtil = 0.0
        self.elements = []

    def addElement(self, element) -> None:
        """
        A Method that add a new element to FFList

        :param element: an element to be added to FFList
        :param element: Element
        :return: None
        """
        self.sumIUtil += element.iUtils
        self.sumRUtil += element.rUtils
        self.elements.append(element)

    def printElement(self) -> None:
        """
        A Method to Print elements in the FFList
        """
        for ele in self.elements:
            print(ele.tid, ele.iUtils, ele.rUtils)


class _Element:
    """
    A class represents an Element of a fuzzy list

    :Attributes:

        tid : int
            keep tact of transaction id
        iUtils : float
            the utility of a fuzzy item in the transaction
        rUtils : float
            the neighbourhood resting value of a fuzzy item in the transaction
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


class FFSPMiner(_ab._fuzzySpatialFrequentPatterns):
    """
    About this algorithm
    ====================

    :Description:   Fuzzy Frequent Spatial Pattern-Miner is desired to find all Spatially frequent fuzzy patterns
                    which is on-trivial and challenging problem to its huge search space.we are using efficient pruning
                    techniques to reduce the search space.

    :Reference:   Reference: P. Veena, B. S. Chithra, R. U. Kiran, S. Agarwal and K. Zettsu, "Discovering Fuzzy Frequent
                  Spatial Patterns in Large Quantitative Spatiotemporal databases," 2021 IEEE International Conference on Fuzzy Systems
                  (FUZZ-IEEE), 2021, pp. 1-8, doi: 10.1109/FUZZ45933.2021.9494594.

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param nFile: str :
                   Name of the input file to mine complete set of frequent patterns
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of fuzzy spatial frequent patterns
        oFile : file
            Name of the oFile file to store complete set of fuzzy spatial frequent patterns
        minSup : float
            The user given minimum support
        neighbors : map
            keep track of neighbours of elements
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime : float
            To record the start time of the mining process
        endTime : float
            To record the completion time of the mining process
        itemsCnt : int
            To record the number of fuzzy spatial itemSets generated
        mapItemSum : map
            To keep track of sum of Fuzzy Values of items
        mapItemRegions : map
            To Keep track of fuzzy regions of item
        joinsCnt : int
            To keep track of the number of FFI-list that was constructed
        BufferSize : int
            represent the size of Buffer
        itemSetBuffer : list
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
        FSFIMining( prefix, prefixLen, fsFim, minSup)
            Method generate FFI from prefix
        construct(px, py)
            A function to construct Fuzzy itemSet from 2 fuzzy itemSets
        Intersection(neighbourX,neighbourY)
            Return common neighbours of 2 itemSet Neighbours
        findElementWithTID(uList, tid)
            To find element with same tid as given
        WriteOut(prefix, prefixLen, item, sumIUtil,period)
            To Store the patten

    Execution methods
    =================


    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 FFSPMiner.py <inputFile> <outputFile> <neighbours> <minSup> <sep>

      Example Usage:

      (.venv) $ python3  FFSPMiner.py sampleTDB.txt output.txt sampleN.txt 3

    .. note::  minSup can be specified  in support count or a value between 0 and 1.

    **Calling from a python program**

    .. code-block:: python

            from PAMI.fuzzyGeoreferencedFrequentPattern import FFSPMiner as alg

            obj = alg.FFSPMiner("input.txt", "neighbours.txt", 2)

            obj.mine()

            fuzzySpatialFrequentPatterns = obj.getPatterns()

            print("Total number of fuzzy frequent spatial patterns:", len(fuzzySpatialFrequentPatterns))

            obj.save("outputFile")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    Credits
    =======
            The complete program was written by B.Sai Chitra under the supervision of Professor Rage Uday Kiran.
    """

    _minSup = str()
    _iFile = " "
    _nFile = " "
    _sep = "\t"

    def __init__(self, iFile: str, nFile: str, minSup: float, sep: str="\t") -> None:
        super().__init__(iFile, nFile, minSup, sep)
        self.oFile = None
        self._mapItemNeighbours = {}
        self._startTime = 0
        self._endTime = 0
        self._mapItemSum = {}
        self._joinsCnt = 0
        self._BufferSize = 200
        self._itemSetBuffer = []
        self._finalPatterns = {}
        self._dbLen = 0
        self._itemsCnt = 0

    def _compareItems(self, o1, o2) -> int:
        """
        A Function that sort all ffi-list in ascending order of Support

        :param o1: First FFI-list
        :type o1: _FFList
        :param o2: Second FFI-list
        :type o2: _FFList
        :return: Comparision Value
        :rtype: int
        """
        compare = self._mapItemSum[o1.item] - self._mapItemSum[o2.item]
        if compare == 0:
            return 0
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
        self._transactions, self._fuzzyValues = [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self.fuzzyValues = self._iFile['Utilities'].tolist()

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

    def _mapNeighbours(self) -> None:
        self._mapItemNeighbours = {}
        if isinstance(self._nFile, _ab._pd.DataFrame):
            data, items = [], []
            if self._nFile.empty:
                print("its empty..")
            i = self._nFile.columns.values.tolist()
            if 'items' in i:
                items = self._nFile['items'].tolist()
            if 'Neighbours' in i:
                data = self._nFile['Neighbours'].tolist()
            for k in range(len(items)):
                self._mapItemNeighbours[items[k]] = data[k]

        if isinstance(self._nFile, str):
            if _ab._validators.url(self._nFile):
                data = _ab._urlopen(self._nFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = [i.rstrip() for i in line.split(self._sep)]
                    parts = [x for x in parts]
                    item = parts[0]
                    neigh1 = []
                    for i in range(1, len(parts)):
                        neigh1.append(parts[i])
                    self._mapItemNeighbours[item] = neigh1
            else:
                try:
                    with open(self._nFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = [i.rstrip() for i in line.split(self._sep)]
                            parts = [x for x in parts]
                            item = parts[0]
                            neigh1 = []
                            for i in range(1, len(parts)):
                                neigh1.append(parts[i])
                            self._mapItemNeighbours[item] = neigh1
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Frequent pattern mining process will start from here

        :return: None
        """
        self.mine()

    def mine(self) -> None:
        """
        Frequent pattern mining process will start from here

        :return: None
        """
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._finalPatterns = {}
        self._mapNeighbours()
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
        listOfFFList = []
        mapItemsToFFLIST = {}
        #self._minSup = self._convert(self._minSup)
        for item1 in self._mapItemSum.keys():
            item = item1
            if self._mapItemSum[item] >= self._minSup:
                fuList = _FFList(item)
                mapItemsToFFLIST[item] = fuList
                listOfFFList.append(fuList)
        listOfFFList.sort(key=_ab._functools.cmp_to_key(self._compareItems))
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
                    if self._mapItemNeighbours.get(pair.item[0]) is None:
                        continue
                    if revisedTransaction[j].item[0] in self._mapItemNeighbours[pair.item[0]]:
                        remainUtil += revisedTransaction[j].quantity
                remainingUtility = remainUtil
                if mapItemsToFFLIST.get(pair.item) is not None:
                    FFListOfItem = mapItemsToFFLIST[pair.item]
                    element = _Element(tid, pair.quantity, remainingUtility)
                    FFListOfItem.addElement(element)
            tid += 1
        itemNeighbours = list(self._mapItemNeighbours.keys())
        self._FSFIMining(self._itemSetBuffer, 0, listOfFFList, self._minSup, itemNeighbours)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def _FSFIMining(self, prefix: List, prefixLen: int, FSFIM: List, minSup: float, itemNeighbours: List):
        """
        Generates FFSPMiner from prefix

        :param prefix: the prefix patterns of FFSPMiner
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
        :param FSFIM: the Fuzzy list of prefix itemSets
        :type FSFIM: list
        :param minSup: the minimum support of
        :type minSup: int
        :param itemNeighbours: the set of common neighbours of prefix
        :type itemNeighbours: list or set
        """
        for i in range(0, len(FSFIM)):
            X = FSFIM[i]
            if X.sumIUtil >= minSup:
                self._WriteOut(prefix, prefixLen, X.item, X.sumIUtil)
            newNeighbours = self._Intersection(self._mapItemNeighbours.get(X.item[0]), itemNeighbours)
            if X.sumRUtil >= minSup:
                exULs = []
                for j in range(i + 1, len(FSFIM)):
                    Y = FSFIM[j]
                    if Y.item[0] in newNeighbours:
                        exULs.append(self._construct(X, Y))
                        self._joinsCnt += 1
                self._itemSetBuffer.insert(prefixLen, X.item)
                self._FSFIMining(self._itemSetBuffer, prefixLen + 1, exULs, minSup, newNeighbours)

    def _Intersection(self, neighbourX: List, neighbourY: List) -> List:
        """
        A function to get common neighbours from 2 itemSets

        :param neighbourX: the set of neighbours of itemSet 1
        :type neighbourX: set or list
        :param neighbourY: the set of neighbours of itemSet 2
        :type neighbourY: set or list
        :return: set of common neighbours of 2 itemSets
        :rtype: set
        """
        result = []
        if neighbourX is None or neighbourY is None:
            return result
        for i in range(0, len(neighbourX)):
            if neighbourX[i] in neighbourY:
                result.append(neighbourX[i])
        return result

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
        A function to construct a new Fuzzy itemSet from 2 fuzzy itemSets

        :param px: the itemSet px
        :type px: FFI-List
        :param py: itemSet py
        :type py: FFI-List
        :return: the itemSet of pxy(px and py)
        :rtype: FFI-List
        """
        pxyUL = _FFList(py.item)
        for ex in px.elements:
            ey = self._findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            eXY = _Element(ex.tid, min([ex.iUtils, ey.iUtils], key=lambda x: float(x)), ey.rUtils)
            pxyUL.addElement(eXY)
        return pxyUL

    def _findElementWithTID(self, uList: _FFList, tid: int) -> _Element:
        """
        To find element with same tid as given

        :param uList: fuzzyList
        :type uList: FFI-List
        :param tid: transaction id
        :type tid: int
        :return: element tid as given
        :rtype: element if exist or None
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

    def _WriteOut(self, prefix: List, prefixLen: int, item: int, sumIUtil: float) -> None:
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
            res += str(prefix[i]) + "\t"
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
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + " : " + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Spatial Fuzzy Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = FFSPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = FFSPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        print("Total number of Spatial Fuzzy Frequent  Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = FFSPMiner('sample.txt', 'nei.txt', 1, ' ')
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
