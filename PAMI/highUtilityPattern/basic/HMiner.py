#  High Utility itemSet Mining (HMinER) is an important algorithm to miner High utility items from the database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilityPattern.basic import HMiner as alg
#
#             obj = alg.HMiner("input.txt", 35)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of high utility Patterns:", len(Patterns))
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

from PAMI.highUtilityPattern.basic import abstract as _ab
from deprecated import deprecated


class _Element:
    """
    A class represents an Element of a utility list.

    :Attributes :

        ts : int
            keep tact of transaction id
        nu : int
            non-closed itemSet utility
        nru : int
             non-closed remaining utility
        pu : int
            prefix utility
        ppos: int
            position of previous item in the list
    """

    def __init__(self, tid, nu, nru, pu, ppos):
        self.tid = tid
        self.nu = nu
        self.nru = nru
        self.pu = pu
        self.ppos = ppos


class _CUList:
    """
    A class represents a UtilityList

    :Attributes :

        item: int
            item 
        sumNu: long
            the sum of item utilities
        sumNru: long
            the sum of remaining utilities
        sumCu : long
            the sum of closed utilities
        sumCru: long
            the sum of closed remaining utilities
        sumCpu: long
            the sum of closed prefix utilities
        elements: list
            the list of elements 
    :Methods :

        addElement(element)
            Method to add an element to this utility list and update the sums at the same time.
    """

    def __init__(self, item):
        self.item = item
        self.sumnu = 0
        self.sumnru = 0
        self.sumCu = 0
        self.sumCru = 0
        self.sumCpu = 0
        self.elements = []

    def addElements(self, element):
        """
        A method to add new element to CUList
        :param element: element to be added to CUList
        :type element: Element
        """
        self.sumnu += element.nu
        self.sumnru += element.nru
        self.elements.append(element)


class _Pair:
    """
    A class represent an item and its utility in a transaction
    """

    def __init__(self):
        self.item = 0
        self.utility = 0


