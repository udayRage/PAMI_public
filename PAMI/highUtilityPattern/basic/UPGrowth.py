# UP-Growth is two-phase algorithm to mine High Utility Itemsets from transactional databases.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilityPattern.basic import UPGrowth as alg
#
#             obj=alg.UPGrowth("input.txt",35)
#
#             obj.mine()
#
#             highUtilityPattern = obj.getPatterns()
#
#             print("Total number of Spatial Frequent Patterns:", len(highUtilityPattern))
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
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated


class _UPItem:
    """
    A class to represent the UPItem

    :Attributes:

        name: int
            name of item
        utility: int
            utility of item

    :Methods:

    getUtility()
        method to get node utility
    setUtility()
        method to set node utility
    getName()
        method to get name of particular item
    """
    name = 0
    utility = 0

    def __init__(self, name: int, utility: int):
        self.name = name
        self.utility = utility

    def getUtility(self) -> int:
        """
        method to get node utility
        :return: Utility value of Node
        :rtype: int
        """
        return self.utility

    def setUtility(self, utility: int) -> None:
        """
        method to set node utility
        :param utility: the utility to set
        :type utility: int
        :return: None
        """
        self.utility = utility

    def getName(self) -> int:
        """
        method to get name for particular item
        :return: name of particular item
        :rtype: int
        """
        return self.name


class _UPNode:
    """
    A class that represent UPNode

    :Attributes:

        itemId :int
            name of the item
        count: int
            represent the count of items
        nodeUtility: int
            Represent the utility of current node
        nodeLink: UPNode
            represent the link to next node with same itemid
        childs: list
            link to next node with same item id (for the header table)
    :Methods:

        getChildWithId( name):
            method to get child node Return the immediate child of this node having a given name
    """
    itemId = -1
    count = 1
    nodeUtility = 0
    childs = []
    nodeLink = -1
    parent = -1

    def __init__(self) -> None:
        self.itemId = -1
        self.count = 1
        self.nodeUtility = 0
        self.childs = []
        self.nodeLink = -1
        self.parent = -1

    def getChildWithId(self, name: int) -> int:
        """
        method to get child node Return the immediate child of this node having a given name
        :param name: represent id of item
        :type name: int
        :return: id of child node with same itemid
        :rtype: int
        """
        for child in self.childs:
            if child.itemId == name:
                return child
        return -1


