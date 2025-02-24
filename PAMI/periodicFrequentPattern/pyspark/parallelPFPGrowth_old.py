# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.periodicFrequentPattern.basic import parallelPFPGrowth as alg
#
#             obj = alg.parallelPFPGrowth(iFile, minSup, maxPer, noWorkers)
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))
#
#             obj.savePatterns(oFile)
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

from PAMI.periodicFrequentPattern.pyspark import abstract as _ab
from pyspark import SparkContext, SparkConf

from PAMI.periodicFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated

_maxPer = float()
_minSup = float()
_lno = int()


class Node(object):
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
        count : int
            To maintain the count of every node

    :Methods:

        addChild(itemName)
            Storing the children to their respective parent nodes
        toString()
            To print the node
    """

    def __init__(self, item, count, children):
        """ Initializing the Node class

        :param item: item of a node
        :param count: count of a node
        :param children: children of a node

        """
        self.item = item
        self.count = count
        self.children = children  # dictionary of children
        self.parent = None
        self.tids = set()

    def __repr__(self):
        return self.toString(0)

    def toString(self, level=0):
        """ To print the node

        :param level: level of a node
        """
        if self.item is None:
            s = "Root("
        else:
            s = "(item=" + str(self.item)
            s += ", count=" + str(self.count)
            for i in self.tids:
                s += " " + str(i)
        tabs = "\t".join(['' for i in range(0, level + 2)])
        for v in self.children.values():
            s += tabs + "\n"
            s += tabs + v.toString(level=level + 1)
        s += ")"
        return s

    def addChild(self, node):
        """ To add the children to a node

        :param node: children of a node
        """
        self.children[node.item] = node
        node.parent = self

    def _getTransactions(self):
        count = self.count
        tids = self.tids
        for child in self.children.values():
            for t in child._getTransactions():
                count -= t[2]
                t[0].insert(0, child.item)
                yield t
        if count > 0:
            yield [], tids, count


class PFPTree(object):
    """

    A class used to represent the periodic frequent pattern tree

    :Attributes:

        root : node
            To maintain the root of the tree
        summaries : dict
            To maintain the summary of the tree

    :Methods:

        add(basket, tid, count)
            To add the basket to the tree
        getTransactions()
            To get the transactions of the tree
        merge(tree)
            To merge the tree
        project(itemId)
            To project the tree
        satisfyPer(tids, maxPer, numTrans)
            To satisfy the periodicity constraint
        extract(minCount, maxPer, numTrans, isResponsible = lambda x:True)
            To extract the periodic frequent patterns

    """

    def __init__(self):
        self.root = Node(None, 0, {})
        self.summaries = {}

    def __repr__(self):
        return repr(self.root)

    def add(self, basket, tid, count):
        """
        To add the basket to the tree

        :param basket: basket of a database
        :param tid: timestamp of a database
        :param count: count of a node
        """
        curr = self.root
        curr.count += count
        for i in tid:
            curr.tids.add(i)

        for i in range(0, len(basket)):
            item = basket[i]
            if item in self.summaries.keys():
                summary = self.summaries.get(item)
            else:
                summary = Summary(0, set())
                self.summaries[item] = summary
            summary.count += count

            if item in curr.children.keys():
                child = curr.children.get(item)
            else:
                child = Node(item, 0, {})
                curr.addChild(child)
            summary.nodes.add(child)
            child.count += count
            for j in tid:
                summary.tids.add(j)
                if i == len(basket) - 1:
                    child.tids.add(j)
            curr = child
        return self

    def getTransactions(self):
        """
        To get the transactions of the tree

        :return: returning the transactions of the tree
        """
        return [x for x in self.root._getTransactions()]

    def merge(self, tree):
        """
        To merge the tree

        :param tree: tree of a database
        """
        for t in tree.getTransactions():
            self.add(t[0], t[1], t[2])
        return self

    def project(self, itemId):
        """
        To project the tree

        :param itemId: item of a node
        """
        newTree = PFPTree()
        summaryItem = self.summaries.get(itemId)
        if summaryItem:
            for element in summaryItem.nodes:
                t = []
                curr = element.parent
                while curr.parent:
                    t.insert(0, curr.item)
                    curr = curr.parent
                newTree.add(t, element.tids, element.count)
        return newTree

    def satisfyPer(self, tids, maxPer, numTrans):
        """
        To satisfy the periodicity constraint

        :param tids: timestamps of a database
        :param maxPer: maximum periodicity
        :param numTrans: number of transactions
        """

        tids = list(tids)
        tids.sort()
        if tids[0] > maxPer:
            return 0
        tids.append(numTrans)
        for i in range(1, len(tids)):
            if (tids[i] - tids[i - 1]) > maxPer:
                return 0
        return 1

    def extract(self, minCount, maxPer, numTrans, isResponsible=lambda x: True):
        """
        To extract the periodic frequent patterns

        :param minCount: minimum count of a node
        :param maxPer: maximum periodicity
        :param numTrans: number of transactions
        :param isResponsible: responsible node of a tree
        """
        for item in sorted(self.summaries, reverse=True):
            summary = self.summaries[item]
            if isResponsible(item):
                if summary.count >= minCount and self.satisfyPer(summary.tids, maxPer, numTrans):
                    yield [item], summary.count
                    for element in self.project(item).extract(minCount, maxPer, numTrans):
                        yield [item] + element[0], element[1]
            for element in summary.nodes:
                parent = element.parent
                parent.tids |= element.tids


class Summary(object):
    """
    A class used to represent the summary of the tree

    :Attributes:

        count : int
            To maintain the count of a node
        nodes : list
            To maintain the nodes of a tree
        tids : set
            To maintain the timestamps of a database

    """

    def __init__(self, count, nodes):
        self.count = count
        self.nodes = nodes
        self.tids = set()


class parallelPFPGrowth(_ab._periodicFrequentPatterns):
    """
    :Description:   ParallelPFPGrowth is one of the fundamental distributed algorithm to discover periodic-frequent patterns in a transactional database. It is based PySpark framework.

    :Reference:   C. Saideep, R. Uday Kiran, Koji Zettsu, Cheng-Wei Wu, P. Krishna Reddy, Masashi Toyoda, Masaru Kitsuregawa: Parallel Mining of Partial Periodic Itemsets in Big Data. IEA/AIE 2020: 807-819

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  minSup: str:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  maxPer: str:
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
        numWorker: int
            The user can specify the number of worker machines to be employed for finding periodic-frequent patterns.
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


    **Methods to execute code on terminal**
    --------------------------------------------
   .. code-block:: console


       Format:


       (.venv) $ python3 parallelPFPGrowth_old.py <inputFile> <outputFile> <minSup> <maxPer> <noWorker>

       Example usage :

       (.venv) $ python3 parallelPFPGrowth_old.py sampleTDB.txt patterns.txt 0.3 0.4 5


               .. note:: minSup will be considered in percentage of database transactions


    **Importing this algorithm into a python program**
    -----------------------------------------------------
    .. code-block:: python

                from PAMI.periodicFrequentPattern.basic import parallelPFPGrowth as alg

                obj = alg.parallelPFPGrowth(iFile, minSup, maxPer)

                obj.mine()

                periodicFrequentPatterns = obj.getPatterns()

                print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))

                obj.savePatterns(oFile)

                Df = obj.getPatternsAsDataFrame()

                memUSS = obj.getMemoryUSS()

                print("Total Memory in USS:", memUSS)

                memRSS = obj.getMemoryRSS()

                print("Total Memory in RSS", memRSS)

                run = obj.getRuntime()

                print("Total ExecutionTime in seconds:", run)

    """
    __startTime = float()
    __endTime = float()
    _minSup = str()
    _maxPer = str()
    _numWorkers = str()
    __finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    __memoryUSS = float()
    __memoryRSS = float()
    __Database = []
    __mapSupport = {}
    __lno = 0
    # __tree = _Tree()
    __rank = {}
    __rankDup = {}
    _numTrans = str()
    __tarunpat = {}
    _perFreqItems = None

    def __init__(self, iFile, minSup, maxPer, numWorker, sep='\t'):
        super().__init__(iFile, minSup, maxPer, numWorker)

    def func1(self, ps1, tid):
        """
        Add the tid to the set

        :param ps1: set
        :param tid: timestamp of a database
        return: set

        """
        ps1.add(tid)
        return ps1

    def func2(self, ps1, ps2):
        """

        Union of two sets

        :param ps1: set.
        :param ps2: set
        return: set

        """

        ps1 |= ps2
        return ps1

    def func3(self, tids, endts):
        """

        Calculate the periodicity of a transaction

        :param tids: timestamps of a database
        return: periodicity
        :param endts: last timestamp
        return: periodicity
        """
        # print(tids)
        z = sorted(tids)
        # print(maxPer)
        cur = 0
        for i in z:
            if i - cur > self._maxPer:
                return -1
            cur = i
        if endts - cur > self._maxPer:
            return -1
        else:
            return len(z)

    def getFrequentItems(self, data):
        """
        Get the frequent items from the database

        :param data: database
        return: frequent items
        """
        singleItems = data.flatMap(lambda x: [(x[i], x[0]) for i in range(1, len(x))])
        ps = set()
        freqItems = singleItems.aggregateByKey(ps, lambda ps1, tid: self.func1(ps1, tid),
                                               lambda tuple1, tuple2: self.func2(tuple1, tuple2))
        # print(freqItems.take(10))
        freqItems = freqItems.map(lambda x: (x[0], self.func3(x[1], self._numTrans.value)))
        # print(freqItems.take(10))
        perFreqItems = [x for (x, y) in
                        sorted(freqItems.filter(lambda c: c[1] >= self._minSup).collect(), key=lambda x: -x[1])]
        # print(perFreqItems)
        return perFreqItems

    def getFrequentItemsets(self, data, freqItems):
        """
        Get the frequent itemsets from the database

        :param data: database
        :param freqItems: frequent items
        return: frequent itemsets

        """
        rank = dict([(index, item) for (item, index) in enumerate(self._perFreqItems)])
        numPartitions = data.getNumPartitions()
        workByPartition = data.flatMap(
            lambda basket: self.genCondTransactions(basket[0], basket[1:], rank, numPartitions))
        emptyTree = PFPTree()
        forest = workByPartition.aggregateByKey(emptyTree,
                                                lambda tree, transaction: tree.add(transaction[0], [transaction[1]], 1),
                                                lambda tree1, tree2: tree1.merge(tree2))
        itemsets = forest.flatMap(
            lambda partId_bonsai: partId_bonsai[1].extract(self._minSup, self._maxPer, self._numTrans.value,
                                                           lambda x: self.getPartitionId(x, numPartitions) ==
                                                                     partId_bonsai[0]))
        frequentItemsets = itemsets.map(
            lambda ranks_count: ([self._perFreqItems[z] for z in ranks_count[0]], ranks_count[1]))

        ### TARUN MODIFICATION ###
        frequentItemsets_list = frequentItemsets.collect()

        for itemset, count in frequentItemsets_list:
            string = "\t".join([str(x) for x in itemset])
            self.__tarunpat[string] = count
        ##########################

        return frequentItemsets

    def genCondTransactions(self, tid, basket, rank, nPartitions):
        """
        Get the conditional transactions from the database

        :param tid: timestamp of a database
        :param basket: basket of a database
        :param rank: rank of a database
        :param nPartitions: number of partitions
        """
        filtered = [rank[int(x)] for x in basket if int(x) in rank.keys()]
        filtered = sorted(filtered)
        output = {}
        for i in range(len(filtered) - 1, -1, -1):
            item = filtered[i]
            partition = self.getPartitionId(item, nPartitions)
            if partition not in output.keys():
                output[partition] = [filtered[:i + 1], tid]
        return [x for x in output.items()]

    def getPartitionId(self, key, nPartitions):
        """
        Get the partition id

        :param key: key of a database
        :param nPartitions: number of partitions
        return: partition id

        """
        return key % nPartitions

    def __convert(self, value):
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self.__Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self.__Database) * value)
            else:
                value = int(value)
        return value

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Start the mining process

        """
        self.__startTime = _ab._time.time()

        APP_NAME = "parallelPFPGrowth"
        conf = _ab.SparkConf().setAppName(APP_NAME)
        # conf = conf.setMaster("local[*]")
        sc = _ab.SparkContext(conf=conf).getOrCreate()
        # sc = SparkContext.getOrCreate();
        data = sc.textFile(self._iFile, minPartitions=self._numWorkers).map(
            lambda x: [int(y) for y in x.strip().split(self._sep)])
        # data = sc.textFile(finput).map(lambda x: [int(y) for y in x.strip().split(' ')])
        data.cache()
        # minSupport = data.count() * threshold/100
        # maxPer = data.count() * periodicity_threshold/100
        self._minSup = self.__convert(self._minSup)
        self._maxPer = self.__convert(self._maxPer)
        self._numTrans = sc.broadcast(data.count())
        self._perFreqItems = self.getFrequentItems(data)
        freqItemsets = self.getFrequentItemsets(data, self._perFreqItems)
        self.__finalPatterns = self.__tarunpat
        sc.stop()
        self.__endTime = _ab._time.time()
        self.__memoryUSS = float()
        self.__memoryRSS = float()
        process = _ab._psutil.Process(_ab._os.getpid())
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss

    def Mine(self):
        """
        Start the mining process

        """
        self.__startTime = _ab._time.time()

        APP_NAME = "parallelPFPGrowth"
        conf = _ab.SparkConf().setAppName(APP_NAME)
        # conf = conf.setMaster("local[*]")
        sc = _ab.SparkContext(conf=conf).getOrCreate()
        # sc = SparkContext.getOrCreate();
        data = sc.textFile(self._iFile, minPartitions=self._numWorkers).map(
            lambda x: [int(y) for y in x.strip().split(self._sep)])
        # data = sc.textFile(finput).map(lambda x: [int(y) for y in x.strip().split(' ')])
        data.cache()
        # minSupport = data.count() * threshold/100
        # maxPer = data.count() * periodicity_threshold/100
        self._minSup = self.__convert(self._minSup)
        self._maxPer = self.__convert(self._maxPer)
        self._numTrans = sc.broadcast(data.count())
        self._perFreqItems = self.getFrequentItems(data)
        freqItemsets = self.getFrequentItemsets(data, self._perFreqItems)
        self.__finalPatterns = self.__tarunpat
        sc.stop()
        self.__endTime = _ab._time.time()
        self.__memoryUSS = float()
        self.__memoryRSS = float()
        process = _ab._psutil.Process(_ab._os.getpid())
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss


    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__endTime - self.__startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self.__tarunpat.items():
            data.append([a.replace('\t', ' '), b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        # print(self.getFrequentItems())
        for x, y in self.__tarunpat.items():
            # print(x,y)
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self.__tarunpat

    def printResults(self):
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 6 or len(_ab._sys.argv) == 7:
        if len(_ab._sys.argv) == 7:
            _ap = parallelPFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5],
                                    _ab._sys.argv[6])
        if len(_ab._sys.argv) == 4:
            _ap = parallelPFPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        _ap.mine()
        print("Total number of Frequent Patterns:", _ab.getPatterns())
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = parallelPFPGrowth('Temporal_T10I4D100K.csv', 500, 5000, 5, '\t')
        _ap.mine()
        # print("Total number of Frequent Patterns:", len( _ab.getPatterns()))
        # _ap.save(_ab._sys.argv[2])
        _ap.printResults()
        # print("Total Memory in USS:", _ap.getMemoryUSS())
        # print("Total Memory in RSS", _ap.getMemoryRSS())
        # print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")