class HMiner(_ab._utilityPatterns):
    """
    :Description:   High Utility itemSet Mining (HMIER) is an importent algorithm to miner High utility items from the database.

    :Reference:


    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility patterns
    :param minUtil: int :
                   The user given minUtil value.
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of frequent patterns
        oFile : file
            Name of the output file to store complete set of frequent patterns
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        minUtil : int
            The user given minUtil
        mapFMAP: list
            EUCS map of the FHM algorithm
        candidates: int
            candidates genetated
        huiCnt: int
            huis created
        neighbors: map
            keep track of nighboues of elements

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
        Explore_SearchTree(prefix, uList, minUtil)
            A method to find all high utility itemSets
        UpdateCLosed(x, culs, st, excul, newT, ex, ey_ts, length)
            A method to update closed values
        saveitemSet(prefix, prefixLen, item, utility)
            A method to save itemSets
        updateElement(z, culs, st, excul, newT, ex, duppos, ey_ts)
            A method to updates vales for duplicates
        construcCUL(x, culs, st, minUtil, length, exnighbors)
            A method to construct CUL's database

    **Executing the code on terminal:**
    --------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 HMiner.py <inputFile> <outputFile> <minUtil>

      Example Usage:

      (.venv) $ python3 HMiner.py sampleTDB.txt output.txt 35

    .. note:: minSup will be considered in percentage of database transactions


    Sample run of importing the code:
    --------------------------------------
    .. code-block:: python

            from PAMI.highUtilityPattern.basic import HMiner as alg
        
            obj = alg.HMiner("input.txt",35)
        
            obj.mine()
        
            Patterns = obj.getPatterns()
        
            print("Total number of high utility Patterns:", len(Patterns))
        
            obj.save("output")
        
            memUSS = obj.getMemoryUSS()
        
            print("Total Memory in USS:", memUSS)
        
            memRSS = obj.getMemoryRSS()
        
            print("Total Memory in RSS", memRSS)
        
            run = obj.getRuntime()
        
            print("Total ExecutionTime in seconds:", run)
    
    **Credits:**
    -----------------------------
            The complete program was written by B.Sai Chitra under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _Database = {}
    _transactions = []
    _utilities = []
    _utilitySum = []
    _iFile = " "
    _oFile = " "
    _minUtil = 0
    _sep = "\t"
    _memoryUSS = float()
    _memoryRSS = float()

    def __init__(self, iFile1, minUtil, sep="\t"):
        super().__init__(iFile1, minUtil, sep)
        self.oFile = None
        self._huiCount = 0
        self._candidates = 0
        self._mapOfTWU = {}
        self._minutil = 0
        self._mapFMAP = {}
        self._finalPatterns = {}

    def _HMiner(self, o1, o2) -> int:
        """
        A Function that sort all FFI-list in ascending order of Support

        :param o1: First FFI-list

        :type o1: _FFList

        :param o2: Second FFI-list

        :type o1: _FFList

        :return: Comparision Value

        :rtype: int
        """
        compare = self._mapOfTWU[o1.item] - self._mapOfTWU[o2.item]
        if compare == 0:
            return int(o1.item) - int(o2.item)
        else:
            return compare

    def _creteItemsets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._transactions, self._utilities, self._utilitySum = [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._transactions = self._iFile['Transactions'].tolist()
            if 'Utilities' in i:
                self._utilities = self._iFile['Utilities'].tolist()
            if 'UtilitySum' in i:
                self._utilitySum = self._iFile['UtilitySum'].tolist()
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                #print("hey")
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    items = parts[0].split(self._sep)
                    self._transactions.append([x for x in items if x])
                    utilities = parts[2].split(self._sep)
                    self._utilities.append(utilities)
                    self._utilitySum.append(int(parts[1]))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            items = parts[0].split(self._sep)
                            self._transactions.append([x for x in items if x])
                            utilities = parts[2].split(self._sep)
                            self._utilities.append(utilities)
                            self._utilitySum.append(int(parts[1]))
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Main program to start the operation
        """
        self.mine()

    def mine(self):
        """
        Main program to start the operation
        """
        self._startTime = _ab._time.time()
        self._creteItemsets()
        self._finalPatterns = {}
        for line in range(len(self._transactions)):
            items_str = self._transactions[line]
            utility_str = self._utilities[line]
            transUtility = self._utilitySum[line]
            for i in range(0, len(items_str)):
                item = items_str[i]
                twu = self._mapOfTWU.get(item)
                if twu is None:
                    twu = transUtility
                else:
                    twu += transUtility
                self._mapOfTWU[item] = twu
        listOfCUList = []
        hashTable = {}
        mapItemsToCUList = {}
        minutil = self._minUtil
        for item in self._mapOfTWU.keys():
            if self._mapOfTWU.get(item) >= self._minUtil:
                uList = _CUList(item)
                mapItemsToCUList[item] = uList
                listOfCUList.append(uList)
        listOfCUList.sort(key=_ab._functools.cmp_to_key(self._HMiner))
        tid = 1
        for line in range(len(self._transactions)):
            items = self._transactions[line]
            utilities = self._utilities[line]
            ru = 0
            newTwu = 0
            tx_key = []
            revisedTrans = []
            for i in range(0, len(items)):
                pair = _Pair()
                pair.item = items[i]
                pair.utility = int(utilities[i])
                if self._mapOfTWU.get(pair.item) >= self._minUtil:
                    revisedTrans.append(pair)
                    tx_key.append(pair.item)
                    newTwu += pair.utility
            revisedTrans.sort(key=_ab._functools.cmp_to_key(self._HMiner))
            tx_key1 = tuple(tx_key)
            if len(revisedTrans) > 0:
                if tx_key1 not in hashTable.keys():
                    hashTable[tx_key1] = len(mapItemsToCUList[revisedTrans[len(revisedTrans) - 1].item].elements)
                    for i in range(len(revisedTrans) - 1, -1, -1):
                        pair = revisedTrans[i]
                        cuListoFItems = mapItemsToCUList.get(pair.item)
                        element = _Element(tid, pair.utility, ru, 0, 0)
                        if i > 0:
                            element.ppos = len(mapItemsToCUList[revisedTrans[i - 1].item].elements)
                        else:
                            element.ppos = - 1
                        cuListoFItems.addElements(element)
                        ru += pair.utility
                else:
                    pos = hashTable[tx_key1]
                    ru = 0
                    for i in range(len(revisedTrans) - 1, -1, -1):
                        cuListoFItems = mapItemsToCUList[revisedTrans[i].item]
                        cuListoFItems.elements[pos].nu += revisedTrans[i].utility
                        cuListoFItems.elements[pos].nru += ru
                        cuListoFItems.sumnu += revisedTrans[i].utility
                        cuListoFItems.sumnru += ru
                        ru += revisedTrans[i].utility
                        pos = cuListoFItems.elements[pos].ppos
                    # EUCS
            for i in range(len(revisedTrans) - 1, -1, -1):
                pair = revisedTrans[i]
                mapFMAPItem = self._mapFMAP.get(pair.item)
                if mapFMAPItem is None:
                    mapFMAPItem = {}
                    self._mapFMAP[pair.item] = mapFMAPItem
                for j in range(i + 1, len(revisedTrans)):
                    pairAfter = revisedTrans[j]
                    twuSUm = mapFMAPItem.get(pairAfter.item)
                    if twuSUm is None:
                        mapFMAPItem[pairAfter.item] = newTwu
                    else:
                        mapFMAPItem[pairAfter.item] = twuSUm + newTwu
            tid += 1
        self._ExploreSearchTree([], listOfCUList, minutil)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("High Utility patterns were generated successfully using HMiner algorithm")

    def _ExploreSearchTree(self, prefix, uList, minutil):
        """
        A method to find all high utility itemSets
        :parm prefix:it represents all items in prefix
        :type prefix:list
        :parm uList:projected Utility list
        :type uList: lists
        :parm minutil:user minUtil
        :type minutil:int
        """
        for i in range(0, len(uList)):
            x = uList[i]
            soted_prefix = [0] * (len(prefix) + 1)
            soted_prefix = prefix[0:len(prefix) + 1]
            soted_prefix.append(x.item)
            if x.sumnu + x.sumCu >= minutil:
                self._saveitemSet(prefix, len(prefix), x.item, x.sumnu + x.sumCu)
            self._candidates += 1
            if x.sumnu + x.sumCu + x.sumnru + x.sumCru >= minutil:
                exULs = self._construcCUL(x, uList, i, minutil, len(soted_prefix))
                self._ExploreSearchTree(soted_prefix, exULs, minutil)

    def _construcCUL(self, x, culs, st, minutil, length):
        """
        A method to construct CUL's database
        :parm x: Compact utility list
        :type x: Node
        :parm culs:list of Compact utility list
        :type culs:lists
        :parm st: starting pos of culs
        :type st:int
        :parm minutil: user minUtil
        :type minutil:int
        :parm length: length of x
        :type length:int
        :return: projectd database of list X
        :rtype: list
        """
        excul = []
        lau = []
        cutil = []
        ey_tid = []
        for i in range(0, len(culs)):
            uList = _CUList(culs[i].item)
            excul.append(uList)
            lau.append(0)
            cutil.append(0)
            ey_tid.append(0)
        sz = len(culs) - (st + 1)
        exSZ = sz
        for j in range(st + 1, len(culs)):
            mapOfTWUF = self._mapFMAP[x.item]
            if mapOfTWUF is not None:
                twuf = mapOfTWUF.get(culs[j].item)
                if twuf is not None and twuf < minutil:
                    excul[j] = None
                    exSZ = sz - 1
                else:
                    uList = _CUList(culs[j].item)
                    excul[j] = uList
                    ey_tid[j] = 0
                    lau[j] = x.sumCu + x.sumCru + x.sumnu + x.sumnru
                    cutil[j] = x.sumCu + x.sumCru
        hashTable = {}
        for ex in x.elements:
            newT = []
            for j in range(st + 1, len(culs)):
                if excul[j] is None:
                    continue
                eylist = culs[j].elements
                while ey_tid[j] < len(eylist) and eylist[ey_tid[j]].tid < ex.tid:
                    ey_tid[j] = ey_tid[j] + 1
                if ey_tid[j] < len(eylist) and eylist[ey_tid[j]].tid == ex.tid:
                    newT.append(j)
                else:
                    lau[j] = lau[j] - ex.nu - ex.nru
                    if lau[j] < minutil:
                        excul[j] = None
                        exSZ = exSZ - 1
            if len(newT) == exSZ:
                self._UpdateCLosed(x, culs, st, excul, newT, ex, ey_tid, length)
            else:
                if len(newT) == 0:
                    continue
                ru = 0
                newT1 = tuple(newT)
                if newT1 not in hashTable.keys():
                    hashTable[newT1] = len(excul[newT[len(newT) - 1]].elements)
                    for i in range(len(newT) - 1, -1, -1):
                        cuListoFItems = excul[newT[i]]
                        y = culs[newT[i]].elements[ey_tid[newT[i]]]
                        element = _Element(ex.tid, ex.nu + y.nu - ex.pu, ru, ex.nu, 0)
                        if i > 0:
                            element.ppos = len(excul[newT[i - 1]].elements)
                        else:
                            element.ppos = - 1
                        cuListoFItems.addElements(element)
                        ru += y.nu - ex.pu
                else:
                    dppos = hashTable[newT1]
                    self._updateElement(x, culs, st, excul, newT, ex, dppos, ey_tid)
            for j in range(st + 1, len(culs)):
                cutil[j] = cutil[j] + ex.nu + ex.nru
        filter_culs = []
        for j in range(st + 1, len(culs)):
            if cutil[j] < minutil or excul[j] is None:
                continue
            else:
                if length > 1:
                    excul[j].sumCu += culs[j].sumCu + x.sumCu - x.sumCpu
                    excul[j].sumCru += culs[j].sumCru
                    excul[j].sumCpu += x.sumCu
                filter_culs.append(excul[j])
        return filter_culs

    def _UpdateCLosed(self, x, culs, st, excul, newT, ex, ey_tid, length):
        """
        A method to update closed values
        :parm x: Compact utility list
        :type x: lists
        :parm culs:list of Compact utility list
        :type culs:lists
        :parm st: starting pos of culs
        :type st:int
        :parm excul: list of culs
        :type excul: list
        :parm newT:transaction to be updated
        :type newT:list
        :parm ex: element ex
        :type ex:element
        :parm ey_tid:list of tss
        :type ey_tid:ts
        :parm length: length of x
        :type length:int
        """
        nru = 0
        for j in range(len(newT) - 1, -1, -1):
            ey = culs[newT[j]]
            eyy = ey.elements[ey_tid[newT[j]]]
            excul[newT[j]].sumCu += ex.nu + eyy.nu - ex.pu
            excul[newT[j]].sumCru += nru
            excul[newT[j]].sumCpu += ex.nu
            nru = nru + eyy.nu - ex.pu

    def _updateElement(self, z, culs, st, excul, newT, ex, duppos, ey_tid):
        """
        A method to updates vales for duplicates

        :Attributes:

        :parm z: Compact utility list
        :type z: lists
        :parm culs:list of Compact utility list
        :type culs:lists
        :parm st: starting pos of culs
        :type st:int
        :parm excul:list of culs
        :type excul:list
        :parm newT:transaction to be updated
        :type newT:list
        :parm ex: element ex
        :type ex:element
        :parm duppos: position of z in excul
        :type duppos:int
        :parm ey_tid:list of tss
        :type ey_tid:ts
        """
        nru = 0
        pos = duppos
        for j in range(len(newT) - 1, -1, -1):
            ey = culs[newT[j]]
            eyy = ey.elements[ey_tid[newT[j]]]
            excul[newT[j]].elements[pos].nu += ex.nu + eyy.nu - ex.pu
            excul[newT[j]].sumnu += ex.nu + eyy.nu - ex.pu
            excul[newT[j]].elements[pos].nru += nru
            excul[newT[j]].sumnru += nru
            excul[newT[j]].elements[pos].pu += ex.nu
            nru = nru + eyy.nu - ex.pu
            pos = excul[newT[j]].elements[pos].ppos

    def _saveitemSet(self, prefix, prefixLen, item, utility):
        """
        A method to save itemSets
        :parm prefix: it represents all items in prefix
        :type prefix :list
        :parm prefixLen: length of prefix
        :type prefixLen:int
        :parm item:item
        :type item: int
        :parm utility:utility of itemSet
        :type utility:int
        """
        self._huiCount += 1
        res = str()
        for i in range(0, prefixLen):
            res += str(prefix[i]) + "\t"
        res += str(item)
        self._finalPatterns[str(res)] = str(utility)

    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe
        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Utility'])
        return dataFrame

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s\n" % patternsAndSupport)

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
       """
        return self._memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self._endTime - self._startTime
    
    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:  # includes separator
            _ap = HMiner(_ab._sys.argv[1], int(_ab._sys.argv[3]), _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:  # to consider "\t" as a separator
            _ap = HMiner(_ab._sys.argv[1], int(_ab._sys.argv[3]))
        _ap.mine()
        _ap.mine()
        print("Total number of huis:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS",  _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

