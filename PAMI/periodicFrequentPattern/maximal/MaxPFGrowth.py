# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.periodicFrequentPattern.maximal import MaxPFGrowth as alg
#
#             obj = alg.MaxPFGrowth("../basic/sampleTDB.txt", "2", "6")
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(Patterns))
#
#             obj.save("patterns")
#
#             Df = obj.getPatternsAsDataFrame()
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


from PAMI.periodicFrequentPattern.maximal import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator

from PAMI.periodicFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated

#global maximalTree
_minSup = float()
_maxPer = float()
_lno = int()


class _Node(object):
    """
     A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int
            storing item of a node
        timeStamps : list
            To maintain the timestamps of Database at the end of the branch
        parent : node
            To maintain the parent of every node
        children : list
            To maintain the children of node

    :Methods:

        addChild(itemName)
            storing the children to their respective parent nodes
    """
    def __init__(self, item: int, children: list) -> None:
        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = []

    def addChild(self, node) -> None:
        """
        To add the children details to the parent node children list

        :param node: children node

        :return: adding to parent node children
        """
        self.children[node.item] = node
        node.parent = self


class _Tree(object):
    """
    A class used to represent the frequentPatternGrowth tree structure

    :Attributes:

        root : Node
            Represents the root node of the tree
        summaries : dictionary
            storing the nodes with same item name
        info : dictionary
            stores the support of items

    :Methods:

        addTransaction(Database)
            creating Database as a branch in frequentPatternTree
        getConditionPatterns(Node)
            generates the conditional patterns from tree for specific node
        conditionalTransaction(prefixPaths,Support)
            takes the prefixPath of a node and support at child of the path and extract the frequent items from
            prefixPaths and generates prefixPaths with items which are frequent
        remove(Node)
            removes the node from tree once after generating all the patterns respective to the node
        generatePatterns(Node)
            starts from the root node of the tree and mines the frequent patterns
    """
    def __init__(self) -> None:
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}
        #self.maximalTree = _MPTree()

    def addTransaction(self, transaction: List[Any], tid: List[int]) -> None:
        """
        adding transaction into database

        :param transaction: transactions in a database
        :param tid: timestamp of the transaction in database
        :return: pftree
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

    def getConditionalPatterns(self, alpha: Any) -> Tuple[List[List[Any]], List[List[int]], Dict[Any, List[int]]]:
        """
        to get the conditional patterns of a node

        :param alpha: node in the tree
        :return: conditional patterns of a node
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
        finalPatterns, finalSets, info = _conditionalTransactions(finalPatterns, finalSets)
        return finalPatterns, finalSets, info

    def removeNode(self, nodeValue: Any) -> None:
        """
        removes the leaf node by pushing its timestamps to parent node

        :param nodeValue: node of a tree
        :return: None
        """
        for i in self.summaries[nodeValue]:
            i.parent.timeStamps = i.parent.timeStamps + i.timeStamps
            del i.parent.children[nodeValue]
            i = None

    def getTimeStamps(self, alpha: Any) -> List[int]:
        """
        to get all the timestamps related to a node in tree

        :param alpha: node of a tree
        :return: timestamps of a node
        """
        temp = []
        for i in self.summaries[alpha]:
            temp += i.timeStamps
        return temp

    def generatePatterns(self, prefix: List[Any], patterns: Dict[Tuple[Any], Tuple[int, int]], maximalTree: Any) -> None:
        """
        To generate the maximal periodic frequent patterns

        :param prefix: an empty list of itemSet to form the combinations
        :param patterns: dictionary of patterns
        :param maximalTree: maximal Tree
        :return: maximal periodic frequent patterns
        """
        #global maximalTree
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x), -x)):
            pattern = prefix[:]
            pattern.append(i)
            condPattern, timeStamps, info = self.getConditionalPatterns(i)
            conditionalTree = _Tree()
            conditionalTree.info = info.copy()
            head = pattern[:]
            tail = []
            for k in info:
                tail.append(k)
            sub = head + tail
            if maximalTree.checkerSub(sub) == 1:
                for pat in range(len(condPattern)):
                    conditionalTree.addTransaction(condPattern[pat], timeStamps[pat])
                if len(condPattern) >= 1:
                    conditionalTree.generatePatterns(pattern, patterns, maximalTree)
                else:
                    maximalTree.addTransaction(pattern)
                    patterns[tuple(pattern)] = self.info[i]
            self.removeNode(i)


