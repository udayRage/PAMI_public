# WUFIM is one of the algorithm to discover weighted frequent patterns in an uncertain transactional database using PUF-Tree.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.weightedUncertainFrequentPattern.basic import basic as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10
#
#             obj = alg.basic(iFile, wFile, minSup, sep)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of  Patterns:", len(Patterns))
#
#             obj.save(oFile)
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
     along with this program.  If not, see `<https://www.gnu.org/licenses/>`_.    
"""

from PAMI.weightedUncertainFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated

#_expSup = str()
#_expWSup = str()
#_weights = {}
#_finalPatterns = {}
_ab._sys.setrecursionlimit(20000)
class _Item:
    """
    A class used to represent the item with probability in transaction of dataset

    :Attributes:

        item : int or word
          Represents the name of the item

        probability : float
          Represent the existential probability(likelihood presence) of an item
    """

    def __init__(self, item: int, probability: float) -> None:
        self.item = item
        self.probability = probability


class _Node(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int
          storing item of a node

        probability : int
          To maintain the expected support of node

        parent : node
          To maintain the parent of every node

        children : list
          To maintain the children of node

    :Methods:

        addChild(itemName)
            storing the children to their respective parent nodes
    """

    def __init__(self, item, children: list) -> None:
        self.item = item
        self.probability = 1
        self.children = children
        self.parent = None

    def addChild(self, node) -> None:
        """
        This method is used to add a child node to the current node in the frequent pattern tree.

        :param node:The node to be added as a child
        :type node:_Node
        :return: None
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

        addTransaction(transaction)
            creating transaction as a branch in frequentPatternTree
        addConditionalPattern(prefixPaths, supportOfItems)
            construct the conditional tree for prefix paths
        conditionalPatterns(Node)
            generates the conditional patterns from tree for specific node
        conditionalTransactions(prefixPaths,Support)
            takes the prefixPath of a node and support at child of the path and extract the frequent items from prefixPaths and generates prefixPaths with items which are frequent
        remove(Node)
            removes the node from tree once after generating all the patterns respective to the node
        generatePatterns(Node)
            starts from the root node of the tree and mines the frequent patterns

    """

    def __init__(self) -> None:
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction) -> None:
        """
        Adding transaction into tree

        :param transaction: it represents the one self.Database in database
        :type transaction: list
        :return: None
        """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i].item not in currentNode.children:
                newNode = _Node(transaction[i].item, {})
                l1 = i - 1
                lp = []
                while l1 >= 0:
                    lp.append(transaction[l1].probability)
                    l1 -= 1
                if len(lp) == 0:
                    newNode.probability = transaction[i].probability
                else:
                    newNode.probability = max(lp) * transaction[i].probability
                currentNode.addChild(newNode)
                if transaction[i].item in self.summaries:
                    self.summaries[transaction[i].item].append(newNode)
                else:
                    self.summaries[transaction[i].item] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i].item]
                l1 = i - 1
                lp = []
                while l1 >= 0:
                    lp.append(transaction[l1].probability)
                    l1 -= 1
                if len(lp) == 0:
                    currentNode.probability += transaction[i].probability
                else:
                    currentNode.probability += max(lp) * transaction[i].probability

    def addConditionalPattern(self, transaction, sup) -> None:
        """
        constructing conditional tree from prefixPaths

        :param transaction : it represents the one self.Database in database
        :type transaction : list
        :param sup : support of prefixPath taken at last child of the path
        :type sup : int
        :return: None
        """
        # This method takes transaction, support and constructs the conditional tree
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = _Node(transaction[i], {})
                newNode.probability = sup
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
                currentNode.probability += sup

    def conditionalPatterns(self, alpha) -> tuple:
        """
        generates all the conditional patterns of respective node

        :param alpha : it represents the Node in tree
        :type alpha : _Node
        :return: tuple
        """
        # This method generates conditional patterns of node by traversing the tree
        finalPatterns = []
        sup = []
        for i in self.summaries[alpha]:
            s = i.probability
            set2 = []
            while i.parent.item is not None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                sup.append(s)
        finalPatterns, support, info = self.conditionalTransactions(finalPatterns, sup)
        return finalPatterns, support, info

    def removeNode(self, nodeValue) -> None:
        """
        Removing the node from tree

        :param nodeValue : it represents the node in tree
        :type nodeValue : node
        :return: None
        """

        for i in self.summaries[nodeValue]:
            del i.parent.children[nodeValue]

    def conditionalTransactions(self, condPatterns, support) -> tuple:
        """
        It generates the conditional patterns with frequent items

        :param condPatterns : conditionalPatterns generated from conditionalPattern method for respective node
        :type condPatterns : list
        :param support : the support of conditional pattern in tree
        :type support : int
        :return: tuple
        """
        #global _expSup, _expWSup
        pat = []
        sup = []
        count = {}
        for i in range(len(condPatterns)):
            for j in condPatterns[i]:
                if j in count:
                    count[j] += support[i]
                else:
                    count[j] = support[i]
        updatedDict = {}
        updatedDict = {k: v for k, v in count.items() if v >= _expSup}
        count = 0
        for p in condPatterns:
            p1 = [v for v in p if v in updatedDict]
            trans = sorted(p1, key=lambda x: updatedDict[x], reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                sup.append(support[count])
                count += 1
        return pat, sup, updatedDict

    def generatePatterns(self, prefix) -> None:
        """
        Generates the patterns

        :param prefix : forms the combination of items
        :type prefix : list
        :return: None
        """

        global _finalPatterns, _expSup, _expWSup, _weights
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x))):
            pattern = prefix[:]
            pattern.append(i)
            weight = 0
            for k in pattern:
                weight = weight + _weights[k]
            weight = weight/len(pattern)
            if self.info.get(i) >= _expSup and self.info.get(i) * weight >= _expWSup:
                _finalPatterns[tuple(pattern)] = self.info.get(i)
                patterns, support, info = self.conditionalPatterns(i)
                conditionalTree = _Tree()
                conditionalTree.info = info.copy()
                for pat in range(len(patterns)):
                    conditionalTree.addConditionalPattern(patterns[pat], support[pat])
                if len(patterns) > 0:
                    conditionalTree.generatePatterns(pattern)
            self.removeNode(i)

