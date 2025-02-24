# UFGrowth is one of the fundamental algorithm to discover frequent patterns in a uncertain transactional database using PUF-Tree.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.uncertainFrequentPattern.basic import UFGrowth as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.UFGrowth(iFile, minSup)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
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

from PAMI.uncertainFrequentPattern.basic import abstract as _ab
from deprecated import deprecated

_minSup = str()
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

    def __init__(self):
        self.itemId = -1
        self.counter = 0
        self.probability = 0
        self.child = []
        self.parent = None
        self.nodeLink = None
        self.expSup = 0

    def getChild(self, id1):
        for i in self.child:
            if i.itemid == id1:
                return i
        return None


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
        self.headerList = []
        self.mapItemNodes = {}
        self.mapItemLastNodes = {}
        self.root = _Node()

    def fixNodeLinks(self, item, newNode):
        if item in self.mapItemLastNodes.keys():
            lastNode = self.mapItemLastNodes[item]
            lastNode.nodeLink = newNode
        self.mapItemLastNodes[item] = newNode
        if item not in self.mapItemNodes.keys():
            self.mapItemNodes[item] = newNode

    def addTransaction(self, transaction):
        y = 0
        current = self.root
        for i in transaction:
            child = current.getChild(i.item)
            if child is None:
                newNode = _Node()
                newNode.counter = 1
                newNode.probability = i.probability
                newNode.itemId = i.item
                newNode.expSup = i.probability
                newNode.parent = current
                current.child.append(newNode)
                self.fixNodeLinks(i.item, newNode)
                current = newNode
            else:
                if child.probability == i.probability:
                    child.counter += 1
                    current = child
                else:
                    newNode = _Node()
                    newNode.counter = 1
                    newNode.itemId = i.item
                    newNode.probability = i.probability
                    newNode.expSup = i.probability
                    newNode.parent = current
                    current.child.append(newNode)
                    self.fixNodeLinks(i.item, newNode)
                    current = newNode
        return y

    def printTree(self, root):
        if root.child is []:
            return
        else:
            for i in root.child:
                print(i.itemid, i.counter)
                self.printTree(i)

    def update(self, mapSup, u1):
        t1 = []
        for i in mapSup:
            if i in u1:
                t1.append(i)
        return t1

    def createHeaderList(self, mapSupport, min_sup):
        t1 = []
        for x, y in mapSupport.items():
            if y >= min_sup:
                t1.append(x)
        mapSup = [k for k, v in sorted(mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.headerList = self.update(mapSup, t1)

    def addPrefixPath(self, prefix, mapSupportBeta, min_sup):
        q = 0
        pathCount = prefix[0].counter
        current = self.root
        prefix.reverse()
        for i in range(0, len(prefix) - 1):
            pathItem = prefix[i]
            # pathCount=mapSupportBeta.get(pathItem.itemId)
            if mapSupportBeta.get(pathItem.itemId) >= min_sup:
                child = current.getChild(pathItem.itemId)
                if child is None:
                    newNode = _Node()
                    q += 1
                    newNode.itemid = pathItem.itemId
                    if newNode.expSup == 0:
                        newNode.expSup = pathItem.expSup
                    newNode.probability = pathItem.probability
                    newNode.parent = current
                    newNode.counter = pathCount
                    current.child.append(newNode)
                    current = newNode
                    self.fixNodeLinks(pathItem.itemid, newNode)
                else:
                    if child.probability == prefix[i].probability:
                        child.counter += pathCount
                        child.expSup = child.expSup * pathItem.expSup
                        current = child
                    else:
                        newNode = _Node()
                        q += 1
                        newNode.itemId = pathItem.itemId
                        newNode.probability = pathItem.probability
                        if newNode.expSup == 0:
                            newNode.expSup = pathItem.expSup
                        newNode.parent = current
                        newNode.counter = pathCount
                        current.child.append(newNode)
                        current = newNode
                        self.fixNodeLinks(pathItem.itemid, newNode)
        return q


class UFGrowth(_ab._frequentPatterns):
    """
    About this algorithm
    ====================

    :Description: It is one of the fundamental algorithm to discover frequent patterns in a uncertain transactional database using PUF-Tree.

    :Reference:  Carson Kai-Sang Leung, Syed Khairuzzaman Tanbeer, "PUF-Tree: A Compact Tree Structure for Frequent Pattern Mining of Uncertain Data",
                 Pacific-Asia Conference on Knowledge Discovery and Data Mining(PAKDD 2013), https://link.springer.com/chapter/10.1007/978-3-642-37453-1_2

    :Attributes:

        iFile : file
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

      (.venv) $ python3 PUFGrowth.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 PUFGrowth.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup can be specified  in support count or a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            from PAMI.uncertainFrequentPattern.basic import UFGrowth as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.UFGrowth(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getmemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    Credits
    =======


             The complete program was written by P.Likhitha under the supervision of Professor Rage Uday Kiran.
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
    _mapSupport = {}
    _lno = 0
    _tree = _Tree()
    _itemsetBuffer = None
    _fpNodeTempBuffer = []
    _maxPatternLength = 1000
    _itemsetCount = 0
    _frequentitems = {}
    _fpnode = 0
    _conditionalnodes = 0

    def __init__(self, iFile, minSup, sep='\t'):
        super().__init__(iFile, minSup, sep)

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
                    with open(self._iFile, 'r') as f:
                        for line in f:
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
                            self._Database.append(tr)
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

    def _ufgrowth(self, tree, prefix, prefixLength, prefixSupport, mapSupport):
        if prefixLength == self._maxPatternLength:
            return
        singlePath = True
        position = 0
        s = 0
        if len(tree.root.child) > 1:
            singlePath = False
        else:
            currentNode = tree.root.child[0]
            while True:
                if len(currentNode.child) > 1:
                    singlePath = False
                    break
                self._fpNodeTempBuffer.insert(position, currentNode)
                s = currentNode.counter
                position += 1
                if len(currentNode.child) == 0:
                    break
                currentNode = currentNode.child[0]
        if singlePath is True:
            self._saveAllcombinations(self._fpNodeTempBuffer, s, position, prefix, prefixLength)
        else:
            for i in reversed(tree.headerList):
                item = i
                betaSupport = mapSupport[item]
                prefix.insert(prefixLength, item)
                # print prefix,betaSupport
                self._saveItemset(prefix, prefixLength + 1, betaSupport)
                if prefixLength + 1 < self._maxPatternLength:
                    prefixPaths = []
                    path = tree.mapItemNodes.get(item)
                    mapSupportBeta = {}
                    while path is not None:
                        if path.parent.itemid != -1:
                            prefixPath = [path]
                            pathCount = path.counter
                            parent1 = path.parent
                            while parent1.itemid != -1:
                                prefixPath.append(parent1)
                                s = (pathCount * path.expSup) * parent1.probability
                                if mapSupportBeta.get(parent1.itemid) is None:
                                    mapSupportBeta[parent1.itemid] = s
                                else:
                                    mapSupportBeta[parent1.itemid] = mapSupportBeta[parent1.itemid] + s
                                parent1 = parent1.parent
                            prefixPaths.append(prefixPath)
                        path = path.nodeLink
                    treeBeta = _Tree()
                    for j in prefixPaths:
                        q = treeBeta.addPrefixPath(j, mapSupportBeta, self._minSup)
                        self._conditionalnodes += q
                    if len(treeBeta.root.child) > 0:
                        treeBeta.createHeaderList(mapSupportBeta, self._minSup)
                        # print(treeBeta.headerList)
                        self._ufgrowth(treeBeta, prefix, prefixLength + 1, betaSupport, mapSupportBeta)

    def _saveItemset(self, prefix, prefixLength, support):
        l = []
        for i in range(prefixLength):
            l.append(prefix[i])
        self._itemsetCount += 1
        l.sort()
        s = '\t'.join(l)
        self._finalPatterns[s] = support

    def _saveAllcombinations(self, TempBuffer, s, position, prefix, prefixLength):
        # support=0
        max1 = 1 << position
        for i in range(1, max1):
            newprefixLength = prefixLength
            for j in range(position):
                isset = i & (1 << j)
                if isset > 0:
                    prefix.insert(newprefixLength, TempBuffer[j].itemid)
                    newprefixLength += 1
                    support = TempBuffer[j].counter
            self._saveItemset(prefix, newprefixLength, s)

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
        self._minSup = self._convert(self._minSup)
        #minSup = self._minSup
        self._finalPatterns = {}
        _mapSupport, plist = self._frequentOneItem()
        for i in self._Database:
            transaction = []
            for j in i:
                if _mapSupport.get(j.item) >= self._minSup:
                    transaction.append(j)
            transaction.sort(key=lambda val: _mapSupport[val.item], reverse=True)
            o = self._tree.addTransaction(transaction)
        self._tree.createHeaderList(_mapSupport, self._minSup)
        if len(self._tree.headerList) > 0:
            self._itemsetBuffer = []
            # self.fpNodeTempBuffer=[]
            self._ufgrowth(self._tree, self._itemsetBuffer, 0, self._lno, _mapSupport)
        print("Frequent patterns were generated from uncertain databases successfully using UF algorithm")
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
            data.append([a.replace('\t', ' '), b])
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
            s1 = x.strip() + ":" + str(y)
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
        This function is used to print the results
        """
        print("Total number of  Uncertain Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = UFGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = UFGrowth(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        print("Total number of Uncertain Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:",  _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