class _MNode(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int
            storing item of a node
        children : list
            To maintain the children of node

    :Methods:

        addChild(itemName)
            storing the children to their respective parent nodes
    """
    def __init__(self, item: Any, children: Dict[Any, Any]) -> None:
        self.item = item
        self.children = children

    def addChild(self, node: Any) -> None:
        """
        To add the children details to parent node children variable

        :param node: children node
        :return: adding children node to parent node
        """
        self.children[node.item] = node
        node.parent = self


class _MPTree(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        root : node
            the root of a tree
        summaries : dict
            to store the items with same name into dictionary

    :Methods:

        addTransaction(itemSet)
            the generated periodic-frequent pattern is added into maximal-tree
        checkerSub(itemSet)
            to check of subset of itemSet is present in tree
    """
    def __init__(self) -> None:
        self.root = _MNode(None, {})
        self.summaries = {}

    def addTransaction(self, transaction: List[Any]) -> None:
        """
        to add the transaction in maximal tree

        :param transaction: resultant periodic frequent pattern
        :return: maximal tree
        """
        currentNode = self.root
        transaction.sort()
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = _MNode(transaction[i], {})
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].insert(0, newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]

    def checkerSub(self, items: List[Any]) -> int:
        """
        To check subset present of items in the maximal tree

        :param items: the pattern to check for subsets
        :return: 1
        """
        items.sort(reverse=True)
        item = items[0]
        if item not in self.summaries:
            return 1
        else:
            if len(items) == 1:
                return 0
        for t in self.summaries[item]:
            cur = t.parent
            i = 1
            while cur.item is not None:
                if items[i] == cur.item:
                    i += 1
                    if i == len(items):
                        return 0
                cur = cur.parent
        return 1


#maximalTree = _MPTree()


def _getPeriodAndSupport(timeStamps: List[int]) -> List[Union[int, float]]:
    """
    To calculate the periodicity and support of a pattern with their respective timeStamps

    :param timeStamps: timeStamps
    :return: Support and periodicity
    """
    timeStamps.sort()
    cur = 0
    per = 0
    sup = 0
    for j in range(len(timeStamps)):
        per = max(per, timeStamps[j] - cur)
        if per > _maxPer:
            return [0, 0]
        cur = timeStamps[j]
        sup += 1
    per = max(per, abs(_lno - cur))
    return [sup, per]


def _conditionalTransactions(condPatterns: List[List[int]], condTimeStamps: List[List[int]]) -> Tuple[List[List[int]], List[List[int]], Dict[int, Tuple[int, float]]]:
    """
    To calculate the timestamps of conditional items in conditional patterns

    :param condPatterns: conditional patterns of node
    :param condTimeStamps: timeStamps of a conditional patterns
    :return: removing items with low minSup or periodicity and sort the conditional transactions
    """
    pat = []
    timeStamps = []
    data1 = {}
    for i in range(len(condPatterns)):
        for j in condPatterns[i]:
            if j in data1:
                data1[j] = data1[j] + condTimeStamps[i]
            else:
                data1[j] = condTimeStamps[i]
    updatedDict = {}
    for m in data1:
        updatedDict[m] = _getPeriodAndSupport(data1[m])
    updatedDict = {k: v for k, v in updatedDict.items() if v[0] >= _minSup and v[1] <= _maxPer}
    count = 0
    for p in condPatterns:
        p1 = [v for v in p if v in updatedDict]
        trans = sorted(p1, key=lambda x: (updatedDict.get(x)[0], -x), reverse=True)
        if len(trans) > 0:
            pat.append(trans)
            timeStamps.append(condTimeStamps[count])
        count += 1
    return pat, timeStamps, updatedDict


