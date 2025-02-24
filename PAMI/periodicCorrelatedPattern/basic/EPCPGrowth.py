# EPCPGrowth is an algorithm to discover periodic-Correlated patterns in a temporal database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#     from PAMI.periodicCorrelatedPattern.basic import EPCPGrowth as alg
#
#     obj = alg.EPCPGrowth(iFile, minSup, minAllCOnf, maxPer, maxPerAllConf)
#
#     obj.mine()
#
#     periodicCorrelatedPatterns = obj.getPatterns()
#
#     print("Total number of Periodic Frequent Patterns:", len(periodicCorrelatedPatterns))
#
#     obj.save(oFile)
#
#     Df = obj.getPatternsAsDataFrame()
#
#     memUSS = obj.getMemoryUSS()
#
#     print("Total Memory in USS:", memUSS)
#
#     memRSS = obj.getMemoryRSS()
#
#     print("Total Memory in RSS", memRSS)
#
#     run = obj.getRuntime()
#
#     print("Total ExecutionTime in seconds:", run)
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


import sys

from PAMI.periodicCorrelatedPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
import pandas as pd

_maxPer = float()
_minAllConf = float()
_minSup = float()
_maxPerAllConf = float()
_frequentList = {}
_lno = int()


class _Node(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int or None
            Storing item of a node
        timeStamps : list
            To maintain the timestamps of a database at the end of the branch
        parent : node
            To maintain the parent of every node
        children : list
            To maintain the children of a node

    :Methods:

        addChild(itemName)
            Storing the children to their respective parent nodes
        """

    def __init__(self, item, children) -> None:
        """
        Initializing the Node class

        :param item: Storing the item of a node
        :type item: int or None
        :param children: To maintain the children of a node
        :type children: dict
        """

        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = []

    def addChild(self, node) -> None:
        """
        To add the children to a node

        :param node: parent node in the tree
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
            Storing the nodes with same item name
        info : dictionary
            Stores the support of the items


    :Methods:

        addTransactions(Database)
            Creating transaction as a branch in frequentPatternTree
        getConditionalPatterns(Node)
            Generates the conditional patterns from tree for specific node
        conditionalTransaction(prefixPaths,Support)
            Takes the prefixPath of a node and support at child of the path and extract the frequent patterns from
            prefixPaths and generates prefixPaths with items which are frequent
        remove(Node)
            Removes the node from tree once after generating all the patterns respective to the node
        generatePatterns(Node)
            Starts from the root node of the tree and mines the periodic-frequent patterns

    """

    def __init__(self) -> None:
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction, tid) -> None:
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
        :param pattern: pattern
        :type pattern: list
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
    def getSupportAndPeriod(timeStamps, pattern) -> list:
        """
        To calculate the periodicity and support

        :param timeStamps: Timestamps of an item set
        :param pattern: pattern
        :return: support, periodicity
        """

        global _minSup, _minAllConf, _maxPer, _maxPerAllConf, _frequentList, _lno
        timeStamps.sort()
        cur = 0
        per = list()
        sup = 0
        for j in range(len(timeStamps)):
            per.append(timeStamps[j] - cur)
            cur = timeStamps[j]
            sup += 1
        per.append(_lno - cur)
        if len(per) == 0:
            return [0, 0, 0, 0]
        l = []
        for i in pattern:
            l.append(_frequentList[i][0])
        l1 = []
        for i in pattern:
            l1.append(_frequentList[i][1])
        conf = sup/max(l)
        perConf = max(per)/min(l1)
        #print(pattern, timeStamps, l, l1, sup, max(per), conf, perConf)
        return [sup, max(per), conf, perConf]

    def conditionalDatabases(self, conditionalPatterns: list, conditionalTimeStamps: list, pattern) -> tuple:
        """
        It generates the conditional patterns with periodic-frequent items

        :param conditionalPatterns: conditionalPatterns generated from conditionPattern method of a respective node
        :type conditionalPatterns: list
        :param conditionalTimeStamps: Represents the timestamps of a conditional patterns of a node
        :type conditionalTimeStamps: list
        :param pattern: pattern
        :type pattern: list
        :returns: Returns conditional transactions by removing non-periodic and non-frequent items
        """
        global _maxPer, _minSup
        temp = pattern
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
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v[0] >= _minSup and v[1] <= _maxPer}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDictionary]
            trans = sorted(p1, key=lambda x: (updatedDictionary.get(x)[0], -x), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                timeStamps.append(conditionalTimeStamps[count])
            count += 1
        return pat, timeStamps, updatedDictionary

    def generatePatterns(self, prefix: list) -> Generator:
        """
        Generates the patterns

        :param prefix: Forms the combination of items
        :type prefix: list
        :returns: yields patterns with their support and periodicity
        """
        global _minSup, _minAllConf, _maxPer, _maxPerAllConf
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x)[0], -x)):
            pattern = prefix[:]
            pattern.append(i)
            #print(pattern, self.info[i][0], self.info[i][1], self.info[i][2], self.info[i][3])
            if self.info[i][0] >= _minSup and self.info[i][1] <= _maxPer and self.info[i][2] >= _minAllConf and self.info[i][3] <= _maxPerAllConf:
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


class EPCPGrowth(_ab._periodicCorrelatedPatterns):
    """
    :Description:   EPCPGrowth is an algorithm to discover periodic-Correlated patterns in a temporal database.

    :Reference:   http://www.tkl.iis.u-tokyo.ac.jp/new/uploads/publication_file/file/897/Venkatesh2018_Chapter_DiscoveringPeriodic-Correlated.pdf

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        minSup : int or float or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        minAllConf : int or float or str
            The user can specify minAllConf either in count or proportion of database size.
            If the program detects the data type of minAllConf is integer, then it treats minAllCOnf is expressed in count.
            Otherwise, it will be treated as float.
            Example: minAllCOnf=10 will be treated as integer, while minAllConf=10.0 will be treated as float
        maxPer : int or float or str
            The user can specify maxPer either in count or proportion of database size.
            If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxPer=10 will be treated as integer, while maxPer=10.0 will be treated as float
        maxPerAllConf : int or float or str
            The user can specify maxPerAllConf either in count or proportion of database size.
            If the program detects the data type of maaxPerAllConf is integer, then it treats maxPerAllConf is expressed in count.
            Otherwise, it will be treated as float.
            Example : maxPerAllConf=10 will be treated as integer, while maxPerAllConf=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime : float
            To record the start time of the mining process
        endTime : float
            To record the completion time of the mining process
        Database : list
            To store the transactions of a database in list
        mapSupport : Dictionary
            To maintain the information of item and their frequency
        lno : int
            To represent the total no of transaction
        tree : class
            To represents the Tree class
        itemSetCount : int
            To represents the total no of patterns
        finalPatterns : dict
            To store the complete patterns

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
            Scans the dataset and stores in a list format
        PeriodicFrequentOneItem()
            Extracts the one-periodic-frequent patterns from database
        updateDatabases()
            Update the database by removing aperiodic items and sort the Database by item decreased support
        buildTree()
            After updating the Database, remaining items will be added into the tree by setting root node as null
        convert()
            to convert the user specified value

    **Executing the code on terminal:**
    ---------------------------------------
        Format:
                    >>> python3 PFPGrowth.py <inputFile> <outputFile> <minSup> <maxPer>

        Examples:
                    >>> python3 PFPGrowth.py sampleTDB.txt patterns.txt 0.3 0.4

    **Sample run of importing the code:**
    ----------------------------------------
    .. code-block:: python

        from PAMI.periodicCorrelatedPattern.basic import EPCPGrowth as alg

        obj = alg.EPCPGrowth(iFile, minSup, minAllCOnf, maxPer, maxPerAllConf)

        obj.mine()

        periodicCorrelatedPatterns = obj.getPatterns()

        print("Total number of Periodic Frequent Patterns:", len(periodicCorrelatedPatterns))

        obj.save(oFile)

        Df = obj.getPatternsAsDataFrame()

        memUSS = obj.getMemoryUSS()

        print("Total Memory in USS:", memUSS)

        memRSS = obj.getMemoryRSS()

        print("Total Memory in RSS", memRSS)

        run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)

    **Credits:**
    --------------
        The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.\n

    """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _minAllCOnf = float()
    _maxPer = float()
    _maxPerAllConf = float()
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

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
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
                tr = [ts[i][0]]
                tr = tr + data[i]
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

    def _periodicFrequentOneItem(self) -> tuple:
        """
        Calculates the support of each item in the database and assign ranks to the items
        by decreasing support and returns the frequent items list

        :returns: return the one-length periodic frequent patterns
        """
        global _frequentList
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
        data = {k: [v[2], v[0], 1, 1] for k, v in data.items() if v[0] <= self._maxPer and v[2] >= self._minSup}
        pfList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        for x, y in self._rank.items():
            _frequentList[y] = data[x]
        return data, pfList

    def _updateDatabases(self, dict1) -> list:
        """
        Remove the items which are not frequent from database and updates the database with rank of items

        :param dict1: frequent items with support
        :type dict1: dictionary
        :return: Sorted and updated transactions
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
    def _buildTree(data, info) -> _Tree:
        """
        It takes the database and support of each item and construct the main tree by setting root node as a null

        :param data: it represents the one Database in database
        :type data: list
        :param info: it represents the support of each item
        :type info: dictionary
        :return: returns root node of tree
        """

        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            set1 = [data[i][0]]
            rootNode.addTransaction(data[i][1:], set1)
        return rootNode

    def _savePeriodic(self, itemSet) -> str:
        """
        To convert the ranks of items in to their original item names

        :param itemSet: frequent pattern.
        :return: frequent pattern with original item names
        """
        t1 = str()
        for i in itemSet:
            t1 = t1 + self._rankedUp[i] + "\t"
        return t1

    def _convert(self, value) -> float:
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

    def startMine(self) -> None:
        """
        Mining process will start from this function
        """

        global _minSup, _maxPer, _minAllConf, _maxPerAllConf, _lno
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._minAllConf = float(self._minAllConf)
        self._maxPer = self._convert(self._maxPer)
        self._maxPerAllConf = float(self._maxPerAllConf)
        _minSup, _minAllConf, _maxPer, _maxPerAllConf, _lno = self._minSup, self._minAllConf,  self._maxPer, self._maxPerAllConf, len(self._Database)
        #print(_minSup, _minAllConf, _maxPer, _maxPerAllConf)
        if self._minSup > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
        generatedItems, pfList = self._periodicFrequentOneItem()
        updatedDatabases = self._updateDatabases(generatedItems)
        for x, y in self._rank.items():
            self._rankedUp[y] = x
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedDatabases, info)
        patterns = Tree.generatePatterns([])
        self._finalPatterns = {}
        for i in patterns:
            sample = self._savePeriodic(i[0])
            self._finalPatterns[sample] = i[1]
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Correlated Periodic-Frequent patterns were generated successfully using EPCPGrowth algorithm ")

    def mine(self) -> None:
        """
        Mining process will start from this function
        """

        global _minSup, _maxPer, _minAllConf, _maxPerAllConf, _lno
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._minAllConf = float(self._minAllConf)
        self._maxPer = self._convert(self._maxPer)
        self._maxPerAllConf = float(self._maxPerAllConf)
        _minSup, _minAllConf, _maxPer, _maxPerAllConf, _lno = self._minSup, self._minAllConf,  self._maxPer, self._maxPerAllConf, len(self._Database)
        #print(_minSup, _minAllConf, _maxPer, _maxPerAllConf)
        if self._minSup > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
        generatedItems, pfList = self._periodicFrequentOneItem()
        updatedDatabases = self._updateDatabases(generatedItems)
        for x, y in self._rank.items():
            self._rankedUp[y] = x
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedDatabases, info)
        patterns = Tree.generatePatterns([])
        self._finalPatterns = {}
        for i in patterns:
            sample = self._savePeriodic(i[0])
            self._finalPatterns[sample] = i[1]
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Correlated Periodic-Frequent patterns were generated successfully using EPCPGrowth algorithm ")

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

    def getPatternsAsDataFrame(self) -> pd.DataFrame:
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1], b[2], b[3]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity', 'allConf', 'maxPerAllConf'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete set of periodic-frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y[0]) + ":" + str(y[1]) + ":" + str(y[2]) + ":" + str(y[3])
            writer.write("%s \n" % s1)

    def getPatterns(self) -> dict:
        """ Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns
    
    def printResults(self) -> None:
        """
        This function is used to print thr results
        """
        print("Total number of Correlated Periodic-Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())
        

if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 7 or len(_ab._sys.argv) == 8:
        if len(_ab._sys.argv) == 8:
            _ap = EPCPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], sys.argv[6], sys.argv[7])
        if len(_ab._sys.argv) == 7:
            _ap = EPCPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], sys.argv[5], sys.argv[6])
        _ap.mine()
        print("Total number of Correlated Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:",  _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")


