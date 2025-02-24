# Top K Spatial High Utility ItemSet Mining (TKSHUIM) aims to discover Top-K Spatial High Utility Itemsets
# (TKSHUIs) in a spatioTemporal database
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilitySpatialPattern.topk import TKSHUIM as alg
#
#             obj=alg.TKSHUIM("input.txt","Neighbours.txt",35)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of  Patterns:", len(Patterns))
#
#             obj.save("output")
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

from PAMI.highUtilitySpatialPattern.topk.abstract import *
from functools import cmp_to_key
import heapq
from deprecated import deprecated

class Transaction:
    """
    A class to store Transaction of a database

    :Attributes:

        items: list
            A list of items in transaction 
        utilities: list
            A list of utilites of items in transaction
        transactionUtility: int
            represent total sum of all utilities in the database
        pmus: list
            represent the pmu (probable maximum utility) of each element in the transaction
        prefixutility:
            prefix Utility values of item
        offset:
            an offset pointer, used by projected transactions

    :Methods:

        projectedTransaction(offsetE):
            A method to create new Transaction from existing till offsetE
        getItems():
            return items in transaction
        getUtilities():
            return utilities in transaction
        getPmus():
            return pmus in transaction
        getLastPosition():
            return last position in a transaction
        removeUnpromisingItems():
            A method to remove items with low Utility than minUtil
        insertionSort():
            A method to sort all items in the transaction
    """
    offset = 0
    prefixUtility = 0
    
    def __init__(self, items, utilities, transactionUtility, pmus=None):
        self.items = items
        self.utilities = utilities
        self.transactionUtility = transactionUtility
        if pmus is not None:
            self.pmus = pmus

    def projectTransaction(self, offsetE):
        """
        A method to create new Transaction from existing till offsetE

        :param offsetE: an offset over the original transaction for projecting the transaction
        :type offsetE: int
        """
        new_transaction = Transaction(self.items, self.utilities, self.transactionUtility)
        utilityE = self.utilities[offsetE]
        new_transaction.prefixUtility = self.prefixUtility + utilityE
        new_transaction.transactionUtility = self.transactionUtility - utilityE
        for i in range(self.offset, offsetE):
            new_transaction.transactionUtility -= self.utilities[i]
        new_transaction.offset = offsetE + 1
        return new_transaction

    def getItems(self):
        """
        A method to return items in transaction
        """
        return self.items

    def getPmus(self):
        """
        A method to return pmus in transaction
        """
        return self.pmus

    def getUtilities(self):
        """
        A method to return utilities in transaction
        """
        return self.utilities

    # get the last position in this transaction
    def getLastPosition(self):
        """
        A method to return last position in a transaction
        """
        return len(self.items) - 1

    def removeUnpromisingItems(self, oldNamesToNewNames):
        """
        A method to remove items with low Utility than minUtil

        :param oldNamesToNewNames: A map represent old namses to new names
        :type oldNamesToNewNames: map
        """
        tempItems = []
        tempUtilities = []
        for idx, item in enumerate(self.items):
            if item in oldNamesToNewNames:
                tempItems.append(oldNamesToNewNames[item])
                tempUtilities.append(self.utilities[idx])
            else:
                self.transactionUtility -= self.utilities[idx]
        self.items = tempItems
        self.utilities = tempUtilities
        self.insertionSort()

    def insertionSort(self):
        """
        A method to sort items in order
        """
        for i in range(1, len(self.items)):
            key = self.items[i]
            utilityJ = self.utilities[i]
            j = i - 1
            while j >= 0 and key < self.items[j]:
                self.items[j + 1] = self.items[j]
                self.utilities[j + 1] = self.utilities[j]
                j -= 1
            self.items[j + 1] = key
            self.utilities[j + 1] = utilityJ