class MaxPFGrowth(_ab._periodicFrequentPatterns):
    """
    :Description:   MaxPF-Growth is one of the fundamental algorithm to discover maximal periodic-frequent
                    patterns in a temporal database.

    :Reference:   R. Uday Kiran, Yutaka Watanobe, Bhaskar Chaudhury, Koji Zettsu, Masashi Toyoda, Masaru Kitsuregawa,
                 "Discovering Maximal Periodic-Frequent Patterns in Very Large Temporal Databases",
                 IEEE 2020, https://ieeexplore.ieee.org/document/9260063

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  minSup: str:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  maxPer: float:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        minSup: int or float or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        maxPer: int or float or str
            The user can specify maxPer either in count or proportion of database size.
            If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxPer=10 will be treated as integer, while maxPer=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default separator is tab space or \t.
            However, the users can override their default separator.
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        Database : list
            To store the transactions of a database in list
        mapSupport : Dictionary
            To maintain the information of item and their frequency
        lno : int
            it represents the total no of transaction
        tree : class
            it represents the Tree class
        itemSetCount : int
            it represents the total no of patterns
        finalPatterns : dict
            it represents to store the patterns

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of periodic-frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of periodic-frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        creatingItemSets(fileName)
            Scans the dataset or dataframes and stores in list format
        PeriodicFrequentOneItem()
            Extracts the one-periodic-frequent patterns from Databases
        updateDatabases()
            update the Databases by removing aperiodic items and sort the Database by item decreased support
        buildTree()
            after updating the Databases ar added into the tree by setting root node as null
        mine()
            the main method to run the program

    **Executing the code on terminal:**
    -------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 maxpfrowth.py <inputFile> <outputFile> <minSup> <maxPer>

       Examples usage :

       (.venv) $ python3 maxpfrowth.py sampleTDB.txt patterns.txt 0.3 0.4


               .. note:: minSup will be considered in percentage of database transactions
            
    **Sample run of the imported code:**
    ------------------------------------------
    .. code-block:: python

            from PAMI.periodicFrequentPattern.maximal import MaxPFGrowth as alg

            obj = alg.MaxPFGrowth("../basic/sampleTDB.txt", "2", "6")

            obj.mine()

            Patterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(Patterns))

            obj.save("patterns")

            Df = obj.getPatternsAsDataFrame()
    
            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    ---------------
        The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.\n

    """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _rank = {}
    _rankedUp = {}
    _lno = 0
    _patterns = {}
    _maximalTree = str()

    def __init__(self, iFile: Any, minSup: Union[int, float, str], maxPer: Union[int, float, str], sep: str='\t') -> None:
        super().__init__(iFile, minSup, maxPer, sep)

    def _creatingItemSets(self) -> None:
        """
        Storing the complete Databases of the database/input file in a database variable
        :rtype: storing transactions into Database variable
        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            data, ts = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                ts = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            for i in range(len(data)):
                tr = [ts[i][0]] + data[i]
                self._Database.append(tr)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
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

    def _periodicFrequentOneItem(self) -> Dict[Any, List[Union[int, float]]]:
        """
        calculates the support of each item in the dataset and assign the ranks to the items
        by decreasing support and returns the frequent items list

        :rtype: return the one-length periodic frequent patterns

        """
        data = {}
        for tr in self._Database:
            for i in range(1, len(tr)):
                if tr[i] not in data:
                    data[tr[i]] = [int(tr[0]), int(tr[0]), 1]
                else:
                    data[tr[i]][0] = max(data[tr[i]][0], (int(tr[0]) - data[tr[i]][1]))
                    data[tr[i]][1] = int(tr[0])
                    data[tr[i]][2] += 1
        for key in data:
            data[key][0] = max(data[key][0], abs(len(self._Database) - data[key][1]))
        data = {k: [v[2], v[0]] for k, v in data.items() if v[0] <= self._maxPer and v[2] >= self._minSup}
        pfList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        return data

    def _updateDatabases(self, dict1: Dict[Any, List[Union[int, float]]]) -> List[List[Union[int, float]]]:
        """
        Remove the items which are not frequent from Databases and updates the Databases with rank of items

        :param dict1: frequent items with support
        :type dict1: dictionary
        :rtype: sorted and updated transactions
        """
        list1 = []
        for tr in self._Database:
            list2 = [int(tr[0])]
            for i in range(1, len(tr)):
                if tr[i] in dict1:
                    list2.append(self._rank[tr[i]])
            if len(list2) >= 2:
                basket = list2[1:]
                basket.sort()
                list2[1:] = basket[0:]
                list1.append(list2)
        return list1

    @staticmethod
    def _buildTree(data: List[List[Union[int, float]]], info: Dict[Any, List[Union[int, float]]]) -> Any:
        """
        it takes the Databases and support of each item and construct the main tree with setting root node as null

        :param data: it represents the one Databases in database
        :type data: list
        :param info: it represents the support of each item
        :type info: dictionary
        :rtype: returns root node of tree
        """

        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            set1 = [data[i][0]]
            rootNode.addTransaction(data[i][1:], set1)
        return rootNode

    def _savePeriodic(self, itemSet: List[Any]) -> List[Any]:
        """
        To convert the ranks of items in to their original item names

        :param itemSet: frequent pattern.
        :return: frequent pattern with original item names
        """
        t1 = []
        for i in itemSet:
            t1.append(self._rankedUp[i])
        return t1

    def _convert(self, value: Union[int, float, str]) -> Union[int, float]:
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
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

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """

        global _minSup, _maxPer, _lno
        self._patterns = {}
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        _minSup, _maxPer, _lno = self._minSup, self._maxPer, len(self._Database)
        if self._minSup > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
        _generatedItems = self._periodicFrequentOneItem()
        _updatedDatabases = self._updateDatabases(_generatedItems)
        for x, y in self._rank.items():
            self._rankedUp[y] = x
        _info = {self._rank[k]: v for k, v in _generatedItems.items()}
        _Tree = self._buildTree(_updatedDatabases, _info)
        self._finalPatterns = {}
        self._maximalTree = _MPTree()
        _Tree.generatePatterns([], self._patterns, self._maximalTree)
        for x, y in self._patterns.items():
            pattern = str()
            x = self._savePeriodic(x)
            for i in x:
                pattern = pattern + i + " "
            self._finalPatterns[pattern] = y
        self._endTime = _ab._time.time()
        _process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = _process.memory_full_info().uss
        self._memoryRSS = _process.memory_info().rss
        print("Maximal Periodic Frequent patterns were generated successfully using MAX-PFPGrowth algorithm ")

    def mine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """

        global _minSup, _maxPer, _lno
        self._patterns = {}
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        _minSup, _maxPer, _lno = self._minSup, self._maxPer, len(self._Database)
        if self._minSup > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
        _generatedItems = self._periodicFrequentOneItem()
        _updatedDatabases = self._updateDatabases(_generatedItems)
        for x, y in self._rank.items():
            self._rankedUp[y] = x
        _info = {self._rank[k]: v for k, v in _generatedItems.items()}
        _Tree = self._buildTree(_updatedDatabases, _info)
        self._finalPatterns = {}
        self._maximalTree = _MPTree()
        _Tree.generatePatterns([], self._patterns, self._maximalTree)
        for x, y in self._patterns.items():
            pattern = str()
            x = self._savePeriodic(x)
            for i in x:
                pattern = pattern + i + " "
            self._finalPatterns[pattern] = y
        self._endTime = _ab._time.time()
        _process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = _process.memory_full_info().uss
        self._memoryRSS = _process.memory_info().rss
        print("Maximal Periodic Frequent patterns were generated successfully using MAX-PFPGrowth algorithm ")


    def getMemoryUSS(self) -> float:
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self) -> float:
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self) -> float:
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete set of periodic-frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.replace(' ', '\t').strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, Tuple[int, int]]:
        """
        Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        print("Total number of Maximal Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = MaxPFGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = MaxPFGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Maximal Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        for i in [100, 200, 300, 400, 500]:
            _ap =  MaxPFGrowth('/Users/Likhitha/Downloads/temporal_T10I4D100K.csv', i, 5000, '\t')
            _ap.mine()
            print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
            _ap.save('/Users/Likhitha/Downloads/output.txt')
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
