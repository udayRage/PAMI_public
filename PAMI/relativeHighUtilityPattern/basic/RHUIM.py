# RHUIM algorithm helps us to mine Relative High Utility itemSets from transactional databases.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.relativeHighUtilityPattern.basic import RHUIM as alg
#
#             obj = alg.RHUIM("input.txt", 35, 20)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
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

import pandas as pd
from deprecated import deprecated
from PAMI.relativeHighUtilityPattern.basic import abstract as _ab


class _Transaction:
    """
    A class to store Transaction of a database

    :Attributes:

        items: list
            A list of items in transaction 
        utilities: list
            A list of utilities of items in transaction
        transactionUtility: int
            represent total sum of all utilities in the database
        prefixUtility:
            prefix Utility values of item
        offset:
            an offset pointer, used by projected transaction

    :Methods:

        projectedTransaction(offsetE):
            A method to create new Transaction from existing starting from offsetE until the end
        getItems():
            return items in transaction
        getUtilities():
            return utilities in transaction
        getLastPosition():
            return last position in a transaction
        removeUnpromisingItems():
            A method to remove items which are having low values when compared with minUtil
        insertionSort():
            A method to sort all items in the transaction
    """
    offset = 0
    prefixUtility = 0

    def __init__(self, items: list, utilities: list, transactionUtility: int) -> None:
        self.items = items
        self.utilities = utilities
        self.transactionUtility = transactionUtility

    def projectTransaction(self, offsetE: int) -> '_Transaction':
        """
        A method to create new Transaction from existing transaction starting from offsetE until the end

        :param offsetE: an offset over the original transaction for projecting the transaction
        :type offsetE: int
        """
        new_transaction = _Transaction(self.items, self.utilities, self.transactionUtility)
        utilityE = self.utilities[offsetE]
        new_transaction.prefixUtility = self.prefixUtility + utilityE
        new_transaction.transactionUtility = self.transactionUtility - utilityE
        for i in range(self.offset, offsetE):
            new_transaction.transactionUtility -= self.utilities[i]
        new_transaction.offset = offsetE + 1
        return new_transaction

    def getItems(self) -> list:
        """
        A method to return items in transaction
        :return: list
        """
        return self.items

    def getUtilities(self) -> list:
        """
        A method to return utilities in transaction
        :return: list
        """
        return self.utilities

    def getLastPosition(self) -> int:
        """
        A method to return last position in a transaction
        :return: int
        """

        return len(self.items) - 1

    def removeUnpromisingItems(self, oldNamesToNewNames: dict) -> None:
        """
        A method to remove items which are not present in the map passed to the function

        :param oldNamesToNewNames: A map represent old names to new names
        :type oldNamesToNewNames: map
        :return: None
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

    def insertionSort(self) -> None:
        """
        A method to sort items in order
        :return: None
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


