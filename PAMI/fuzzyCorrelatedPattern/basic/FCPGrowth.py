#  FCPGrowth is the algorithm to discover Correlated Fuzzy-frequent patterns in a transactional database.
#  it is based on traditional fuzzy frequent pattern mining.
#
# **Importing this algorithm into a python program**
# -------------------------------------------------------
#
#             from PAMI.fuzzyCorrelatedPattern.basic import FCPGrowth as alg
#
#             obj = alg.FCPGrowth("input.txt",2,0.4)
#
#             obj.mine()
#
#             correlatedFuzzyFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Correlated Fuzzy Frequent Patterns:", len(correlatedFuzzyFrequentPatterns))
#
#             obj.save("output")
#
#             memUSS = obj.getMemoryUSS()
#
#             print("Total Memory in USS:", memUSS)
#
#             memRSS = obj.getMemoryRSS()
#
#             print("Total Memory in RSS", memRSS)
#
#             run = obj.getRuntime
#
#             print("Total ExecutionTime in seconds:", run)
#





from PAMI.fuzzyCorrelatedPattern.basic import abstract as _ab
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

    def __init__(self, itemName: str, region: str) -> None:
        self.item = itemName
        self.region = region
        self.sumIUtil = 0.0
        self.sumRUtil = 0.0
        self.elements = []

    def addElement(self, element: 'Element') -> None:
        """
        A Method that add a new element to FFList

        :param element: an element to be added to FFList
        :param element: Element
        """

        self.sumIUtil += element.IUtils
        self.sumRUtil += element.RUtils
        self.elements.append(element)


class Element:
    """
    A class represents an Element of a fuzzy list

    :Attributes:

        tid : int
            keep tact of transaction id
        IUtils: float
            the utility of a fuzzy item in the transaction
        RUtil : float
            the neighbourhood resting value of a fuzzy item in the transaction
    """

    def __init__(self, tid: int, IUtil: float, RUtil: float) -> None:
        self.tid = tid
        self.IUtils = IUtil
        self.RUtils = RUtil


class _Regions:
    """
    A class calculate the region value

    :Attributes:

        low : int
            low region value
        middle: int
            middle region value
        high : int
            high region values
    """

    def __init__(self, item: str, quantity: int, regionsNumber: int, mapOfRegions: Dict) -> None:
        self.low = 0
        self.middle = 0
        self.high = 0
        if regionsNumber == 3:
            if 0 < quantity <= 1:
                self.low = 1
                self.high = 0
                self.middle = 0
                t1 = (item, 'L')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1
            elif 1 <= quantity < 6:
                self.low = float((-0.2 * quantity) + 1.2)
                self.middle = float((0.2 * quantity) - 0.2)
                self.high = 0
                t1 = (item, 'L')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1
                t1 = (item, 'M')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1
            elif 6 <= quantity <= 11:
                self.low = 0
                self.middle = float((-0.2 * quantity) + 2.2)
                self.high = float((0.2 * quantity) - 1.2)
                t1 = (item, 'M')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1
                t1 = (item, 'H')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1

            else:
                self.low = 0
                self.middle = 0
                self.high = 1
                t1 = (item, 'H')
                if t1 not in mapOfRegions.keys():
                    mapOfRegions[t1] = 1
                else:
                    temp = mapOfRegions[t1]
                    mapOfRegions[t1] = temp + 1


class _Pair:

    """
    A class to store item and it's quantity together
    """

    def __init__(self) -> None:
        """
        A Class to Store item and its quantity together
        """
        self.item = 0
        self.quantity = 0
        self.region = 'N'


