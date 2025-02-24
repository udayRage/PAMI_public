# GFPGrowth algorithm is used to discover geo-referenced frequent patterns in a uncertain transactional database using GFP-Tree.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.uncertainGeoreferencedFrequentPattern.basic import GFPGrowth as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.GFPGrowth(iFile, nFile, minSup,sep, oFile)
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
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PAMI.uncertainGeoreferencedFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated

_minSup = str()
_neighbourList = {}
_ab._sys.setrecursionlimit(20000)
_finalPatterns = {}


class _Item:
    """
    A class used to represent the item with probability in transaction of dataset

    :Attributes:

        item : int or word
            Represents the name of the item

        probability : float
            Represent the existential probability(likelihood presence) of an item
    """

    def __init__(self, item, probability):
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

    def __init__(self, item, children):
        self.item = item
        self.probability = 1
        self.children = children
        self.parent = None

    def addChild(self, node):
        """
        This method adds a child node to the current node in the frequent pattern tree. It updates the children
        dictionary of the current node with the new child node and sets the parent of the child node to the current node.

        :param node: The child node to be added.
        :type node: _Node
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
            takes the prefixPath of a node and support at child of the path and extract the frequent items from
            prefixPaths and generates prefixPaths with items which are frequent
        remove(Node)
            removes the node from tree once after generating all the patterns respective to the node
        generatePatterns(Node)
            starts from the root node of the tree and mines the frequent patterns
    """

    def __init__(self):
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction):
        """
        Adding transaction into tree

        :param transaction : it represents the one self.Database in database
        :type transaction : list
        """
        global _neighbourList
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i].item not in currentNode.children:
                newNode = _Node(transaction[i].item, {})
                nei = _neighbourList.get(transaction[i].item)
                l1 = i - 1
                lp = []
                while l1 >= 0:
                    if nei is None:
                        break
                    if transaction[l1].item in nei:
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

    def addConditionalPattern(self, transaction, sup):
        """
        constructing conditional tree from prefixPaths

        :param transaction : it represents the one self.Database in database
        :type transaction : list
        :param sup : support of prefixPath taken at last child of the path
        :type sup : int
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

    def conditionalPatterns(self, alpha):
        """
        Generates all the conditional patterns of respective node

        :param alpha : it represents the Node in tree
        :type alpha : _Node
        """

        # This method generates conditional patterns of node by traversing the tree
        global _neighbourList
        finalPatterns = []
        sup = []
        for i in self.summaries[alpha]:
            j = i.item
            s = i.probability
            set2 = []
            while i.parent.item is not None:
                if _neighbourList.get(j) is not None:
                    #print(_neighbourList.get(j))
                    if i.parent.item in _neighbourList[j]:
                        set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                sup.append(s)
        finalPatterns, support, info = self.conditionalTransactions(finalPatterns, sup)
        return finalPatterns, support, info

    def removeNode(self, nodeValue):
        """
        Removing the node from tree

        :param nodeValue : it represents the node in tree
        :type nodeValue : node
        """

        for i in self.summaries[nodeValue]:
            del i.parent.children[nodeValue]

    def conditionalTransactions(self, condPatterns, support):
        """
        It generates the conditional patterns with frequent items

        :param condPatterns : conditionalPatterns generated from conditionalPattern method for respective node
        :type condPatterns : list
        :param support : the support of conditional pattern in tree
        :type support : int
        """

        #global minSup
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
        updatedDict = {k: v for k, v in count.items() if v >= minSup}
        count = 0
        for p in condPatterns:
            p1 = [v for v in p if v in updatedDict]
            trans = sorted(p1, key=lambda x: updatedDict[x], reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                sup.append(support[count])
                count += 1
        return pat, sup, updatedDict

    def generatePatterns(self, prefix):
        """
        Generates the patterns

        :param prefix : forms the combination of items
        :type prefix : list
        """

        _finalPatterns = None
        minSup = None
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x))):
            pattern = prefix[:]
            pattern.append(i)
            s = 0
            for x in self.summaries[i]:
                s += x.probability
            _finalPatterns[tuple(pattern)] = self.info[i]
            if s >= minSup:
                patterns, support, info = self.conditionalPatterns(i)
                conditionalTree = _Tree()
                conditionalTree.info = info.copy()
                for pat in range(len(patterns)):
                    conditionalTree.addConditionalPattern(patterns[pat], support[pat])
                if len(patterns) > 0:
                    conditionalTree.generatePatterns(pattern)
            self.removeNode(i)


class GFPGrowth(_ab._frequentPatterns):
    """
    About this algorithm
    ====================

    :Description: GFPGrowth algorithm is used to discover geo-referenced frequent patterns in a uncertain transactional database using GFP-Tree.

    :Reference:  Palla Likhitha,Pamalla Veena, Rage, Uday Kiran, Koji Zettsu (2023).
                 "Discovering Geo-referenced Frequent Patterns in Uncertain Geo-referenced
                 Transactional Databases".  PAKDD 2023.
                 https://doi.org/10.1007/978-3-031-33380-4_3


    :param  iFile: str :
                   Name of the Input file to mine complete set of uncertain Geo referenced Frequent Patterns
    :param  oFile: str :
                   Name of the output file to store complete set of Uncertain Geo referenced frequent patterns
    :param  minSup: str:
                   minimum support thresholds were tuned to find the appropriate ranges in the limited memory
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file

        oFile : file
            Name of the output file or path of the output file

        minSup: float or int or str
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
        savePatterns(oFile)
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

       (.venv) $ python3 GFPGrowth.py <inputFile> <neighborFile> <outputFile> <minSup>

       Examples usage:

       (.venv) $ python3 GFPGrowth.py sampleTDB.txt sampleNeighbor.txt patterns.txt 3

    .. note:: minSup  will be considered in support count or frequency
    
    **Calling from a python program**:

     .. code-block:: python

            from PAMI.uncertainGeoreferencedFrequentPattern.basic import GFPGrowth as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.GFPGrowth(iFile, nFile, minSup)

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
        
    Credits
    =======


            The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.\n

    """


    _startTime = float()
    _endTime = float()
    _minSup = str()
    _finalPatterns = {}
    _iFile = " "
    oFile = " "
    _sep = " "
    _memoryUSS = float()
    memoryRSS = float()
    _Database = []
    _rank = {}
    Database1 = None


    def __init__(self, iFile, nFile, minSup, sep='\t'):
        super().__init__(iFile, nFile, minSup, sep)

    def _creatingItemSets(self):
        """
        Scans the uncertain transactional dataset
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
                    temp1 = line.strip()
                    temp1 = temp1.split(':')
                    temp = [i.rstrip() for i in temp1[0].split(self._sep)]
                    uncertain = [float(i.rstrip()) for i in temp1[1].split(self._sep)]
                    tr = []
                    for i in range(len(temp)):
                        item = temp[i]
                        probability = uncertain[i]
                        product = _Item(item, probability)
                        tr.append(product)
                    self._Database.append(tr)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            temp1 = line.strip()
                            temp1 = temp1.split(':')
                            #temp1[0], temp1[1] = [i for i in temp1[0] if i], [i for i in temp1[1] if i]
                            temp = [i.rstrip() for i in temp1[0].split(self._sep) if i]
                            uncertain = [float(i.rstrip()) for i in temp1[1].split(self._sep) if i]
                            tr = []
                            for i in range(len(temp)):
                                item = temp[i]
                                probability = uncertain[i]
                                product = _Item(item, probability)
                                tr.append(product)
                            self._Database.append(tr)
                except IOError:
                    print("File Not Found")
                    
    def _creatingNeighbours(self):
        """
        Scans the uncertain transactional dataset
        """
        global _neighbourList
        _neighbourList = {}
        if isinstance(self._nFile, _ab._pd.DataFrame):
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
        if isinstance(self._nFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    tr = []
                    for i in temp:
                        i1 = i.index('(')
                        i2 = i.index(')')
                        item = i[0:i1]
                        probability = float(i[i1 + 1:i2])
                        product = _Item(item, probability)
                        tr.append(product)
                    self._Database.append(temp)
            else:
                try:
                    with open(self._nFile, 'r') as f:
                        for line in f:
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            _neighbourList[temp[0]] = temp[1:]
                except IOError:
                    print("File Not Found")

    def _frequentOneItem(self):
        """
        Takes the self.Database and calculates the support of each item in the dataset and assign the ranks to the items by decreasing support and returns the frequent items list

        :param self.Database : it represents the one self.Database in database
        :type self.Database : list
        """

        mapSupport = {}
        for i in self._Database:
            for j in i:
                if j.item not in mapSupport:
                    mapSupport[j.item] = j.probability
                else:
                    mapSupport[j.item] += j.probability
        mapSupport = {k: v for k, v in mapSupport.items() if v >= self._minSup}
        plist = [k for k, v in sorted(mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.rank = dict([(index, item) for (item, index) in enumerate(plist)])
        return mapSupport, plist

    @staticmethod
    def _buildTree(data, info):
        """
        It takes the self.Database and support of each item and construct the main tree with setting root node as null

        :param data : it represents the one self.Database in database
        :type data : list
        :param info : it represents the support of each item
        :type info : dictionary
        """

        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            rootNode.addTransaction(data[i])
        return rootNode

    def _updateTransactions(self, dict1):
        """
        Remove the items which are not frequent from self.Database and updates the self.Database with rank of items

        :param dict1 : frequent items with support
        :type dict1 : dictionary
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
    def _check(i, x):
        """
        To check the presence of item or pattern in transaction

        :param x: it represents the pattern
        :type x : list
        :param i : represents the uncertain self.Database
        :type i : list
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

    def _convert(self, value):
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

    def _removeFalsePositives(self):
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
            if y >= self._minSup:
                sample = str()
                for i in x:
                    sample = sample + i + "\t"
                self._finalPatterns[sample] = y

    @deprecated(
        "It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Main method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patterns
        """
        self.mine()

    def mine(self):
        """
        Main method where the patterns are mined by constructing tree and remove the false patterns by counting the original support of a patterns
        """
        #global minSup
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._creatingNeighbours()
        # self._minSup = self._convert(self._minSup)
        minSup = self._minSup
        self._finalPatterns = {}
        mapSupport, plist = self._frequentOneItem()
        self.Database1 = self._updateTransactions(mapSupport)
        info = {k: v for k, v in mapSupport.items()}
        Tree1 = self._buildTree(self.Database1, info)
        Tree1.generatePatterns([])
        self._removeFalsePositives()
        print("Geo-Referenced Frequent patterns were generated from uncertain databases successfully using GFP algorithm")
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self.memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss

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

        return self.memoryRSS

    def getRuntime(self):
        """

        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, outFile):
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """

        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns
    
    def printResults(self):
        """
        This function is used to print the result
        """
        print("Total number of Patterns:", len(self.getPatterns()))
        self.save("patterns.txt")
        memUSS = self.getMemoryUSS()
        print("Total Memory in USS:", memUSS)
        memRSS = self.getMemoryRSS()
        print("Total Memory in RSS", memRSS)
        run = self.getRuntime()
        print("Total ExecutionTime in ms:", run)


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = GFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = GFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        _Patterns = _ap.getPatterns()
        print("Total number of Patterns:", len(_Patterns))
        _ap.save(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
