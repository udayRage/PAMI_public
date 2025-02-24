# WFRIMiner is one of the fundamental algorithm to discover weighted frequent regular patterns in a transactional database. It stores the database in compressed WFRI-tree decreasing the memory usage and extracts the patterns from tree.It employs downward closure property to  reduce the search space effectively.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.weightedFrequentRegularPattern.basic import WFRIMiner as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.WFRIMiner(iFile, WS, regularity)
#
#             obj.mine()
#
#             weightedFrequentRegularPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(weightedFrequentRegularPatterns))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternInDataFrame()
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
"""

from PAMI.weightedFrequentRegularPattern.basic import abstract as _fp
import pandas as pd
from deprecated import deprecated
from typing import List, Dict


_WS = str()
_regularity = str()
_lno = int()
_weights = {}
_wf = {}
_fp._sys.setrecursionlimit(20000)


class _Node:
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        itemId: int
            storing item of a node

        counter: int
            To maintain the support of node

        parent: node
            To maintain the parent of node

        children: list
            To maintain the children of node

    :Methods:

        addChild(node)
            Updates the nodes children list and parent for the given node

    """

    def __init__(self, item: int, children: dict) -> None:
        """
        Initializing the Node class

        :param item: Storing the item of a node
        :type item: int or None
        :param children: To maintain the children of a node
        :type children: dict
        :return: None
        """

        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = []

    def addChild(self, node) -> None:
        """
        To add the children to a node

        :param node: parent node in the tree
        :return: None
        """

        self.children[node.item] = node
        node.parent = self


