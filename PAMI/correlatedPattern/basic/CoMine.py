# CoMine is one of the fundamental algorithm to discover correlated patterns in a transactional database.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.correlatedPattern.basic import CoMine as alg
#
#             iFile = 'sampleTDB.txt'
#
#             minSup = 0.25 # can be specified between 0 and 1
#
#             minAllConf = 0.2 # can  be specified between 0 and 1
#
#             obj = alg.CoMine(iFile, minSup, minAllConf, sep)
#
#             obj.mine()
#
#             Rules = obj.getPatterns()
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
     Copyright (C)  2021 Rage Uday Kiran

"""

from PAMI.correlatedPattern.basic import abstract as _ab
import pandas as _pd
from typing import List, Dict, Tuple, Union
from deprecated import deprecated
from collections import Counter


class _Node:
    """
    A class used to represent the node of frequentPatternTree

    :**Attributes**:    - **itemId** (*int*) -- *storing item of a node.*
                        - **counter** (*int*) -- *To maintain the support of node.*
                        - **parent** (*node*) -- *To maintain the parent of node.*
                        - **children** (*list*) -- *To maintain the children of node.*

    :**Methods**:   - **addChild(node)** -- *Updates the nodes children list and parent for the given node.*
    """

    def __init__(self, item, count, parent) -> None:
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}

    def addChild(self, item, count = 1):
        """

        Adds a child node to the current node with the specified item and count.

        :param item: The item associated with the child node.
        :type item: List
        :param count: The count or support of the item. Default is 1.
        :type count: int
        :return: The child node added.
        :rtype: List
        """
        if item not in self.children:
            self.children[item] = _Node(item, count, self)
        else:
            self.children[item].count += count
        return self.children[item]
    
    def traverse(self) -> Tuple[List[int], int]:
        """
        Traversing the tree to get the transaction

        :return: transaction and count of each item in transaction
        :rtype: Tuple, List and int
        """
        transaction = []
        count = self.count
        node = self.parent
        while node.parent is not None:
            transaction.append(node.item)
            node = node.parent
        return transaction[::-1], count

class CoMine(_ab._correlatedPatterns):
    """
    **About this algorithm**

    :**Description**: CoMine is one of the fundamental algorithm to discover correlated  patterns in a transactional database. It is based on the traditional FP-Growth algorithm. This algorithm uses depth-first search technique to find all correlated patterns in a transactional database.

    :**Reference**: Lee, Y.K., Kim, W.Y., Cao, D., Han, J. (2003). CoMine: efficient mining of correlated patterns. In ICDM (pp. 581–584).

    :**parameters**:    - **iFile** (*str*) -- *Name of the Input file to mine complete set of correlated patterns*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of correlated patterns*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.*
                        - **minAllConf** (*float*) -- *The user can specify minAllConf values within the range (0, 1).*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **minSup** (*int*) -- *The user given minSup.*
                        - **minAllConf** (*float*) -- *The user given minimum all confidence Ratio(should be in range of 0 to 1).*
                        - **Database** (*list*) -- *To store the transactions of a database in list.*
                        - **mapSupport** (*Dictionary*) -- *To maintain the information of item and their frequency.*
                        - **lno** (*int*) -- *it represents the total no of transactions.*
                        - **tree** (*class*) -- *it represents the Tree class.*
                        - **itemSetCount** (*int*) -- *it represents the total no of patterns.*
                        - **finalPatterns** (*dict*) -- *it represents to store the patterns.*
                        - **itemSetBuffer** (*list*) -- *it represents the store the items in mining.*
                        - **maxPatternLength** (*int*) -- *it represents the constraint for pattern length.*

    **Execution methods**

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 CoMine.py <inputFile> <outputFile> <minSup> <minAllConf> <sep>

      Example Usage:

      (.venv) $ python3 CoMine.py sampleTDB.txt output.txt 0.25 0.2

    .. note:: minSup can be specified in support count or a value between 0 and 1.

    **Calling from a python program**

    .. code-block:: python

            from PAMI.correlatedPattern.basic import CoMine as alg

            iFile = 'sampleTDB.txt'

            minSup = 0.25 # can be specified between 0 and 1

            minAllConf = 0.2 # can  be specified between 0 and 1

            obj = alg.CoMine(iFile, minSup, minAllConf,sep)

            obj.mine()

            patterns = obj.getPatterns()

            print("Total number of  Patterns:", len(patterns))

            obj.savePatterns(oFile)

            df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits**

    The complete program was written by B.Sai Chitra and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _minSup = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _minAllConf = 0.0
    _Database = []
    _mapSupport = {}
    _lno = 0
    _tree = str()
    _itemSetBuffer = None
    _fpNodeTempBuffer = []
    _itemSetCount = 0
    _maxPatternLength = 1000
    _sep = "\t"
    _counter = 0

    def __init__(self, iFile: Union[str, _pd.DataFrame], minSup: Union[int, float, str], minAllConf: float, sep: str="\t") ->None:
        """
        param iFile: give the input file
        type iFile: str or DataFrame or url
        param minSup: minimum support
        type minSup:   int or float
        param sep: Delimiter of input file
        type sep: str
        """

        super().__init__(iFile, minSup, minAllConf, sep)

    def _creatingItemSets(self) -> None:
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
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    
    def _convert(self, value: Union[int, float, str]):
        """
        To convert the type of user specified minSup value

        :param value: user specified minSup value
        :type value: int or float or str
        :return: None
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

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        main method to start
        """
        self.mine()

    def _maxSup(self, itemSet, item):
        """
        Calculate the maximum support value for a given itemSet and item.

        :param itemSet: A set of items to compare.
        :type itemSet: list or set
        :param item: An individual item to compare.
        :type item: Any
        :return: The maximum support value from the itemSet and the individual item.
        :rtype: float or int
        """
        sups = [self._mapSupport[i] for i in itemSet] + [self._mapSupport[item]]
        return max(sups)

    def _allConf(self, itemSet):
        """
        Calculate the all-confidence value for a given itemSet.

        :param itemSet: A set of items for which to calculate the all-confidence.
        :type itemSet: list or set
        :return: The all-confidence value for the itemSet.
        :rtype: float
        """
        return self._finalPatterns[itemSet] / max([self._mapSupport[i] for i in itemSet])
    
    def recursive(self, item, nodes, root):
        """
        Recursively build the tree structure for itemsets and find patterns that meet
        the minimum support and all-confidence thresholds.

        :param item: The current item being processed.
        :type item: Any
        :param nodes: The list of nodes to be processed.
        :type nodes: list of _Node
        :param root: The root node of the current tree.
        :type root: _Node
        :return: None
        """

        if root.item is None:
            newRoot = _Node([item], 0, None)
        else:
            newRoot = _Node(root.item + [item], 0, None)

        itemCounts = {}
        transactions = []
        for node in nodes:
            transaction, count = node.traverse()
            transactions.append([transaction, count])
            for item in transaction:
                if item not in itemCounts:
                    itemCounts[item] = 0
                itemCounts[item] += count

        # print(newRoot.item, itemCounts.keys())
        itemCounts = {k:v for k, v in itemCounts.items() if v >= self._minSup}
        if len(itemCounts) == 0:
            return

        itemNodes = {}
        for transaction, count in transactions:
            transaction = [i for i in transaction if i in itemCounts]
            transaction = sorted(transaction, key=lambda _item: itemCounts[_item], reverse=True)
            node = newRoot
            for item in transaction:
                node = node.addChild(item, count)
                if item not in itemNodes:
                    itemNodes[item] = [set(), 0]
                itemNodes[item][0].add(node)
                itemNodes[item][1] += count

        itemNodes = {k:v for k, v in sorted(itemNodes.items(), key=lambda x: x[1][1], reverse=True)}


        for item in itemCounts:
            conf = itemNodes[item][1] / self._maxSup(newRoot.item, item)
            if conf >= self._minAllConf:
                self._finalPatterns[tuple(newRoot.item + [item])] = [itemCounts[item], conf]
                self.recursive(item, itemNodes[item][0], newRoot)

    def mine(self) -> None:
        """
        main method to start
        """
        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)

        itemCount = Counter()
        for transaction in self._Database:
            itemCount.update(transaction)

        self._mapSupport = {k: v for k, v in itemCount.items() if v >= self._minSup}
        self._Database = [[item for item in transaction if item in self._mapSupport] for transaction in self._Database]
        self._Database = [sorted(transaction, key=lambda item: self._mapSupport[item], reverse=True) for transaction in self._Database]
        
        root = _Node(None, 0, None)
        itemNode = {}
        # itemNode[item] = [node, count]
        for transaction in self._Database:
            node = root
            for item in transaction:
                node = node.addChild(item)
                if item not in itemNode:
                    itemNode[item] = [set(), 0]
                itemNode[item][0].add(node)
                itemNode[item][1] += 1

        itemNode = {k:v for k, v in sorted(itemNode.items(), key=lambda x: x[1][1], reverse=True)}

        for item in itemNode:
            self._finalPatterns[tuple([item])] = [itemNode[item][1],1]
            self.recursive(item, itemNode[item][0], root)

        print("Correlated patterns were generated successfully using CoMine algorithm")
        self._endTime = _ab._time.time()
        self._memoryUSS = float()
        self._memoryRSS = float()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

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

    def getPatternsAsDataFrame(self) -> _pd.DataFrame:
        """
        Storing final correlated patterns in a dataframe

        :return: returning correlated patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            pat = " "
            for i in a:
                pat += str(i) + " "
            data.append([pat, b[0], b[1]])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Confidence'])
        return dataframe

    def save(self, outFile) -> None:
        """
        Complete set of correlated patterns will be saved into an output file

        :param outFile: name of the outputfile
        :type outFile: file
        :return: None
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            pat = ""
            for i in x:
                pat += str(i) + "\t"
            patternsAndSupport = pat.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % patternsAndSupport)

    def getPatterns(self) -> Dict[Tuple[int], List[Union[int, float]]]:
        """
        Function to send the set of correlated patterns after completion of the mining process

        :return: returning correlated patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self) -> None:
        """
        function to print the result after completing the process

        :return: None
        """
        print("Total number of Correlated Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())

if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = CoMine(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = CoMine(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]))
        _ap.mine()
        _ap.mine()
        print("Total number of Correlated-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
