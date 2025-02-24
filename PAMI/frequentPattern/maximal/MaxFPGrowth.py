# MaxFP-Growth is one of the fundamental algorithm to discover maximal frequent patterns in a transactional database.
#
# **Importing this algorithm into a python program**
# ---------------------------------------------------------
#
#             from PAMI.frequentPattern.maximal import MaxFPGrowth as alg
#
#             obj = alg.MaxFPGrowth("../basic/sampleTDB.txt", "2")
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
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
"""


from PAMI.frequentPattern.maximal import abstract as _ab
from deprecated import deprecated


_minSup = str()
#global maximalTree


class _Node(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:
        item : int
            storing item of a node
        counter : list
            To maintain the support of the node
        parent : node
            To maintain the parent of every node
        children : list
            To maintain the children of node

    :Methods:
        addChild(itemName)
            storing the children to their respective parent nodes
    """

    def __init__(self, item, children):
        """
        Initializing the Node class
        :param item: Storing the item of a node
        :type item: int or None
        :param children: To maintain the children of a node
        :type children: dict
        """
        self.item = item
        self.children = children
        self.counter = int()
        self.parent = None

    def addChild(self, node):
        """
        Adding a child to the created nodes
        :param node: node object
        :type node: Node
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
        addConditionalTransaction(prefixPaths, supportOfItems)
            construct the conditional tree for prefix paths
        condPatterns(Node)
            generates the conditional patterns from tree for specific node
        conditionalTransaction(prefixPaths,Support)
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
        #self.maximalTree = _MPTree()

    def addTransaction(self, transaction):
        """

        Adding transactions into tree

        :param transaction: represents the transaction in a database

        :type transaction: list

        :return: tree

        """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = _Node(transaction[i], {})
                newNode.counter = 1
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
                currentNode.counter += 1

    def addConditionalTransaction(self, transaction, count):
        """

        Loading the database into a tree

        :param transaction: conditional transaction of a node

        :type transaction: list

        :param count: the support of conditional transaction

        :type count: int

        :return: conditional tree

        """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = _Node(transaction[i], {})
                newNode.counter = count
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
                currentNode.counter += count

    def getConditionalPatterns(self, alpha):
        """
        Generates all the conditional patterns of respective node
        :param alpha: it represents the Node in tree
        :type alpha: int
        :return: conditional patterns of a node
        """
        finalPatterns = []
        finalSets = []
        for i in self.summaries[alpha]:
            set1 = i.counter
            set2 = []
            while i.parent.item is not None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                finalSets.append(set1)
        finalPatterns, finalSets, info = self.conditionalTransactions(finalPatterns, finalSets)
        return finalPatterns, finalSets, info

    def conditionalTransactions(self, condPatterns, condFreq):
        """
        sorting and removing the items from conditional transactions which don't satisfy minSup
        :param condPatterns: conditional patterns if a node
        :type condPatterns: list
        :param condFreq: frequency at leaf node of conditional transaction
        :type condFreq: int
        :return: conditional patterns and their frequency respectively
        """
        global _minSup
        pat = []
        tids = []
        data1 = {}
        for i in range(len(condPatterns)):
            for j in condPatterns[i]:
                if j not in data1:
                    data1[j] = condFreq[i]
                else:
                    data1[j] += condFreq[i]
        updatedDict = {}
        updatedDict = {k: v for k, v in data1.items() if v >= _minSup}
        count = 0
        for p in condPatterns:
            p1 = [v for v in p if v in updatedDict]
            trans = sorted(p1, key=lambda x: (updatedDict.get(x), -x), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                tids.append(condFreq[count])
            count += 1
        return pat, tids, updatedDict

    def removeNode(self, nodeValue):
        """
        To remove the node from the original tree
        :param nodeValue: leaf node of tree
        :type nodeValue: int
        :return: tree after deleting node
        """
        for i in self.summaries[nodeValue]:
            del i.parent.children[nodeValue]
            i = None

    def generatePatterns(self, prefix, patterns, maximalTree):
        """
        Generates the patterns
        :param prefix: forms the combination of items
        :type prefix: str
        :param patterns: the patterns we want to generate for this node
        :type patterns: list
        :param maximalTree: maximal frequent patterns
        :type maximalTree: _MPTree()
        :return: the maximal frequent patterns
        :rtype: list
        """
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x), -x)):
            pattern = prefix[:]
            pattern.append(i)
            condPatterns, tids, info = self.getConditionalPatterns(i)
            conditional_tree = _Tree()
            conditional_tree.info = info.copy()
            head = pattern[:]
            tail = []
            for la in info:
                tail.append(la)
            sub = head + tail
            if maximalTree.checkerSub(sub) == 1:
                for pat in range(len(condPatterns)):
                    conditional_tree.addConditionalTransaction(condPatterns[pat], tids[pat])
                if len(condPatterns) >= 1:
                    conditional_tree.generatePatterns(pattern, patterns, maximalTree)
                else:
                    maximalTree.addTransaction(pattern)
                    patterns[tuple(pattern)] = self.info[i]
            self.removeNode(i)


class _MNode(object):
    """
    A class used to represent the node in maximal tree

    :Attributes:
        item : int
            storing item of a node
        children : list
            To maintain the children of node

    :Methods:
        addChild(itemName)
            storing the children to their respective parent nodes
    """

    def __init__(self, item, children):
        self.item = item
        self.children = children

    def addChild(self, node):
        """
        To add the children details to a parent node
        :param node: children node
        :type node: _MNode
        :return: adding children details to parent node
        """
        self.children[node.item] = node
        node.parent = self


class _MPTree(object):
    """
    A class used to represent the frequentPatternGrowth tree structure

    :Attributes:

        root : Node
            Represents the root node of the tree
        summaries : dictionary
            storing the nodes with same item name


    :Methods:

        addTransaction(transaction)
            creating transaction as a branch in frequentPatternTree
        addConditionalTransaction(prefixPaths, supportOfItems)
            construct the conditional tree for prefix paths
        checkerSub(items):
            Given a set of items to the subset of them is present or not
    """

    def __init__(self):
        self.root = _MNode(None, {})
        self.summaries = {}

    def addTransaction(self, transaction):
        """
        To construct the maximal frequent pattern into maximal tree
        :param transaction: the maximal frequent patterns extracted till now
        :type transaction: list
        :return: the maximal tree
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

    def checkerSub(self, items):
        """
        To check the subset of pattern present in tree
        :param items: the sub frequent pattern
        :type items: list
        :return: checks if subset present in the tree
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


# Initialising the  variable for maximal tree
#maximalTree = _MPTree()


class MaxFPGrowth(_ab._frequentPatterns):
    """
    :Description: MaxFP-Growth is one of the fundamental algorithm to discover maximal frequent patterns in a transactional database.

    :Reference:   Grahne, G. and Zhu, J., "High Performance Mining of Maximal Frequent itemSets",
                  http://users.encs.concordia.ca/~grahne/papers/hpdm03.pdf

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
    :param  maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.



    :Attributes:

        startTime : float
          To record the start time of the mining process

        endTime : float
          To record the completion time of the mining process

        finalPatterns : dict
          Storing the complete set of patterns in a dictionary variable

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
        itemSetCount : int
            it represents the total no of patterns
        finalPatterns : dict
            it represents to store the patterns


    **Methods to execute code on terminal**
    ---------------------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 MaxFPGrowth.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 MaxFPGrowth.py sampleDB.txt patterns.txt 0.3

    .. note:: minSup will be considered in percentage of database transactions



    **Importing this algorithm into a python program**
    ---------------------------------------------------------

    .. code-block:: python

            from PAMI.frequentPattern.maximal import MaxFPGrowth as alg

            obj = alg.MaxFPGrowth("../basic/sampleTDB.txt", "2")

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.savePatterns("patterns")

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    **Credits:**
    -------------------
                The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

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
    _rankdup = {}
    _lno = 0
    _maximalTree = str()

    def _creatingItemSets(self):
        """
            Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
                self._Database = [x.split(self._sep) for x in self._Database]
            else:
                print("The column name should be Transactions and each line should be separated by tab space or a seperator specified by the user")

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
                            #print(line)
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def _frequentOneItem(self):
        """
        To extract the one-length frequent itemSets
        :return: 1-length frequent items
        """
        _mapSupport = {}
        k = 0
        for tr in self._Database:
            k += 1
            for i in range(0, len(tr)):
                if tr[i] not in _mapSupport:
                    _mapSupport[tr[i]] = 1
                else:
                    _mapSupport[tr[i]] += 1
        _mapSupport = {k: v for k, v in _mapSupport.items() if v >= self._minSup}
        #print(len(mapSupport), self.minSup)
        genList = [k for k, v in sorted(_mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(genList)])
        return _mapSupport, genList

    def _updateTransactions(self, oneLength):
        """
        To sort the transactions in their support descending order and allocating ranks respectively
        :param oneLength: 1-length frequent items in dictionary
        :type oneLength: dict
        :return: returning the sorted list
        :Example: oneLength = {'a':7, 'b': 5, 'c':'4', 'd':3}
                    rank = {'a':0, 'b':1, 'c':2, 'd':3}
        """
        list1 = []
        for tr in self._Database:
            list2 = []
            for i in range(0, len(tr)):
                if tr[i] in oneLength:
                    list2.append(self._rank[tr[i]])
            if len(list2) >= 2:
                list2.sort()
                list1.append(list2)
        return list1


    def _buildTree(self, data, info):
        """
        creating the root node as null in fp-tree and adding all transactions into tree.
        :param data: updated transactions
        :type data: dict
        :param info: rank of items in transactions
        :type info: dict
        :return: fp-tree
        """
        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            rootNode.addTransaction(data[i])
        return rootNode


    def _convert(self, value):
        """
        To convert the type of user specified minSup value
        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = ((len(self._Database)) * value)
            else:
                value = int(value)
        return value

    def _convertItems(self, itemSet):
        """
        To convert the item ranks into their original item names
        :param itemSet: itemSet or a pattern
        :type itemSet: list
        :return: original pattern
        """
        t1 = []
        for i in itemSet:
            t1.append(self._rankdup[i])
        return t1

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Mining process will start from this function
        """

        self.mine()

    def mine(self):
        """
        Mining process will start from this function
        """

        global _minSup
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        _minSup = self._minSup
        generatedItems, pfList = self._frequentOneItem()
        updatedTransactions = self._updateTransactions(generatedItems)
        for x, y in self._rank.items():
            self._rankdup[y] = x
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        patterns = {}
        self._finalPatterns = {}
        self._maximalTree = _MPTree()
        Tree = self._buildTree(updatedTransactions, info)
        Tree.generatePatterns([], patterns, self._maximalTree)
        for x, y in patterns.items():
            pattern = str()
            x = self._convertItems(x)
            for i in x:
                pattern = pattern + i + "\t"
            self._finalPatterns[pattern] = y
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Maximal Frequent patterns were generated successfully using MaxFp-Growth algorithm ")

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

        return self._memoryRSS

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

        # dataframe = {}
        # data = []
        # for a, b in self._finalPatterns.items():
        #     data.append([a.replace('\t', ' '), b])
        #     dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])

        dataframe = _ab._pd.DataFrame(list([[x.replace('\t', ' '), y] for x,y in self._finalPatterns.items()]), columns=['Patterns', 'Support'])

        return dataframe

    def save(self, outFile):
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csvfile
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
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
        This functon is used to print the results
        """
        print('Total number of Maximal Frequent Patterns: ' + str(len(self.getPatterns())))
        print('Runtime: ' + str(self.getRuntime()))
        print('Memory (RSS): ' + str(self.getMemoryRSS()))
        print('Memory (USS): ' + str(self.getMemoryUSS()))


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = MaxFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = MaxFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        _ap.save(_ab._sys.argv[2])
        print("Total number of Maximal Frequent Patterns:", len(_ap.getPatterns()))
        print("Total Memory in USS:",  _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