class Dataset:
    """
    A class represent the list of transactions in this dataset

    :Attributes:

    transactions:
        the list of transactions in this dataset
    maxItem:
        the largest item name
        
    :methods:

        createTransaction(line):
            Create a transaction object from a line from the input file
        getMaxItem():
            return Maximum Item
        getTransactions():
            return transactions in database

    """
    transactions = []
    maxItem = 0

    
    def __init__(self, datasetpath, sep):
        self.strToint = {}
        self.intTostr = {}
        self.cnt = 1
        self.sep = sep
        with open(datasetpath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.transactions.append(self.createTransaction(line))
        f.close()

    def createTransaction(self, line):
        """
        A method to create Transaction from dataset given

        :param line: represent a single line of database
        :type line: string
        :return : Transaction.
        :rtype: int
        """
        pmuString = None
        trans_list = line.strip().split(':')
        transactionUtility = int(trans_list[1])
        itemsString = trans_list[0].strip().split(self.sep)
        utilityString = trans_list[2].strip().split(self.sep)
        if len(trans_list) == 4:
            pmuString = trans_list[3].strip().split(self.sep)
        items = []
        utilities = []
        pmus = []
        for idx, item in enumerate(itemsString):
            if self.strToint.get(item) is None:
                self.strToint[item] = self.cnt
                self.intTostr[self.cnt] = item
                self.cnt += 1
            item_int = self.strToint.get(item)
            if item_int > self.maxItem:
                self.maxItem = item_int
            items.append(item_int)
            utilities.append(int(utilityString[idx]))
            if len(trans_list) == 4:
                pmus.append(int(pmuString[idx]))
        return Transaction(items, utilities, transactionUtility, pmus)

    def getMaxItem(self):
        """
        A method to return name of the largest item
        """
        return self.maxItem

    def getTransactions(self):
        """
        A method to return transactions from database
        """
        return self.transactions


class TKSHUIM(utilityPatterns):
    """
    :Description:
       Top K Spatial High Utility ItemSet Mining (TKSHUIM) aims to discover Top-K Spatial High Utility Itemsets
       (TKSHUIs) in a spatioTemporal database

    :Reference:

       P. Pallikila et al., "Discovering Top-k Spatial High Utility Itemsets in Very Large Quantitative Spatiotemporal 
       databases," 2021 IEEE International Conference on Big Data (Big Data), Orlando, FL, USA, 2021, pp. 4925-4935, 
       doi: 10.1109/BigData52589.2021.9671912.

    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility Spatial patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility Spatial patterns
    :param minUtil: int :
                   Minimum utility threshold given by User
    :param maxMemory: int :
                   Maximum memory used by this program for running
    :param candidateCount: int :
                   Number of candidates to consider when calculating a high utility spatial pattern
    :param nFile: str :
                   Name of the input file to mine complete set of High Utility Spatial patterns
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of frequent patterns
        nFile : file
            Name of the Neighbours file that contain neighbours of items
        oFile : file
            Name of the output file to store complete set of frequent patterns
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        k : int
            The user given k value
        candidateCount: int
             Number of candidates 
        utilityBinArrayLU: list
             A map to hold the pmu values of the items in database
        utilityBinArraySU: list
            A map to hold the subtree utility values of the items is database
        oldNamesToNewNames: list
            A map to hold the subtree utility values of the items is database
        newNamesToOldNames: list
            A map to store the old name corresponding to new name
        Neighbours : map
            A dictionary to store the neighbours of a item
        maxMemory: float
            Maximum memory used by this program for running
        itemsToKeep: list
            keep only the promising items ie items having twu >= minUtil
        itemsToExplore: list
            keep items that subtreeUtility grater than minUtil

    :Methods:

        mine()
                Mining process will start from here
        getPatterns()
                Complete set of patterns will be retrieved with this function
        save(oFile)
                Complete set of patterns will be loaded in to a output file
        getPatternsAsDataFrame()
                Complete set of patterns will be loaded in to a dataframe
        getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
               Total amount of runtime taken by the mining process will be retrieved from this function
        calculateNeighbourIntersection(self, prefixLength)
               A method to return common Neighbours of items
        backtrackingEFIM(transactionsOfP, itemsToKeep, itemsToExplore, prefixLength)
               A method to mine the TKSHUIs Recursively
        useUtilityBinArraysToCalculateUpperBounds(transactionsPe, j, itemsToKeep, neighbourhoodList)
               A method to  calculate the sub-tree utility and local utility of all items that can extend itemSet P and e
        output(tempPosition, utility)
               A method ave a high-utility itemSet to file or memory depending on what the user chose
        is_equal(transaction1, transaction2)
               A method to Check if two transaction are identical
        intersection(lst1, lst2)
               A method that return the intersection of 2 list
        useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(dataset)
              Scan the initial database to calculate the subtree utility of each items using a utility-bin array
        sortDatabase(self, transactions)
              A Method to sort transaction in the order of PMU
        sort_transaction(self, trans1, trans2)
              A Method to sort transaction in the order of PMU
        useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset)
             A method to scan the database using utility bin array to calculate the pmus                   

    **Executing the code on terminal:**
    -------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 TKSHUIM.py <inputFile> <outputFile> <Neighbours> <k> <sep>

      Example Usage:

      (.venv) $ python3 TKSHUIM.py sampleTDB.txt output.txt sampleN.txt 35

    .. note:: maxMemory will be considered as Maximum memory used by this program for running


    **Sample run of importing the code:**
    ----------------------------------------
    .. code-block:: python
        
            from PAMI.highUtilitySpatialPattern.topk import TKSHUIM as alg

            obj=alg.TKSHUIM("input.txt","Neighbours.txt",35)

            obj.mine()

            Patterns = obj.getPatterns()

            obj.save("output")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    ---------------
            The complete program was written by Pradeep Pallikila under the supervision of Professor Rage Uday Kiran.
    """
    candidateCount = 0
    utilityBinArrayLU = {}
    utilityBinArraySU = {}
    oldNamesToNewNames = {}
    newNamesToOldNames = {}
    strToint = {}
    intTostr = {}
    Neighbours = {}
    temp = [0] * 5000
    maxMemory = 0
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    nFile = " "
    sep = "\t"
    minUtil = 0
    memoryUSS = float()
    memoryRSS = float()
    heapList = []
    dataset = None

    def __init__(self, iFile, nFile, k, sep="\t"):
        super().__init__(iFile, nFile, k, sep)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Main function of the program.
        """
        self.mine()

    def mine(self):
        """
        Main function of the program.
        """
        self.startTime = time.time()
        self.finalPatterns = {}
        self.dataset = Dataset(self.iFile, self.sep)
        with open(self.nFile, 'r') as o:
            lines = o.readlines()
            for line in lines:
                line = line.split("\n")[0]
                line_split = line.split(self.sep)
                item = self.dataset.strToint.get(line_split[0])
                lst = []
                for i in range(1, len(line_split)):
                    lst.append(self.dataset.strToint.get(line_split[i]))
                self.Neighbours[item] = lst
        o.close()
        InitialMemory = psutil.virtual_memory()[3]
        self.useUtilityBinArrayToCalculateLocalUtilityFirstTime(self.dataset)
        itemsToKeep = []
        for key in self.utilityBinArrayLU.keys():
            if self.utilityBinArrayLU[key] >= self.minUtil:
                itemsToKeep.append(key)
        itemsToKeep = sorted(itemsToKeep, key=lambda x: self.utilityBinArrayLU[x])
        currentName = 1
        for idx, item in enumerate(itemsToKeep):
            self.oldNamesToNewNames[item] = currentName
            self.newNamesToOldNames[currentName] = item
            itemsToKeep[idx] = currentName
            currentName += 1
        for transaction in self.dataset.getTransactions():
            transaction.removeUnpromisingItems(self.oldNamesToNewNames)
        self.sortDatabase(self.dataset.getTransactions())
        emptyTransactionCount = 0
        for transaction in self.dataset.getTransactions():
            if len(transaction.getItems()) == 0:
                emptyTransactionCount += 1
        self.dataset.transactions = self.dataset.transactions[emptyTransactionCount:]
        self.useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self.dataset)
        self.heapList = []
        itemsToExplore = []
        for item in itemsToKeep:
            if self.utilityBinArraySU[item] >= self.minUtil:
                itemsToExplore.append(item)
        commonitems = []
        for i in range(self.dataset.maxItem):
            commonitems.append(i)
        self.backtrackingEFIM(self.dataset.getTransactions(), itemsToKeep, itemsToExplore, 0)
        finalMemory = psutil.virtual_memory()[3]
        memory = (finalMemory - InitialMemory) / 10000
        if memory > self.maxMemory:
            self.maxMemory = memory
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = float()
        self.memoryRSS = float()
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        for item in self.heapList:
            self.finalPatterns[item[1]] = item[0]
        print('TOP-K mining process is completed by TKSHUIM')

    def backtrackingEFIM(self, transactionsOfP, itemsToKeep, itemsToExplore, prefixLength):
        """
        A method to mine the TKSHUIs Recursively

        :param transactionsOfP: the list of transactions containing the current prefix P
        :type transactionsOfP: list
        :param itemsToKeep: the list of secondary items in the p-projected database
        :type itemsToKeep: list
        :param itemsToExplore: the list of primary items in the p-projected database
        :type itemsToExplore: list
        :param prefixLength: current prefixLength
        :type prefixLength: int
        """
        self.candidateCount += len(itemsToExplore)
        for idx, e in enumerate(itemsToExplore):
            initialMemory = psutil.virtual_memory()[3]
            transactionsPe = []
            utilityPe = 0
            if len(transactionsOfP) == 0:
                break 
            previousTransaction = transactionsOfP[0]
            consecutiveMergeCount = 0
            for transaction in transactionsOfP:
                items = transaction.getItems()
                if e in items:
                    positionE = items.index(e)
                    if transaction.getLastPosition() == positionE:
                        utilityPe += transaction.getUtilities()[positionE] + transaction.prefixUtility
                    else:
                        projectedTransaction = transaction.projectTransaction(positionE)
                        utilityPe += projectedTransaction.prefixUtility
                        if previousTransaction == transactionsOfP[0]:
                            previousTransaction = projectedTransaction
                        elif self.is_equal(projectedTransaction, previousTransaction):
                            if consecutiveMergeCount == 0:
                                items = previousTransaction.items[previousTransaction.offset:]
                                utilities = previousTransaction.utilities[previousTransaction.offset:]
                                itemsCount = len(items)
                                positionPrevious = 0
                                positionProjection = projectedTransaction.offset
                                while positionPrevious < itemsCount:
                                    utilities[positionPrevious] += projectedTransaction.utilities[positionProjection]
                                    positionPrevious += 1
                                    positionProjection += 1
                                previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                                sumUtilities = previousTransaction.prefixUtility
                                previousTransaction = Transaction(items, utilities, previousTransaction.transactionUtility + projectedTransaction.transactionUtility)
                                previousTransaction.prefixUtility = sumUtilities
                            else:
                                positionPrevious = 0
                                positionProjected = projectedTransaction.offset
                                itemsCount = len(previousTransaction.items)
                                while positionPrevious < itemsCount:
                                    previousTransaction.utilities[positionPrevious] += projectedTransaction.utilities[
                                        positionProjected]
                                    positionPrevious += 1
                                    positionProjected += 1
                                previousTransaction.transactionUtility += projectedTransaction.transactionUtility
                                previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                            consecutiveMergeCount += 1
                        else:
                            transactionsPe.append(previousTransaction)
                            previousTransaction = projectedTransaction
                            consecutiveMergeCount = 0
                    transaction.offset = positionE
            if previousTransaction != transactionsOfP[0]:
                transactionsPe.append(previousTransaction)
            self.temp[prefixLength] = self.newNamesToOldNames[e]
            if utilityPe >= self.minUtil:
                self.output(prefixLength, utilityPe)
            neighbourhoodList = self.calculateNeighbourIntersection(prefixLength)
            self.useUtilityBinArraysToCalculateUpperBounds(transactionsPe, idx, itemsToKeep, neighbourhoodList)
            newItemsToKeep = []
            newItemsToExplore = []
            for l in range(idx + 1, len(itemsToKeep)):
                itemK = itemsToKeep[l]
                if self.utilityBinArraySU[itemK] >= self.minUtil:
                    if itemK in neighbourhoodList:
                        newItemsToExplore.append(itemK)
                        newItemsToKeep.append(itemK)
                elif self.utilityBinArrayLU[itemK] >= self.minUtil:
                    if itemK in neighbourhoodList:
                        newItemsToKeep.append(itemK)
            self.backtrackingEFIM(transactionsPe, newItemsToKeep, newItemsToExplore, prefixLength + 1)
            finalMemory = psutil.virtual_memory()[3]
            memory = (finalMemory - initialMemory) / 10000
            if self.maxMemory < memory:
                self.maxMemory = memory

    def useUtilityBinArraysToCalculateUpperBounds(self, transactionsPe, j, itemsToKeep, neighbourhoodList):
        """
        A method to  calculate the sub-tree utility and local utility of all items that can extend itemSet P U {e}

        :param transactionsPe: transactions the projected database for P U {e}
        :type transactionsPe: list
        :param j:the position of j in the list of promising items
        :type j:int
        :param itemsToKeep :the list of promising items
        :type itemsToKeep: list
        :param neighbourhoodList: list of neighbourhood elements
        :type neighbourhoodList: list
        """
        for i in range(j + 1, len(itemsToKeep)):
            item = itemsToKeep[i]
            self.utilityBinArrayLU[item] = 0
            self.utilityBinArraySU[item] = 0
        for transaction in transactionsPe:
            length = len(transaction.getItems())
            i = length - 1
            while i >= transaction.offset:
                item = transaction.getItems()[i]
                if item in itemsToKeep:
                    remainingUtility = 0
                    if self.newNamesToOldNames[item] in self.Neighbours:
                        item_neighbours = self.Neighbours[self.newNamesToOldNames[item]]
                        for k in range(i, length):
                            transaction_item = transaction.getItems()[k]
                            if self.newNamesToOldNames[transaction_item] in item_neighbours and transaction_item in neighbourhoodList:
                                remainingUtility += transaction.getUtilities()[k]

                    remainingUtility += transaction.getUtilities()[i]
                    self.utilityBinArraySU[item] += remainingUtility + transaction.prefixUtility
                    self.utilityBinArrayLU[item] += transaction.transactionUtility + transaction.prefixUtility
                i -= 1

    def calculateNeighbourIntersection(self, prefixLength):
        """
        A method to find common Neighbours

        :param prefixLength: the prefix itemSet
        :type prefixLength:int
        """
        intersectionList = self.Neighbours.get(self.temp[0])
        for i in range(1, prefixLength+1):
            intersectionList = self.intersection(self.Neighbours[self.temp[i]], intersectionList)
        finalIntersectionList = []
        if intersectionList is None:
            return finalIntersectionList
        for item in intersectionList:
            if item in self.oldNamesToNewNames:
                finalIntersectionList.append(self.oldNamesToNewNames[item])
        return finalIntersectionList
    
    def output(self, tempPosition, utility):
        """
        A method save all high-utility itemSet to file or memory depending on what the user chose

        :param tempPosition: position of last item
        :type tempPosition : int
        :param utility: total utility of itemSet
        :type utility: int
        """
        s1 = str()
        for i in range(0, tempPosition+1):
            s1 += self.dataset.intTostr.get((self.temp[i]))
            if i != tempPosition:
                s1 += "\t"
        self.additemset(s1, utility)

    def is_equal(self, transaction1, transaction2):
        """
        A method to Check if two transaction are identical

        :param  transaction1: the first transaction.
        :type  transaction1: Transaction
        :param  transaction2:   the second transaction.
        :type  transaction2: Transaction
        :return : whether both are identical or not
        :rtype: bool
        """

        length1 = len(transaction1.items) - transaction1.offset
        length2 = len(transaction2.items) - transaction2.offset
        if length1 != length2:
            return False
        position1 = transaction1.offset
        position2 = transaction2.offset
        while position1 < len(transaction1.items):
            if transaction1.items[position1] != transaction2.items[position2]:
                return False
            position1 += 1
            position2 += 1
        return True
    
    def intersection(self, lst1, lst2):
        """
        A method that return the intersection of 2 list

        :param  lst1: items neighbour to item1
        :type lst1: list
        :param lst2: items neighbour to item2
        :type lst2: list
        :return :intersection of two lists
        :rtype : list
        """
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3

    def useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self, dataset):
        """
        Scan the initial database to calculate the subtree utility of each item using a utility-bin array

        :param dataset: the transaction database
        :type dataset: Dataset
        """
        for transaction in dataset.getTransactions():
            items = transaction.getItems()
            utilities = transaction.getUtilities()
            for idx, item in enumerate(items):
                if item not in self.utilityBinArraySU:
                    self.utilityBinArraySU[item] = 0
                if self.newNamesToOldNames[item] not in self.Neighbours:
                    self.utilityBinArraySU[item] += utilities[idx]
                    continue
                i = idx + 1
                sumSu = utilities[idx]
                while i < len(items):
                    if self.newNamesToOldNames[items[i]] in self.Neighbours[self.newNamesToOldNames[item]]:
                        sumSu += utilities[i]
                    i += 1
                self.utilityBinArraySU[item] += sumSu

    def sortDatabase(self, transactions):
        """
        A Method to sort transaction in the order of PMU

        :param transactions: transaction of items
        :type transactions: Transaction
        :return: sorted transaction
        :rtype: Transaction
        """
        cmp_items = cmp_to_key(self.sort_transaction)
        transactions.sort(key=cmp_items)

    def sort_transaction(self, trans1, trans2):
        """
        A Method to sort transaction in the order of PMU

        :param trans1: the first transaction.
        :type trans1: Transaction
        :param trans2:the second transaction.
        :type trans2: Transaction
        :return: sorted transaction.
        :rtype: int
        """
        trans1_items = trans1.getItems()
        trans2_items = trans2.getItems()
        pos1 = len(trans1_items) - 1
        pos2 = len(trans2_items) - 1
        if len(trans1_items) < len(trans2_items):
            while pos1 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return -1
        elif len(trans1_items) > len(trans2_items):
            while pos2 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return 1
        else:
            while pos2 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return 0

    def useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset):
        """
        A method to scan the database using utility bin array to calculate the pmus

        :param dataset: the transaction database.
        :type dataset: database
        """
        utilityMatrix = defaultdict(lambda: defaultdict(int))
        for transaction in dataset.getTransactions():
            for idx, item in enumerate(transaction.getItems()):
                pmu = transaction.getUtilities()[idx]
                if item in self.Neighbours:
                    neighbors = self.Neighbours[item]
                    for idn, item1 in enumerate(transaction.getItems()):
                        if item1 in neighbors:
                            pmu += transaction.getUtilities()[idn]
                if item in self.utilityBinArrayLU:
                    # self.utilityBinArrayLU[item] += transaction.getPmus()[idx]
                    self.utilityBinArrayLU[item] += pmu
                else:
                    # self.utilityBinArrayLU[item] = transaction.getPmus()[idx]
                    self.utilityBinArrayLU[item] = pmu
                utilityMatrix[item][item] += transaction.getUtilities()[idx]
                if item in self.Neighbours:
                    neighbors = self.Neighbours[item]
                    utility = transaction.getUtilities()[idx]
                    for i, itemj in enumerate(transaction.getItems()):
                        if (itemj != item) and (itemj in neighbors):
                            utilityMatrix[item][itemj] += (utility + transaction.getUtilities()[i])

        for item in utilityMatrix.keys():
            for itemj in utilityMatrix[item].keys():
                if itemj >= item:
                    val = utilityMatrix[item][itemj]
                    if val != 0 and val > self.minUtil:
                        if itemj == item:
                            itemset = str(item)
                        else:
                            itemset = str(item) + str(itemj)
                        self.additemset(itemset, val)

    def additemset(self, itemset, utility):
        """
        adds the itemset to the priority queue

        :param itemset: the itemset to be added

        :type itemset: str

        :param utility: utility matrix for the itemset to be added

        :type utility: numpy.array
        """
        heapq.heappush(self.heapList, (utility, itemset))
        if len(self.heapList) > self.k:
            while len(self.heapList) > self.k:
                heapq.heappop(self.heapList)
                if len(self.heapList) == 0:
                    break
            self.minUtil = heapq.nsmallest(1, self.heapList)[0][0]

    def getPatternsAsDataFrame(self):
        """
        Storing final patterns in a dataframe

        :return: returning patterns in a dataframe
        :rtype: pd.DataFrame
        """
        dataFrame = {}
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Utility'])

        return dataFrame
    
    def getPatterns(self):
        """
        Function to send the set of patterns after completion of the mining process

        :return: returning patterns
        :rtype: dict
        """
        return self.finalPatterns

    def save(self, outFile):
        """
        Complete set of patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self.finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self.memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """
        return self.memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self.endTime-self.startTime

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Top K Spatial  High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())

def main():
    inputFile = 'mushroom_utility_spmf.txt'
    neighborFile = 'mushroom_neighbourhood.txt' #Users can also specify this constraint between 0 to 1.
    k = 1000
    seperator = ' ' 
    obj = TKSHUIM(iFile=inputFile, nFile=neighborFile, k=k,  sep=seperator)    #initialize
    obj.mine()
    obj.mine()
    obj.printResults()
    print(obj.getPatterns())

if __name__ == '__main__':
    main()
    # _ap = str()
    # if len(sys.argv) == 5 or len(sys.argv) == 6:
    #     if len(sys.argv) == 6:
    #         _ap = TKSHUIM(sys.argv[1], sys.argv[3], int(sys.argv[4]), sys.argv[5])
    #     if len(sys.argv) == 5:
    #         _ap = TKSHUIM(sys.argv[1], sys.argv[3], int(sys.argv[4]))
    #     _ap.mine()
    #     _ap.mine()
    #     print("Top K Spatial  High Utility Patterns:", len(_ap.getPatterns()))
    #     _ap.save(sys.argv[2])
    #     print("Total Memory in USS:", _ap.getMemoryUSS())
    #     print("Total Memory in RSS",  _ap.getMemoryRSS())
    #     print("Total ExecutionTime in seconds:", _ap.getRuntime())
    # else:
    #     for i in [1000, 5000]:
    #         _ap = TKSHUIM('/Users/Likhitha/Downloads/mushroom_main_2000.txt',
    #                 '/Users/Likhitha/Downloads/mushroom_neighbors_2000.txt', i, ' ')
    #         _ap.mine()
    #         _ap.mine()
    #         print("Total number of Spatial High Utility Patterns:", len(_ap.getPatterns()))
    #         print("Total Memory in USS:", _ap.getMemoryUSS())
    #         print("Total Memory in RSS", _ap.getMemoryRSS())
    #         print("Total ExecutionTime in seconds:", _ap.getRuntime())
    #     print("Error! The number of input parameters do not match the total number of parameters provided")