class _Dataset:
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

    def __init__(self, datasetPath: str, sep: str) -> None:
        self.strToInt = {}
        self.intToStr = {}
        self.cnt = 1
        self.sep = sep
        self.createItemSets(datasetPath)

    def createItemSets(self, datasetPath: str) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :return: None
        """
        self.transactions = []
        itemsets, utilities, utilityValues = [], [], []
        if isinstance(datasetPath, _ab._pd.DataFrame):
            utilities, data, utilityValues = [], [], []
            if datasetPath.empty:
                print("its empty..")
            i = datasetPath.columns.values.tolist()
            if 'Transactions' in i:
                itemsets = datasetPath['Transactions'].tolist()
            if 'Utilities' in i:
                utilities = datasetPath['Patterns'].tolist()
            if 'UtilitySum' in i:
                utilityValues = datasetPath['utilitySum'].tolist()
            for k in range(len(itemsets)):
                self.transactions.append(self.createTransaction(itemsets[k], utilities[k], utilityValues[k]))
        if isinstance(datasetPath, str):
            if _ab._validators.url(datasetPath):
                data = _ab._urlopen(datasetPath)
                for line in data:
                    line = line.decode("utf-8")
                    trans_list = line.strip().split(':')
                    transactionUtility = int(trans_list[1])
                    itemsString = trans_list[0].strip().split(self.sep)
                    itemsString = [x for x in itemsString if x]
                    utilityString = trans_list[2].strip().split(self.sep)
                    utilityString = [x for x in utilityString if x]
                    self.transactions.append(self.createTransaction(itemsString, utilityString, transactionUtility))
            else:
                try:
                    with open(datasetPath, 'r', encoding='utf-8') as f:
                        for line in f:
                            trans_list = line.strip().split(':')
                            transactionUtility = int(trans_list[1])
                            itemsString = trans_list[0].strip().split(self.sep)
                            itemsString = [x for x in itemsString if x]
                            utilityString = trans_list[2].strip().split(self.sep)
                            utilityString = [x for x in utilityString if x]
                            self.transactions.append(
                                self.createTransaction(itemsString, utilityString, transactionUtility))
                except IOError:
                    print("File Not Found")
                    quit()

    def createTransaction(self, itemSet: list, utilities: list, utilitySum: int) -> _Transaction:
        """
        A method to create Transaction from dataset given
            
        :Attributes:

        :param itemSet: represent a transactions itemset in database
        :type itemSet: list
        :param utilities: utility values of respective transaction itemSets
        :type utilities: list
        :param utilitySum: represent the sum of utility Sum
        :type utilitySum: int
        :return : Transaction.
        :rtype: Transaction
        """
        transactionUtility = utilitySum
        itemsString = itemSet
        utilityString = utilities
        items = []
        utilities = []
        for idx, item in enumerate(itemsString):
            if self.strToInt.get(item) is None:
                self.strToInt[item] = self.cnt
                self.intToStr[self.cnt] = item
                self.cnt += 1
            item_int = self.strToInt.get(item)
            if item_int > self.maxItem:
                self.maxItem = item_int
            items.append(item_int)
            utilities.append(int(utilityString[idx]))
        return _Transaction(items, utilities, transactionUtility)

    def getMaxItem(self) -> int:
        """
        A method to return name of the largest item
        :return; int
        """
        return self.maxItem

    def getTransactions(self) -> list:
        """
        A method to return transactions from database
        :return: list
        """
        return self.transactions


class RHUIM(_ab._utilityPatterns):
    """
    :Description:   RHUIM algorithm helps us to mine Relative High Utility itemSets from transactional databases.
    
    :Reference:   R. U. Kiran, P. Pallikila, J. M. Luna, P. Fournier-Viger, M. Toyoda and P. K. Reddy,
                 "Discovering Relative High Utility Itemsets in Very Large Transactional Databases Using Null-Invariant Measure,"
                  2021 IEEE International Conference on Big Data (Big Data), Orlando, FL, USA, 2021, pp. 252-262,
                  doi: 10.1109/BigData52589.2021.9672064.

    :param  iFile: str :
                   Name of the Input file to mine complete set of Relative High Utility patterns
    :param  oFile: str :
                   Name of the output file to store complete set of Relative High Utility patterns
    :param  minSup: float or int or str :
                    minSup measure constraints the minimum number of transactions in a database where a pattern must appear
                    Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    :param  minUtil: int :
                   The minimum utility threshold.

    :Attributes:

        iFile : file
            Name of the input file to mine complete set of patterns
        oFile : file
            Name of the output file to store complete set of patterns
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime : float
            To record the start time of the mining process
        endTime : float
            To record the completion time of the mining process
        minUtil : int
            The user given minUtil value
        minUR : float
            The user given minUR value
        relativeHighUtilityItemSets : map
            set of relative high utility itemSets
        candidateCount : int
             Number of candidates 
        utilityBinArrayLU : list
             A map to hold the local utility values of the items in database
        utilityBinArraySU : list
            A map to hold the subtree utility values of the items is database
        oldNamesToNewNames : list
            A map which contains old names, new names of items as key value pairs
        newNamesToOldNames : list
            A map which contains new names, old names of items as key value pairs
        maxMemory : float
            Maximum memory used by this program for running
        patternCount : int
            Number of RHUI's
        itemsToKeep : list
            keep only the promising items i.e items that can extend other items to form RHUIs
        itemsToExplore : list
            list of items that needs to be explored

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
        backTrackingRHUIM(transactionsOfP, itemsToKeep, itemsToExplore, prefixLength)
               A method to mine the RHUIs Recursively
        useUtilityBinArraysToCalculateUpperBounds(transactionsPe, j, itemsToKeep)
               A method to calculate the sub-tree utility and local utility of all items that can extend itemSet P and e
        output(tempPosition, utility)
               A method to output a relative-high-utility itemSet to file or memory depending on what the user chose
        is_equal(transaction1, transaction2)
               A method to Check if two transaction are identical
        useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(dataset)
              A method to calculate the sub tree utility values for single items
        sortDatabase(self, transactions)
              A Method to sort transaction
        sort_transaction(self, trans1, trans2)
              A Method to sort transaction
        useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset)
             A method to calculate local utility values for single itemSets

    **Methods to execute code on terminal**
    -------------------------------------------
    .. code-block:: console

      Format:

      (.venv) $ python3 RHUIM.py <inputFile> <outputFile> <minUtil> <sep>

      Example usage:

      (.venv) $ python3 RHUIM.py sampleTDB.txt output.txt 35 20


              .. note:: minSup will be considered in times of minSup and count of database transactions



    **Importing this algorithm into a python program**
    -----------------------------------------------------
    .. code-block:: python

            from PAMI.relativeHighUtilityPattern.basic import RHUIM as alg

            obj=alg.RHUIM("input.txt", 35, 20)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.savePatterns(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getmemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    -----------------
             The complete program was written by  Pradeep Pallikila  under the supervision of Professor Rage Uday Kiran.

    """

    _relativeHighUtilityItemSets = []
    _candidateCount = 0
    _utilityBinArrayLU = {}
    _utilityBinArraySU = {}
    _oldNamesToNewNames = {}
    _newNamesToOldNames = {}
    _singleItemSetsUtilities = {}
    _strToInt = {}
    _intToStr = {}
    _temp = [0] * 5000
    _patternCount = int()
    _maxMemory = 0
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    oFile = " "
    _nFile = " "
    _lno = 0
    _sep = "\t"
    _minUtil = 0
    _minUR = 0
    _memoryUSS = float()
    _memoryRSS = float()
    _dataset = None

    def __init__(self, iFile: str, minUtil: int, minUR: float, sep: str = "\t") -> None:
        super().__init__(iFile, minUtil, minUR, sep)

    def startMine(self) -> None:
        self.mine()

    def mine(self) -> None:
        """
        Mining process will start from this function
        :return: None
        """
        self._startTime = _ab._time.time()
        self._dataset = _Dataset(self._iFile, self._sep)
        self._finalPatterns = {}
        self._useUtilityBinArrayToCalculateLocalUtilityFirstTime(self._dataset)
        _minUtil = int(self._minUtil)
        _minUR = float(self._minUR)
        # print(minUR)
        self._singleItemSetsUtilities = _ab._defaultdict(int)
        itemsToKeep = []
        for key in self._utilityBinArrayLU.keys():
            if self._utilityBinArrayLU[key] >= _minUtil:
                itemsToKeep.append(key)
        itemsToKeep = sorted(itemsToKeep, key=lambda x: self._utilityBinArrayLU[x])
        currentName = 1
        for idx, item in enumerate(itemsToKeep):
            self._oldNamesToNewNames[item] = currentName
            self._newNamesToOldNames[currentName] = item
            itemsToKeep[idx] = currentName
            currentName += 1
        for transaction in self._dataset.getTransactions():
            transaction.removeUnpromisingItems(self._oldNamesToNewNames)
        self.sortDatabase(self._dataset.getTransactions())
        emptyTransactionCount = 0
        for transaction in self._dataset.getTransactions():
            if len(transaction.getItems()) == 0:
                emptyTransactionCount += 1
        self._dataset.transactions = self._dataset.transactions[emptyTransactionCount:]
        self._useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self._dataset)
        itemsToExplore = []
        for item in itemsToKeep:
            if self._utilityBinArraySU[item] >= _minUtil:
                itemsToExplore.append(item)
        utilitySum = 0
        self._backTrackingRHUIM(self._dataset.getTransactions(), itemsToKeep, itemsToExplore, 0, utilitySum)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Relative High Utility patterns were generated successfully using RHUIM algorithm")

    def _backTrackingRHUIM(self, transactionsOfP: list, itemsToKeep: list, itemsToExplore: list, prefixLength: int,
                           utilitySumP: int) -> None:
        """
        A method to mine the RHUIs Recursively

        :Attributes:

        :param transactionsOfP: the list of transactions containing the current prefix P
        :type transactionsOfP: list
        :param itemsToKeep: the list of secondary items in the p-projected database
        :type itemsToKeep: list
        :param itemsToExplore: the list of primary items in the p-projected database
        :type itemsToExplore: list
        :param prefixLength: current prefixLength
        :type prefixLength: int
        :param utilitySumP: a variable to hold sum of utilities of all items in P
        :type utilitySumP int
        :return: None
        """
        self._candidateCount += len(itemsToExplore)
        for idx, e in enumerate(itemsToExplore):
            transactionsPe = []
            utilityPe = 0
            utilitySumPe = utilitySumP + self._singleItemSetsUtilities[e]
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
                        elif self._isEqual(projectedTransaction, previousTransaction):
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
                                previousTransaction = _Transaction(items, utilities,
                                                                   previousTransaction.transactionUtility + projectedTransaction.transactionUtility)
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
            self._temp[prefixLength] = self._newNamesToOldNames[e]
            utility_ratio_pe = float(utilityPe / utilitySumPe)
            if (utilityPe >= self._minUtil) and (utility_ratio_pe * 100 >= self._minUR):
                self._output(prefixLength, utilityPe, utility_ratio_pe)
            self._useUtilityBinArraysToCalculateUpperBounds(transactionsPe, idx, itemsToKeep)
            newItemsToKeep = []
            newItemsToExplore = []
            for l in range(idx + 1, len(itemsToKeep)):
                itemK = itemsToKeep[l]
                utility_sum_pek = utilitySumPe + self._singleItemSetsUtilities[itemK]
                subtree_utility_ratio = float(self._utilityBinArraySU[itemK] / utility_sum_pek)
                local_utility_ratio = float(self._utilityBinArrayLU[itemK] / utility_sum_pek)
                if self._utilityBinArraySU[itemK] >= self._minUtil and subtree_utility_ratio * 100 >= self._minUR:
                    newItemsToExplore.append(itemK)
                    newItemsToKeep.append(itemK)
                elif self._utilityBinArrayLU[itemK] >= self._minUtil and local_utility_ratio * 100 >= self._minUR:
                    newItemsToKeep.append(itemK)
            self._backTrackingRHUIM(transactionsPe, newItemsToKeep, newItemsToExplore, prefixLength + 1, utilitySumPe)

    def _useUtilityBinArraysToCalculateUpperBounds(self, transactionsPe: list, j: int, itemsToKeep: list) -> None:
        """
        A method to  calculate the subtree utility and local utility of all items that can extend itemSet P U {e}

        :Attributes:

        :param transactionsPe: transactions the projected database for P U {e}
        :type transactionsPe: list or Dataset
        :param j: the position of j in the list of promising items
        :type j:int
        :param itemsToKeep :the list of promising items
        :type itemsToKeep: list or Dataset
        :return: None
        """
        for i in range(j + 1, len(itemsToKeep)):
            item = itemsToKeep[i]
            self._utilityBinArrayLU[item] = 0
            self._utilityBinArraySU[item] = 0
        for transaction in transactionsPe:
            sumRemainingUtility = 0
            i = len(transaction.getItems()) - 1
            while i >= transaction.offset:
                item = transaction.getItems()[i]
                if item in itemsToKeep:
                    sumRemainingUtility += transaction.getUtilities()[i]
                    self._utilityBinArraySU[item] += sumRemainingUtility + transaction.prefixUtility
                    self._utilityBinArrayLU[item] += transaction.transactionUtility + transaction.prefixUtility
                i -= 1

    def _output(self, tempPosition: int, utility: int, utilityRatio: float) -> None:
        """
         Method to print relative high utility itemSet

         :Attributes:

         :param tempPosition: position of last item 
         :type tempPosition : int 
         :param utility: total utility of itemSet
         :type utility: int
         :param utilityRatio: utility ratio of an itemSet
         :type utilityRatio: float
         :return: None
        """
        self._patternCount += 1
        s1 = str()
        for i in range(0, tempPosition + 1):
            s1 += self._dataset.intToStr.get((self._temp[i]))
            if i != tempPosition:
                s1 += "\t"
        self._finalPatterns[s1] = [utility, utilityRatio]

    def _isEqual(self, transaction1: _Transaction, transaction2: _Transaction) -> bool:
        """
         A method to Check if two transaction are identical

         :Attributes:

         :param  transaction1: the first transaction.
         :type  transaction1: Transaction
         :param  transaction2:   The second transaction.
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

    def _useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self, dataset: _Dataset) -> None:
        """
        Scan the initial database to calculate the subtree utility of each item using a utility-bin array

        :Attributes:

        :param dataset: the transaction database
        :type dataset: Dataset
        :return: None
        """
        for transaction in dataset.getTransactions():
            sumSU = 0
            i = len(transaction.getItems()) - 1
            while i >= 0:
                item = transaction.getItems()[i]
                currentUtility = transaction.getUtilities()[i]
                sumSU += currentUtility
                self._singleItemSetsUtilities[item] += currentUtility
                if item in self._utilityBinArraySU.keys():
                    self._utilityBinArraySU[item] += sumSU
                else:
                    self._utilityBinArraySU[item] = sumSU
                i -= 1

    def sortDatabase(self, transactions: list) -> None:
        """
        A Method to sort transaction

        :Attributes:

        :param transactions: transaction of items
        :type transactions: list
        :return: sorted transactions.
        :rtype: Transactions or list
        """
        cmp_items = _ab._functools.cmp_to_key(self.sort_transaction)
        transactions.sort(key=cmp_items)

    def sort_transaction(self, trans1: _Transaction, trans2: _Transaction) -> int:
        """
        A Method to sort transaction

        :Attributes:

        :param trans1: the first transaction .
        :type trans1: Transaction
        :param trans2:the second transaction.
        :type trans2: Transaction
        :return: sorted transaction.
        :rtype:   Transaction
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

    def _useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset: _Dataset) -> None:
        """
        A method to calculate local utility of single itemSets

        :Attributes:

        :param dataset: the transaction database.
        :type dataset: database
        :return: None

        """
        for transaction in dataset.getTransactions():
            for item in transaction.getItems():
                if item in self._utilityBinArrayLU:
                    self._utilityBinArrayLU[item] += transaction.transactionUtility
                else:
                    self._utilityBinArrayLU[item] = transaction.transactionUtility

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """Storing final patterns in a dataframe

        :return: returning patterns in a dataframe
        :rtype: pd.DataFrame
            """
        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b[0], b[1]])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Utility', 'UtilityRatio'])

        return dataFrame

    def getPatterns(self) -> dict:
        """ Function to send the set of patterns after completion of the mining process

        :return: returning patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile: str) -> None:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: file
        :return: None
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y[0]) + ":" + str(y[1])
            writer.write("%s \n" % patternsAndSupport)

    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

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

    def printResults(self) -> None:
        """
        This function is used to print the results
        :return: None
        """
        print("Total number of Relative Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == '__main__':
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:  #includes separator
            _ap = RHUIM(_ab._sys.argv[1], int(_ab._sys.argv[3]), float(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:  #takes "\t" as a separator
            _ap = RHUIM(_ab._sys.argv[1], int(_ab._sys.argv[3]), float(_ab._sys.argv[4]))
        _ap.mine()
        print("Total number of Relative High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = RHUIM('/Users/likhitha/Downloads/utility_datasets/Utility_T10I4D100K.csv', 150000, 0.6, '\t')
        _ap.mine()
        print("Total number of Relative High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
