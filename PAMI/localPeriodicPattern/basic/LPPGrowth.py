# Local Periodic Patterns, which are patterns (sets of events) that have a periodic behavior in some non predefined
# time-intervals. A pattern is said to be a local periodic pattern if it appears regularly and continuously in some
# time-intervals. The maxSoPer (maximal period of spillovers) measure allows detecting time-intervals of variable
# lengths where a pattern is continuously periodic, while the minDur (minimal duration) measure ensures that those
# time-intervals have a minimum duration.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.localPeriodicPattern.basic import LPPGrowth as alg
#
#             obj = alg.LPPGrowth(iFile, maxPer, maxSoPer, minDur)
#
#             obj.mine()
#
#             localPeriodicPatterns = obj.getPatterns()
#
#             print(f'Total number of local periodic patterns: {len(localPeriodicPatterns)}')
#
#             obj.save(oFile)
#
#             Df = obj.getPatternsAsDataFrame()
#
#             memUSS = obj.getMemoryUSS()
#
#             print(f'Total memory in USS: {memUSS}')
#
#             memRSS = obj.getMemoryRSS()
#
#             print(f'Total memory in RSS: {memRSS}')
#
#             runtime = obj.getRuntime()
#
#             print(f'Total execution time in seconds: {runtime})
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



from PAMI.localPeriodicPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated

class Node:
    """
    A class used to represent the node of localPeriodicPatternTree

    :Attributes:

        item : int
            storing item of a node
        parent : node
            To maintain the parent of every node
        child : list
            To maintain the children of node
        nodeLink : node
            To maintain the next node of node
        tidList : set
            To maintain timestamps of node

    :Methods:

        getChild(itemName)
            storing the children to their respective parent nodes
    """
    
    def __init__(self) -> None:
        self.item = -1
        self.parent = None
        self.child = []
        self.nodeLink = None
        self.tidList = set()

    def getChild(self, item: int) -> 'Node':
        """
        This function is used to get child node from the parent node

        :param item: item of the parent node

        :type item: int

        :return: if node have node of item, then return it. if node don't have return []

        :rtype: Node
        """
        for child in self.child:
            if child.item == item:
                return child
        return []


class Tree:
    """
        A class used to represent the frequentPatternGrowth tree structure

        :Attributes:

            root : node
                Represents the root node of the tree
            nodeLinks : dictionary
                storing last node of each item
            firstNodeLink : dictionary
                storing first node of each item

        :Methods:

            addTransaction(transaction,timeStamp)
                creating transaction as a branch in frequentPatternTree
            fixNodeLinks(itemName, newNode)
                add newNode link after last node of item
            deleteNode(itemName)
                delete all node of item
            createPrefixTree(path,timeStampList)
                create prefix tree by path

    """
    def __init__(self) -> None:
        self.root = Node()
        self.nodeLinks = {}
        self.firstNodeLink = {}

    def addTransaction(self, transaction: List[int], tid: int) -> None:
        """
        add transaction into tree

        :param transaction: it represents the one transaction in database
        :type transaction: list
        :param tid: represents the timestamp of transaction
        :type tid: list or int
        :return: None
        """
        current = self.root
        for item in transaction:
            child = current.getChild(item)
            if not child:
                newNode = Node()
                newNode.item = item
                newNode.parent = current
                current.child.append(newNode)
                current = newNode
                self.fixNodeLinks(item, newNode)
            else:
                current = child
            current.tidList.add(tid)

    def fixNodeLinks(self, item: int, newNode: 'Node') -> None:
        """
        fix node link

        :param item: it represents item name of newNode
        :type item: string
        :param newNode: it represents node which is added
        :type newNode: Node
        :return: None
        """
        if item in self.nodeLinks:
            lastNode = self.nodeLinks[item]
            lastNode.nodeLink = newNode
        self.nodeLinks[item] = newNode
        if item not in self.firstNodeLink:
            self.firstNodeLink[item] = newNode

    def deleteNode(self, item: int) -> None:
        """
        delete the node from tree

        :param item: it represents the item name of node
        :type item: str
        :return: None
        """
        deleteNode = self.firstNodeLink[item]
        parentNode = deleteNode.parent
        parentNode.child.remove(deleteNode)
        parentNode.child += deleteNode.child
        parentNode.tidList |= deleteNode.tidList
        for child in deleteNode.child:
            child.parent = parentNode
        while deleteNode.nodeLink:
            deleteNode = deleteNode.nodeLink
            parentNode = deleteNode.parent
            parentNode.child.remove(deleteNode)
            parentNode.child += deleteNode.child
            parentNode.tidList |= deleteNode.tidList
            for child in deleteNode.child:
                child.parent = parentNode

    def createPrefixTree(self, path: List[int], tidList: List[int]) -> None:
        """
        create prefix tree by path

        :param path: it represents path to root from prefix node
        :type path: list
        :param tidList: it represents tid of each item
        :type tidList: list
        :return: None
        """
        currentNode = self.root
        for item in path:
            child = currentNode.getChild(item)
            if not child:
                newNode = Node()
                newNode.item = item
                newNode.parent = currentNode
                currentNode.child.append(newNode)
                currentNode = newNode
                self.fixNodeLinks(item, newNode)
            else:
                currentNode = child
            currentNode.tidList |= tidList


