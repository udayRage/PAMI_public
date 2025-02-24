# SWFPGrowth is an algorithm to mine the weighted spatial frequent patterns in spatiotemporal databases.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.weightFrequentNeighbourhoodPattern.basic import SWFPGrowth as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.SWFPGrowth(iFile, wFile, nFile, minSup, minWeight, sep)
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

from PAMI.weightedFrequentNeighbourhoodPattern.basic import abstract as _fp
import pandas as pd
from deprecated import deprecated
from typing import List, Dict, Tuple, Union, Iterable

_minWS = str()
_weights = {}
_rank = {}
_neighbourList = {}

_fp._sys.setrecursionlimit(20000)


class _WeightedItem:
    """
    A class used to represent the weight of the item

    :Attributes:

        item: str
            storing item of the frequent pattern

        weight: float
            stores the weight of the item

    """
    def __init__(self, item: str, weight: float) -> None:
        self.item = item
        self.weight = weight


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

    def __init__(self, item: str, children: Dict[str, '_Node']) -> None:
        self.itemId = item
        self.counter = 1
        self.weight = 0
        self.parent = None
        self.children = children

    def addChild(self, node: '_Node') -> None:
        """
        Retrieving the child from the tree

        :param node: Children node.
        :type node: Node
        :return: Updates the children nodes and parent nodes
        :return: None

        """
        self.children[node.itemId] = node
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
            sort the patterns by removing the items with lower minWS
        generatePatterns(prefix)
            generating the patterns from fp-tree
    """

    def __init__(self) -> None:
        self.root = _Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction: List[_WeightedItem], count: int) -> None:
        """
        Adding transaction into tree

        :param transaction: it represents the one transaction in database
        :type transaction: list
        :param count: frequency of item
        :type count: int
        :return: None
        """

        # This method takes transaction as input and returns the tree
        global _neighbourList, _rank
        currentNode = self.root
        for i in range(len(transaction)):
            wei = 0
            l1 = i
            while l1 >= 0:
                wei += transaction[l1].weight
                l1 -= 1
            if transaction[i].item not in currentNode.children:
                newNode = _Node(transaction[i].item, {})
                newNode.freq = count
                newNode.weight = wei
                currentNode.addChild(newNode)
                if _rank[transaction[i].item] in self.summaries:
                    self.summaries[_rank[transaction[i].item]].append(newNode)
                else:
                    self.summaries[_rank[transaction[i].item]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i].item]
                currentNode.freq += count
                currentNode.weight += wei

    def addConditionalPattern(self, transaction: List[_WeightedItem], count: int) -> None:
        """
        Adding transaction into tree

        :param transaction: it represents the one transaction in database
        :type transaction: list
        :param count: frequency of item
        :type count: int
        :return : None
        """
        # This method takes transaction as input and returns the tree
        global _neighbourList, _rank
        currentNode = self.root
        for i in range(len(transaction)):
            wei = 0
            l1 = i
            while l1 >= 0:
                wei += transaction[l1].weight
                l1 -= 1
            if transaction[i].itemId not in currentNode.children:
                newNode = _Node(transaction[i].itemId, {})
                newNode.freq = count
                newNode.weight = wei
                currentNode.addChild(newNode)
                if _rank[transaction[i].itemId] in self.summaries:
                    self.summaries[_rank[transaction[i].itemId]].append(newNode)
                else:
                    self.summaries[_rank[transaction[i].itemId]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i].itemId]
                currentNode.freq += count
                currentNode.weight += wei

    def printTree(self, root: _Node) -> None:
        """
        To print the details of tree

        :param root: root node of the tree
        :return: details of tree
        """
        if len(root.children) == 0:
            return
        else:
            for x, y in root.children.items():
                #print(y.itemId, y.parent.itemId, y.freq, y.weight)
                self.printTree(y)


    def getFinalConditionalPatterns(self, alpha: int) -> Tuple[List[List[_Node]], List[float], Dict[int, float]]:
        """
        Generates the conditional patterns for a node

        :param alpha: node to generate conditional patterns
        :return: returns conditional patterns, frequency of each item in conditional patterns
        """
        finalPatterns = []
        finalFreq = []
        global _neighbourList
        for i in self.summaries[alpha]:
            set1 = i.weight
            set2 = []
            while i.parent.itemId is not None:
                if i.parent.itemId in _neighbourList[i.itemId]:
                    set2.append(i.parent)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                finalFreq.append(set1)
        finalPatterns, finalFreq, info = self.getConditionalTransactions(finalPatterns, finalFreq)
        return finalPatterns, finalFreq, info

    @staticmethod
    def getConditionalTransactions(ConditionalPatterns: List[List[_Node]], conditionalFreq: List[float]) -> Tuple[List[List[_Node]], List[float], Dict[int, float]]:
        """
        To calculate the frequency of items in conditional patterns and sorting the patterns

        :param ConditionalPatterns: paths of a node
        :param conditionalFreq: frequency of each item in the path
        :return: conditional patterns and frequency of each item in transactions
        """
        global _rank
        pat = []
        freq = []
        data1 = {}
        for i in range(len(ConditionalPatterns)):
            for j in ConditionalPatterns[i]:
                if j.itemId in data1:
                    data1[j.itemId] += conditionalFreq[i]
                else:
                    data1[j.itemId] = conditionalFreq[i]
        up_dict = {k: v for k, v in data1.items() if v >= _minWS}
        count = 0
        for p in ConditionalPatterns:
            p1 = [v for v in p if v.itemId in up_dict]
            trans = sorted(p1, key=lambda x: (up_dict.get(x)), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                freq.append(conditionalFreq[count])
            count += 1
        up_dict = {_rank[k]: v for k, v in up_dict.items()}
        return pat, freq, up_dict

    def generatePatterns(self, prefix: List[int]) -> Iterable[Tuple[List[int], float]]:
        """
        To generate the frequent patterns

        :param prefix: an empty list
        :return: Frequent patterns that are extracted from fp-tree

        """
        global _minWS
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x))):
            pattern = prefix[:]
            pattern.append(i)
            yield pattern, self.info[i]
            patterns, freq, info = self.getFinalConditionalPatterns(i)
            conditionalTree = _Tree()
            conditionalTree.info = info.copy()
            for pat in range(len(patterns)):
                conditionalTree.addConditionalPattern(patterns[pat], freq[pat])
            if len(patterns) > 0:
                for q in conditionalTree.generatePatterns(pattern):
                    yield q


class SWFPGrowth(_fp._weightedFrequentSpatialPatterns):
    """
    About this algorithm
    ====================

    :Description: SWFPGrowth is an algorithm to mine the weighted spatial frequent patterns in spatiotemporal databases.

    :Reference: R. Uday Kiran, P. P. C. Reddy, K. Zettsu, M. Toyoda, M. Kitsuregawa and P. Krishna Reddy,
                "Discovering Spatial Weighted Frequent Itemsets in Spatiotemporal Databases," 2019 International
                Conference on Data Mining Workshops (ICDMW), 2019, pp. 987-996, doi: 10.1109/ICDMW.2019.00143.

    :param  iFile: str :
                   Name of the Input file to mine complete set of weighted Frequent Neighbourhood Patterns.
    :param  oFile: str :
                   Name of the output file to store complete set of weighted Frequent Neighbourhood Patterns.
    :param  minSup: int or str or float:
                   minimum support thresholds were tuned to find the appropriate ranges in the limited memory
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    :param  maxper: floot :
                   where maxPer represents the maximum periodicity threshold value specified by the user.


    :Attributes:

        iFile : file
            Input file name or path of the input file

        minWS: float or int or str
            The user can specify minWS either in count or proportion of database size.
            If the program detects the data type of minWS is integer, then it treats minWS is expressed in count.
            Otherwise, it will be treated as float.
            Example: minWS=10 will be treated as integer, while minWS=10.0 will be treated as float

        minWeight: float or int or str
            The user can specify minWeight either in count or proportion of database size.
            If the program detects the data type of minWeight is integer, then it treats minWeight is expressed in count.
            Otherwise, it will be treated as float.
            Example: minWeight=10 will be treated as integer, while minWeight=10.0 will be treated as float

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

    :Methods :

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

       (.venv) $ python3 SWFPGrowth.py <inputFile> <weightFile> <outputFile> <minSup> <minWeight>

       Example usage :

       (.venv) $ python3 SWFPGrowth.py sampleDB.txt weightFile.txt patterns.txt 10  2

    .. note:: minSup will be considered in support count or frequency


    **Calling from a python program**

    .. code-block:: python

            from PAMI.weightFrequentNeighbourhoodPattern.basic import SWFPGrowth as alg

            obj = alg.SWFPGrowth(iFile, wFile, nFile, minSup, minWeight, seperator)

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

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


            The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    __startTime = float()
    __endTime = float()
    _Weights = {}
    _minWS = str()
    __finalPatterns = {}
    _neighbourList = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    __memoryUSS = float()
    __memoryRSS = float()
    __Database = []
    __mapSupport = {}
    __lno = 0
    __tree = _Tree()
    __rank = {}
    __rankDup = {}

    def __init__(self, iFile: Union[str, _fp._pd.DataFrame], nFile: Union[str, _fp._pd.DataFrame], minWS: Union[int, float, str], sep='\t') -> None:
        super().__init__(iFile, nFile, minWS, sep)

    def __creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable

        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, _fp._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
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
                            line = line.strip()
                            line = line.split(':')
                            temp1 = [i.rstrip() for i in line[0].split(self._sep)]
                            temp2 = [int(i.strip()) for i in line[1].split(self._sep)]
                            tr = []
                            for i in range(len(temp1)):
                                we = _WeightedItem(temp1[i], temp2[i])
                                tr.append(we)
                            self._Database.append(tr)
                except IOError:
                    print("File Not Found")
                    quit()

    def _scanNeighbours(self) -> None:
        """
        Scans the neighbors file and creates a dictionary of items and their corresponding neighbor lists.

        :return: None
        """
        self._neighbourList = {}
        if isinstance(self._nFile, _fp._pd.DataFrame):
            data, items = [], []
            if self._nFile.empty:
                print("its empty..")
            i = self._nFile.columns.values.tolist()
            if 'item' in i:
                items = self._nFile['items'].tolist()
            if 'Neighbours' in i:
                data = self._nFile['Neighbours'].tolist()
            for k in range(len(items)):
                self._neighbourList[items[k][0]] = data[k]
            # print(self.Database)
        if isinstance(self._nFile, str):
            if _fp._validators.url(self._nFile):
                data = _fp._urlopen(self._nFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._neighbourList[temp[0]] = temp[1:]
            else:
                try:
                    with open(self._nFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._neighbourList[temp[0]] = temp[1:]
                except IOError:
                    print("File Not Found2")
                    quit()

    def __convert(self, value: Union[int, float, str]) -> Union[int, float]:
        """
        To convert the type of user specified minWS value

        :param value: user specified minWS value
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

    def __frequentOneItem(self) -> List[str]:
        """
        Generating One frequent items sets

        :return: None
        """
        global _maxWeight
        self._mapSupport = {}
        for tr in self._Database:
            for i in tr:
                nn = [j for j in tr if j.item in self._neighbourList[i.item]]
                if i.item not in self._mapSupport:
                    self._mapSupport[i.item] = i.weight
                else:
                    self._mapSupport[i.item] += i.weight
                for k in nn:
                    self._mapSupport[i.item] += k.weight
        self._mapSupport = {k: v for k, v in self._mapSupport.items() if v >= self._minWS}
        genList = [k for k, v in sorted(self._mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.__rank = dict([(index, item) for (item, index) in enumerate(genList)])
        return genList

    def __updateTransactions(self, itemSet: List[str]) -> List[List[_WeightedItem]]:
        """
        Updates the items in transactions with rank of items according to their support

        :Example: oneLength = {'a':7, 'b': 5, 'c':'4', 'd':3}
                  rank = {'a':0, 'b':1, 'c':2, 'd':3}
        :param itemSet: list of one-frequent items
        :return: list
        """
        list1 = []
        for tr in self._Database:
            list2 = []
            for i in range(len(tr)):
                if tr[i].item in itemSet:
                    list2.append(tr[i])
            if len(list2) >= 1:
                basket = list2
                basket.sort(key=lambda val: self.__rank[val.item])
                list1.append(basket)
        return list1

    @staticmethod
    def __buildTree(transactions: List[List[_WeightedItem]], info: Dict[int, float]) -> _Tree:
        """
        Builds the tree with updated transactions

        :param transactions: updated transactions
        :param info: support details of each item in transactions.
        :return: transactions compressed in fp-tree.
        """
        rootNode = _Tree()
        rootNode.info = info.copy()
        for i in range(len(transactions)):
            rootNode.addTransaction(transactions[i], 1)
        return rootNode

    def __savePeriodic(self, itemSet: List[str]) -> str:
        """
        The duplication items and their ranks

        :param itemSet: frequent itemSet that generated
        :return: patterns with original item names.

        """
        temp = str()
        for i in itemSet:
            temp = temp + self.__rankDup[i] + "\t"
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
        global _minWS, _neighbourList, _rank
        self.__startTime = _fp._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minWS is None:
            raise Exception("Please enter the Minimum Support")
        self.__creatingItemSets()
        self._scanNeighbours()
        self._minWS = self.__convert(self._minWS)
        _minWS = self._minWS
        itemSet = self.__frequentOneItem()
        updatedTransactions = self.__updateTransactions(itemSet)
        info = {self.__rank[k]: v for k, v in self._mapSupport.items()}
        _rank = self.__rank
        for x, y in self.__rank.items():
            self.__rankDup[y] = x
        _neighbourList = self._neighbourList
        #self._neighbourList = {k:v for k, v in self._neighbourList.items() if k in self._mapSupport.keys()}
        # for x, y in self._neighbourList.items():
        #     xx = [self.__rank[i] for i in y if i in self._mapSupport.keys()]
        #     _neighbourList[self.__rank[x]] = xx
        # print(_neighbourList)
        __Tree = self.__buildTree(updatedTransactions, info)
        patterns = __Tree.generatePatterns([])
        self.__finalPatterns = {}
        for k in patterns:
            s = self.__savePeriodic(k[0])
            self.__finalPatterns[str(s)] = k[1]
        print("Weighted Frequent patterns were generated successfully using SWFPGrowth algorithm")
        self.__endTime = _fp._time.time()
        self.__memoryUSS = float()
        self.__memoryRSS = float()
        process = _fp._psutil.Process(_fp._os.getpid())
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self) -> float:
        """

        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryUSS

    def getMemoryRSS(self) -> float:
        """

        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self.__memoryRSS

    def getRuntime(self) -> float:
        """

        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__endTime - self.__startTime

    def getPatternsAsDataFrame(self) -> _fp._pd.DataFrame:
        """

        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self.__finalPatterns.items():
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
        for x, y in self.__finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self) -> Dict[str, float]:
        """

        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self.__finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of  Weighted Spatial Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_fp._sys.argv) == 4 or len(_fp._sys.argv) == 5:
        if len(_fp._sys.argv) == 5:
            _ap = SWFPGrowth(_fp._sys.argv[1], _fp._sys.argv[3], _fp._sys.argv[4], _fp._sys.argv[5])
        if len(_fp._sys.argv) == 4:
            _ap = SWFPGrowth(_fp._sys.argv[1], _fp._sys.argv[3], _fp._sys.argv[4])
        _ap.mine()
        _ap.mine()
        print("Total number of Weighted Spatial Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_fp._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS",  _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = SWFPGrowth('sample.txt', 'neighbourSample.txt', 150, ' ')
        _ap.mine()
        print("Total number of Weighted Spatial Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