class _UPTree:
    """
    A class to represent UPTree

    :Attributes:

        headerList: list
            Lists of items in the header table
        mapItemNodes: map
            Maps that indicates the last node for each item using the node links
        root : UPNode
            root of the tree
        mapItemToLastNode: map
            List of pairs (item, Utility) of the header table
        hasMoreThanOnePath :bool
            Variable that indicate if the tree has more than one path

    :Methods:

        addTransaction(transaction,rtu)
            To add a transaction (for initial construction)
        addLocalTransaction(localPath, pathUtility, mapItemToMinimumItemUtility, pathCount)
            Add a transaction to the UP-Tree (for a local UP-Tree)
        insertNewNode(currentLocalNode, itemName, nodeUtility)
            Insert a new node in the UP-Tree as child of a parent node
        createHeaderList(mapItemToTwu)
            Method for creating the list of items in the header table, in descending order of TWU or path utility.
    """
    headerList = []
    hasMoreThanOnePath = False
    mapItemNodes = {}
    root = _UPNode()
    mapItemToLastNode = {}

    def __init__(self) -> None:
        self.headerList = []
        self.hasMoreThanOnePath = False
        self.mapItemToLastNode = {}
        self.mapItemNodes = {}
        self.root = _UPNode()

    def addTransaction(self, transaction: list, RTU: int) -> int:
        """
        A Method to add new Transaction to tree
        :param transaction: the reorganised transaction
        :type transaction: list
        :param RTU :reorganised transaction utility
        :type RTU: int
        :return: the number of transactions added
        :rtype: int
        """
        currentNode = self.root
        NumberOfNodes = 0
        RemainingUtility = 0
        # for idx, item in enumerate(transaction):
        #     itemName = item.name
        #     child = currentNode.getChildWithId(itemName)
        #     RemainingUtility += item.utility
        #     if child == -1:
        #         NumberOfNodes += 1
        #         nodeUtility = RemainingUtility
        #         currentNode = self.insertNewNode(currentNode, itemName, nodeUtility)
        #     else:
        #         child.count += 1
        #         child.nodeUtility += RemainingUtility
        #         currentNode = child
        for idx, item in enumerate(transaction):
            for k in range(idx + 1, len(transaction)):
                RemainingUtility += transaction[k].getUtility()
            itemName = item.name
            child = currentNode.getChildWithId(itemName)
            if child == -1:
                NumberOfNodes += 1
                nodeUtility = RTU - RemainingUtility
                RemainingUtility = 0
                currentNode = self.insertNewNode(currentNode, itemName, nodeUtility)
            else:
                currentNU = child.nodeUtility
                nodeUtility = currentNU + (RTU - RemainingUtility)
                RemainingUtility = 0
                child.count += 1
                child.nodeUtility = nodeUtility
                currentNode = child
        return NumberOfNodes

    def addLocalTransaction(self, localPath: list, pathUtility: int, mapItemToMinimumItemutility: dict, pathCount: int) -> int:
        """
        A Method to add addLocalTransaction to tree
        :param localPath: The path to insert
        :type localPath: list
        :param pathUtility: the Utility of path
        :type pathUtility: int
        :param mapItemToMinimumItemutility: the map storing minimum item utility
        :type mapItemToMinimumItemutility: map
        :param pathCount: the Path count
        :type pathCount: int
        :return: The number of nodes in the tree that have been added or removed from the tree
        :rtype: int
        """
        currentLocalNode = self.root
        RemainingUtility = 0
        NumberOfNodes = 0
        # for item in localPath:
        #     RemainingUtility += mapItemToMinimumItemutility[item] * pathCount
        # for item in localPath:
        #     RemainingUtility -= mapItemToMinimumItemutility[item] * pathCount
        #     child = currentLocalNode.getChildWithId(item)
        #     if child == -1:
        #         NumberOfNodes += 1
        #         currentLocalNode = self.insertNewNode(currentLocalNode, item, pathUtility - RemainingUtility)
        #     else:
        #         child.count += 1
        #         child.nodeUtility += (pathUtility - RemainingUtility)
        #         currentLocalNode = child
        for idx, item in enumerate(localPath):
            for k in range(idx + 1, len(localPath)):
                search = localPath[k]
                RemainingUtility += mapItemToMinimumItemutility[search] * pathCount
            child = currentLocalNode.getChildWithId(item)
            if child == -1:
                NumberOfNodes += 1
                nodeUtility = pathUtility - RemainingUtility
                RemainingUtility = 0
                currentLocalNode = self.insertNewNode(currentLocalNode, item, nodeUtility)
            else:
                currentNU = child.nodeUtility
                nodeUtility = currentNU + (pathUtility - RemainingUtility)
                RemainingUtility = 0
                child.count += 1
                child.nodeUtility = nodeUtility
                currentLocalNode = child
        return NumberOfNodes

    def insertNewNode(self, currentlocalNode: _UPNode, itemName: int, nodeUtility: int) -> _UPNode:
        """
        A method to Insert a new node in the UP-Tree as child of a parent node
        :param currentlocalNode: The parent Node
        :type currentlocalNode: UPNode
        :param itemName: name of item in new Node
        :type itemName: int
        :param nodeUtility: Utility of new node
        :type nodeUtility: int
        :return: The newly created UPNode
        :rtype: _UPNode
        """
        newNode = _UPNode()
        newNode.itemId = itemName
        newNode.count = 1
        newNode.nodeUtility = nodeUtility
        newNode.parent = currentlocalNode
        currentlocalNode.childs.append(newNode)
        if not self.hasMoreThanOnePath and len(currentlocalNode.childs) > 1:
            self.hasMoreThanOnePath = True
        if itemName in self.mapItemNodes:
            lastNode = self.mapItemToLastNode[itemName]
            lastNode.nodeLink = newNode
            self.mapItemToLastNode[itemName] = newNode
        else:
            self.mapItemNodes[itemName] = newNode
            self.mapItemToLastNode[itemName] = newNode
        return newNode

    def createHeaderList(self, mapItemToTwu: dict) -> None:
        """
        A Method for creating the list of items in the header table, in descending order of TWU or path utility.
        :param mapItemToTwu: the Utilities of each item
        :type mapItemToTwu: map
        :return: None
        """
        self.headerList = list(self.mapItemNodes.keys())
        self.headerList = sorted(self.headerList, key=lambda x: mapItemToTwu[x], reverse=True)