class _Tree:
    """
    A class used to represent the frequentPatternGrowth tree structure

    :Attributes:

        root : Node
            The first node of the tree set to Null.

        summaries : dictionary
            Stores the nodes itemId which shares same itemId

        info : dictionary
            frequency of items in the transactions

    :Methods:
        addTransaction(transaction, freq)
            adding items of  transactions into the tree as nodes and freq is the count of nodes
        getFinalConditionalPatterns(node)
            getting the conditional patterns from fp-tree for a node
        getConditionalPatterns(patterns, frequencies)
            sort the patterns by removing the items with lower minSup
        generatePatterns(prefix)
            generating the patterns from fp-tree
    """

    def __init__(self) -> None:
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction: list, tid: list) -> None:
        """
        Adding a transaction into tree

        :param transaction: To represent the complete database
        :type transaction: list
        :param tid: To represent the timestamp of a database
        :type tid: list
        :return: pfp-growth tree
        """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = _Node(transaction[i], {})
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
        currentNode.timeStamps = currentNode.timeStamps + tid

    def getConditionalPatterns(self, alpha, pattern) -> tuple:
        """
        Generates all the conditional patterns of a respective node

        :param alpha: To represent a Node in the tree
        :type alpha: Node
        :param pattern: prefix of the pattern
        :type alpha: list
        :return: A tuple consisting of finalPatterns, conditional pattern base and information
        """
        finalPatterns = []
        finalSets = []
        for i in self.summaries[alpha]:
            set1 = i.timeStamps
            set2 = []
            while i.parent.item is not None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                finalSets.append(set1)
        finalPatterns, finalSets, info = self.conditionalDatabases(finalPatterns, finalSets, pattern)
        return finalPatterns, finalSets, info

    @staticmethod
    def generateTimeStamps(node) -> list:
        """
        To get the timestamps of a node

        :param node: A node in the tree
        :return: Timestamps of a node
        """

        finalTimeStamps = node.timeStamps
        return finalTimeStamps

    def removeNode(self, nodeValue) -> None:
        """
        Removing the node from tree

        :param nodeValue: To represent a node in the tree
        :type nodeValue: node
        :return: Tree with their nodes updated with timestamps
        """

        for i in self.summaries[nodeValue]:
            i.parent.timeStamps = i.parent.timeStamps + i.timeStamps
            del i.parent.children[nodeValue]

    def getTimeStamps(self, alpha) -> list:
        """
        To get all the timestamps of the nodes which share same item name

        :param alpha: Node in a tree
        :return: Timestamps of a  node
        """
        temporary = []
        for i in self.summaries[alpha]:
            temporary += i.timeStamps
        return temporary

    @staticmethod
    def getSupportAndPeriod(timeStamps: list, pattern: list) -> list:
        """
        To calculate the periodicity and support

        :param timeStamps: Timestamps of an item set
        :type timeStamps: list
        :param pattern: pattern to evaluate the weighted frequent regular or not
        :type pattern: list
        :return: support, periodicity
        """
        global _WS, _regularity, _lno, _weights
        timeStamps.sort()
        cur = 0
        per = list()
        sup = 0
        for j in range(len(timeStamps)):
            per.append(timeStamps[j] - cur)
            cur = timeStamps[j]
            sup += 1
        per.append(_lno - cur)
        l = int()
        for i in pattern:
            l = l + _weights[i]
        wf = (l / (len(pattern))) * sup
        if len(per) == 0:
            return [0, 0]
        return [sup, max(per), wf]

    def conditionalDatabases(self, conditionalPatterns: list, conditionalTimeStamps: list, pattern: list) -> tuple:
        """
        It generates the conditional patterns with periodic-frequent items

        :param conditionalPatterns: conditionalPatterns generated from conditionPattern method of a respective node
        :type conditionalPatterns: list
        :param conditionalTimeStamps: Represents the timestamps of a conditional patterns of a node
        :type conditionalTimeStamps: list
        :param pattern: prefix of the pattern
        :type pattern: list
        :returns: Returns conditional transactions by removing non-periodic and non-frequent items
        """
        global _WS, _regularity
        pat = []
        timeStamps = []
        data1 = {}
        for i in range(len(conditionalPatterns)):
            for j in conditionalPatterns[i]:
                if j in data1:
                    data1[j] = data1[j] + conditionalTimeStamps[i]
                else:
                    data1[j] = conditionalTimeStamps[i]
        updatedDictionary = {}
        for m in data1:
            updatedDictionary[m] = self.getSupportAndPeriod(data1[m], pattern + [m])
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v[0] >= _WS and v[1] <= _regularity}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDictionary]
            trans = sorted(p1, key=lambda x: (updatedDictionary.get(x)[0], -x), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                timeStamps.append(conditionalTimeStamps[count])
            count += 1
        return pat, timeStamps, updatedDictionary

    def generatePatterns(self, prefix: list):
        """
        Generates the patterns

        :param prefix: Forms the combination of items
        :type prefix: list
        :returns: yields patterns with their support and periodicity
        """
        global _WS
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x)[0], -x)):
            pattern = prefix[:]
            pattern.append(i)
            if self.info[i][2] >= _WS:
                yield pattern, self.info[i]
                patterns, timeStamps, info = self.getConditionalPatterns(i, pattern)
                conditionalTree = _Tree()
                conditionalTree.info = info.copy()
                for pat in range(len(patterns)):
                    conditionalTree.addTransaction(patterns[pat], timeStamps[pat])
                if len(patterns) > 0:
                    for q in conditionalTree.generatePatterns(pattern):
                        yield q
            self.removeNode(i)