class WUFIM(_ab._weightedFrequentPatterns):
    """
    About this algorithm
    ====================

    :Description: It is one of the algorithm to discover weighted frequent patterns in a uncertain transactional database using PUF-Tree.

    :Reference: Efficient Mining of Weighted Frequent Itemsets in Uncertain Databases.
           In : Machine Learning and Data Mining in Pattern Recognition book Chun-Wei Jerry Lin, Wensheng Gan, Philippe Fournier Viger, Tzung-Pei Hong

    :param  iFile: str :
                   Name of the Input file to mine complete set of Weighted Uncertain Periodic Frequent Patterns
    :param  oFile: str :
                   Name of the output file to store complete set of Weighted  Uncertain Periodic Frequent Patterns
    :param  minSup: str:
                   minimum support thresholds were tuned to find the appropriate ranges in the limited memory
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    :param  wFile: str :
                    This is a weighted file.


    :Attributes:

        iFile : file
          Name of the Input file or path of the input file

        wFile : file
          Name of the Input file or path of the input file

        oFile : file
          Name of the output file or path of the output file

        minSup : float or int or str
          The user can specify minSup either in count or proportion of database size.
          If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
          Otherwise, it will be treated as float.
          Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float

        sep : str
          This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
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
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        creatingItemSets(fileName)
            Scans the dataset and stores in a list format
        frequentOneItem()
            Extracts the one-length frequent patterns from database
        updateTransactions()
            Update the transactions by removing non-frequent items and sort the Database by item decreased support
        buildTree()
            After updating the Database, remaining items will be added into the tree by setting root node as null
        convert()
            to convert the user specified value
        mine()
            Mining process will start from this function

    Execution methods
    =================


    **Terminal command**


    .. code-block:: console

      Format:

      (.venv) $ python3 basic.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 basic.py sampleTDB.txt patterns.txt 3

    .. note:: minSup  will be considered in support count or frequency

    **Calling from a python program**

    .. code-block:: python

            from PAMI.weightedUncertainFrequentPattern.basic import basic as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.basic(iFile, wFile, expSup, expWSup)

            obj.mine()

            Patterns = obj.getPatterns()

            print("Total number of  Patterns:", len(Patterns))

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

   """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _finalPatterns = {}
    _iFile = " "
    _wFile = " "
    oFile = " "
    _sep = " "
    _memoryUSS = float()
    memoryRSS = float()
    _Database = []
    _rank = {}
    _expSup = float()
    _expWSup = float()
    Database1 = None

    def __init__(self, iFile, wFile, expSup, expWSup, sep='\t') -> None:
        super().__init__(iFile, wFile, expSup, expWSup, sep)

    def _creatingItemSets(self) -> None:
        """
        Scans the uncertain transactional dataset

        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            uncertain, data = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
            if 'uncertain' in i:
                uncertain = self._iFile['uncertain'].tolist()
            for k in range(len(data)):
                tr = []
                for j in range(len(data[k])):
                    product = _Item(data[k][j], uncertain[k][j])
                    tr.append(product)
                self._Database.append(tr)

            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.strip()
                    line = [i for i in line.split(':')]
                    temp1 = [i.rstrip() for i in line[0].split(self._sep)]
                    temp2 = [i.rstrip() for i in line[1].split(self._sep)]
                    temp1 = [x for x in temp1 if x]
                    temp2 = [x for x in temp2 if x]
                    tr = []
                    for i in range(len(temp1)):
                        item = temp1[i]
                        probability = float(temp2[i])
                        product = _Item(item, probability)
                        tr.append(product)
                    self._Database.append(tr)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            line = line.strip()
                            line = [i for i in line.split(':')]
                            temp1 = [i.rstrip() for i in line[0].split(self._sep)]
                            temp2 = [i.rstrip() for i in line[1].split(self._sep)]
                            temp1 = [x for x in temp1 if x]
                            temp2 = [x for x in temp2 if x]
                            tr = []
                            for i in range(len(temp1)):
                                item = temp1[i]
                                probability = float(temp2[i])
                                product = _Item(item, probability)
                                tr.append(product)
                            self._Database.append(tr)
                except IOError:
                    print("File Not Found")

    def _scanningWeights(self) -> None:
        """
        Scans the uncertain transactional dataset

        :return: None
        """
        if isinstance(self._wFile, _ab._pd.DataFrame):
            weights, data = [], []
            if self._wFile.empty:
                print("its empty..")
            i = self._wFile.columns.values.tolist()
            if 'items' in i:
                data = self._wFile['items'].tolist()
            if 'weights' in i:
                weights = self._wFile['weights'].tolist()
            for k in range(len(data)):
                self._weights[data[k]] = int(float(weights[k]))

            # print(self.Database)
        if isinstance(self._wFile, str):
            if _ab._validators.url(self._wFile):
                data = _ab._urlopen(self._wFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._weights[temp[0]] = int(float(temp[1]))
            else:
                try:
                    with open(self._wFile, 'r') as f:
                        for line in f:
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._weights[temp[0]] = float(temp[1])
                except IOError:
                    print("File Not Found")

    def _frequentOneItem(self) -> tuple:
        """
        Takes the self.Database and calculates the support of each item in the dataset and assign the ranks to the items by decreasing support and returns the frequent items list

        :param self.Database : it represents the one self.Database in database
        :type self.Database : list
        :return: tuple
        """

        mapSupport = {}
        for i in self._Database:
            for j in i:
                if j.item not in mapSupport:
                    if self._weights.get(j.item) is not None:
                        mapSupport[j.item] = [j.probability, self._weights[j.item]]
                else:
                    mapSupport[j.item][0] += j.probability
        mapSupport = {k: v[0] for k, v in mapSupport.items() if v[0] >= self._expSup and v[0] * v[1] >= self._expWSup}
        plist = [k for k, v in sorted(mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.rank = dict([(index, item) for (item, index) in enumerate(plist)])
        return mapSupport, plist

    @staticmethod
    def _buildTree(data, info) -> _Tree:
        """
        It takes the self.Database and support of each item and construct the main tree with setting root node as null

        :param data : it represents the one self.Database in database
        :type data : list
        :param info : it represents the support of each item
        :type info : dictionary
        :return: tree
        """

        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            rootNode.addTransaction(data[i])
        return rootNode

    def _updateTransactions(self, dict1) -> list:
        """
        Remove the items which are not frequent from self.Database and updates the self.Database with rank of items

        :param dict1 : frequent items with support
        :type dict1 : dictionary
        :return: list
        """
        list1 = []
        for tr in self._Database:
            list2 = []
            for i in range(0, len(tr)):
                if tr[i].item in dict1:
                    list2.append(tr[i])
            if len(list2) >= 2:
                basket = list2
                basket.sort(key=lambda val: self.rank[val.item])
                list2 = basket
                list1.append(list2)
        return list1

    @staticmethod
    def _check(i, x) -> int:
        """
        To check the presence of item or pattern in transaction

        :param x: it represents the pattern
        :type x : list
        :param i : represents the uncertain self.Database
        :type i : list
        :return: integer number
        """

        # This method taken a transaction as input and returns the tree
        for m in x:
            k = 0
            for n in i:
                if m == n.item:
                    k += 1
            if k == 0:
                return 0
        return 1

    def _convert(self, value) -> float:
        """
        To convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type minSup value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def _removeFalsePositives(self) -> None:
        """
        To remove the false positive patterns generated in frequent patterns.

        :return: patterns with accurate probability
        """
        global _finalPatterns
        periods = {}
        for i in self._Database:
            for x, y in _finalPatterns.items():
                if len(x) == 1:
                    periods[x] = y
                else:
                    s = 1
                    check = self._check(i, x)
                    if check == 1:
                        for j in i:
                            if j.item in x:
                                s *= j.probability
                        if x in periods:
                            periods[x] += s
                        else:
                            periods[x] = s
        for x, y in periods.items():
            weight = 0
            for i in x:
                weight += self._weights[i]
            weight = weight / len(x)
            if weight * y >= self._expWSup:
                sample = str()
                for i in x:
                    sample = sample + i + "\t"
                self._finalPatterns[sample] = y

    @deprecated(
        "It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        mine() method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patterns.
        """
        self.mine()

    def mine(self) -> None:
        """
        mine() method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patternS
        """
        global _expSup, _expWSup, _weights, _finalPatterns
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._scanningWeights()
        _weights = self._weights
        self._expSup = float(self._expSup)
        self._expWSup = float(self._expWSup)
        _expSup = self._expSup
        _expWSup = self._expWSup
        self._finalPatterns = {}
        mapSupport, plist = self._frequentOneItem()
        self.Database1 = self._updateTransactions(mapSupport)
        info = {k: v for k, v in mapSupport.items()}
        Tree1 = self._buildTree(self.Database1, info)
        Tree1.generatePatterns([])
        self._removeFalsePositives()
        print("Weighted Frequent patterns were generated  successfully using basic algorithm")
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self.memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss

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
        return self.memoryRSS

    def getRuntime(self) -> float:
        """

        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self) -> pd.DataFrame:
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """
        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            s = str()
            for i in a:
                s = s + i + " "
            data.append([s, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, outFile: str) -> None:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: Specify name of the output file
        :type outFile: csv file
        :return: None
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s = str()
            for i in x:
                s = s + i + "\t"
            s1 = s.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> dict:
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
        print("Total number of  Weighted Uncertain Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 6 or len(_ab._sys.argv) == 7:
        if len(_ab._sys.argv) == 7:
            _ap = WUFIM(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6])
        if len(_ab._sys.argv) == 6:
            _ap = WUFIM(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        _ap.mine()
        _ap.mine()
        print("Total number of Weighted Uncertain Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        for k in [120, 140, 160, 180, 200]:
            _ap = WUFIM('/Users/likhitha/Downloads/uncertainTransaction_T10I4D200K.csv', '/Users/likhitha/Downloads/T10_weights.txt',
                        k, 500, '\t')
            _ap.mine()
            print("Total number of Weighted Uncertain Frequent Patterns:", len(_ap.getPatterns()))
            _ap.save('/Users/likhitha/Downloads/WUFIM_output.txt')
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
