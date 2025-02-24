# PPGrowth is one of the fundamental algorithm to discover periodic-frequent patterns in a transactional database.
#
# **Importing this algorithm into a python program**
#
#     from PAMI.periodicFrequentPattern.basic import PPGrowth as alg
#
#     obj = alg.PPGrowth(iFile, minSup, maxPer)
#
#     obj.mine()
#
#     periodicFrequentPatterns = obj.getPatterns()
#
#     print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))
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

import pandas as pd
from deprecated import deprecated
from PAMI.partialPeriodicPatternInMultipleTimeSeries import abstract as _ab



_lno = int()
_periodicSupport = float()
_period = float()

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
        self.parent = None
        self.timeStamps = []

    def addChild(self, node):
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

    def __init__(self):
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction, tid):
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

    def getConditionalPatterns(self, alpha):
        """
        Generates all the conditional patterns of a respective node

        :param alpha: To represent a Node in the tree
        :type alpha: Node
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
        finalPatterns, finalSets, info = self.conditionalDatabases(finalPatterns, finalSets)
        return finalPatterns, finalSets, info

    @staticmethod
    def generateTimeStamps(node):
        """
        To get the timestamps of a node

        :param node: A node in the tree
        :return: Timestamps of a node
        """

        finalTimeStamps = node.timeStamps
        return finalTimeStamps

    def removeNode(self, nodeValue):
        """
        Removing the node from tree

        :param nodeValue: To represent a node in the tree
        :type nodeValue: node
        :return: Tree with their nodes updated with timestamps
        """

        for i in self.summaries[nodeValue]:
            i.parent.timeStamps = i.parent.timeStamps + i.timeStamps
            del i.parent.children[nodeValue]

    def getTimeStamps(self, alpha):
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
    def getSupportAndPeriod(timeStamps):
        """
        To calculate the periodicity and support

        :param timeStamps: Timestamps of an item set
        :return: support, periodicity
        """

        #global _maxPer, _lno,_period,_periodicSupport
        timeStamps.sort()
        cur = 0
        per = list()
        sup = 0
        for j in range(len(timeStamps)):
            timedif=timeStamps[j] - cur
            per.append(timedif)
            cur = timeStamps[j]
            if _period>=timedif:
                sup += 1
        per.append(_lno - cur)
        if len(per) == 0:
            return [0, 0]
        return [sup, max(per)]

    def conditionalDatabases(self, conditionalPatterns, conditionalTimeStamps):
        """
        It generates the conditional patterns with periodic-frequent items

        :param conditionalPatterns: conditionalPatterns generated from conditionPattern method of a respective node
        :type conditionalPatterns: list
        :param conditionalTimeStamps: Represents the timestamps of a conditional patterns of a node
        :type conditionalTimeStamps: list
        :returns: Returns conditional transactions by removing non-periodic and non-frequent items
        """

        global _periodicSupport,_period
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
            updatedDictionary[m] = self.getSupportAndPeriod(data1[m])
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v[0] >= _periodicSupport and v[1] <= _period}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDictionary]
            trans = sorted(p1, key=lambda x: (updatedDictionary.get(x)[0], -x), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                timeStamps.append(conditionalTimeStamps[count])
            count += 1
        return pat, timeStamps, updatedDictionary

    def generatePatterns(self, prefix):
        """
        Generates the patterns

        :param prefix: Forms the combination of items
        :type prefix: list
        :returns: yields patterns with their support and periodicity
        """

        for i in sorted(self.summaries, key=lambda x: (self.info.get(x)[0], -x)):
            pattern = prefix[:]
            pattern.append(i)
            yield pattern, self.info[i]
            patterns, timeStamps, info = self.getConditionalPatterns(i)
            conditionalTree = _Tree()
            conditionalTree.info = info.copy()
            for pat in range(len(patterns)):
                conditionalTree.addTransaction(patterns[pat], timeStamps[pat])
            if len(patterns) > 0:
                for q in conditionalTree.generatePatterns(pattern):
                    yield q
            self.removeNode(i)


class PPGrowth(_ab._partialPeriodicPatterns):
    """
    About this algorithm
    ====================

    :Description:   PPGrowth is one of the fundamental algorithm to discover periodic-frequent patterns in a transactional database.

    :Reference:   C. Saideep, R. Uday Kiran, K. Zettsu, P. Fournier-Viger, M. Kitsuregawa and P. Krishna Reddy,
                 "Discovering Periodic Patterns in Irregular Time Series," 2019 International Conference on Data Mining Workshops (ICDMW), 2019,
                  pp. 1020-1028, doi: 10.1109/ICDMW.2019.00147.

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
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

    Execution methods
    =================


    **Terminal command**


    .. code-block:: console

       Format:

       (.venv) $ python3 PPGrowth.py <inputFile> <outputFile> <minSup> <maxPer>

       Examples:

       (.venv) $  python3 PPGrowth.py sampleTDB.txt patterns.txt 0.3 0.4

    **Sample run of importing the code:**
    ----------------------------------------

        from PAMI.periodicFrequentPattern.basic import PPGrowth as alg

        obj = alg.PPGrowth(iFile, minSup, maxPer)

        obj.mine()

        periodicFrequentPatterns = obj.getPatterns()

        print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))

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


            The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """
    _startTime = float()
    _endTime = float()
    _periodicSupport = str()
    _period = float()
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

    def _creatingItemSets(self):
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

    def _periodicFrequentOneItem(self):
        """
        Calculates the support of each item in the database and assign ranks to the items
        by decreasing support and returns the frequent items list

        :returns: return the one-length periodic frequent patterns
        """
        global _periodicSupport,_period
        data = {}
        for tr in self._Database:
            for i in range(1, len(tr)):
                if tr[i] not in data:
                    data[tr[i]] = [int(tr[0]), int(tr[0]), 1]
                else:
                    data[tr[i]][0] = max(data[tr[i]][0], (int(tr[0]) - data[tr[i]][1]))
                    data[tr[i]][1] = int(tr[0])
                    if _period>=int(tr[0]) - data[tr[i]][1]:
                        data[tr[i]][2] += 1
        for key in data:
            data[key][0] = max(data[key][0], abs(len(self._Database) - data[key][1]))
        data = {k: [v[2], v[0]] for k, v in data.items() if v[2] >= _periodicSupport}
        pfList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        return data, pfList

    def _updateDatabases(self, dict1):
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
    def _buildTree(data, info):
        """
        It takes the database and support of an each item and construct the main tree by setting root node as a null

        :param data: it represents the one Databases in database
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

    def _savePeriodic(self, itemSet,change):
        """
        To convert the ranks of items in to their original item names

        :param itemSet: frequent pattern
        :return: frequent pattern with original item names
        """
        t1 = str()
        for i in itemSet:
            t1 = str(t1) + change[(self._rankedUp[i])] + "\t"
        return t1

    def _convert(self, value):
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

    def _convertNumber(self):
        """
        To convert the given number
        """
        changeDic={}
        rechangeDic={}
        newDatabase=[]
        count=0
        for i in self._Database:
            line=[int(i[0])]
            for j in i[1:]:
                if j not in changeDic:
                    changeDic[j]=count
                    rechangeDic[count]=j
                    line.append(count)
                    count=count+1
                else:
                    line.append(changeDic[j])
            newDatabase.append(line)
        self._Database=newDatabase
        return rechangeDic

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Mining process will start from this function
        """

        #global _minSup, _maxPer, _lno,_period,_periodicSupport
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._periodicSupport is None:
            raise Exception("Please enter the Periodic Support")
        self._creatingItemSets()
        changeDic = self._convertNumber()
        self._periodicSupport = self._convert(self._periodicSupport)
        self._period = self._convert(self._period)
        _periodicSupport, _period, _lno = self._periodicSupport, self._period, len(self._Database)
        if self._periodicSupport > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")

        generatedItems, pfList = self._periodicFrequentOneItem()
        updatedDatabases = self._updateDatabases(generatedItems)
        self._rankedUp={y:x for x, y in self._rank.items()}
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedDatabases, info)
        patterns = Tree.generatePatterns([])

        self._finalPatterns = {}
        self._finalPatterns={self._savePeriodic(i[0],changeDic):i[1]for i in patterns}
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Periodic Frequent patterns were generated successfully using PPGrowth algorithm ")

    def Mine(self):
        """
        Mining process will start from this function
        """

        #global _minSup, _maxPer, _lno,_period,_periodicSupport
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._periodicSupport is None:
            raise Exception("Please enter the Periodic Support")
        self._creatingItemSets()
        changeDic = self._convertNumber()
        self._periodicSupport = self._convert(self._periodicSupport)
        self._period = self._convert(self._period)
        _periodicSupport, _period, _lno = self._periodicSupport, self._period, len(self._Database)
        if self._periodicSupport > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")

        generatedItems, pfList = self._periodicFrequentOneItem()
        updatedDatabases = self._updateDatabases(generatedItems)
        self._rankedUp={y:x for x, y in self._rank.items()}
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedDatabases, info)
        patterns = Tree.generatePatterns([])

        self._finalPatterns = {}
        self._finalPatterns={self._savePeriodic(i[0],changeDic):i[1]for i in patterns}
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Periodic Frequent patterns were generated successfully using PPGrowth algorithm ")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of periodic-frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Partial Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = PPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = PPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