class FCPGrowth(_ab._corelatedFuzzyFrequentPatterns):
    """
    :Description:   FCPGrowth is the algorithm to discover Correlated Fuzzy-frequent patterns in a transactional database.
                    it is based on traditional fuzzy frequent pattern mining.

    :Reference:   Lin, N.P., & Chueh, H. (2007). Fuzzy correlation rules mining.
                  https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.416.6053&rep=rep1&type=pdf

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param minAllConf: float :
                    The user can specify minAllConf values within the range (0, 1).

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of fuzzy spatial frequent patterns
        oFile : file
            Name of the oFile file to store complete set of fuzzy spatial frequent patterns
        minSup : int
            The user given support
        minAllConf: float
            user Specified minAllConf( should be in range 0 and 1)
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTimeTime:float
            To record the startTime time of the mining process
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

    :Methods:

        startTimeMine()
            Mining process will startTime from here
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
        getRatio(self, prefix, prefixLen, item)
            Method to calculate the ration of itemSet
        convert(value):
            To convert the given user specified value  
        FSFIMining( prefix, prefixLen, fsFim, minSup)
            Method generate FFI from prefix
        construct(px, py)
            A function to construct Fuzzy itemSet from 2 fuzzy itemSets
        findElementWithTID(uList, tid)
            To find element with same tid as given
        WriteOut(prefix, prefixLen, item, sumIUtil,ratio)
            To Store the patten      

    **Executing the code on terminal :**
    ------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 FCPGrowth.py <inputFile> <outputFile> <minSup> <minAllConf> <sep>

      Example Usage:

      (.venv) $ python3 FCPGrowth.py sampleTDB.txt output.txt 2 0.2

    .. note:: minSup will be considered in percentage of database transactions


    **Sample run of importing the code:**
    -----------------------------------------
    .. code-block:: python

            from PAMI.fuzzyCorrelatedPattern.basic import FCPGrowth as alg

            obj = alg.FCPGrowth("input.txt",2,0.4)

            obj.mine()

            correlatedFuzzyFrequentPatterns = obj.getPatterns()

            print("Total number of Correlated Fuzzy Frequent Patterns:", len(correlatedFuzzyFrequentPatterns))

            obj.save("output")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    -------------------

            The complete program was written by B.Sai Chitra under the supervision of Professor Rage Uday Kiran.

    """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _minAllConf = 0.0
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []

    def __init__(self, iFile: str, minSup: int, minAllConf: float, sep: str="\t") -> None:
        super().__init__(iFile, minSup, minAllConf, sep)
        self._temp = {}
        self._mapItemRegionSum = {}
        self._itemsCnt = 0
        self._mapItemsLowSum = {}
        self._mapItemsMidSum = {}
        self._mapItemsHighSum = {}
        self._mapItemSum = {}
        self._mapItemRegions = {}
        self._joinsCnt = 0
        self._BufferSize = 200
        self._itemSetBuffer = []
        self._finalPatterns = {}
        self._dbLen = 0
        self._transactions = []
        self._fuzzyValues = []

    def _compareItems(self, o1: _FFList, o2: _FFList) -> int:
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
            # return int(o1.item) - int(o2.item)
            return 1
        else:
            return compare

    def _findElementWithTID(self, uList: _FFList, tid: int) -> Element:
        """
        To find element with same tid as given

        :param uList: fuzzyList
        :type uList: FFI-List
        :param tid: transaction id
        :type tid: int
        :return: element eith tid as given
        :rtype: element if exists or None
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

    def _convert(self, value: Union[int, float, str]) -> float:
        """
        To convert the given user specified value

        :param value: user specified value

        :return: converted value

        :rtype: float
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._transactions) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._transactions) * value)
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
                self._transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValues = self._iFile['Utilities'].tolist()
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
                    self._fuzzyValues.append([x for x in quantities])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            items = parts[0].split()
                            quantities = parts[1].split()
                            self._transactions.append([x for x in items])
                            self._fuzzyValues.append([x for x in quantities])
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """ 
        Frequent pattern mining process will startTime from here
        """
        self.mine()


    def mine(self) -> None:
        """
        Frequent pattern mining process will startTime from here
        """
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        for tr in range(len(self._transactions)):
            items = self._transactions[tr]
            quantities = self._fuzzyValues[tr]
            for i in range(0, len(items)):
                item = items[i]
                regions = _Regions(item, float(quantities[i]), 3, self._mapItemRegionSum)
                if item in self._mapItemsLowSum.keys():
                    low = self._mapItemsLowSum[item]
                    low += regions.low
                    self._mapItemsLowSum[item] = low
                else:
                    self._mapItemsLowSum[item] = regions.low
                if item in self._mapItemsMidSum.keys():
                    mid = self._mapItemsMidSum[item]
                    mid += regions.middle
                    self._mapItemsMidSum[item] = mid
                else:
                    self._mapItemsMidSum[item] = regions.middle
                if item in self._mapItemsHighSum.keys():
                    high = self._mapItemsHighSum[item]
                    high += regions.high
                    self._mapItemsHighSum[item] = high
                else:
                    self._mapItemsHighSum[item] = regions.high
        listOfFFIList = []
        mapItemsToFFLIST = {}
        self._minSup = self._convert(self._minSup)
        #minSup = self._minSup
        self._minAllConf = float(self._minAllConf)
        for item1 in self._mapItemsLowSum.keys():
            item = item1
            region = 'N'
            low = self._mapItemsLowSum[item]
            mid = self._mapItemsMidSum[item]
            high = self._mapItemsHighSum[item]
            if low >= mid and low >= high:
                self._mapItemSum[item] = low
                self._mapItemRegions[item] = "L"
                region = 'L'
            elif mid >= low and mid >= high:
                self._mapItemSum[item] = mid
                self._mapItemRegions[item] = "M"
                region = 'M'
            elif high >= low and high >= mid:
                self._mapItemRegions[item] = "H"
                region = 'H'
                self._mapItemSum[item] = high
            if self._mapItemSum[item] >= self._minSup:
                fuList = _FFList(item, region)
                mapItemsToFFLIST[item] = fuList
                listOfFFIList.append(fuList)
        listOfFFIList.sort(key=_ab._functools.cmp_to_key(self._compareItems))
        tid = 0
        for tr in range(len(self._transactions)):
            items = self._transactions[tr]
            quantities = self._fuzzyValues[tr]
            revisedTransaction = []
            for i in range(0, len(items)):
                pair = _Pair()
                pair.item = items[i]
                regions = _Regions(pair.item, float(quantities[i]), 3, self._temp)
                item = pair.item
                if self._mapItemSum[item] >= self._minSup:
                    if self._mapItemRegions[pair.item] == "L":
                        pair.quantity = regions.low
                        pair.region = 'L'
                    elif self._mapItemRegions[pair.item] == "M":
                        pair.region = 'M'
                        pair.quantity = regions.middle
                    elif self._mapItemRegions[pair.item] == "H":
                        pair.quantity = regions.high
                        pair.region = 'H'
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
                if mapItemsToFFLIST.get(pair.item) is not None:
                    FFListOfItem = mapItemsToFFLIST[pair.item]
                    element = Element(tid, pair.quantity, remainingUtility)
                    FFListOfItem.addElement(element)
            tid += 1
        self._FSFIMining(self._itemSetBuffer, 0, listOfFFIList, self._minSup)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Fuzzy Correlated Patterns Successfully generated using FCPGrowth algorithms")

    def _FSFIMining(self, prefix: List[_FFList], prefixLen: int, FSFIM: List[_FFList], minSup: float) -> None:
        """
        Generates FFSI from prefix

        :param prefix: the prefix patterns of FFSI
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
        :param FSFIM: the Fuzzy list of prefix itemSets
        :type FSFIM: list
        :param minSup: the minimum support of
        :type minSup:int
        """
        for i in range(0, len(FSFIM)):
            X = FSFIM[i]
            if X.sumIUtil >= minSup:
                ratio = self._getRatio(prefix, prefixLen, X)
                if ratio >= self._minAllConf:
                    self._WriteOut(prefix, prefixLen, X, ratio)
            if X.sumRUtil >= minSup:
                exULs = []
                for j in range(i + 1, len(FSFIM)):
                    Y = FSFIM[j]
                    exULs.append(self._construct(X, Y))
                    self._joinsCnt += 1
                self._itemSetBuffer.insert(prefixLen, X)
                self._FSFIMining(self._itemSetBuffer, prefixLen + 1, exULs, minSup)

    def _construct(self, px: _FFList, py: _FFList) -> _FFList:
        """
        A function to construct a new Fuzzy itemSet from 2 fuzzy itemSets

        :param px:the itemSet px
        :type px:FFI-List
        :param py:itemSet py
        :type py:FFI-List
        :return :the itemSet of pxy(px and py)
        :rtype :FFI-List
        """
        pxyUL = _FFList(py.item, py.region)
        for ex in px.elements:
            ey = self._findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            eXY = Element(ex.tid, min([ex.IUtils, ey.IUtils], key=lambda x: float(x)), ey.RUtils)
            pxyUL.addElement(eXY)
        return pxyUL

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

    def _getRatio(self, prefix: List[_FFList], prefixLen: int, item: _FFList) -> float:
        """
        Method to calculate the ration of itemSet

        :param prefix: prefix of itemSet
        :type prefix: list
        :param prefixLen: length of prefix
        :type prefixLen: int
        :param item: the last item
        :type item: FFList
        :return : correlated ratio
        :rtype: float
        """
        res = 1.0
        #n = prefixLen
        for i in prefix:
            if self._mapItemRegionSum.get((i.item, i.region)) is not None and res < self._mapItemRegionSum[(i.item, i.region)]:
                res = self._mapItemRegionSum[(i.item, i.region)]
        if self._mapItemRegionSum.get((item.item, item.region)) is not None and res < self._mapItemRegionSum[
            (item.item, item.region)]:
            res = self._mapItemRegionSum[(item.item, item.region)]
        return item.sumIUtil / res

    def _WriteOut(self, prefix: List[_FFList], prefixLen: int, item: _FFList, ratio: float) -> None:
        """
        To Store the patten

        :param prefix: prefix of itemSet
        :type prefix: list
        :param prefixLen: length of prefix
        :type prefixLen: int
        :param item: the last item
        :type item: FFList
        :param ratio: the ratio of itemSet
        :type ratio: float
        :return: None
        """
        self._itemsCnt += 1
        res = ""
        for i in range(0, prefixLen):
            res += str(prefix[i].item) + "." + str(prefix[i].region) + '\t'
        res += str(item.item) + "." + str(item.region)
        #res1 = str(item.sumIUtil) + " : " + str(ratio) + "\n"
        self._finalPatterns[res] = [item.sumIUtil, ratio]

    def getPatterns(self) -> Dict[str, List[float]]:
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """
        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1]])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Confidence'])
        return dataframe

    def save(self, outFile: str) -> None:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % patternsAndSupport)

    def printResults(self) -> None:
        """
        This function is used to print the result
        """
        print("Total number of Fuzzy Correlated Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())

def main():
    inputFile = 'https://u-aizu.ac.jp/~udayrage/datasets/fuzzyDatabases/Fuzzy_T10I4D100K.csv'

    minimumSupportCount=1200  #Users can also specify this constraint between 0 to 1.
    ratioExample=0.8
    seperator='\t' 

    obj = FCPGrowth(inputFile, minimumSupportCount,ratioExample,seperator)    #initialize
    obj.mine()


if __name__ == "__main__":
    main()
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = FCPGrowth(_ab._sys.argv[1], int(_ab._sys.argv[3]), float(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = FCPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]))
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy Correlated Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:",  _ap.getMemoryUSS())
        print("Total Memory in RSS",  _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
