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
import numpy as np
from deprecated import deprecated

_minPS = float()
_period = float()
_lno = int()

class _Node(object):
    """
    A class used to represent the node of frequentPatternTree

    :**Attributes**:    - **item** (*int or None*) -- *Storing item of a node.*
                        - **timeStamps** (*list*) -- *To maintain the timestamps of a database at the end of the branch.*
                        - **parent** (*list*) -- *To maintain the parent of every node.*
                        - **children** (*list*) -- *To maintain the children of a node.*

    :**Methods**:    -**addChild(itemName)** -- *Storing the children to their respective parent nodes.*
    """

    def __init__(self, item, locations, parent=None):
        self.item = item
        self.locations = locations
        self.parent = parent
        self.children = {}

    def addChild(self, item, locations):
        """
        This method takes an item and locations as input, adds a new child node
        if the item does not already exist among the current node's children, or
        updates the locations of the existing child node if the item is already present.

        :param item: Represents the distinct item to be added as a child node.
        :type item: Any
        :param locations: Represents the locations associated with the item.
        :type locations: list
        :return: The child node associated with the item.
        :rtype: _Node
        """
        if item not in self.children:
            self.children[item] = _Node(item, locations, self)
        else:
            self.children[item].locations = locations + self.children[item].locations
            
        return self.children[item]

    def traverse(self):
        """
        This method constructs a transaction by traversing from the current node to the root node, collecting items along the way.

        :return: A tuple containing the transaction and the locations associated with the current node.
        :rtype: tuple(list, Any)
        """
        transaction = []
        locs = self.locations
        node = self.parent
        while node.parent is not None:
            transaction.append(node.item)
            node = node.parent
        return transaction[::-1], locs


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
    _maxTS = None

    def _creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: None
        """
        self._Database = []
        if isinstance(self._iFile, pd.DataFrame):
            data, ts = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'TS' in i:
                ts = self._iFile['TS'].tolist()
            if 'Transactions' in i:
                data = self._iFile['Transactions'].tolist()
            for i in range(len(data)):
                if data[i]:
                    tr = [str(ts[i])] + [x for x in data[i].split(self._sep)]
                    self._Database.append(tr)
                else:
                    self._Database.append([str(ts[i])])

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


    def _convert(self, value: Union[int, float, str]) -> Union[int, float]:
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._maxTS * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._maxTS * value)
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

    def _getPerSup(self, arr):
        arr = list(arr)
        arr = np.sort(arr)
        arr = np.diff(arr)
        locs = len(np.where(arr <= self._period)[0])

        return locs
    

    def _construct(self, items, data):

        """
        This method filters the items based on the minimum support (minSup) and
        maximum period (maxPer). It then constructs a tree structure from the
        filtered items and data.

        :param items: A dictionary where keys are items and values are lists of timestamps.
        :type items: dict
        :param data: The dataset used to construct the tree, where each entry is a list with
                     an index followed by items.
        :type data: list of lists
        :param minSup: The minimum support threshold.
        :type minSup: int
        :param maxPer: The maximum period threshold.
        :type maxPer: int or float
        :param maxTS: The maximum timestamp.
        :type maxTS: int or float
        :param patterns: A dictionary to store the patterns discovered during the construction.
        :type patterns: dict
        :return: A tuple containing the root node of the constructed tree and a dictionary
                 of item nodes.
        :rtype: tuple(_Node, dict)
        """


        items = {k: v for k, v in items.items() if self._getPerSup(v) >= self._minPS}

        #tested ok
        for item, ts in items.items():
            self._finalPatterns[tuple([item])] = self._getPerSup(ts)

        root = _Node([], None, None)
        itemNodes = {}
        for line in data:
            currNode = root
            index = int(line[0])
            line = line[1:]
            line = sorted([item for item in line if item in items], key = lambda x: len(items[x]), reverse = True)
            for item in line:
                currNode = currNode.addChild(item, [index])   # heavy
                if item in itemNodes:
                    itemNodes[item].add(currNode)
                else:
                    itemNodes[item] = set([currNode])

        return root, itemNodes

    
    def _recursive(self, root, itemNode):
        """
        This method recursively constructs a pattern tree from the given root node,
        filtering items based on the minimum support (minSup) and maximum period (maxPer).
        It updates the patterns dictionary with the discovered patterns.

        :param root: The current root node of the pattern tree.
        :type root: _Node
        :param itemNode: A dictionary where keys are items and values are sets of nodes
                         associated with those items.
        :type itemNode: dict
        :param minSup: The minimum support threshold.
        :type minSup: int
        :param maxPer: The maximum period threshold.
        :type maxPer: int or float
        :param patterns: A dictionary to store the patterns discovered during the recursion.
        :type patterns: dict
        :param maxTS: The maximum timestamp.
        :type maxTS: int or float
        """

        for item in itemNode:
            newRoot = _Node(root.item + [item], None, None)

            itemLocs = {}
            transactions = {}
            for node in itemNode[item]:
                transaction, locs = node.traverse()
                if len(transaction) < 1:
                    continue
                # transactions.append((transaction, locs))
                if tuple(transaction) in transactions:
                    transactions[tuple(transaction)].extend(locs)
                else:
                    transactions[tuple(transaction)] = locs

                for item1 in transaction:
                    if item1 in itemLocs:
                        itemLocs[item1] += locs
                    else:
                        itemLocs[item1] = list(locs)

            # Precompute getMaxPer results for itemLocs
            # maxPerResults = {item: self._getMaxPer(itemLocs[item], maxTS) for item in itemLocs if len(itemLocs[item]) >= minSup}
            maxPerResults = {item: self._getPerSup(itemLocs[item]) for item in itemLocs}

            # Filter itemLocs based on minSup and maxPer
            itemLocs = {k: len(v) for k, v in itemLocs.items() if maxPerResults[k] >= self._minPS}

            # Iterate over filtered itemLocs
            for item3 in itemLocs:
                self._finalPatterns[tuple(newRoot.item3 + [item3])] = maxPerResults[item3]
            
            if not itemLocs:
                continue

            newItemNodes = {}

            for transaction, locs in transactions.items():
                transaction = sorted([item for item in transaction if item in itemLocs], key = lambda x: itemLocs[x], reverse = True)
                if len(transaction) < 1:
                    continue
                currNode = newRoot
                for item2 in transaction:
                    currNode = currNode.addChild(item2, locs)
                    if item2 in newItemNodes:
                        newItemNodes[item2].add(currNode)
                    else:
                        newItemNodes[item2] = set([currNode])

            self._recursive(newRoot, newItemNodes)


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
        

        items = {}
        for line in self._Database:
            index = int(line[0])
            self._maxTS = max(self._maxTS, index)
            for item in line[1:]:
                if item not in items:
                    items[item] = []
                items[item].append(index)

        self._minPS = self._convert(self._minPS)
        self._period = self._convert(self._period)

        root, itemNodes = self._construct(items, self._Database)
        self._recursive(root, itemNodes)

        newPattern = {}
        for k, v in self._finalPatterns.items():
            newPattern["\t".join([str(x) for x in k])] = v

        self._finalPatterns = newPattern


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

        # dataFrame = {}
        # data = []
        # for a, b in self._finalPatterns.items():
        #     data.append([a.replace('\t', ' '), b])
        #     dataFrame = _abstract._pd.DataFrame(data, columns=['Patterns', 'periodicSupport'])
        # return dataFrame
        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
        dataFrame = pd.DataFrame(data, columns=['Patterns', 'Periodicity'])
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
            print(_ap.getPatternsAsDataFrame())
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())