class LPPGrowth(_ab._localPeriodicPatterns):
    """
    :Description:

        Local Periodic Patterns, which are patterns (sets of events) that have a periodic behavior in some non predefined
        time-intervals. A pattern is said to be a local periodic pattern if it appears regularly and continuously in some
        time-intervals. The maxSoPer (maximal period of spillovers) measure allows detecting time-intervals of variable
        lengths where a pattern is continuously periodic, while the minDur (minimal duration) measure ensures that those
        time-intervals have a minimum duration.

    :Reference:

        Fournier-Viger, P., Yang, P., Kiran, R. U., Ventura, S., Luna, J. M.. (2020). Mining Local Periodic Patterns in
        a Discrete Sequence. Information Sciences, Elsevier, to appear. [ppt] DOI: 10.1016/j.ins.2020.09.044

    :param  iFile: str :
                   Name of the Input file to mine complete set of local periodic pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of local periodic patterns
    :param  minDur: str:
                   Minimal duration in seconds between consecutive periods of time-intervals where a pattern is continuously periodic.
    :param  maxPer: float:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.
    :param  maxSoPer: float:
                   Controls the maximum number of time periods between consecutive periods of time-intervals where a pattern is continuously periodic.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

            iFile : str
                Input file name or path of the input file
            oFile : str
                Output file name or path of the output file
            maxPer : float
                User defined maxPer value.
            maxSoPer : float
                User defined maxSoPer value.
            minDur : float
                User defined minDur value.
            tsMin : int / date
                First time stamp of input data.
            tsMax : int / date
                Last time stamp of input data.
            startTime : float
                Time when start of execution the algorithm.
            endTime : float
                Time when end of execution the algorithm.
            finalPatterns : dict
                To store local periodic patterns and its PTL.
            tsList : dict
                To store items and its time stamp as bit vector.
            root : Tree
                It is root node of transaction tree of whole input data.
            PTL : dict
                Storing the item and its PTL.
            items : list
                Storing local periodic item list.
            sep: str
                separator used to distinguish items from each other. The default separator is tab space.

    :Methods:

            findSeparator(line)
                Find the separator of the line which split strings.
            creteLPPlist()
                Create the local periodic patterns list from input data.
            createTSList()
                Create the tsList as bit vector from input data.
            generateLPP()
                Generate 1 length local periodic pattens by tsList and execute depth first search.
            createLPPTree()
                Create LPPTree of local periodic item from input data.
            patternGrowth(tree, prefix, prefixPFList)
                Execute pattern growth algorithm. It is important function in this program.
            calculatePTL(tsList)
                Calculate PTL from input tsList as integer list.
            calculatePTLbit(tsList)
                Calculate PTL from input tsList as bit vector.
            mine()
                Mining process will start from here.
            getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function.
            getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function.
            getRuntime()
                Total amount of runtime taken by the mining process will be retrieved from this function.
            getLocalPeriodicPatterns()
                return local periodic patterns and its PTL
            save(oFile)
                Complete set of local periodic patterns will be loaded in to an output file.
            getPatternsAsDataFrame()
                Complete set of local periodic patterns will be loaded in to a dataframe.

    **Executing the code on terminal:**
    ---------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 LPPMGrowth.py <inputFile> <outputFile> <maxPer> <minSoPer> <minDur>

      Example Usage:

      (.venv) $ python3 LPPMGrowth.py sampleDB.txt patterns.txt 0.3 0.4 0.5

    .. note: minDur will be considered as time interval between two consecutive periods


    **Sample run of importing the code:**
    ----------------------------------------
    .. code-block:: python

            from PAMI.localPeriodicPattern.basic import LPPGrowth as alg

            obj = alg.LPPGrowth(iFile, maxPer, maxSoPer, minDur)

            obj.mine()

            localPeriodicPatterns = obj.getPatterns()

            print(f'Total number of local periodic patterns: {len(localPeriodicPatterns)}')

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print(f'Total memory in USS: {memUSS}')

            memRSS = obj.getMemoryRSS()

            print(f'Total memory in RSS: {memRSS}')

            runtime = obj.getRuntime()

            print(f'Total execution time in seconds: {runtime})

    **Credits:**
    --------------
        The complete program was written by So Nakamura under the supervision of Professor Rage Uday Kiran.
    """
    _localPeriodicPatterns__iFile = ' '
    _localPeriodicPatterns__oFile = ' '
    _localPeriodicPatterns__maxPer = str()
    _localPeriodicPatterns__maxSoPer = str()
    _localPeriodicPatterns__minDur = str()
    __tsMin = 0
    __tsMax = 0
    _localPeriodicPatterns__startTime = float()
    _localPeriodicPatterns__endTime = float()
    _localPeriodicPatterns__memoryUSS = float()
    _localPeriodicPatterns__memoryRSS = float()
    _localPeriodicPatterns__finalPatterns = {}
    __tsList = {}
    __root = Tree()
    __PTL = {}
    __items = []
    _localPeriodicPatterns__sep = ' '
    __Database = []

    def __creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._localPeriodicPatterns__iFile, _ab._pd.DataFrame):
            if self._localPeriodicPatterns__iFile.empty:
                print("its empty..")
            i = self._localPeriodicPatterns__iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.__Database = self._localPeriodicPatterns__iFile['Transactions'].tolist()
            if 'Patterns' in i:
                self.__Database = self._localPeriodicPatterns__iFile['Patterns'].tolist()

        if isinstance(self._localPeriodicPatterns__iFile, str):
            if _ab._validators.url(self._localPeriodicPatterns__iFile):
                data = _ab._urlopen(self._localPeriodicPatterns__iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._localPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._localPeriodicPatterns__iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._localPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def __createLPPlist(self) -> None:
        """
        Create Local Periodic Pattern list from temporal data.
        """
        LPPList = {}
        PTL = {}
        start = {}
        tsPre = {}
        for line in self.__Database:
            soPer = ' '
            self.__tsMin = int(line.pop(0))
            ts = self.__tsMin
            for item in line:
                if item in LPPList:
                    per = ts - tsPre[item]
                    if per <= self._localPeriodicPatterns__maxPer and start == -1:
                        start = tsPre[item]
                        soPer = self._localPeriodicPatterns__maxSoPer
                    if start != -1:
                        soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                        if soPer > self._localPeriodicPatterns__maxSoPer:
                            if tsPre[item] - start[item] <= self._localPeriodicPatterns__minDur:
                                PTL[item].add((start[item], tsPre[item]))
                                LPPList[item] = PTL[item]
                            start[item] = -1
                else:
                    tsPre[item] = ts
                    start[item] = -1
                    LPPList[item] = set()
            for line1 in self.__Database:
                ts = int(line1.pop(0))
                for item in line1:
                    if item in LPPList:
                        per = ts - tsPre[item]
                        if per <= self._localPeriodicPatterns__maxPer and start[item] == -1:
                            start[item] = tsPre[item]
                            soPer = self._localPeriodicPatterns__maxSoPer
                        if start[item] != -1:
                            soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                            if soPer > self._localPeriodicPatterns__maxSoPer:
                                PTL[item].add((start[item], tsPre[item]))
                                LPPList[item] = PTL[item]
                            start[item] = -1
                        tsPre[item] = ts
                    else:
                        tsPre[item] = ts
                        start[item] = -1
                        LPPList[item] = set()

    def __createTSList(self) -> None:
        """
        Create tsList as bit vector from temporal data.
        """
        # for line in self.__Database:
        #     count = 1
        #     bitVector = 0b1 << count
        #     bitVector = bitVector | 0b1
        #     self.__tsMin = int(line.pop(0))
        #     self.__tsList = {item: bitVector for item in line}
        #     count += 1
        #     ts = ' '
        count = 1
        bitVector = None
        for line in self.__Database:
            bitVector = 0b1 << count
            bitVector = bitVector | 0b1
            # print(line)
            ts = line[0]
            for item in line[1:]:
                if self.__tsList.get(item):
                    different = abs(bitVector.bit_length() - self.__tsList[item].bit_length())
                    self.__tsList[item] = self.__tsList[item] << different
                    self.__tsList[item] = self.__tsList[item] | 0b1
                else:
                    self.__tsList[item] = bitVector
            count += 1
            self.__tsMax = int(ts)

        for item in self.__tsList:
            different = abs(bitVector.bit_length() - self.__tsList[item].bit_length())
            self.__tsList[item] = self.__tsList[item] << different
        self._localPeriodicPatterns__maxPer = self.__convert(self._localPeriodicPatterns__maxPer)
        self._localPeriodicPatterns__maxSoPer = self.__convert(self._localPeriodicPatterns__maxSoPer)
        self._localPeriodicPatterns__minDur = self.__convert(self._localPeriodicPatterns__minDur)

    def __generateLPP(self) -> None:
        """
        Generate local periodic items from bit vector tsList.
        """
        PTL = {}
        for item in self.__tsList:
            PTL[item] = set()
            ts = list(bin(self.__tsList[item]))
            ts = ts[2:]
            start = -1
            currentTs = 1
            soPer = ' '
            tsPre = ' '
            for t in ts[currentTs:]:
                if t == '0':
                    currentTs += 1
                    continue
                else:
                    tsPre = currentTs
                    currentTs += 1
                    break
            for t in ts[currentTs:]:
                if t == '0':
                    currentTs += 1
                    continue
                else:
                    per = currentTs - tsPre
                    if per <= self._localPeriodicPatterns__maxPer and start == -1:
                        start = tsPre
                        soPer = self._localPeriodicPatterns__maxSoPer
                    if start != -1:
                        soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                        if soPer > self._localPeriodicPatterns__maxSoPer:
                            if tsPre - start >= self._localPeriodicPatterns__minDur:
                                PTL[item].add((start, tsPre))
                            """else:
                                bitVector = 0b1 << currentTs
                                different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                                bitVector = bitVector | 0b1
                                bitVector = bitVector << different
                                self.tsList[item] = self.tsList[item] | bitVector"""
                            start = -1
                    tsPre = currentTs
                    currentTs += 1
            if start != -1:
                soPer = max(0, soPer + self.__tsMax - tsPre - self._localPeriodicPatterns__maxPer)
                if soPer > self._localPeriodicPatterns__maxSoPer and tsPre - start >= self._localPeriodicPatterns__minDur:
                    PTL[item].add((start, tsPre))
                """else:
                    bitVector = 0b1 << currentTs+1
                    different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                    bitVector = bitVector | 0b1
                    bitVector = bitVector << different
                    self.tsList[item] = self.tsList[item] | bitVector"""
                if soPer <= self._localPeriodicPatterns__maxSoPer and self.__tsMax - start >= self._localPeriodicPatterns__minDur:
                    PTL[item].add((start, self.__tsMax))
                """else:
                    bitVector = 0b1 << currentTs+1
                    different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                    bitVector = bitVector | 0b1
                    bitVector = bitVector << different
                    self.tsList[item] = self.tsList[item] | bitVector"""
        self.__PTL = {k: v for k, v in PTL.items() if len(v) > 0}
        self.__items = list(self.__PTL.keys())

    def __createLPPTree(self) -> None:
        """
        Create transaction tree of local periodic item from input data.
        """
        for line in self.__Database:
            ts = int(line[0])
            tempTransaction = [item for item in line[1:] if item in self.__items]
            transaction = sorted(tempTransaction, key=lambda x: len(self.__PTL[x]), reverse=True)
            self.__root.addTransaction(transaction, ts)
            # for line in self.__Database:
            #     tid = int(transaction[0])
            #     tempTransaction = [item for item in transaction[1:] if item in self.__items]
            #     transaction = sorted(tempTransaction, key=lambda x: len(self.__PTL[x]), reverse=True)
            #     self.__root.addTransaction(transaction, tid)

    def __patternGrowth(self, tree: 'Tree', prefix: List[int], prefixPFList: Dict[Any, Any]) -> None:
        """
        Create prefix tree and prefixPFList. Store finalPatterns and its PTL.

        :param tree: The root node of prefix tree.
        :type tree: Node or Tree
        :param prefix: Prefix item list.
        :type prefix: list
        :param prefixPFList: tsList of prefix patterns.
        :type prefixPFList: dict or list
        :return: None
        """
        items = list(prefixPFList)
        if not prefix:
            items = reversed(items)
        for item in items:
            prefixCopy = prefix.copy()
            prefixCopy.append(item)
            PFList = {}
            prefixTree = Tree()
            prefixNode = tree.firstNodeLink[item]
            tidList = prefixNode.tidList
            path = []
            currentNode = prefixNode.parent
            while currentNode.item != -1:
                path.insert(0, currentNode.item)
                currentNodeItem = currentNode.item
                if currentNodeItem in PFList:
                    PFList[currentNodeItem] |= tidList
                else:
                    PFList[currentNodeItem] = tidList
                currentNode = currentNode.parent
            prefixTree.createPrefixTree(path, tidList)
            while prefixNode.nodeLink:
                prefixNode = prefixNode.nodeLink
                tidList = prefixNode.tidList
                path = []
                currentNode = prefixNode.parent
                while currentNode.item != -1:
                    path.insert(0, currentNode.item)
                    currentNodeItem = currentNode.item
                    if currentNodeItem in PFList:
                        PFList[currentNodeItem] = PFList[currentNodeItem] | tidList
                    else:
                        PFList[currentNodeItem] = tidList
                    currentNode = currentNode.parent
                prefixTree.createPrefixTree(path, tidList)
            if len(prefixCopy) == 1:
                self._localPeriodicPatterns__finalPatterns[prefixCopy[0]] = self.__calculatePTLbit(self.__tsList[item])
            else:
                self._localPeriodicPatterns__finalPatterns[tuple(prefixCopy)] = self.__calculatePTL(prefixPFList[item])
            candidateItems = list(PFList)
            for i in candidateItems:
                PTL = self.__calculatePTL(PFList[i])
                if len(PTL) == 0:
                    prefixTree.deleteNode(i)
                    del PFList[i]
            if PFList:
                self.__patternGrowth(prefixTree, prefixCopy, PFList)

    def __calculatePTL(self, tsList: List[int]) -> set:
        """
        Calculate PTL from input tsList as integer list

        :param tsList: It is tsList which store time stamp as integer.
        :type tsList: list
        :return: PTL
        :rtype: set
        """
        start = -1
        PTL = set()
        tsList = sorted(tsList)
        tsPre = tsList[0]
        soPer = ' '
        for ts in tsList[1:]:
            per = ts - tsPre
            if per <= self._localPeriodicPatterns__maxPer and start == -1:
                start = tsPre
                soPer = self._localPeriodicPatterns__maxSoPer
            if start != -1:
                soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                if soPer > self._localPeriodicPatterns__maxSoPer:
                    if tsPre - start >= self._localPeriodicPatterns__minDur:
                        PTL.add((start, tsPre))
                    start = -1
            tsPre = ts
        if start != -1:
            soPer = max(0, soPer + self.__tsMax - tsPre - self._localPeriodicPatterns__maxPer)
            if soPer > self._localPeriodicPatterns__maxSoPer and tsPre - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, tsPre))
            if soPer <= self._localPeriodicPatterns__maxSoPer and self.__tsMax - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, self.__tsMax))
        return PTL

    def __calculatePTLbit(self, tsList: List[int]) -> set:
        """
        Calculate PTL from input tsList as bit vector.

        :param tsList: It is tsList which store time stamp as bit vector.
        :type tsList: list
        :return: PTL
        :rtype: set
        """
        tsList = list(bin(tsList))
        tsList = tsList[2:]
        start = -1
        currentTs = 1
        PTL = set()
        tsPre = ' '
        soPer = ' '
        for ts in tsList[currentTs:]:
            if ts == '0':
                currentTs += 1
                continue
            else:
                tsPre = currentTs
                currentTs += 1
                break
        for ts in tsList[currentTs:]:
            if ts == '0':
                currentTs += 1
                continue
            else:
                per = currentTs - tsPre
                if per <= self._localPeriodicPatterns__maxPer and start == -1:
                    start = tsPre
                    soPer = self._localPeriodicPatterns__maxSoPer
                if start != -1:
                    soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                    if soPer > self._localPeriodicPatterns__maxSoPer:
                        if tsPre - start >= self._localPeriodicPatterns__minDur:
                            PTL.add((start, tsPre))
                        start = -1
                tsPre = currentTs
                currentTs += 1
        if start != -1:
            soPer = max(0, soPer + self.__tsMax - tsPre - self._localPeriodicPatterns__maxPer)
            if soPer > self._localPeriodicPatterns__maxSoPer and tsPre - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, tsPre))
            if soPer <= self._localPeriodicPatterns__maxSoPer and self.__tsMax - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, tsPre))
        return PTL

    def __convert(self, value: Any) -> float:
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        :rtype: float
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self.__Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self.__Database) * value)
            else:
                value = int(value)
        return value

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Mining process start from here.
        """
        self.mine()

    def mine(self) -> None:
        """
        Mining process start from here.
        """
        self._localPeriodicPatterns__startTime = _ab._time.time()
        self._localPeriodicPatterns__finalPatterns = {}
        self.__creatingItemSets()
        self._localPeriodicPatterns__maxPer = self.__convert(self._localPeriodicPatterns__maxPer)
        self._localPeriodicPatterns__maxSoPer = self.__convert(self._localPeriodicPatterns__maxSoPer)
        self._localPeriodicPatterns__minDur = self.__convert(self._localPeriodicPatterns__minDur)
        self.__createTSList()
        self.__generateLPP()
        self.__createLPPTree()
        self.__patternGrowth(self.__root, [], self.__items)
        self._localPeriodicPatterns__endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._localPeriodicPatterns__memoryUSS = float()
        self._localPeriodicPatterns__memoryRSS = float()
        self._localPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._localPeriodicPatterns__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__memoryUSS

    def getMemoryRSS(self) -> float:
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__memoryRSS

    def getRuntime(self) -> float:
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__endTime - self._localPeriodicPatterns__startTime

    def getPatternsAsDataFrame(self) -> '_ab._pd.DataFrame':
        """
        Storing final local periodic patterns in a dataframe

        :return: returning local periodic patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._localPeriodicPatterns__finalPatterns.items():
            pat = str()
            for i in a:
                pat = pat + i + ' '
            data.append([pat, b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'PTL'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete set of local periodic patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._localPeriodicPatterns__oFile = outFile
        writer = open(self._localPeriodicPatterns__oFile, 'w+')
        for x, y in self._localPeriodicPatterns__finalPatterns.items():
            pat = str()
            for i in x:
                pat = pat + i + '\t'
            pat = pat + ":"
            for i in y:
                pat = pat + str(i) + '\t'
            patternsAndPTL = pat.strip()
            writer.write("%s \n" % patternsAndPTL)

    def getPatterns(self) -> Dict:
        """
        Function to send the set of local periodic patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._localPeriodicPatterns__finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Local Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == '__main__':
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = LPPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]), _ab._sys.argv[5])
            _ap.mine()
            _ap.save(_ab._sys.argv[2])
        if len(_ab._sys.argv) == 5:
            _ap = LPPGrowth(_ab._sys.argv[1], _ab._sys.argv[2], float(_ab._sys.argv[3]),_ab._sys.argv[4])
            _ap.mine()

        print("Total number of Local Periodic Patterns:", len(_ap.getPatterns()))
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