class UPGrowth(_ab._utilityPatterns):
    """
    :Description:   UP-Growth is two-phase algorithm to mine High Utility Itemsets from transactional databases.

    :Reference:     Vincent S. Tseng, Cheng-Wei Wu, Bai-En Shie, and Philip S. Yu. 2010. UP-Growth: an efficient algorithm for high utility itemset mining.
                    In Proceedings of the 16th ACM SIGKDD international conference on Knowledge discovery and data mining (KDD '10).
                    Association for Computing Machinery, New York, NY, USA, 253–262. DOI:https://doi.org/10.1145/1835804.1835839

    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility patterns
    :param minUtil: int :
                   The user given minUtil value.
    :param candidateCount: int
                   Number of candidates specified by user
    :param maxMemory: int
                   Maximum memory used by this program for running
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
        NumberOfNodes : int
            Total number of nodes generated while building the tree
        ParentNumberOfNodes : int
           Total number of nodes required to build the parent tree
        MapItemToMinimumUtility : map
           A map to store the minimum utility of item in the database
        phuis : list
            A list to store the phuis
        MapItemToTwu : map
            A map to store the twu of each item in database

    :Methods:

        mine()
                Mining process will start from here
        getPatterns()
                Complete set of patterns will be retrieved with this function
        createLocalTree(tree, item)
            A Method to Construct conditional pattern base
        UPGrowth( tree, alpha)
            A Method to Mine UP Tree recursively
        PrintStats()
            A Method to print number of phuis
        save(oFile)
                Complete set of frequent patterns will be loaded in to an output file
        getPatternsAsDataFrame()
                Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
               Total amount of runtime taken by the mining process will be retrieved from this function

    **Executing the code on terminal:**
    ---------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 UPGrowth <inputFile> <outputFile> <Neighbours> <minUtil> <sep>

      Example Usage:

      (.venv) $ python3 UPGrowth sampleTDB.txt output.txt sampleN.txt 35

    .. note:: maxMemory will be considered as Maximum memory used by this program for running


    Sample run of importing the code:
    -------------------------------------
    .. code-block:: python
    
            from PAMI.highUtilityPattern.basic import UPGrowth as alg

            obj=alg.UPGrowth("input.txt",35)

            obj.mine()

            highUtilityPattern = obj.getPatterns()

            print("Total number of Spatial Frequent Patterns:", len(highUtilityPattern))

            obj.save("output")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    -----------------------
            The complete program was written by Pradeep pallikila under the supervision of Professor Rage Uday Kiran.

    """

    _maxMemory = 0
    _startTime = 0
    _endTime = 0
    _minUtil = 0
    _memoryUSS = float()
    _memoryRSS = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _NumberOfNodes = 0
    _ParentNumberOfNodes = 0
    _MapItemToMinimumUtility = {}
    _MapItemsetsToUtilities = _ab._defaultdict(int)
    _phuis = []
    _Database = []
    _MapItemToTwu = {}
    _sep = " "

    def __init__(self, iFile: str, minUtil: int, sep: str='\t') -> None:
        super().__init__(iFile, minUtil, sep)
        self.oFile = None

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            timeStamp, data = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            if 'Utilities' in i:
                data = self._iFile['Utilities'].tolist()
            if 'UtilitySum' in i:
                data = self._iFile['UtilitySum'].tolist()
            for i in range(len(data)):
                tr = timeStamp[i]
                tr.append(data[i])
                self._Database.append(tr)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    self._Database.append(line)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            self._Database.append(line)
                except IOError:
                    print("File Not Found")
                    quit()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Mining process will start from here
        :return: None
        """
        self.mine()

    def mine(self) -> None:
        """
        Mining process will start from here
        :return: None
        """
        self._startTime = _ab._time.time()
        tree = _UPTree()
        self._creatingItemSets()
        self._finalPatterns = {}
        for line in self._Database:
            line = line.split("\n")[0]
            transaction = line.strip().split(':')
            items = transaction[0].split(self._sep)
            transactionUtility = int(transaction[1])
            for item in items:
                Item = int(item)
                if Item in self._MapItemToTwu:
                    self._MapItemToTwu[Item] += transactionUtility
                else:
                    self._MapItemToTwu[Item] = transactionUtility
        for line in self._Database:
            line = line.split("\n")[0]
            transaction = line.strip().split(':')
            items = transaction[0].split(self._sep)
            utilities = transaction[2].split(self._sep)
            remainingUtility = 0
            revisedTransaction = []
            for idx, item in enumerate(items):
                Item = int(item)
                utility = int(utilities[idx])
                if self._MapItemToTwu[Item] >= self._minUtil:
                    element = _UPItem(Item, utility)
                    revisedTransaction.append(element)
                    remainingUtility += utility
                    if Item in self._MapItemToMinimumUtility:
                        minItemUtil = self._MapItemToMinimumUtility[Item]
                        if minItemUtil >= utility:
                            self._MapItemToMinimumUtility[Item] = utility
                    else:
                        self._MapItemToMinimumUtility[Item] = utility
            revisedTransaction = sorted(revisedTransaction, key=lambda x: self._MapItemToTwu[x.name], reverse=True)
            self._ParentNumberOfNodes += tree.addTransaction(revisedTransaction, remainingUtility)
        tree.createHeaderList(self._MapItemToTwu)
        alpha = []
        self._finalPatterns = {}
        # print("number of nodes in parent tree", self.ParentNumberOfNodes)
        self._UPGrowth(tree, alpha)
        # self.phuis = sorted(self.phuis, key=lambda x: len(x))
        # print(self.phuis[0:10])
        for line in self._Database:
            line = line.split("\n")[0]
            transaction = line.strip().split(':')
            items = transaction[0].split(self._sep)
            utilities = transaction[2].split(self._sep)
            mapItemToUtility = {}
            for idx, item in enumerate(items):
                Item = int(item)
                utility = int(utilities[idx])
                if self._MapItemToTwu[Item] >= self._minUtil:
                    mapItemToUtility[Item] = utility
            for itemset in self._phuis:
                l = len(itemset)
                count = 0
                utility = 0
                for item in itemset:
                    item = int(item)
                    if item in mapItemToUtility:
                        utility += mapItemToUtility[item]
                        count += 1
                if count == l:
                    self._MapItemsetsToUtilities[tuple(itemset)] += utility

        for itemset in self._phuis:
            util = self._MapItemsetsToUtilities[tuple(itemset)]
            if util >= self._minUtil:
                s = str()
                for item in itemset:
                    s = s + str(item)
                    s = s + "\t"
                self._finalPatterns[s] = util
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("High Utility patterns were generated successfully using UPGrowth algorithm")

    def _UPGrowth(self, tree: _UPTree, alpha: list) -> None:
        """
        A Method to Mine UP Tree recursively
        :param tree: UPTree to mine
        :type tree: UPTree
        :param alpha: prefix itemset
        :type alpha: list
        :return: None
        """
        for item in reversed(tree.headerList):
            localTree = self._createLocalTree(tree, item)
            node = tree.mapItemNodes[item]
            ItemTotalUtility = 0
            while node != -1:
                ItemTotalUtility += node.nodeUtility
                node = node.nodeLink
            if ItemTotalUtility >= self._minUtil:
                beta = alpha + [item]
                self._phuis.append(beta)
                # str1 = ' '.join(map(str, beta))
                # self.finalPatterns[str1] = ItemTotalUtility
                if len(localTree.headerList) > 0:
                    self._UPGrowth(localTree, beta)

    def _createLocalTree(self, tree: _UPTree, item: int) -> _UPTree:
        """
        A Method to Construct conditional pattern base
        :param tree: the UPtree
        :type tree: UP Tree
        :param item: item that need to construct conditional patterns
        :type item: int
        :return: the conditional pattern based UPTree
        :rtype: _UPTree
        """
        prefixPaths = []
        path = tree.mapItemNodes[item]
        itemPathUtility = {}
        while path != -1:
            nodeUtility = path.nodeUtility
            if path.parent != -1:
                prefixPath = [path]
                ParentNode = path.parent
                while ParentNode.itemId != -1:
                    prefixPath.append(ParentNode)
                    itemName = ParentNode.itemId
                    if itemName in itemPathUtility:
                        itemPathUtility[itemName] += nodeUtility
                    else:
                        itemPathUtility[itemName] = nodeUtility
                    ParentNode = ParentNode.parent
                prefixPaths.append(prefixPath)
            path = path.nodeLink
        localTree = _UPTree()
        for prefixPath in prefixPaths:
            pathUtility = prefixPath[0].nodeUtility
            pathCount = prefixPath[0].count
            localPath = []
            for i in range(1, len(prefixPath)):
                node = prefixPath[i]
                if itemPathUtility[node.itemId] >= self._minUtil:
                    localPath.append(node.itemId)
                else:
                    pathUtility -= pathCount * self._MapItemToMinimumUtility[node.itemId]
            localPath = sorted(localPath, key=lambda x: itemPathUtility[x], reverse=True)
            self._NumberOfNodes += localTree.addLocalTransaction(localPath, pathUtility, self._MapItemToMinimumUtility,
                                                                pathCount)
        localTree.createHeaderList(itemPathUtility)
        return localTree

    def PrintStats(self) -> None:
        """
        A Method to print number of phuis
        :return: None
        """
        print('number of PHUIS are ' + str(len(self._phuis)))

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
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Utility'])
        return dataFrame

    def getPatterns(self) -> dict:
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
            writer.write("%s\n" % patternsAndSupport)

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
        return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self._endTime - self._startTime

    def printResults(self) -> None:
        """
        This function is used to print the results
        :return: None
        """
        print("Total number of High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = UPGrowth(_ab._sys.argv[1], int(_ab._sys.argv[3]), _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = UPGrowth(_ab._sys.argv[1], int(_ab._sys.argv[3]))
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = UPGrowth('/Users/likhitha/Downloads/Utility_T10I4D100K.csv', 50000, '\t')
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save('/Users/likhitha/Downloads/UPGrowth_output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
