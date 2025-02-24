# GPFgrowth is algorithm to mine the partial periodic frequent pattern in temporal database.
#
#
# **Importing this algorithm into a python program**
#
#           from PAMI.partialPeriodicFrequentPattern.basic import GPFgrowth as alg
#
#           iFile = 'sampleTDB.txt'
#
#           minSup = 0.25 # can be specified between 0 and 1
#
#           maxPer = 300 # can  be specified between 0 and 1
#
#           minPR = 0.7 # can  be specified between 0 and 1
#
#           obj = alg.GPFgrowth(inputFile, minSup, maxPer, minPR, sep)
#
#           obj.mine()
#
#           partialPeriodicFrequentPatterns = obj.getPatterns()
#
#           print("Total number of partial periodic Patterns:", len(partialPeriodicFrequentPatterns))
#
#           obj.save(oFile)
#
#           Df = obj.getPatternInDf()
#
#           memUSS = obj.getMemoryUSS()
#
#           print("Total Memory in USS:", memUSS)
#
#           memRSS = obj.getMemoryRSS()
#
#           print("Total Memory in RSS", memRSS)
#
#           run = obj.getRuntime()
#
#           print("Total ExecutionTime in seconds:", run)
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

from abc import ABC

import deprecated
from PAMI.partialPeriodicFrequentPattern.basic.abstract import *

orderOfItem = {}


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


