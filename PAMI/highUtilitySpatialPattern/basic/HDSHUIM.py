# Spatial High Utility ItemSet Mining (SHUIM) [3] is an important model in data
# mining with many real-world applications. It involves finding all spatially interesting itemSets having high value
# in a quantitative spatio-temporal database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilitySpatialPattern.basic import HDSHUIM as alg
#
#             obj=alg.HDSHUIM("input.txt","Neighbours.txt",35)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of Spatial High-Utility Patterns:", len(Patterns))
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

from PAMI.highUtilitySpatialPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated

class _Element:
    """
    A class represents an Element of a utility list as used by the HDSHUIM algorithm.

    :Attributes:

        ts : int
            keep tact of transaction id
        snu : int
            Spatial non-closed itemSet utility
        remainingUtility : int
            Spatial non-closed remaining utility
        pu : int
            prefix utility
        prevPos: int
            position of previous item in the list
    """

    def __init__(self, ts: int, snu: int, remainingUtility: int, pu: int, prevPos: int) -> None:
        self.ts = ts
        self.snu = snu
        self.remainingUtility = remainingUtility
        self.pu = pu
        self.prevPos = prevPos


class _CUList:
    """
        A class represents a UtilityList as used by the HDSHUIM algorithm.

    :Attributes:

        item: int
            item 
        sumSnu: long
            the sum of item utilities
        sumRemainingUtility: long
            the sum of remaining utilities
        sumCu : long
            the sum of closed utilities
        sumCru: long
            the sum of closed remaining utilities
        sumCpu: long
            the sum of closed prefix utilities
        elements: list
            the list of elements 

    :Methods:

        addElement(element)
            Method to add an element to this utility list and update the sums at the same time.

    """

    def __init__(self, item: str) -> None:
        self.item = item
        self.sumSnu = 0
        self.sumRemainingUtility = 0
        self.sumCu = 0
        self.sumCru = 0
        self.sumCpu = 0
        self.elements = []

    def addElements(self, element: _Element) -> None:
        """
        A method to add new element to CUList

        :param element: element to be added to CUList
        :type element: Element
        :return: None
        """
        self.sumSnu += element.snu
        self.sumRemainingUtility += element.remainingUtility
        self.elements.append(element)


class _Pair:
    """
    A class represent an item and its utility in a transaction
    """

    def __init__(self) -> None:
        self.item = 0
        self.utility = 0


