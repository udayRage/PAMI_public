# High-utility pattern mining over data stream is one of the challenging problems in data stream mining.
# HUPMS is an algorithm that discovers high-utility patterns from data streams without rebuilding the tree.
# It stores the database of the current window in form of HUSTree and adjusts the tree based on upcoming
# transactions removing the oldest batch.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilitySpatialPattern.basic import HUPMS as alg
#
#             obj=alg.HUPMS("input.txt","Neighbours.txt",35)
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

import abstract as _hus
import pandas as pd
from functools import reduce
from operator import and_ 
from deprecated import deprecated

_minSup = str()
_hus._sys.setrecursionlimit(20000)


class _Node:
    """
    A class used to represent a node in the HUS tree

    :Attributes:

        itemName : str
            name of the item

        utility : int
            utility of the item

        children : dict
            dictionary of children of the node

        next : _Node
            pointer to the next node with same item in the tree

        batchIndex : int
            index of the batch with respect to window to which the node belongs

        utility : list
            List of utilities of the node with respect to each batch in the window

        parent : _Node
            pointer to the parent of the node

    :Methods:

        addUtility(utility, batchIndex)
            Adds utility to the node at specified batch index

        removeUtility(utility)
            Removes utility from the node

        shiftUtility()
            Shifts the utility values of the node to the left useful for removing the oldest batch information
    """

    def __init__(self, itemName, utility, batchSize, batchIndex):
        self.itemName = itemName
        self.utility = [0 for _ in range(batchSize)]
        self.children = dict()
        self.next = None
        self.batchIndex = batchIndex
        self.utility[batchIndex] = utility
        self.parent = None

    def addUtility(self, utility, batchIndex):
        """
        Adds utility to the node

        :param utility : Next utility value to be added

        :type utility : int

        :param batchIndex : Index of the batch with respect to window to which the node belongs

        :type batchIndex : int
        """

        self.utility[batchIndex] += utility

    def removeUtility(self, utility):
        """
        Removes utility from the node

        :param utility : Next utility value to be removed

        :type utility : int
        """

        self.utility -= utility

    def shiftUtility(self):
        """
        Shifts the utility values of the node to the left
        """

        self.utility.pop(0)
        self.utility.append(0)


class _HeaderTable:
    """
    A class used to represent the header table of the HUS tree

    :Attributes:

        table : dict
            dictionary of items as keys and list of utility and pointer to the node in the tree as values
            representing the header table

        orderedItems : list
            list of items in the header table in lexicographical order

    :Methods:

        updateUtility(item, utility, node)
            Updates the utility of the item with node pointer in the header table

        addUtility(item, utility)
            Adds utility to the item in the header table

        removeUtility(item, utility)
            Removes utility from the item in the header table

        itemOrdering()
            Orders the items in the header table in lexicographical order
    """

    def __init__(self):
        self.table = dict()
        self.orderedItems = list()

    def updateUtility(self, item, utility, node):
        """
        Updates the utility of the item in the header table

        :param item: name of the item to which utility needs to be updated

        :type item: str

        :param utility: Next utility of the item to be updated

        :type utility: int

        :param node: pointer to the node in the tree to which the item belongs

        :type node: _Node
        """

        if item in self.table:
            self.table[item][0] += utility
            tempNode = self.table[item][1]

            while tempNode.next is not None:
                tempNode = tempNode.next
            
            tempNode.next = node

        else:
            self.table[item] = [utility, node]
    
        self.itemOrdering()

    def addUtility(self, item, utility):
        """
        Adds utility to the item in the header table

        :param item: Name of the item to which utility needs to be added

        :type item: str

        :param utility: Next utility of the item to be added

        :type utility: int
        """
        self.table[item][0] += utility
    

    def removeUtility(self, item, utility):
        """
        Removes utility from the item in the header table

        :param item: Name of the item to which utility needs to be removed

        :type item: str

        :param utility: The utility of the item to be removed

        :type utility: int
        """
        self.table[item][0] -= utility

        if self.table[item][0] == 0:
            del self.table[item]

        self.itemOrdering()

    def itemOrdering(self):
        """
        Orders the items in the header table in lexicographical order
        """        
        self.orderedItems = list(sorted(self.table.keys()))