class GPFgrowth(partialPeriodicPatterns, ABC):
    """
    **About this algorithm**

    :**Description**: GPFgrowth is algorithm to mine the partial periodic frequent pattern in temporal database.
    
    :**Reference**: R. Uday Kiran, J.N. Venkatesh, Masashi Toyoda, Masaru Kitsuregawa, P. Krishna Reddy, Discovering partial periodic-frequent patterns in a transactional database,
                  Journal of Systems and Software, Volume 125, 2017, Pages 170-182, ISSN 0164-1212, https://doi.org/10.1016/j.jss.2016.11.035.

    :**parameters**:    - **iFile** (*str*) -- *Name of the Input file to mine complete set of correlated patterns.*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of correlated patterns.*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.*
                        - **minPR** (*str*) -- *Controls the maximum number of transactions in which any two items within a pattern can reappear.*
                        - **maxPer** (*str*) -- *Controls the maximum number of transactions in which any two items within a pattern can reappear.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **minSup** (*int*) -- *The user given minSup.*
                        - **maxPer** (*int*) -- *The user given maxPer.*
                        - **minPR** (*int*) -- *The user given minPR.*
                        - **finalPatterns** (*dict*) -- *It represents to store the pattern.*

    :**Methods**:           - **mine()** -- *Mining process will start from here.*
                        - **getPatterns()** -- *Complete set of patterns will be retrieved with this function.*
                        - **storePatternsInFile(ouputFile)** -- *Complete set of frequent patterns will be loaded in to an output file.*
                        - **getPatternsAsDataFrame()** -- *Complete set of frequent patterns will be loaded in to an output file.*
                        - **getMemoryUSS()** -- *Total amount of USS memory consumed by the mining process will be retrieved from this function.*
                        - **getMemoryRSS()** -- *Total amount of RSS memory consumed by the mining process will be retrieved from this function.*
                        - **getRuntime()** -- *Total amount of runtime taken by the mining process will be retrieved from this function.*

    **Execution methods**

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 GPFgrowth.py <inputFile> <outputFile> <minSup> <maxPer> <minPR>

      Example Usage:

      (.venv) $ python3 GPFgrowth.py sampleTDB.txt output.txt 0.25 300 0.7

    .. note:: minSup can be specified in support count or a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            from PAMI.partialPeriodicFrequentPattern.basic import GPFgrowth as alg

            iFile = 'sampleTDB.txt'

            minSup = 0.25 # can be specified between 0 and 1

            maxPer = 300 # can  be specified between 0 and 1

            minPR = 0.7 # can  be specified between 0 and 1

            obj = alg.GPFgrowth(inputFile, minSup, maxPer, minPR, sep)

            obj.mine()

            partialPeriodicFrequentPatterns = obj.getPatterns()

            print("Total number of partial periodic Patterns:", len(partialPeriodicFrequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDf()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits**

    The complete program was written by Nakamura and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """
    _partialPeriodicPatterns__iFile = ' '
    _partialPeriodicPatterns__oFile = ' '
    _partialPeriodicPatterns__sep = str()
    _partialPeriodicPatterns__startTime = float()
    _partialPeriodicPatterns__endTime = float()
    _partialPeriodicPatterns__minSup = str()
    _partialPeriodicPatterns__maxPer = str()
    _partialPeriodicPatterns__minPR = str()
    _partialPeriodicPatterns__finalPatterns = {}
    runTime = 0
    _partialPeriodicPatterns__memoryUSS = float()
    _partialPeriodicPatterns__memoryRSS = float()
    __Database = []
    _maxTS = None
    __runTime = None
    oFile = None



    def __convert(self, value):
        """
        To convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type
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

    def __creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._partialPeriodicPatterns__iFile, pd.DataFrame):
            timeStamp, data = [], []
            if self._partialPeriodicPatterns__iFile.empty:
                print("its empty..")
            i = self._partialPeriodicPatterns__iFile.columns.values.tolist()
            if 'ts' or 'TS' in i:
                timeStamp = self._partialPeriodicPatterns__iFile['timeStamps'].tolist()
            if 'Transactions' in i:
                data = self._partialPeriodicPatterns__iFile['Transactions'].tolist()
            if 'Patterns' in i:
                data = self._partialPeriodicPatterns__iFile['Patterns'].tolist()
            for i in range(len(data)):
                tr = [timeStamp[i]]
                tr.append(data[i])
                self.__Database.append(tr)

        if isinstance(self._partialPeriodicPatterns__iFile, str):
            if validators.url(self._partialPeriodicPatterns__iFile):
                data = urlopen(self._partialPeriodicPatterns__iFile)
                for line in data:
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._partialPeriodicPatterns__iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def startMine(self):
        self.mine()

    def _ratioCalc(self, v):
        """
        This function take input v as input and returns the ratio.

        :param v: here v is an item.
        :type v: int or float.
        :return: int or float.
        """
        ratio = self._getPerSup(v) / (len(v) + 1)

        return ratio
    
    def _getPerSup(self, arr):
        """
        This function takes the arr as input and returns locs as output

        :param arr: an array contains the items.
        :type arr: array
        :return: locs
        """
        arr = list(arr) + [self._maxTS, 0]
        arr = list(set(arr))
        arr = np.sort(arr)
        arr = np.diff(arr)

        locs = len(np.where(arr <= self._partialPeriodicPatterns__maxPer)[0])

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


        items = {k: v for k, v in items.items() if len(v) >= self._partialPeriodicPatterns__minSup}

        for item, ts in items.items():
            ratio = self._ratioCalc(ts)
            if ratio >= self._partialPeriodicPatterns__minPR:
                self._partialPeriodicPatterns__finalPatterns[tuple([item])] = [len(ts), ratio]

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
        :param itemNode: A dictionary where keys are items and values are sets of nodes associated with those items.
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
            maxPerResults = {item: self._ratioCalc(itemLocs[item]) for item in itemLocs if len(itemLocs[item]) >= self._partialPeriodicPatterns__minSup}

            for item3 in maxPerResults:
                if maxPerResults[item3] >= self._partialPeriodicPatterns__minPR:
                    self._partialPeriodicPatterns__finalPatterns[tuple(newRoot.item3 + [item3])] = [len(itemLocs[item3]), maxPerResults[item3]]

            # Filter itemLocs based on minSup and maxPer
            itemLocs = {k: len(v) for k, v in itemLocs.items() if len(v) >= self._partialPeriodicPatterns__minSup}

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

    def mine(self):
        self._partialPeriodicPatterns__startTime = time.time()
        self._partialPeriodicPatterns__finalPatterns = {}
        self.__creatingItemSets()
        
        self._partialPeriodicPatterns__minPR = float(self._partialPeriodicPatterns__minPR)
        
        self._maxTS = 0
        items = {}
        for line in self.__Database:
            index = int(line[0])
            self._maxTS = max(self._maxTS, index)
            for item in line[1:]:
                if item not in items:
                    items[item] = []
                items[item].append(index)

        self._partialPeriodicPatterns__minSup = self.__convert(self._partialPeriodicPatterns__minSup)
        self._partialPeriodicPatterns__maxPer = self.__convert(self._partialPeriodicPatterns__maxPer)

        # def _construct(self, items, data, patterns):
        root, itemNodes = self._construct(items, self.__Database)
        self._recursive(root, itemNodes)
        
        temp = {}
        for k,v in self._partialPeriodicPatterns__finalPatterns.items():
            k = list(k)
            k = "\t".join(k)
            temp[k] = v
        self._partialPeriodicPatterns__finalPatterns = temp


        self._partialPeriodicPatterns__endTime = time.time()
        self.__runTime = self._partialPeriodicPatterns__endTime - self._partialPeriodicPatterns__startTime
        process = psutil.Process(os.getpid())
        self._partialPeriodicPatterns__memoryUSS = float()
        self._partialPeriodicPatterns__memoryRSS = float()
        self._partialPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._partialPeriodicPatterns__memoryRSS = process.memory_info().rss


    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__runTime

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        # writer = open(self.oFile, 'w+')
        # for x, y in self._partialPeriodicPatterns__finalPatterns.items():
        #     if len(x) == 1:
        #         writer.write(f'{x[0][0]}:{y[0]}:{y[1]}\n')
        #     else:
        #         writer.write(f'{x[0][0]}')
        #         for item in x[1:]:
        #             writer.write(f'\t{item[0]}')
        #         writer.write(f':{y[0]}:{y[1]}\n')\

        with open(self.oFile, 'w') as f:
            for x, y in self._partialPeriodicPatterns__finalPatterns.items():
                # print(list(x), y)
                f.write(x + ":" + str(y[0]) + ":" + str(y[1]) + "\n")

    def getPatternsAsDataFrame(self):
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._partialPeriodicPatterns__finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodic Ratio'])
        return dataFrame
    
    def getPatterns(self):
        """
        This function returns the final partial Periodic Patterns.

        :return: dictionary
        """
        return self._partialPeriodicPatterns__finalPatterns


    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Partial Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())

if __name__ == '__main__':
    ap = str()
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        if len(sys.argv) == 7:
            ap = GPFgrowth(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        if len(sys.argv) == 6:
            ap = GPFgrowth(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
        ap.mine()
        print("Total number of Frequent Patterns:", len(ap.getPatterns()))
        ap.save(sys.argv[2])
        print("Total Memory in USS:", ap.getMemoryUSS())
        print("Total Memory in RSS", ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", ap.getRuntime())
    else:

        print("Error! The number of input parameters do not match the total number of parameters provided")