class HDSHUIM(_ab._utilityPatterns):
    """
    :Description:

        Spatial High Utility ItemSet Mining (SHUIM) [3] is an important model in data
        mining with many real-world applications. It involves finding all spatially interesting itemSets having high value 
        in a quantitative spatio temporal database.

    :Reference:

        P. Pallikila et al., "Discovering Top-k Spatial High Utility Itemsets in Very Large Quantitative Spatiotemporal 
        databases," 2021 IEEE International Conference on Big Data (Big Data), Orlando, FL, USA, 2021, pp. 4925-4935,
        doi: 10.1109/BigData52589.2021.9671912.

    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility Spatial patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility Spatial patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param minUtil: int :
                   Minimum utility threshold given by User
    :param nFile: str :
                   Name of the input file to mine complete set of High Utility Spatial patterns
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : str
            Name of the input file to mine complete set of frequent patterns
        oFile : str
            Name of the output file to store complete set of frequent patterns
        nFile: str
           Name of Neighbourhood items file
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
            candidates generated
        huiCnt: int
            huis created
        neighbors: map
            keep track of neighbours of elements
        mapOfPMU: map
            a map to keep track of Probable Maximum utility(PMU) of each item
    :Methods:

            mine()
                Mining process will start from here
            getPatterns()
                Complete set of patterns will be retrieved with this function
            save(oFile)
                Complete set of frequent patterns will be loaded in to a output file
            constructCUL(x, compactUList, st, minUtil, length, exNeighbours)
                A method to construct CUL's database
            getPatternsAsDataFrame()
                Complete set of frequent patterns will be loaded in to a dataframe
            getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
            getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
            getRuntime()
                Total amount of runtime taken by the mining process will be retrieved from this function
            Explore_SearchTree(prefix, uList, exNeighbours, minUtil)
                A method to find all high utility itemSets
            updateClosed(x, compactUList, st, exCul, newT, ex, eyTs, length)
                A method to update closed values
            saveItemSet(prefix, prefixLen, item, utility)
               A method to save itemSets
            updateElement(z, compactUList, st, exCul, newT, ex, duPrevPos, eyTs)
               A method to updates vales for duplicates


    **Executing the code on terminal:**
    -------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 HDSHUIM.py <inputFile> <outputFile> <Neighbours> <minUtil> <separator>

      Example Usage:

      (.venv) $ python3 HDSHUIM.py sampleTDB.txt output.txt sampleN.txt 35 ','

    .. note:: minSup will be considered in percentage of database transactions


    **Sample run of importing the code:**
    ---------------------------------------
    .. code-block:: python
        
            from PAMI.highUtilityGeoreferencedFrequentPattern.basic import HDSHUIM as alg

            obj=alg.HDSHUIM("input.txt","Neighbours.txt",35)

            obj.mine()

            Patterns = obj.getPatterns()

            print("Total number of Spatial High-Utility Patterns:", len(Patterns))

            obj.save("output")

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
    _nFile = " "
    _minUtil = 0
    _memoryUSS = float()
    _memoryRSS = float()
    _sep = "\t"

    def __init__(self, iFile: str, nFile: str, minUtil: int, sep: str="\t") -> None:
        super().__init__(iFile, nFile, minUtil, sep)
        self.oFile = None
        self._startTime = 0
        self._endTime = 0
        self._huiCount = 0
        self._candidates = 0
        self._mapOfPMU = {}
        self._mapFMAP = {}
        self._neighbors = {}
        self._finalPatterns = {}

    def _compareItems(self, o1: Any, o2: Any) -> int:
        """
        A Function that sort all FFI-list in ascending order of Support

        :param o1: First FFI-list

        :type o1: _FFList

        :param o2: Second FFI-list

        :type o1: _FFList

        :return: Comparision Value

        :rtype: int
        """
        compare = self._mapOfPMU[o1.item] - self._mapOfPMU[o2.item]
        if compare == 0:
            return int(o1.item) - int(o2.item)
        else:
            return compare

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        main program to start the operation
        """
        self.mine()



    def mine(self) -> None:
        """
        main program to start the operation
        """
        minUtil = self._minUtil
        self._startTime = _ab._time.time()
        with open(self._nFile, 'r') as file1:
            for line in file1:
                line = line.split("\n")[0]
                parts = line.split(self._sep)
                parts = [i_.strip() for i_ in parts]
                item = parts[0]
                neigh1 = list()
                for j in range(1, len(parts)):
                    neigh1.append(parts[j])
                self._neighbors[item] = set(neigh1)
        with open(self._iFile, 'r') as file:
            for line in file:
                parts = line.split(":")
                itemString = (parts[0].split("\n")[0]).split(self._sep)
                utilityString = (parts[2].split("\n")[0]).split(self._sep)
                transUtility = int(parts[1])
                trans1 = set()
                for j in range(0, len(itemString)):
                    trans1.add(itemString[j])
                for j in range(0, len(itemString)):
                    item = itemString[j]
                    twu = self._mapOfPMU.get(item)
                    if twu is None:
                        twu = int(utilityString[j])
                    else:
                        twu += int(utilityString[j])
                    self._mapOfPMU[item] = twu
                    if self._neighbors.get(item) is None:
                        continue
                    neighbours2 = trans1.intersection(self._neighbors.get(item))
                    for item2 in neighbours2:
                        if self._mapOfPMU.get(item2) is None:
                            self._mapOfPMU[item2] = int(utilityString[j])
                        else:
                            self._mapOfPMU[item2] += int(utilityString[j])

        listOfCUList = []
        hashTable = {}
        mapItemsToCUList = {}
        for item in self._mapOfPMU.keys():
            if self._mapOfPMU.get(item) >= minUtil:
                uList = _CUList(item)
                mapItemsToCUList[item] = uList
                listOfCUList.append(uList)
        listOfCUList.sort(key=_ab._functools.cmp_to_key(self._compareItems))
        ts = 1
        with open(self._iFile, 'r') as file:
            for line in file:
                parts = line.split(":")
                items = (parts[0].split("\n")[0]).split(self._sep)
                utilities = (parts[2].split("\n")[0]).split(self._sep)
                ru = 0
                newTwu = 0
                txKey = []
                revisedTrans = []
                for j in range(0, len(items)):
                    pair = _Pair()
                    pair.item = items[j]
                    pair.utility = int(utilities[j])
                    if self._mapOfPMU.get(pair.item) >= minUtil:
                        revisedTrans.append(pair)
                        txKey.append(pair.item)
                        newTwu += pair.utility
                revisedTrans.sort(key=_ab._functools.cmp_to_key(self._compareItems))
                txKey1 = tuple(txKey)
                if len(revisedTrans) > 0:
                    if txKey1 not in hashTable.keys():
                        hashTable[txKey1] = len(mapItemsToCUList[revisedTrans[len(revisedTrans) - 1].item].elements)
                        for j in range(len(revisedTrans) - 1, -1, -1):
                            pair = revisedTrans[j]
                            cuListOfItems = mapItemsToCUList.get(pair.item)
                            element = _Element(ts, pair.utility, ru, 0, 0)
                            if j > 0:
                                element.prevPos = len(mapItemsToCUList[revisedTrans[j - 1].item].elements)
                            else:
                                element.prevPos = -1
                            cuListOfItems.addElements(element)
                            ru += pair.utility
                    else:
                        pos = hashTable[txKey1]
                        ru = 0
                        for j in range(len(revisedTrans) - 1, -1, -1):
                            cuListOfItems = mapItemsToCUList[revisedTrans[j].item]
                            cuListOfItems.elements[pos].snu += revisedTrans[j].utility
                            cuListOfItems.elements[pos].remainingUtility += ru
                            cuListOfItems.sumSnu += revisedTrans[j].utility
                            cuListOfItems.sumRemainingUtility += ru
                            ru += revisedTrans[j].utility
                            pos = cuListOfItems.elements[pos].prevPos
                # EUCS
                for j in range(len(revisedTrans) - 1, -1, -1):
                    pair = revisedTrans[j]
                    mapFMAPItem = self._mapFMAP.get(pair.item)
                    if mapFMAPItem is None:
                        mapFMAPItem = {}
                        self._mapFMAP[pair.item] = mapFMAPItem
                    for j in range(j + 1, len(revisedTrans)):
                        pairAfter = revisedTrans[j]
                        twuSUm = mapFMAPItem.get(pairAfter.item)
                        if twuSUm is None:
                            mapFMAPItem[pairAfter.item] = newTwu
                        else:
                            mapFMAPItem[pairAfter.item] = twuSUm + newTwu
                ts += 1
        exNeighbours = set(self._mapOfPMU.keys())
        # print(self.Neighbours)
        self._ExploreSearchTree([], listOfCUList, exNeighbours, minUtil)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def _ExploreSearchTree(self, prefix: List[str], uList: List[_CUList], exNeighbours: set, minUtil: int) -> None:
        """
        A method to find all high utility itemSets
        :parm prefix: it represents all items in prefix
        :type prefix :list
        :parm uList:projected Utility list.
        :type uList: list
        :parm exNeighbours: keep track of common Neighbours
        :type exNeighbours: set
        :parm minUtil:user minUtil
        :type minUtil:int
        :return: None
        """
        for k in range(0, len(uList)):
            x = uList[k]
            if x.item not in exNeighbours:
                continue
            self._candidates += 1
            sortedPrefix = [0] * (len(prefix) + 1)
            sortedPrefix = prefix[0:len(prefix) + 1]
            sortedPrefix.append(x.item)
            if (x.sumSnu + x.sumCu >= minUtil) and (x.item in exNeighbours):
                self._saveItemSet(prefix, len(prefix), x.item, x.sumSnu + x.sumCu)
            if x.sumSnu + x.sumCu + x.sumRemainingUtility + x.sumCru >= minUtil:  # U-Prune # and (x.item in exNeighbours)):
                ULIST = []
                for j in range(k, len(uList)):
                    if (uList[j].item in exNeighbours) and (self._neighbors.get(x.item) is not None) and (
                            uList[j].item in self._neighbors.get(x.item)):
                        ULIST.append(uList[j])
                exULs = self._constructCUL(x, ULIST, -1, minUtil, len(sortedPrefix), exNeighbours)
                if self._neighbors.get(x.item) is not None and exNeighbours is not None:
                    set1 = exNeighbours.intersection(self._neighbors.get(x.item))
                    if exULs is None or set1 is None:
                        continue
                    self._ExploreSearchTree(sortedPrefix, exULs, set1, minUtil)

    def _constructCUL(self, x: _Element, compactUList: List[_CUList], st: int, minUtil: int, length: int, exNeighbours: set) -> List[_CUList]:
        """
        A method to construct CUL's database
        :parm x: Compact utility list
        :type x: Node
        :parm compactUList:list of Compact utility lists.
        :type compactUList:list
        :parm st: starting pos of compactUList
        :type st:int
        :parm minUtil: user minUtil
        :type minUtil:int
        :parm length: length of x
        :type length:int
        :parm exNeighbours: common Neighbours
        :type exNeighbours: set
        :return: projected database of list X
        :rtype: list or set
        """
        exCul = []
        lau = []
        cUtil = []
        eyTs = []
        for i__ in range(0, len(compactUList)):
            uList = _CUList(compactUList[i__].item)
            exCul.append(uList)
            lau.append(0)
            cUtil.append(0)
            eyTs.append(0)
        sz = len(compactUList) - (st + 1)
        exSZ = sz
        for j in range(st + 1, len(compactUList)):
            mapOfTWUF = self._mapFMAP[x.item]
            if mapOfTWUF is not None:
                twuf = mapOfTWUF.get(compactUList[j].item)
                if twuf is not None and twuf < minUtil or (not (exCul[j].item in exNeighbours)):
                    exCul[j] = None
                    exSZ = sz - 1
                else:
                    uList = _CUList(compactUList[j].item)
                    exCul[j] = uList
                    eyTs[j] = 0
                    lau[j] = x.sumCu + x.sumCru + x.sumSnu + x.sumRemainingUtility
                    cUtil[j] = x.sumCu + x.sumCru
        hashTable = {}
        for ex in x.elements:
            newT = []
            for j in range(st + 1, len(compactUList)):
                if exCul[j] is None:
                    continue
                eyList = compactUList[j].elements
                while eyTs[j] < len(eyList) and eyList[eyTs[j]].ts < ex.ts:
                    eyTs[j] = eyTs[j] + 1
                if eyTs[j] < len(eyList) and eyList[eyTs[j]].ts == ex.ts:
                    newT.append(j)
                else:
                    lau[j] = lau[j] - ex.snu - ex.remainingUtility
                    if lau[j] < minUtil:
                        exCul[j] = None
                        exSZ = exSZ - 1
            if len(newT) == exSZ:
                self._updateClosed(x, compactUList, st, exCul, newT, ex, eyTs, length)
            else:
                if len(newT) == 0:
                    continue
                ru = 0
                newT1 = tuple(newT)
                if newT1 not in hashTable.keys():
                    hashTable[newT1] = len(exCul[newT[len(newT) - 1]].elements)
                    for i__ in range(len(newT) - 1, -1, -1):
                        cuListOfItems = exCul[newT[i__]]
                        y = compactUList[newT[i__]].elements[eyTs[newT[i__]]]
                        element = _Element(ex.ts, ex.snu + y.snu - ex.pu, ru, ex.snu, 0)
                        if i__ > 0:
                            element.prevPos = len(exCul[newT[i__ - 1]].elements)
                        else:
                            element.prevPos = -1
                        cuListOfItems.addElements(element)
                        ru += y.snu - ex.pu
                else:
                    dPrevPos = hashTable[newT1]
                    self._updateElement(x, compactUList, st, exCul, newT, ex, dPrevPos, eyTs)
            for j in range(st + 1, len(compactUList)):
                cUtil[j] = cUtil[j] + ex.snu + ex.remainingUtility
        filter_compactUList = []
        for j in range(st + 1, len(compactUList)):
            if cUtil[j] < minUtil or exCul[j] is None:
                continue
            else:
                if length > 1:
                    exCul[j].sumCu += compactUList[j].sumCu + x.sumCu - x.sumCpu
                    exCul[j].sumCru += compactUList[j].sumCru
                    exCul[j].sumCpu += x.sumCu
                filter_compactUList.append(exCul[j])
        return filter_compactUList

    def _updateClosed(self, x: _Element, compactUList: List[_CUList], st: int, exCul: List[_CUList], newT: List[int], ex: _Element, eyTs: List[int], length: int) -> None:
        """
        A method to update closed values
        :parm x: Compact utility list.
        :type x: list
        :parm compactUList:list of Compact utility lists.
        :type compactUList:list
        :parm st: starting pos of compactUList
        :type st:int
        :parm newT:transaction to be updated
        :type newT:list
        :parm ex: element ex
        :type ex:element
        :parm eyTs:list of tss
        :type eyTs:ts
        :parm length: length of x
        :type length:int
        :return: None
        """
        remainingUtility = 0
        for j in range(len(newT) - 1, -1, -1):
            ey = compactUList[newT[j]]
            eyy = ey.elements[eyTs[newT[j]]]
            exCul[newT[j]].sumCu += ex.snu + eyy.snu - ex.pu
            exCul[newT[j]].sumCru += remainingUtility
            exCul[newT[j]].sumCpu += ex.snu
            remainingUtility = remainingUtility + eyy.snu - ex.pu

    def _updateElement(self, z: _Element, compactUList: List[_CUList], st: int, exCul: List[_CUList], newT: List[int], ex: _Element, duPrevPos: int, eyTs: List[int]) -> None:
        """
        A method to updates vales for duplicates
        :parm z: Compact utility list
        :type z: list
        :parm compactUList:list of Compact utility lists
        :type compactUList:list
        :parm st: starting pos of compactUList
        :type st:int
        :parm exCul:list of compactUList
        :type exCul:list
        :parm newT:transaction to be updated
        :type newT:list
        :parm ex: element ex
        :type ex:element
        :parm duPrevPos: position of z in exCul
        :type duPrevPos:int
        :parm eyTs:list of tss
        :type eyTs:ts
        :return: None
        """
        remainingUtility = 0
        pos = duPrevPos
        for j in range(len(newT) - 1, -1, -1):
            ey = compactUList[newT[j]]
            eyy = ey.elements[eyTs[newT[j]]]
            exCul[newT[j]].elements[pos].snu += ex.snu + eyy.snu - ex.pu
            exCul[newT[j]].sumSnu += ex.snu + eyy.snu - ex.pu
            exCul[newT[j]].elements[pos].remainingUtility += remainingUtility
            exCul[newT[j]].sumRemainingUtility += remainingUtility
            exCul[newT[j]].elements[pos].pu += ex.snu
            remainingUtility = remainingUtility + eyy.snu - ex.pu
            pos = exCul[newT[j]].elements[pos].prevPos

    def _saveItemSet(self, prefix: List[str], prefixLen: int, item: str, utility: int) -> None:
        """
         A method to save itemSets
        :parm prefix: it represents all items in prefix
        :type prefix :list
        :parm item:item
        :type item: int
        :parm utility:utility of itemSet
        :type utility:int
        :return: None
        """
        self._huiCount += 1
        res = str()
        for _ in range(0, prefixLen):
            res += str(prefix[_]) + "\t"
        res += str(item)
        res1 = str(utility)
        self._finalPatterns[res] = res1

    def getPatternsAsDataFrame(self) -> Dict[str, str]:
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
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

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

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Spatial High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:  # to  include a user specified separator
            _ap = HDSHUIM(_ab._sys.argv[1], _ab._sys.argv[3], int(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:  # to consider "\t" as a separator
            _ap = HDSHUIM(_ab._sys.argv[1], _ab._sys.argv[3], int(_ab._sys.argv[4]))
        _ap.mine()
        _ap.mine()
        print("Total number of Spatial High-Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        for i in [100000, 500000]:
            _ap = HDSHUIM('/Users/Likhitha/Downloads/mushroom_main_2000.txt',
                    '/Users/Likhitha/Downloads/mushroom_neighbors_2000.txt', i, ' ')
            _ap.mine()
            _ap.mine()
            print("Total number of Spatial High Utility Patterns:", len(_ap.getPatterns()))
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