class WFRIMiner(_fp._weightedFrequentRegularPatterns):
    """
    About this algorithm
    ====================

    :Description: WFRIMiner is one of the fundamental algorithm to discover weighted frequent regular patterns in a transactional database.
       * It stores the database in compressed WFRI-tree decreasing the memory usage and extracts the patterns from tree.It employs downward closure property to  reduce the search space effectively.

    :Reference:  K. Klangwisan and K. Amphawan, "Mining weighted-frequent-regular itemsets from transactional database,"
                 2017 9th International Conference on Knowledge and Smart Technology (KST), 2017, pp. 66-71,
                 doi: 10.1109/KST.2017.7886090.

    :param  iFile: str :
                   Name of the Input file to mine complete set of Weighted Frequent Regular Patterns.
    :param  oFile: str :
                   Name of the output file to store complete set of Weighted Frequent Regular Patterns.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    :param  wFile: str :
                   This is a weighted file.



    :Attributes:

        iFile : file
            Input file name or path of the input file

        WS: float or int or str
            The user can specify WS either in count or proportion of database size.
            If the program detects the data type of WS is integer, then it treats WS is expressed in count.
            Otherwise, it will be treated as float.
            Example: WS=10 will be treated as integer, while WS=10.0 will be treated as float

        regularity: float or int or str
            The user can specify regularity either in count or proportion of database size.
            If the program detects the data type of regularity is integer, then it treats regularity is expressed in count.
            Otherwise, it will be treated as float.
            Example: regularity=10 will be treated as integer, while regularity=10.0 will be treated as float

        sep : str
            This variable is used to distinguish items from one another in a transaction. The default separator is tab space or \t.
            However, the users can override their default separator.

        oFile : file
            Name of the output file or the path of the output file

        startTime:float
            To record the start time of the mining process

        endTime:float
            To record the completion time of the mining process

        memoryUSS : float
            To store the total amount of USS memory consumed by the program

        memoryRSS : float
            To store the total amount of RSS memory consumed by the program

        Database : list
            To store the transactions of a database in list

        mapSupport : Dictionary
            To maintain the information of item and their frequency

        lno : int
            it represents the total no of transactions

        tree : class
            it represents the Tree class

        finalPatterns : dict
            it represents to store the patterns

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
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
        creatingItemSets()
            Scans the dataset or dataframes and stores in list format
        frequentOneItem()
            Extracts the one-frequent patterns from transactions


    Execution methods
    =================


    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 WFRIMiner.py <inputFile> <outputFile> <weightSupport> <regularity>

      Example Usage:

      (.venv) $ python3 WFRIMiner.py sampleDB.txt patterns.txt 10 5

    .. note:: WS & regularity will be considered in support count or frequency


    **Calling from a python program**

    .. code-block:: python

            from PAMI.weightedFrequentRegularpattern.basic import WFRIMiner as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.WFRIMiner(iFile, WS, regularity)

            obj.mine()

            weightedFrequentRegularPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(weightedFrequentRegularPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    Credits
    =======

             The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _WS = str()
    _regularity = str()
    _weight = {}
    _finalPatterns = {}
    _wFile = " "
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}
    _lno = 0
    _tree = _Tree()
    _rank = {}
    _rankDup = {}

    def __init__(self, iFile, _wFile, WS, regularity, sep='\t') -> None:
        super().__init__(iFile, _wFile, WS, regularity, sep)

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable

        :return: None
        """
        self._Database = []
        self._weight = {}
        if isinstance(self._iFile, _fp._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()

        if isinstance(self._wFile, _fp._pd.DataFrame):
            _items, _weights = [], []
            if self._wFile.empty:
                print("its empty..")
            i = self._wFile.columns.values.tolist()
            if 'items' in i:
                _items = self._wFile['items'].tolist()
            if 'weight' in i:
                _weights = self._wFile['weight'].tolist()
            for i in range(len(_items)):
                self._weight[_items[i]] = _weights[i]

            # print(self.Database)
        if isinstance(self._iFile, str):
            if _fp._validators.url(self._iFile):
                data = _fp._urlopen(self._iFile)
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

        if isinstance(self._wFile, str):
            if _fp._validators.url(self._wFile):
                data = _fp._urlopen(self._wFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._weight[temp[0]] = float(temp[1])
            else:
                try:
                    with open(self._wFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._weight[temp[0]] = float(temp[1])
                except IOError:
                    print("File Not Found")
                    quit()

    def _convert(self, value) -> float:
        """
        To convert the type of user specified minSup value

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

    def _frequentOneItem(self) -> List[str]:
        """
        Generating One frequent items sets

        :return: list
        """
        global _lno, _wf, _weights
        self._mapSupport = {}
        _owf = {}
        for tr in self._Database:
            for i in range(1, len(tr)):
                if tr[i] not in self._mapSupport:
                    self._mapSupport[tr[i]] = [int(tr[0]), int(tr[0]), 1]
                else:
                    self._mapSupport[tr[i]][0] = max(self._mapSupport[tr[i]][0], (int(tr[0]) - self._mapSupport[tr[i]][1]))
                    self._mapSupport[tr[i]][1] = int(tr[0])
                    self._mapSupport[tr[i]][2] += 1
        for key in self._mapSupport:
            self._mapSupport[key][0] = max(self._mapSupport[key][0], abs(len(self._Database) - self._mapSupport[key][1]))
        _lno = len(self._Database)
        self._mapSupport = {k: [v[2], v[0]] for k, v in self._mapSupport.items() if v[0] <= self._regularity}
        for x, y in self._mapSupport.items():
            if self._weight.get(x) is None:
                self._weight[x] = 0
        gmax = max([self._weight[values] for values in self._mapSupport.keys()])
        for x, y in self._mapSupport.items():
            _owf[x] = y[0] * gmax
        self._mapSupport = {k: v for k, v in self._mapSupport.items() if v[0] * _owf[k] >= self._WS}
        for x, y in self._mapSupport.items():
            temp = self._weight[x] * y[0]
            _wf[x] = temp
            self._mapSupport[x].append(temp)
        genList = [k for k, v in sorted(self._mapSupport.items(), key=lambda x: x[1], reverse= True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(genList)])
        for x, y in self._rank.items():
            _weights[y] = self._weight[x]
        return genList

    def _updateTransactions(self, itemSet) -> List[List[int]]:
        """
        Updates the items in transactions with rank of items according to their support

        :Example: oneLength = {'a':7, 'b': 5, 'c':'4', 'd':3}
                  rank = {'a':0, 'b':1, 'c':2, 'd':3}

        :param itemSet: list of one-frequent items
        :return: None
        """
        list1 = []
        for tr in self._Database:
            list2 = [int(tr[0])]
            for i in range(1, len(tr)):
                if tr[i] in itemSet:
                    list2.append(self._rank[tr[i]])
            if len(list2) >= 2:
                basket = list2[1:]
                basket.sort()
                list2[1:] = basket[0:]
                list1.append(list2)
        return list1

    @staticmethod
    def _buildTree(transactions, info) -> _Tree:
        """
        Builds the tree with updated transactions

        :param transactions: updated transactions
        :param info: support details of each item in transactions
        :return: transactions compressed in fp-tree

        """
        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(transactions)):
            set1 = [transactions[i][0]]
            rootNode.addTransaction(transactions[i][1:], set1)
        return rootNode

    def _savePeriodic(self, itemSet) -> str:
        """
        The duplication items and their ranks

        :param itemSet: frequent itemSet that generated
        :return: patterns with original item names.

        """
        temp = str()
        for i in itemSet:
            temp = temp + self._rankDup[i] + "\t"
        return temp

    @deprecated(
        "It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self) -> None:
        """
        Frequent pattern mining process will start from here
        """
        global _WS, _regularity, _weights
        self._startTime = _fp._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._WS is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._WS = self._convert(self._WS)
        self._regularity = self._convert(self._regularity)
        _WS, _regularity, _weights = self._WS, self._regularity, self._weight
        itemSet = self._frequentOneItem()
        updatedTransactions = self._updateTransactions(itemSet)
        for x, y in self._rank.items():
            self._rankDup[y] = x
        info = {self._rank[k]: v for k, v in self._mapSupport.items()}
        _Tree = self._buildTree(updatedTransactions, info)
        patterns = _Tree.generatePatterns([])
        self._finalPatterns = {}
        for k in patterns:
            s = self._savePeriodic(k[0])
            self._finalPatterns[str(s)] = k[1]
        print("Weighted Frequent Regular patterns were generated successfully using WFRIM algorithm")
        self._endTime = _fp._time.time()
        self._memoryUSS = float()
        self._memoryRSS = float()
        process = _fp._psutil.Process(_fp._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

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

    def getPatternsAsDataFrame(self) -> _fp._pd.DataFrame:
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataframe = _fp._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

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
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, float]:
        """

        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of  Weighted Frequent Regular Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_fp._sys.argv) == 6 or len(_fp._sys.argv) == 7:
        if len(_fp._sys.argv) == 7:
            _ap = WFRIMiner(_fp._sys.argv[1], _fp._sys.argv[3], _fp._sys.argv[4], _fp._sys.argv[5], _fp._sys.argv[6])
        if len(_fp._sys.argv) == 5:
            _ap = WFRIMiner(_fp._sys.argv[1], _fp._sys.argv[3], _fp._sys.argv[4], _fp._sys.argv[5])
        _ap.mine()
        _ap.mine()
        print("Total number of Weighted Frequent Regular Patterns:", len(_ap.getPatterns()))
        _ap.save(_fp._sys.argv[2])
        print("Total Memory in USS:",  _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