class _HUSTree:

    """
    A class used to represent the HUS tree

    :Attributes:

        root : _Node
            root node of the tree

        headerTable : _HeaderTable
            header table of the tree

        batchSize : int
            size of the batch

        windowSize : int
            size of the window

        batchIndex : int
            index of the current batch with respect to window

        windowUtility : int
            utility of the current window

    :Methods:

        addTransaction(transaction, utility)
            Adds transaction to the tree

        removeBatch()
            Removes the oldest batch from the tree

        removeBatchUtility()
            Removes the utility of the oldest batch from each subtree

    """

    def __init__(self, batchSize, windowSize):
        self.root = _Node(None, 0, batchSize, 0)
        self.headerTable = _HeaderTable()
        self.batchSize = batchSize
        self.windowSize = windowSize
        self.batchIndex = 0
        self.windowUtility = 0

    def addTransaction(self, transaction, utility):
        """
        Adds transaction to the tree

        :param transaction: list of items in the transaction

        :type transaction: list

        :param utility: Next utility of the transaction

        :type utility: int
        """
        transaction.sort(key = lambda x: x[0])
        currentNode = self.root
        self.windowUtility += utility
        for item in transaction:
            if item in currentNode.children:
                currentNode = currentNode.children[item]
                currentNode.addUtility(utility, self.batchIndex)
                self.headerTable.addUtility(item, utility)

            else:
                newNode = _Node(item, utility, self.batchSize, self.batchIndex)
                currentNode.children[item] = newNode
                newNode.parent = currentNode
                self.headerTable.updateUtility(item, utility, newNode)
                currentNode = newNode

    def removeBatch(self):

        """
        Removes the oldest batch from the tree
        """

        currentNode = self.root

        curChilds = list(currentNode.children.keys())

        for child in curChilds:
            self.windowUtility -= currentNode.children[child].utility[0]
            self.removeBatchUtility(currentNode.children[child])

            if sum(currentNode.children[child].utility) == 0:
                del currentNode.children[child]


    def removeBatchUtility(self, tempNode):
        
        """
        Removes the utility of the oldest batch from each subtree

        :param tempNode:  pointer to the node in the tree

        :type tempNode: _Node
        """
        if tempNode is None:
            return

        for item in tempNode.children:
            self.removeBatchUtility(tempNode.children[item])

        curBatchUtility = tempNode.utility[0]
        tempNode.shiftUtility()

        if sum(tempNode.utility) == 0:
            if tempNode.itemName in self.headerTable.table:
                curNode = self.headerTable.table[tempNode.itemName][1]

                if curNode == tempNode:
                    self.headerTable.table[tempNode.itemName][1] = tempNode.next

                else:
                    while curNode is not None and curNode.next is not tempNode:
                        curNode = curNode.next

                    if curNode is not None:
                        curNode.next = tempNode.next
        
        self.headerTable.removeUtility(tempNode.itemName, curBatchUtility)

        curChilds = list(tempNode.children.keys())
        for child in curChilds:
            if sum(tempNode.children[child].utility) == 0:
                del tempNode.children[child]

    
