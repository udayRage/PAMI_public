# PPPGrowth is fundamental approach to mine the partial periodic patterns in temporal database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#         from PAMI.periodicFrequentPattern.basic import PPPGrowth as alg
#
#         obj = alg.PPPGrowth(iFile, minPS, period)
#
#         obj.mine()
#
#         partialPeriodicPatterns = obj.getPatterns()
#
#         print("Total number of partial periodic Patterns:", len(partialPeriodicPatterns))
#
#         obj.save(oFile)
#
#         Df = obj.getPatternInDf()
#
#         memUSS = obj.getMemoryUSS()
#
#         print("Total Memory in USS:", memUSS)
#
#         memRSS = obj.getMemoryRSS()
#
#         print("Total Memory in RSS", memRSS)
#
#         run = obj.getRuntime()
#
#         print("Total ExecutionTime in seconds:", run)
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


from PAMI.partialPeriodicPattern.basic import abstract as _abstract
from typing import List, Dict, Tuple, Set, Union, Any, Iterable, Generator
import validators as _validators
from urllib.request import urlopen as _urlopen
import sys as _sys
import pandas as pd
from deprecated import deprecated

_minPS = float()
_period = float()
_lno = int()

class _Node(object):
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int
            storing item of a node
        timeStamps : list
            To maintain the timestamps of transaction at the end of the branch
        parent : node
            To maintain the parent of every node
        children : list
            To maintain the children of node

    :Methods:

        addChild(itemName)
        storing the children to their respective parent nodes
    """

    def __init__(self, item: int, children: Dict) -> None:
        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = []

    def addChild(self, node: '_Node') -> None:
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
        getConditionalPatterns(Node)
            generates the conditional patterns from tree for specific node
        conditionalTransactions(prefixPaths,Support)
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

    def _addTransaction(self, transaction: List, tid: List) -> None:
        """
        adding transaction into tree

        :param transaction : it represents the one transactions in database
        :type transaction : list
        :param tid : represents the timestamp of transaction
        :type tid : list
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

    def _getConditionalPatterns(self, alpha: '_Node') -> Tuple[List, List, Dict]:
        """
        generates all the conditional patterns of respective node

        :param alpha : it represents the Node in tree
        :type alpha : Node
        :return: tuple
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
        finalPatterns, finalSets, info = self._conditionalTransactions(finalPatterns, finalSets)
        return finalPatterns, finalSets, info

    def _generateTimeStamps(self, node: '_Node') -> List:
        """
        generates the Time Stamps

        :param node : it represents the node in tree
        :type node : list
        """
        finalTs = node.timeStamps
        return finalTs

    def _removeNode(self, nodeValue: int) -> None:
        """
        removing the node from tree

        :param nodeValue : it represents the node in tree
        :type nodeValue : node
        :return: None
        """
        for i in self.summaries[nodeValue]:
            i.parent.timeStamps = i.parent.timeStamps + i.timeStamps
            del i.parent.children[nodeValue]

    def _getTimeStamps(self, alpha: '_Node') -> List:
        """
        Returns the timeStamps of a node

        :param alpha: node of tree
        :return: timeStamps of a node

        """
        temporary = []
        for i in self.summaries[alpha]:
            temporary += i.timeStamps
        return temporary

    def _getPeriodicSupport(self, timeStamps: List) -> int:
        """
        calculates the support and periodicity with list of timestamps

        :param timeStamps : timestamps of a pattern
        :type timeStamps : lis
        :return: int
        """
        timeStamps.sort()
        per = 0
        sup = 0
        for i in range(len(timeStamps) - 1):
            j = i + 1
            if abs(timeStamps[j] - timeStamps[i]) <= _period:
                per += 1
            sup += 1
        return per

    def _conditionalTransactions(self, conditionalPatterns: List, conditionalTimeStamps: List) -> Tuple[List, List, Dict]:
        """
        It generates the conditional patterns with periodic frequent items

        :param conditionalPatterns : conditional_patterns generated from condition_pattern method for
                                respective node
        :type conditionalPatterns : list
        :param conditionalTimeStamps : represents the timestamps of conditional patterns of a node
        :type conditionalTimeStamps : list

        :return: tuple
        """
        global _minPS, _period
        patterns = []
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
            updatedDictionary[m] = self._getPeriodicSupport(data1[m])
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v >= _minPS}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDictionary]
            trans = sorted(p1, key=lambda x: (updatedDictionary.get(x), -x), reverse=True)
            if len(trans) > 0:
                patterns.append(trans)
                timeStamps.append(conditionalTimeStamps[count])
            count += 1
        return patterns, timeStamps, updatedDictionary

    def _generatePatterns(self, prefix: List) -> Iterable[Tuple[List, int]]:
        """
        generates the patterns

        :param prefix : forms the combination of items
        :type prefix : list
        :return : list
        """
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x), -x)):
            pattern = prefix[:]
            pattern.append(i)
            yield pattern, self.info[i]
            patterns, timeStamps, info = self._getConditionalPatterns(i)
            conditionalTree = _Tree()
            conditionalTree.info = info.copy()
            for pat in range(len(patterns)):
                conditionalTree._addTransaction(patterns[pat], timeStamps[pat])
            if len(patterns) > 0:
                for q in conditionalTree._generatePatterns(pattern):
                    yield q
            self._removeNode(i)


class PPPGrowth(_abstract._partialPeriodicPatterns):
    """
    :Description:   3pgrowth is fundamental approach to mine the partial periodic patterns in temporal database.

    :Reference:   Discovering Partial Periodic Itemsets in Temporal Databases,SSDBM '17: Proceedings of the 29th International Conference on Scientific and Statistical Database ManagementJune 2017
                  Article No.: 30 Pages 1–6https://doi.org/10.1145/3085504.3085535

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minPS: float:
                   Minimum partial periodic pattern...
    :param  period: float:
                   Minimum partial periodic...

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        minPS: float or int or str
            The user can specify minPS either in count or proportion of database size.
            If the program detects the data type of minPS is integer, then it treats minPS is expressed in count.
            Otherwise, it will be treated as float.
            Example: minPS=10 will be treated as integer, while minPS=10.0 will be treated as float
        period: float or int or str
            The user can specify period either in count or proportion of database size.
            If the program detects the data type of period is integer, then it treats period is expressed in count.
            Otherwise, it will be treated as float.
            Example: period=10 will be treated as integer, while period=10.0 will be treated as float
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
            Complete set of frequent patterns will be loaded in to a output file
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
        partialPeriodicOneItem()
            Extracts the one-frequent patterns from transactions
        updateTransactions()
            updates the transactions by removing the aperiodic items and sort the transactions with items
            by decreasing support
        buildTree()
            constrcuts the main tree by setting the root node as null
        mine()
            main program to mine the partial periodic patterns

    **Executing the code on terminal:**
    --------------------------------------
      .. code-block:: console


       Format:

       (.venv) $python3 PPPGrowth.py <inputFile> <outputFile> <minPS> <period>
    
       Examples:

       (.venv) $ python3 PPPGrowth.py sampleDB.txt patterns.txt 10.0 2.0


    **Sample run of the importing code:**
    -----------------------------------------
    .. code-block:: python

            from PAMI.periodicFrequentPattern.basic import PPPGrowth as alg

            obj = alg.PPPGrowth(iFile, minPS, period)

            obj.mine()

            partialPeriodicPatterns = obj.getPatterns()

            print("Total number of partial periodic Patterns:", len(partialPeriodicPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDf()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

                run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)


    **Credits:**
    -----------------
    The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.\n

    """
    _minPS = float()
    _period = float()
    _startTime = float()
    _endTime = float()
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

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _abstract._pd.DataFrame):
            data, tids = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                tids = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            for i in range(len(data)):
                tr = [tids[i][0]]
                tr = tr + data[i]
                self._Database.append(tr)
            self._lno = len(self._Database)
            # print(self.Database)
        if isinstance(self._iFile, str):
            if _validators.url(self._iFile):
                data = _urlopen(self._iFile)
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

    def _partialPeriodicOneItem(self) -> Tuple[Dict, List]:
        """
        calculates the support of each item in the dataset and assign the ranks to the items by decreasing support and returns the frequent items list
        :return: tuple
        """
        data = {}
        self._period = self._convert(self._period)
        self._minPS = self._convert(self._minPS)
        for tr in self._Database:
            for i in range(1, len(tr)):
                if tr[i] not in data:
                    data[tr[i]] = [0, int(tr[0]), 1]
                else:
                    lp = int(tr[0]) - data[tr[i]][1]
                    if lp <= self._period:
                        data[tr[i]][0] += 1
                    data[tr[i]][1] = int(tr[0])
                    data[tr[i]][2] += 1
        data = {k: v[0] for k, v in data.items() if v[0] >= self._minPS}
        pfList = [k for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        return data, pfList

    def _updateTransactions(self, dict1: Dict) -> List[List]:
        """
        remove the items which are not frequent from transactions and updates the transactions with rank of items

        :param dict1 : frequent items with support
        :type dict1 : dictionary
        :return: list
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

    def _buildTree(self, data: List[List], info: Dict) -> '_Tree':
        """
        it takes the transactions and support of each item and construct the main tree with setting root
                            node as null

        :param data : it represents the one transactions in database
        :type data : list
        :param info : it represents the support of each item
        :type info : dictionary
        :return: tree
        """
        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            set1 = [data[i][0]]
            rootNode._addTransaction(data[i][1:], set1)
        return rootNode

    def _savePeriodic(self, itemset: List) -> str:
        """
        To convert the pattern with its original item name

        :param itemset: partial periodic pattern.
        :return: pattern with original item name
        """
        temp = str()
        for i in itemset:
            temp = temp + self._rankdup[i] + "\t"
        return temp

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
        Main method where the patterns are mined by constructing tree.
        :return: None
        """

        self.mine()


    def mine(self) -> None:
        """
        Main method where the patterns are mined by constructing tree.
        :return: None

        """
        global _minPS, _period, _lno
        self._startTime = _abstract._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minPS is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        generatedItems, pfList = self._partialPeriodicOneItem()
        _minPS, _period, _lno = self._minPS, self._period, len(self._Database)
        updatedTransactions = self._updateTransactions(generatedItems)
        for x, y in self._rank.items():
            self._rankdup[y] = x
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedTransactions, info)
        patterns = Tree._generatePatterns([])
        self._finalPatterns = {}
        for i in patterns:
            s = self._savePeriodic(i[0])
            self._finalPatterns[s] = i[1]
        self._endTime = _abstract._time.time()
        process = _abstract._psutil.Process(_abstract._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Partial Periodic Patterns were generated successfully using 3PGrowth algorithm ")


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

    def getPatternsAsDataFrame(self) -> _abstract._pd.DataFrame:
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _abstract._pd.DataFrame(data, columns=['Patterns', 'periodicSupport'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, int]:
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        :return: None
        """
        print("Total number of Partial Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_sys.argv) == 5 or len(_sys.argv) == 6:
        if len(_sys.argv) == 6:
            _ap = PPPGrowth(_sys.argv[1], _sys.argv[3], _sys.argv[4], _sys.argv[5])
        if len(_sys.argv) == 5:
            _ap = PPPGrowth(_sys.argv[1], _sys.argv[3], _sys.argv[4])
        _ap.mine()
        print("Total number of Partial Periodic Patterns:", len(_ap.getPatterns()))
        _ap.save(_sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:",  _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
        for i in [100, 200, 300, 400, 500]:
            _ap = PPPGrowth('/Users/tarunsreepada/Downloads/Temporal_T10I4D100K.csv', i, 5000, '\t')
            _ap.mine()
            print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
            _ap.save('/Users/tarunsreepada/Downloads/output.txt')
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
