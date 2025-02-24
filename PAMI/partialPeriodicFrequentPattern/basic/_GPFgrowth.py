# GPFgrowth is algorithm to mine the partial periodic frequent pattern in temporal database.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#     from PAMI.partialPeriodicFrequentPattern.basic import GPFgrowth as alg
#
#     obj = alg.GPFgrowth(inputFile, outputFile, minSup, maxPer, minPR)
#
#     obj.mine()
#
#     partialPeriodicFrequentPatterns = obj.getPatterns()
#
#     print("Total number of partial periodic Patterns:", len(partialPeriodicFrequentPatterns))
#
#     obj.save(oFile)
#
#     Df = obj.getPatternInDf()
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

class Node:
    """
    A class used to represent the node of frequentPatternTree

    :Attributes:

        item : int
            storing item of a node
        parent : node
            To maintain the parent of every node
        child : list
            To maintain the children of node
        nodeLink : node
            To maintain the next node of node
        tidList : set
            To maintain timestamps of node

    :Methods:

        getChild(itemName)
            storing the children to their respective parent nodes
    """

    def __init__(self):
        self.item = -1
        self.parent = None
        self.child = []
        self.nodeLink = None
        self.tidList = set()

    def getChild(self, item):
        """
        :param item:
        :return: if node have node of item, then return it. if node don't have return []
        """
        for child in self.child:
            if child.item == item:
                return child
        return []


class Tree:
    """
    A class used to represent the frequentPatternGrowth tree structure

    :Attributes:

        root : node
            Represents the root node of the tree
        nodeLinks : dictionary
            storing last node of each item
        firstNodeLink : dictionary
            storing first node of each item

    :Methods:

        addTransaction(transaction,timeStamp)
            creating transaction as a branch in frequentPatternTree
        fixNodeLinks(itemName, newNode)
            add newNode link after last node of item
        deleteNode(itemName)
            delete all node of item
        createPrefixTree(path,timeStampList)
            create prefix tree by path
        createConditionalTree(PFList, minSup, maxPer, minPR, last)
            create conditional tree. Its nodes are satisfy IP / (minSup+1) >= minPR

    """
    def __init__(self):
        self.root = Node()
        self.nodeLinks = {}
        self.firstNodeLink = {}

    def addTransaction(self, transaction, tid):
        """
        add transaction into tree

        :param transaction: it represents the one transactions in database
        :type transaction: list
        :param tid: represents the timestamp of transaction
        :type tid: list
        """
        current = self.root
        for item in transaction:
            child = current.getChild(item)
            if not child:
                newNode = Node()
                newNode.item = item
                newNode.parent = current
                current.child.append(newNode)
                current = newNode
                self.fixNodeLinks(item, newNode)
            else:
                current = child
            current.tidList.add(tid)

    def fixNodeLinks(self, item, newNode):
        """
        fix node link

        :param item: it represents item name of newNode
        :type item: string
        :param newNode: it represents node which is added
        :type newNode: Node
        """
        if item in self.nodeLinks:
            lastNode = self.nodeLinks[item]
            lastNode.nodeLink = newNode
        self.nodeLinks[item] = newNode
        if item not in self.firstNodeLink:
            self.firstNodeLink[item] = newNode

    def deleteNode(self, item):
        """
        delete the node from tree

        :param item: it represents the item name of node
        :type item: str
        """
        deleteNode = self.firstNodeLink[item]
        parentNode = deleteNode.parent
        parentNode.child.remove(deleteNode)
        parentNode.child += deleteNode.child
        parentNode.tidList |= deleteNode.tidList
        for child in deleteNode.child:
            child.parent = parentNode
        while deleteNode.nodeLink:
            deleteNode = deleteNode.nodeLink
            parentNode = deleteNode.parent
            parentNode.child.remove(deleteNode)
            parentNode.child += deleteNode.child
            parentNode.tidList |= deleteNode.tidList
            for child in deleteNode.child:
                child.parent = parentNode

    def createPrefixTree(self, path, tidList):
        """
        create prefix tree by path

        :param path: it represents path to root from prefix node
        :type path: list
        :param tidList: it represents tid of each item
        :type tidList: list
        """
        currentNode = self.root
        for item in path:
            child = currentNode.getChild(item)
            if not child:
                newNode = Node()
                newNode.item = item
                newNode.parent = currentNode
                currentNode.child.append(newNode)
                currentNode = newNode
                self.fixNodeLinks(item, newNode)
            else:
                currentNode = child
            currentNode.tidList |= tidList

    def createConditionalTree(self, PFList, minSup, maxPer, minPR, last):
        """
        create conditional tree by PFlist

        :param PFList: it represents timestamp each item
        :type PFList: dict
        :param minSup: it represents minSup
        :param maxPer: it represents maxPer
        :param minPR: it represents minPR
        :param last: it represents last timestamp in database
        :return: return is PFlist which satisfy ip / (minSup+1) >= minPR
        """
        keys = list(PFList)
        for item in keys:
            ip = calculateIP(maxPer, PFList[item], last).run()
            if ip / (minSup+1) >= minPR:
                continue
            else:
                self.deleteNode(item)
                del PFList[item]
        return PFList

