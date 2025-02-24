# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.stablePeriodicFrequentPattern.basic import SPPGrowthDump as alg
#
#             obj = alg.SPPGrowthDump(iFile, minSup, maxPer, maxLa)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of Stable Periodic Frequent Patterns:", len(Patterns))
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

from PAMI.stablePeriodicFrequentPattern.basic import abstract as _ab
#import pandas as pd
from deprecated import deprecated

from urllib.request import urlopen
import validators
import pandas as pd
import resource
import time
import sys
import os
import psutil

_minSup = int()
_maxPer = int()
_maxLa = int()
_last = int()


class _Node:

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

class _Tree:
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
        global _maxPer, _last
        previous = 0
        la = 0
        tsList = sorted(timeStamps)
        for ts in tsList:
            la = max(0, la + ts - previous - _maxPer)
            previous = ts
        la = max(0, la + _last - previous - _maxPer)
        return len(timeStamps), la

    def conditionalDatabases(self, conditionalPatterns, conditionalTimeStamps):
        """
        It generates the conditional patterns with periodic-frequent items

        :param conditionalPatterns: conditionalPatterns generated from conditionPattern method of a respective node
        :type conditionalPatterns: list
        :param conditionalTimeStamps: Represents the timestamps of a conditional patterns of a node
        :type conditionalTimeStamps: list
        :returns: Returns conditional transactions by removing non-periodic and non-frequent items
        """

        global _maxPer, _minSup, _maxLa
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
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v[0] >= _minSup and v[1] <= _maxLa}
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

class SPPGrowth:
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _maxLa = float()
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
    SPPList = {}

    def __init__(self, inputFile, minSup, maxPer, maxLa, sep='\t'):
        self._iFile = inputFile
        self._minSup = minSup
        self._maxPer = maxPer
        self._maxLa = maxLa
        self._sep = sep

    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
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
                tr = [ts[i][0]]
                tr = tr + data[i]
                self._Database.append(tr)

        if isinstance(self._iFile, str):
            if validators.url(self._iFile):
                data = urlopen(self._iFile)
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
        Calculates the support of each item in the database and assign ranks to the items by decreasing support and returns the frequent items list

        :returns: return the one-length periodic frequent patterns
        """
        global _last
        tidLast = {}
        la = {}
        for transaction in self._Database:
            ts = int(transaction[0])
            for item in transaction[1:]:
                if item not in self.SPPList:
                    la[item] = max(0, ts - self._maxPer)
                    self.SPPList[item] = [1, la[item]]
                else:
                    s = self.SPPList[item][0] + 1
                    la[item] = max(0, la[item] + ts - tidLast.get(item) - self._maxPer)
                    self.SPPList[item] = [s, max(la[item], self.SPPList[item][1])]
                tidLast[item] = ts
            _last = ts
        for item in self.SPPList:
            la[item] = max(0, la[item] + _last - tidLast[item] - self._maxPer)
            self.SPPList[item][1] = max(la[item], self.SPPList[item][1])
        self.SPPList = {k: v for k, v in self.SPPList.items() if v[0] >= self._minSup and v[1] <= self._maxLa}
        self.SPPList = {k: v for k, v in sorted(self.SPPList.items(), key=lambda x: x[1][0], reverse=True)}
        data = self.SPPList
        pfList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self._rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        #print(len(pfList))
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
        It takes the database and support of each item and construct the main tree by setting root node as a null

        :param data: it represents the one Database in database
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

    def _savePeriodic(self, itemSet):
        """
        To convert the ranks of items in to their original item names

        :param itemSet: frequent pattern.
        :return: frequent pattern with original item names
        """
        t1 = str()
        for i in itemSet:
            t1 = t1 + self._rankedUp[i] + " "
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

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Mining process will start from this function
        """

        self.mine()

    def mine(self):
        """
        Mining process will start from this function
        """

        global _minSup, _maxPer, _maxLa # _lno,
        self._startTime = time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._maxPer = self._convert(self._maxPer)
        self._maxLa = self._convert(self._maxLa)
        _minSup, _maxPer, _maxLa, _lno = self._minSup, self._maxPer, self._maxLa, len(self._Database)
        print(_minSup, _maxPer, _maxLa)
        if self._minSup > len(self._Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
        generatedItems, pfList = self._periodicFrequentOneItem()
        updatedDatabases = self._updateDatabases(generatedItems)
        for x, y in self._rank.items():
            self._rankedUp[y] = x
        info = {self._rank[k]: v for k, v in generatedItems.items()}
        Tree = self._buildTree(updatedDatabases, info)
        patterns = Tree.generatePatterns([])
        self._finalPatterns = {}
        for i in patterns:
            sample = self._savePeriodic(i[0])
            self._finalPatterns[sample] = i[1]
        self._endTime = time.time()
        process = psutil.Process(os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Stable Periodic Frequent patterns were generated successfully using topk algorithm ")


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
            data.append([a, b[0], b[1]])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of periodic-frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns


if __name__ == "__main__":
    _ap = str()
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        if len(sys.argv) == 7:
            _ap = SPPGrowth(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5],sys.argv[6])
        if len(sys.argv) == 6:
            _ap = SPPGrowth(sys.argv[1], sys.argv[3], sys.argv[4],sys.argv[5])
        _ap.mine()
        _ap.mine()
        _Patterns = _ap.getPatterns()
        print("Total number of Patterns:", len(_Patterns))
        _ap.save(sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        '''ap = topk('https://www.u-aizu.ac.jp/~udayrage/datasets/temporalDatabases/temporal_retail.csv', 0.001, 0.005, 0.004)
        #ap = topk('/Users/likhitha/Downloads/contextPrefixSpan.txt', 3, 6, 2, ' ')
        ap.mine()
        Patterns = ap.getPatterns()
        print("Total number of Frequent Patterns:", len(Patterns))
        ap.save('/Users/Likhitha/Downloads/output')
        memUSS = ap.getMemoryUSS()
        print("Total Memory in USS:", memUSS)
        memRSS = ap.getMemoryRSS()
        print("Total Memory in RSS", memRSS)
        run = ap.getRuntime()
        print("Total ExecutionTime in ms:", run)'''
        print("Error! The number of input parameters do not match the total number of parameters provided")

