#  ParallelPFPGrowth is one of the fundamental distributed algorithm to discover periodic-frequent patterns in a transactional database. It is based PySpark framework.
#
# *Importing this algorithm into a python program*
# --------------------------------------------------------
#
#
#             from PAMI.periodicFrequentPattern.basic import parallelPFPGrowth as alg
#
#             obj = alg.parallelPFPGrowth(iFile, minSup, maxPer, numWorkers, sep='\t')
#
#             obj.mine()
#
#             periodicFrequentPatterns = obj.getPatterns()
#
#             print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))
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


_copyright_ = """
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

import sys
from collections import defaultdict
from operator import add
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
import time
import psutil
import os
import pandas as pd


class Node:
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

    def _init_(self, item, prefix):
        """
        Initializing the Node class

        :param item: item of a node
        :param count: count of a node
        :param children: children of a node

        """
        self.item = item
        self.count = 0
        self.children = {}
        self.prefix = prefix


class Tree:
    def _init_(self):
        """
        Initializes the Tree class with a root node, a dictionary to keep track of node links, and
        a defaultdict to store item counts.

        :param root: The root node of the FP-Tree, initialized as an empty node.
        :param nodeLink: A dictionary that links nodes of the same item for efficient traversal.
        :param itemCount: A defaultdict to keep count of item frequencies across transactions.
        """
        self.root = Node(None, [])
        self.nodeLink = {}
        self.itemCount = defaultdict(int)

    def addTransaction(self, transaction, count):
        """
        Adds a transaction to the FP-Tree, updating item counts and building the tree structure.

        :param transaction: A list of items in the transaction to be added to the tree.
        :param count: The count associated with this transaction, used to increment node counts.
        :return: None
        """
        current = self.root
        for item in transaction:
            if item not in current.children:
                current.children[item] = Node(item, transaction[0:transaction.index(item)])
                current.children[item].count += count
                self.addNodeToNodeLink(current.children[item])
            else:
                current.children[item].count += count
            self.itemCount[item] += count
            current = current.children[item]

    def addNodeToNodeLink(self, node):
        """
        Adds a node to the nodeLink dictionary, which maintains a list of nodes per item
        for easy lookup of nodes with the same item.

        :param node: The node to be added to the nodeLink structure.
        :return: None
        """
        if node.item not in self.nodeLink:
            self.nodeLink[node.item] = [node]
        else:
            self.nodeLink[node.item].append(node)

    def generateConditionalTree(self, item):
        """
        Generates a conditional FP-Tree for the specified item, which includes only paths
        containing that item and their counts.

        :param item: The item for which to generate a conditional tree.
        :return: A new Tree object representing the conditional FP-Tree.
        """
        tree = Tree()
        for node in self.nodeLink[item]:
            tree.addTransaction(node.prefix, node.count)
        return tree


class Parallel_PPFP:
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

    def __init__(self, inputData, minSup, maxPeriod, numWorkers, sep='\t'):
        self._oFile = None
        self._minSup = minSup
        self._maxPeriod = int(maxPeriod)
        self._numPartitions = int(numWorkers)
        self._startTime = 0.0
        self._endTime = 0.0
        self._finalPatterns = {}
        self._FPList = []
        self._inputData = inputData
        self._sep = sep
        self._memoryUSS = 0.0
        self._memoryRSS = 0.0
        self._lno = 0
        self.sc = None

    def startMine(self):
        """
        Start the mining process

        """
        self._minSup = self._convert(self._minSup)
        self._startTime = time.time()

        # Initialize SparkContext
        conf = SparkConf().setAppName("Parallel_PPFP").setMaster("local[*]")
        sc = SparkContext(conf=conf)

        if isinstance(self._inputData, str):  # Check if input is a file path
            rdd = sc.textFile(self._inputData, self._numPartitions).map(lambda x: x.split(self._sep)).persist()
        else:  # Assume input is already an RDD
            rdd = self._inputData.map(lambda x: x.split(self._sep)).persist()

        self._lno = rdd.count()
        self._minSup = self._convert(self._minSup)
        self._maxPeriod = self._convert(self._maxPeriod)

        # Get frequent items that meet the minimum support
        freqItems = rdd.flatMap(lambda trans: [(item, 1) for item in trans]) \
            .reduceByKey(add) \
            .filter(lambda x: x[1] >= self._minSup) \
            .sortBy(lambda x: x[1], ascending=False) \
            .collect()

        self._finalPatterns = dict(freqItems)
        self._FPList = [x[0] for x in freqItems]
        rank = dict([(item, index) for (index, item) in enumerate(self._FPList)])

        # Generate conditional transactions by partition
        workByPartition = rdd.flatMap(lambda x: self.genCondTransaction(x, rank)).groupByKey()

        # Fold data by key to create individual trees per partition
        trees = workByPartition.foldByKey(Tree(), lambda tree, data: self.buildTree(tree, data))

        # Generate periodic frequent patterns from the generated trees
        freqPatterns = trees.flatMap(lambda tree_tuple: self.genPeriodicFrequentPatterns(tree_tuple))

        result = freqPatterns.map(
            lambda ranks_count: (tuple([self._FPList[z] for z in ranks_count[0]]), ranks_count[1])) \
            .collect()

        # Update final patterns with results from frequent patterns
        self._finalPatterns.update(dict(result))

        # Track execution time and memory usage
        self._endTime = time.time()
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

        # Stop the SparkContext
        sc.stop()

        print("Periodic frequent patterns were generated successfully using Parallel Periodic FPGrowth algorithm")

    def _convert(self, value):
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        elif type(value) is float:
            value = (self._lno * value)
        elif type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._lno * value)
            else:
                value = int(value)
        else:
            print("minSup is not correct")
        return value

    def getPartitionId(self, value):
        """
        Get the frequent items from the database

        :param value: value
        :return: frequent items

        """
        return value % self._numPartitions

    def genCondTransaction(self, trans, rank):
        """
        Get the conditional transactions from the database

        :param trans: Transactions
        :param rank: rank of a database
        """
        newTrans = [rank[item] for item in trans if item in rank.keys()]
        newTrans = sorted(newTrans)
        condTrans = {}
        for i in reversed(newTrans):
            partition = self.getPartitionId(i)
            if partition not in condTrans:
                condTrans[partition] = newTrans[:newTrans.index(i) + 1]
        return [x for x in condTrans.items()]

    @staticmethod
    def buildTree(tree, data):
        """
        Constructs the FP-Tree by adding transactions from the dataset.

        :param tree: The FP-Tree being constructed.
        :param data: A list of transactions, where each transaction is a list of items.
        :return: The constructed FP-Tree with transactions added.
        """
        for trans in data:
            tree.addTransaction(trans, 1)
        return tree

    def genPeriodicFrequentPatterns(self, tree_tuple):
        """
        Generates periodic frequent patterns for a partitioned FP-Tree.

        :param tree_tuple: A tuple containing partition ID and an FP-Tree.
        :return: A generator of periodic frequent patterns and their support counts.
        """
        itemList = sorted(tree_tuple[1].itemCount.items(), key=lambda x: x[1])
        itemList = [x[0] for x in itemList]
        freqPatterns = {}
        for item in itemList:
            if self.getPartitionId(item) == tree_tuple[0]:
                freqPatterns.update(self.genPeriodicPatterns(item, [item], tree_tuple[1]))
        return freqPatterns.items()

    def genPeriodicPatterns(self, item, prefix, tree):
        """
        Recursively generates periodic patterns for an item, based on a given prefix
        and an FP-Tree structure.

        :param item: The current item being analyzed.
        :param prefix: The prefix pattern leading up to this item.
        :param tree: The FP-Tree from which to generate patterns.
        :return: A dictionary of periodic frequent patterns and their support counts.
        """
        condTree = tree.generateConditionalTree(item)
        freqPatterns = {}
        freqItems = {}
        for i in condTree.nodeLink.keys():
            freqItems[i] = 0
            for node in condTree.nodeLink[i]:
                freqItems[i] += node.count

        # Apply periodicity check
        freqItems = {key: value for key, value in freqItems.items() if value >= self._minSup}
        for i in freqItems:
            pattern = prefix + [i]
            freqPatterns[tuple(pattern)] = freqItems[i]
            freqPatterns.update(self.genPeriodicPatterns(i, pattern, condTree))
        return freqPatterns

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
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """
        dataFrame = pd.DataFrame(list(self._finalPatterns.items()), columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        with open(self._oFile, 'w+') as writer:
            for x, y in self._finalPatterns.items():
                if type(x) == tuple:
                    pattern = " ".join(map(str, x))
                    s1 = f"{pattern}:{y}"
                else:
                    s1 = f"{x}:{y}"
                writer.write(f"{s1}\n")

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    if len(sys.argv) == 6:
        inputData = sys.argv[1] if sys.argv[1].lower().endswith('.txt') else sc.textFile(sys.argv[1])
        pp_fp = Parallel_PPFP(inputData, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        pp_fp.mine()
        finalPatterns = pp_fp.getPatterns()
        print("Total number of Periodic Frequent Patterns:", len(finalPatterns))
        pp_fp.save(sys.argv[2])
        memUSS = pp_fp.getMemoryUSS()
        print("Total Memory in USS:", memUSS)
        memRSS = pp_fp.getMemoryRSS()
        print("Total Memory in RSS", memRSS)
        run = pp_fp.getRuntime()
        print("Total ExecutionTime in ms:", run)
    else:
        print("Error! The number of input parameters does not match the total number of parameters provided")