class HUPMS(_hus._highUtilityPatternStreamMining):
    """
    :Description:   High-utility pattern mining over data stream is one of the challenging problems in data stream mining.
                    HUPMS is an algorithm that discovers high-utility patterns from data streams without rebuilding the tree.
                    It stores the database of the cuurent window in form of HUSTree and adjusts the tree based on upcoming
                    transactions removing the oldest batch.

    :References:   Chowdhury Farhan Ahmed and Syed Khairuzzaman Tanbeer and Byeong-Soo Jeong and Ho-Jin Choi : Interactive
                   mining of high utility patterns over data streams. Expert Systems with Applications Vol 39, 11979 - 11991, 2012.
                   https://doi.org/10.1016/j.eswa.2012.03.062


    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility patterns in Streams
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility patterns in Streams
    :param minUtil: int :
                   Minimum utility threshold
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.



    :Attributes:

        __startTime : float
            start time of the mining process

        __endTime : float
            end time of the mining process

        _minUtil : str
            minimum utility threshold

        __finalPatterns : dict
            dictionary of the final patterns generated in each window

        _iFile : str
            input file name

        _oFile : str
            output file name

        _sep : str
            seperator of the input file

        __memoryUSS : float
            memory usage of the algorithm in user space

        __memoryRSS : float
            memory usage of the algorithm in resident set size

        __transactions : list
            list of transactions in the database

        __utilities : list
            list of utilities of each item of a transaction in the database

        __utilitySum : list
            list of utility sum of each transaction in the database

        __tree : _HUSTree
            HUS tree of the current window

        __windowSize : int
            The size of the sliding window. It specifies the number of panes to be considered for mining patterns.

        __paneSize : int
            The size of the pane. It specifies the number of transactions to be considered for mining in each pane.

    :Methods:

        _createItemsets()
            Storing the complete transactions of the database/input file in a transaction variable with their utilities.

        createPrefixBranch(root)
            Creates the prefix branch of the current HUS-Tree for construction of prefix tree

        fixUtility(root)
            Fixes the utility of the nodes in the tree by merging the utility values

        createConditionalTree(root, transactions, minUtil)
            Creates the conditional tree for the given prefix tree

        contains(superset, subset)
            Checks if the superset contains the subset

        treeGenerations(root, netUtil, candidatePattern, curItem)
            Generates the tree of the high utility patterns

        mine()
            Starts the mining process

        printTree(root, level)
            Prints the HUS-tree in a readable format

        getMemoryRSS()
            Returns the memory usage of the algorithm in resident set size

        getMemoryUSS()
            Returns the memory usage of the algorithm in user space

        getPatterns()
            Returns the final patterns generated in each window

        getPatternsAsDataFrame()
            Returns the final patterns generated in each window as a pandas dataframe

        getRuntime()
            Returns the runtime of the algorithm

        printResults()
            Prints the stats of the mining process

        save()
            Saves the patterns generated from each window in a file


    **Executing the code on terminal:**
    -------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 HUPMS.py <inputFile> <outputFile> <minUtil> <windowSize> <paneSize> <separator>

      Example Usage:

      (.venv) $ python3 HUPMS.py retail.txt output.txt 107 100 1000 ','

    .. note:: Here minimum utility is 107, Window size is 100 and pane size is 1000. The separator is comma for the input file

    **Credits:**
    -------------

    The code is written by Vipul Chhabra under the supervision of Prof. Rage Uday Kiran.
    
    """

    __startTime = float()
    __endTime = float()
    _minUtil = str()
    __finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    __memoryUSS = float()
    __memoryRSS = float()
    __transactions = []
    __utilities = []
    __utilitySum = []
    __tree = None
    __windowSize = 0
    __paneSize = 0

    def __init__(self, iFile, oFile, minUtil, windowSize, paneSize, sep = ","):
        super().__init__(iFile, minUtil, windowSize, paneSize, sep)
        self._oFile = oFile

    def _createItemsets(self):
        """
        Storing the complete transactions of the database/input file in a transaction variable
        """
        self._transactions, self._utilities, self._utilitySum = [], [], []
        if isinstance(self._iFile, _hus._pd.DataFrame):
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
            if _hus._validators.url(self._iFile):
                data = _hus._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    items = parts[0].split(self._sep)
                    self.__transactions.append([x for x in items if x])
                    utilities = parts[2].split(self._sep)
                    utilities = [float(x) for x in utilities]
                    self.__utilities.append(utilities)
                    self.__utilitySum.append(int(parts[1]))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            items = parts[0].split(self._sep)
                            self._transactions.append([x for x in items if x])
                            utilities = parts[2].split(self._sep)
                            utilities = [float(x) for x in utilities]
                            self._utilities.append(utilities)
                            self._utilitySum.append(float(parts[1]))
                except IOError:
                    print("File Not Found")
                    quit()

    def createPrefixBranch(self, root):
        """
        Creates the prefix branch of the node

        :param root: pointer to the root node of the sub-tree

        :type root: Node

        :return stack: list of the nodes in prefix branch

        :rtype: list

        :return curUtil: Utility of the prefix branch

        :rtype: int
        """
        stack = []

        while root is not None:
            stack.append(root)
            root = root.parent

        chosenItemset = stack[0]
        curUtil = sum(chosenItemset.utility)
        return stack, curUtil

    def fixUtility(self, root):
        """
        Fixes the utility of the nodes in the tree by merging the utility values

        :param root : pointer to the root node of the subtree

        :type root: Node
        """
        
        if root is None:
            return
        
        if len(root.utility) > 1:
            root.utility = [sum(root.utility)]

        for child in root.children:
            self.fixUtility(root.children[child])

    def createConditionalTree(self, root, transactions, minUtil):
        """
        Creates the conditional tree for the given prefix tree

        :param root: pointer to the root node of the prefix tree

        :type root: Node

        :param transactions: list of transactions in prefix tree

        :type transactions: list

        :param minUtil: minimum utility threshold

        :type minUtil: int


        :return tempTree: conditional tree for the given prefix tree

        :rtype: _HUSTree
        """
        
        for transaction in transactions:
            for item in transaction["transaction"]:
                if root.headerTable.table[item][0] < minUtil:
                    transaction["transaction"].remove(item)

        tempTree = _HUSTree(1, 1)
        for transaction in transactions:
            if len(transaction["transaction"]) != 0:
                tempTree.addTransaction(transaction["transaction"], transaction["utility"])

        self.fixUtility(tempTree.root)

        return tempTree
    
    def contains(self, superset, subset):
        """
        Checks if the superset contains the subset

        :param superset: list of items in the superset

        :type superset: list

        :param subset: list of items in the subset

        :type subset: list

        :return bool: True if the superset contains the subset, False otherwise

        :rtype: bool
        """
     
        return reduce(and_, [i in superset for i in subset])

    def treeGenerations(self, root, netUtil, candidatePattern, curItem = None):
        """
        Generates the tree of the high utility patterns

        :param root: pointer to the root of the tree

        :type root: _Node

        :param netUtil: Net utility of the transaction

        :type netUtil: int

        :param candidatePattern: Candidate patterns generated with utility

        :type candidatePattern: list

        :param curItem: list of items in the current itemsets

        :type curItem: list
        """

        if root is None:
            return


        for item in reversed(root.headerTable.orderedItems):
            if root.headerTable.table[item][0] >= netUtil:
                prefixBranches = []

                tempNode = root.headerTable.table[item][1]

                while tempNode is not None:
                    curPrefixBranch, curUtil = self.createPrefixBranch(tempNode)
                    prefixBranches.append([curPrefixBranch, curUtil])
                    tempNode = tempNode.next
                
                prefixTree = _HUSTree(1, 1)
                completeTransactions = []

                for branch in prefixBranches:
                    transaction = []
                    for node in reversed(branch[0][1:-1]):
                        transaction.append(node.itemName)

                    prefixTree.addTransaction(transaction, branch[1])

                    completeTransactions.append({"transaction" : transaction, "utility" : branch[1]})

                conditionalTree = self.createConditionalTree(prefixTree, completeTransactions, netUtil)

                newItemset = curItem.copy()
                newItemset.append(item)

                if len(newItemset) not in candidatePattern:
                    candidatePattern[len(newItemset)] = [newItemset]

                else:
                    candidatePattern[len(newItemset)].append(newItemset)

                if len(conditionalTree.headerTable.table) != 0:
                    self.treeGenerations(conditionalTree, netUtil, candidatePattern, newItemset)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        This function will start the mining process
        """
        self.mine()

    def mine(self):
        """
        This function will start the mining process
        """
        #global _minUtil
        self.__startTime = _hus._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minUtil is None:
            raise Exception("Please enter the Minimum Support")
        if self._windowSize is None:
            raise Exception("Please enter the Window Size")
        if self._paneSize is None:
            raise Exception("Please enter the Pane Size")
        self.__windowSize = int(self._windowSize)
        self.__paneSize = int(self._paneSize)

        self._createItemsets()
        self._minUtil = float(self._minUtil)
        self.__tree = _HUSTree(self.__windowSize, self.__paneSize)

        transactionwiseUtility = []

        for i in range(len(self._transactions)):
            curTrans = {}
            for j in range(len(self._transactions[i])):
                curTrans[self._transactions[i][j]] = self._utilities[i][j]
            transactionwiseUtility.append(curTrans)

        for i in range(0, self.__windowSize):
            self.__tree.batchIndex = i
            for j in range(0, self.__paneSize):
                self.__tree.addTransaction(self._transactions[i * self.__paneSize + j],
                                           self._utilitySum[i * self.__paneSize + j])

        startIndex = 0
        endIndex = self.__windowSize * self.__paneSize

        while endIndex <= len(self._transactions):

            filteredItemsets = {}

            self.treeGenerations(self.__tree, self._minUtil, filteredItemsets)

            results = []

            for itemSetLen in filteredItemsets:
                for itemSet in filteredItemsets[itemSetLen]:
                    itemSetUtility = 0
                    for transId in range(startIndex, endIndex):
                        if self.contains(list(transactionwiseUtility[transId].keys()), itemSet):
                            for item in itemSet:
                                itemSetUtility += transactionwiseUtility[transId][item]

                    if itemSetUtility >= self._minUtil:
                        results.append([itemSet, itemSetUtility])

            self.__finalPatterns[(startIndex, endIndex)] = results

            if endIndex >= len(self._transactions):
                break

            self.__tree.removeBatch()

            for i in range(0, self.__paneSize):
                self.__tree.addTransaction(self._transactions[endIndex + i], self._utilitySum[endIndex + i])

            startIndex += self.__paneSize
            endIndex += self.__paneSize

        self.__endTime = _hus._time.time()
        self.__memoryUSS = float()
        self.__memoryRSS = float()
        process = _hus._psutil.Process(_hus._os.getpid())
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss

    def printTree(self, root, level = 0):
        """
        Prints the tree in a readable format.

        :param root: CPSTreeNode object for the root of the tree

        :type root: _Node

        :param level: Current level of the root node

        :type level: int
        """

        print('  ' * level, level, root.itemName, root.utility, root.parent.itemName if root.parent else None )
        
        for child in root.children.values():
            self.printTree(child, level + 1)

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """
        return self.__memoryRSS

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """
        return self.__memoryUSS

    def getPatterns(self):
        """
        Returns the frequent patterns generated by the mining process over the complete datastream.

        :return: returning frequent patterns generated by the mining process
        :rtype: dict
        """
        return self.__finalPatterns

    def getPatternsAsDataFrame(self):
        """
        Stores the final patterns generated by the mining process in a dataframe.

        :return: returning dataframe containing the final patterns generated by the mining process
        :rtype: pandas.DataFrame
        """

        dataframe = {}
        data = []
        for x, y in self.__finalPatterns.items():
            for pattern in y:
                patternString = ' '.join(pattern[0])
                data.append([x[0], x[1], patternString, pattern[1]])
        dataframe = pd.DataFrame(data, columns=['Window Start Index', 'Window End Index', 'Pattern', 'Utility'])
        return dataframe

    def getRuntime(self):
        """
        Total amount of time taken by the mining process will be retrieved from this function

        :return: returning time taken by the mining process
        :rtype: float
        """

        return self.__endTime - self.__startTime

    def printResults(self):
        """
        Prints the results of the mining process
        """
        print("Total number of Windows Processed:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


    def save(self,):
        """
        Complete set of frequent patterns will be loaded in to an output file
        """
        print("Output file name", self._oFile)
        writer = open(self._oFile, 'w+')
        for x, y in self.__finalPatterns.items():
            writer.write("Window Start Index : %s , End Index : %s \n" % (x[0], x[1]))
            for pattern in y:
                patternString = '\t'.join(pattern[0])
                patternString += '\t' + ":" + '\t' + str(pattern[1])
                writer.write("%s \n" % patternString)


if __name__ == "__main__":
    _ap = str()
    if len(_hus._sys.argv) == 6 or len(_hus._sys.argv) == 7:
        if len(_hus._sys.argv) == 7:
            _ap = HUPMS(_hus._sys.argv[1], _hus._sys.argv[2], _hus._sys.argv[3], _hus._sys.argv[4], _hus._sys.argv[5], _hus._sys.argv[6])
        if len(_hus._sys.argv) == 6:
            _ap = HUPMS(_hus._sys.argv[1], _hus._sys.argv[2], _hus._sys.argv[3], _hus._sys.argv[4], _hus._sys.argv[5])
        _ap.mine()
        _ap.mine()
        print("Total number of Windows Processes:", len( _ap.getPatterns()))

        _ap.getPatternsAsDataFrame().to_csv("result.csv", index = False, sep='\t')
        _ap.save()
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