class calculateIP:
    """
    This class calculate ip from timestamp

    :Attributes:

    maxPer : float
        it represents user defined maxPer value
    timeStamp : list
        it represents timestamp of item
    timeStampFinal : int
        it represents last timestamp of database

    :Methods:

    run
        calculate ip from its timestamp list

    """
    def __init__(self, maxPer, timeStamp, timeStampFinal):
        self.maxPer = maxPer
        self.timeStamp = timeStamp
        self.timeStampFinal = timeStampFinal

    def run(self):
        """
        calculate ip from timeStamp list
        :return: it represents ip value
        """
        ip = 0
        self.timeStamp = sorted(list(self.timeStamp))
        if len(self.timeStamp) <= 0:
            return ip
        if self.timeStamp[0] - 0 <= self.maxPer:
            ip += 1
        for i_ in range(len(self.timeStamp) - 1):
            if (self.timeStamp[i_ + 1] - self.timeStamp[i_]) <= self.maxPer:
                ip += 1
        if abs(self.timeStamp[(len(self.timeStamp)-1)] - self.timeStampFinal) <= self.maxPer:
            ip += 1
        return ip


class generatePFListver2:
    """
    generate time stamp list from input file

    :Attributes:

        inputFile : str
            it is input file name
        minSup : float
            user defined minimum support value
        maxPer : float
            user defined max Periodicity value
        minPR : float
            user defined min PR value
        PFList : dict
            storing timestamps each item
    """
    def __init__(self, Database, minSup, maxPer, minPR):
        self.Database = Database
        self.minSup = minSup
        self.maxPer = maxPer
        self.minPR = minPR
        self.PFList = {}
        self.tsList = {}

    def run(self):
        """
        generate PFlist
        :return: timestamps and last timestamp
        """
        global orderOfItem
        #tidList = {}
        last = None
        tid = 1
        for transaction in self.Database:
            timestamp = int(transaction[0])
            for item in transaction[1:]:
                if item not in self.PFList:
                    self.tsList[item] = {}
                    self.tsList[item][tid] = timestamp
                    ip = 0
                    if timestamp <= self.maxPer:
                        ip = 1
                    self.PFList[item] = [1, ip, timestamp]
                else:
                    self.tsList[item][tid] = timestamp
                    if timestamp - self.PFList[item][2] <= self.maxPer:
                        self.PFList[item][1] += 1
                    self.PFList[item][0] += 1
                    self.PFList[item][2] = timestamp
            tid += 1
            last = timestamp
        for item in self.PFList:
            if last - self.PFList[item][2] <= self.maxPer:
                self.PFList[item][1] += 1
            if self.PFList[item][1] / (self.minSup + 1) < self.minPR or self.PFList[item][0] < self.minSup:
                del self.tsList[item]
        #self.PFList = {tuple([k]): v for k, v in sorted(self.PFList.items(), key=lambda x:x[1], reverse=True)}
        tidList = {tuple([k]): v for k, v in sorted(self.tsList.items(), key=lambda x:len(x[1]), reverse=True)}
        orderOfItem = tidList.copy()
        return tidList, last

    def findSeparator(self, line):
        """
        find separator of line in database

        :param line: it represents one line in database
        :type line: list
        :return: return separator
        """
        separator = ['\t', ',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        for i__ in separator:
            if i__ in line:
                return i__
        return None

class generatePFTreever2:
    """
    create tree from tidList and input file

    :Attributes:

        inputFile : str
            it represents input file name
        tidList : dict
            storing tids each item
        root : Node
            it represents the root node of the tree

    :Methods:

        run
            it create tree
        find separator(line)
            find separator in the line of database

    """
    def __init__(self, Database, tidList):
        self.Database = Database
        self.tidList = tidList
        self.root = Tree()

    def run(self):
        """
        create tree from database and tidList
        :return: the root node of tree
        """
        tid = 1
        for transaction in self.Database:
            timestamp = int(transaction[0])
            transaction = [tuple([item]) for item in transaction[1:] if tuple([item]) in self.tidList]
            transaction = sorted(transaction, key=lambda x: len(self.tidList[x]), reverse=True)
            self.root.addTransaction(transaction, timestamp)
            tid += 1
        return self.root

    def findSeparator(self, line):
        """
        find separator of line in database

        :param line: it represents one line in database
        :type line: list
        :return: return separator
        """
        separator = ['\t', ',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        for j in separator:
            if j in line:
                return j
        return None

class PFgrowth:
    """
    This class is pattern growth algorithm

    :Attributes:

        tree : Node
            represents the root node of prefix tree
        prefix : list
            prefix is list of prefix items
        PFList : dict
            storing time stamp each item
        minSup : float
            user defined min Support
        maxPer : float
            user defined max Periodicity
        minPR : float
            user defined min PR
        last : int
            represents last time stamp in database

    :Methods:

        run
            it is pattern growth algorithm

    """
    def __init__(self, tree, prefix, PFList, minSup, maxPer, minPR, last):
        self.tree = tree
        self.prefix = prefix
        self.PFList = PFList
        self.minSup = minSup
        self.maxPer = maxPer
        self.minPR = minPR
        self.last = last

    def run(self):
        """
        run the pattern growth algorithm
        :return: partial periodic frequent pattern in conditional pattern
        """
        global orderOfItem
        result = {}
        items = self.PFList
        if not self.prefix:
            items = reversed(self.PFList)
        for item in items:
            prefix = self.prefix.copy()
            prefix.append(item)
            PFList = {}
            prefixTree = Tree()
            prefixNode = self.tree.firstNodeLink[item]
            tidList = prefixNode.tidList
            path = []
            currentNode = prefixNode.parent
            while currentNode.item != -1:
                path.insert(0, currentNode.item)
                currentNodeItem = currentNode.item
                if currentNodeItem in PFList:
                    PFList[currentNodeItem] |= tidList
                else:
                    PFList[currentNodeItem] = tidList
                currentNode = currentNode.parent
            prefixTree.createPrefixTree(path, tidList)
            while prefixNode.nodeLink:
                prefixNode = prefixNode.nodeLink
                tidList = prefixNode.tidList
                path = []
                currentNode = prefixNode.parent
                while currentNode.item != -1:
                    path.insert(0, currentNode.item)
                    currentNodeItem = currentNode.item
                    if currentNodeItem in PFList:
                        PFList[currentNodeItem] = PFList[currentNodeItem] | tidList
                    else:
                        PFList[currentNodeItem] = tidList
                    currentNode = currentNode.parent
                prefixTree.createPrefixTree(path, tidList)
            ip = calculateIP(self.maxPer, self.PFList[item], self.last).run()
            s = len(self.PFList[item])
            if ip / (s+1) >= self.minPR and s >= self.minSup:
                result[tuple(prefix)] = [s, ip / (s+1)]
            if PFList:
                PFList = {k: v for k, v in sorted(PFList.items(), key=lambda x:len(orderOfItem[x[0]]), reverse=True)}
                PFList = prefixTree.createConditionalTree(PFList, self.minSup, self.maxPer, self.minPR, self.last)
            if PFList:
                #self.PFList = {tuple([k]): v for k, v in sorted(self.PFList.items(), key=lambda x: x[1], reverse=True)}
                obj = PFgrowth(prefixTree, prefix, PFList, self.minSup, self.maxPer, self.minPR, self.last)
                result1 = obj.run()
                result = {**result, **result1}
        return result

class GPFgrowth(partialPeriodicPatterns, ABC):
    """
    :Description:   GPFgrowth is algorithm to mine the partial periodic frequent pattern in temporal database.
    
    :Reference:   R. Uday Kiran, J.N. Venkatesh, Masashi Toyoda, Masaru Kitsuregawa, P. Krishna Reddy, Discovering partial periodic-frequent patterns in a transactional database,
                  Journal of Systems and Software, Volume 125, 2017, Pages 170-182, ISSN 0164-1212, https://doi.org/10.1016/j.jss.2016.11.035.

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: str:
                   The user can specify minSup either in count or proportion of database size.
    :param  minPR: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.
    :param  maxPer: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        inputFile : file
            Name of the input file to mine complete set of frequent pattern
        minSup : float
            The user defined minSup
        maxPer : float
            The user defined maxPer
        minPR : float
            The user defined minPR
        finalPatterns : dict
            it represents to store the pattern
        runTime : float
            storing the total runtime of the mining process
        memoryUSS : float
            storing the total amount of USS memory consumed by the program
        memoryRSS : float
            storing the total amount of RSS memory consumed by the program

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        storePatternsInFile(ouputFile)
            Complete set of frequent patterns will be loaded in to an output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to an output file
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function

    **Executing code on Terminal:**
    ----------------------------------
            Format:
                    >>> python3 GPFgrowth.py <inputFile> <outputFile> <minSup> <maxPer> <minPR>

            Examples:
                    >>> python3 GPFgrowth.py sampleDB.txt patterns.txt 10 10 0.5

    **Sample run of the importing code:**
    --------------------------------------
    ...     code-block:: python

            from PAMI.partialPeriodicFrequentPattern.basic import GPFgrowth as alg

            obj = alg.GPFgrowth(inputFile, outputFile, minSup, maxPer, minPR)

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

    **Credits:**
    --------------
            The complete program was written by Nakamura  under the supervision of Professor Rage Uday Kiran.

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
    __inputFile = None
    __runTime = None
    oFile = None

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

    def __readDatabase(self):
        self.__Database = []
        if isinstance(self.__inputFile, pd.DataFrame):
            if self.__inputFile.empty:
                print("its empty..")
            j_ = self.__inputFile.columns.values.tolist()
            if 'Transactions' in j_:
                self.__Database = self.__inputFile['Transactions'].tolist()
            if 'Patterns' in j_:
                self.__Database = self.__inputFile['Patterns'].tolist()
        if isinstance(self.__inputFile, str):
            if validators.url(self.__inputFile):
                data = urlopen(self.__inputFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [k.rstrip() for k in line.split(self._partialPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self.__inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [k_.rstrip() for k_ in line.split(self._partialPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()
    
    def startMine(self):
        self.mine()

    def mine(self):
        self.__inputFile = self._partialPeriodicPatterns__iFile
        self._partialPeriodicPatterns__startTime = time.time()
        self._partialPeriodicPatterns__finalPatterns = {}
        self.__readDatabase()
        self._partialPeriodicPatterns__minSup = self.__convert(self._partialPeriodicPatterns__minSup)
        self._partialPeriodicPatterns__maxPer = self.__convert(self._partialPeriodicPatterns__maxPer)
        # self.minPR = self.convert(self.minPR)
        self._partialPeriodicPatterns__finalPatterns = {}
        obj = generatePFListver2(self.__Database, self._partialPeriodicPatterns__minSup, self._partialPeriodicPatterns__maxPer, self._partialPeriodicPatterns__minPR)
        tidList, last = obj.run()
        PFTree = generatePFTreever2(self.__Database, tidList).run()
        obj2 = PFgrowth(PFTree, [], tidList, self._partialPeriodicPatterns__minSup, self._partialPeriodicPatterns__maxPer, self._partialPeriodicPatterns__minPR, last)
        self._partialPeriodicPatterns__finalPatterns = obj2.run()
        self._partialPeriodicPatterns__endTime = time.time()
        self.__runTime = self._partialPeriodicPatterns__endTime - self._partialPeriodicPatterns__startTime
        process = psutil.Process(os.getpid())
        self._partialPeriodicPatterns__memoryUSS = float()
        self._partialPeriodicPatterns__memoryRSS = float()
        self._partialPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._partialPeriodicPatterns__memoryRSS = process.memory_info().rss


    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.__runTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe
        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._partialPeriodicPatterns__finalPatterns.items():
            if len(a) == 1:
                pattern = f'{a[0][0]}'
            else:
                pattern = f'{a[0][0]}'
                for item in a[1:]:
                    pattern = pattern + f' {item[0]}'
            #print(pattern)
            data.append([pattern, b[0], b[1]])
            dataframe = pd.DataFrame(data, columns=['Patterns', 'Support', 'PeriodicRatio'])
        return dataframe

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._partialPeriodicPatterns__finalPatterns.items():
            if len(x) == 1:
                writer.write(f'{x[0][0]}:{y[0]}:{y[1]}\n')
            else:
                writer.write(f'{x[0][0]}')
                for item in x[1:]:
                    writer.write(f'\t{item[0]}')
                writer.write(f':{y[0]}:{y[1]}\n')\

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._partialPeriodicPatterns__finalPatterns

    def printResults(self):
        """ this function is used to print the results
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
        for i in [350]:
            _ap = GPFgrowth('/Users/tarunsreepada/Downloads/Temporal_T10I4D100K.csv', i, 300, 0.7, '\t')
            _ap.mine()
            print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
            # _ap.save('/Users/Likhitha/Downloads/output.txt')
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
