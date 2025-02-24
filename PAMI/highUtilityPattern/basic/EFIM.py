# EFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.highUtilityPattern.basic import EFIM as alg
#
#             obj=alg.EFIM("input.txt",35)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of high utility Patterns:", len(Patterns))
#
#             obj.save("output")
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

from PAMI.highUtilityPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated


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
            an offset pointer, used by projected transactions
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
        :return: a new transaction after projecting the transaction starting from offsetE until the end of the transaction
        :rtype: _Transaction
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
        :return: list of items in transaction after projecting the transaction starting from offsetE until the end of the transaction
        :rtype: list
        """
        return self.items

    def getUtilities(self) -> list:
        """
        A method to return utilities in transaction
        :return: list of utilities in transaction
        :rtype: list
        """
        return self.utilities

    def getLastPosition(self) -> int:
        """
        A method to return last position in a transaction
        :return: last position in a transaction after projecting the transaction starting from offsetE until the end of the transaction
        :rtype: int
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

        transactions :
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
    
    def __init__(self,datasetPath: Union[str, _ab._pd.DataFrame], sep: str) -> None:
        self.strToInt = {}
        self.intToStr = {}
        self.transactions = []
        self.maxItem = 0
        self.cnt = 1
        self.sep = sep
        self.createItemsets(datasetPath)
        self.Database = []

    def createItemsets(self, datasetPath: Union[str, _ab._pd.DataFrame]) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        :param datasetPath: It represents the peth for the dataset
        :type datasetPath: str
        :return: None
        """

        if isinstance(datasetPath, _ab._pd.DataFrame):
            utilities, data, transactionUtility = [], [], []
            if datasetPath.empty:
                print("its empty..")
            i = datasetPath.columns.values.tolist()
            if 'Transactions' in i:
                data = datasetPath['Transactions'].tolist()
            if 'Utilities' in i:
                utilities = datasetPath['Utilities'].tolist()
            if 'UtilitySum' in i:
                transactionUtility = datasetPath['UtilitySum'].tolist()
            self.transactions.append(self.createTransaction(data, utilities, transactionUtility))
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

    def createTransaction(self, itemsString: list, utilityString: list, transactionUtility: int) -> '_Transaction':
        """
        A method to create Transaction from dataset given
        :param itemsString: List of strings representing transactions
        :type itemsString: list
        :param utilityString: List of strings representing utility
        :type utilityString: list
        :param transactionUtility: Integer representing transaction utility
        :type transactionUtility: int
        :return: created Transaction from the given dataset
        :rtype: _Transaction
        """


        '''trans_list = line.strip().split(':')
        transactionUtility = int(trans_list[1])
        itemsString = trans_list[0].strip().split(self.sep)
        itemsString = [x for x in itemsString if x]
        utilityString = trans_list[2].strip().split(self.sep)
        utilityString = [x for x in utilityString if x]'''
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
        :return: the largest item
        :rtype: int
        """
        return self.maxItem

    def getTransactions(self) -> list:
        """
        A method to return transactions from database
        :return: the list of transactions from database
        :rtype: list
        """
        return self.transactions


class EFIM(_ab._utilityPatterns):
    """
    :Description:   EFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
    
    :Reference:      Zida, S., Fournier-Viger, P., Lin, J.CW. et al. EFIM: a fast and memory efficient algorithm for
                    high-utility itemset mining. Knowl Inf Syst 51, 595–625 (2017). https://doi.org/10.1007/s10115-016-0986-0

    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility patterns
    :param minUtil: int :
                   The user given minUtil value.
    :param candidateCount: int
                   Number of candidates specified by user
    :param maxMemory: int
                   Maximum memory used by this program for running
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : file
            Name of the input file to mine complete set of high utility patterns
        oFile : file
            Name of the output file to store complete set of high utility patterns
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        minUtil : int
            The user given minUtil value
        highUtilityitemSets: map
            set of high utility itemSets
        candidateCount: int
             Number of candidates 
        utilityBinArrayLU: list
             A map to hold the local utility values of the items in database
        utilityBinArraySU: list
            A map to hold the subtree utility values of the items is database
        oldNamesToNewNames: list
            A map which contains old names, new names of items as key value pairs
        newNamesToOldNames: list
            A map which contains new names, old names of items as key value pairs
        maxMemory: float
            Maximum memory used by this program for running
        patternCount: int
            Number of HUI's
        itemsToKeep: list
            keep only the promising items ie items having local utility values greater than or equal to minUtil
        itemsToExplore: list
            list of items that have subtreeUtility value greater than or equal to minUtil

    :Methods :

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
        backTrackingEFIM(transactionsOfP, itemsToKeep, itemsToExplore, prefixLength)
               A method to mine the HUIs Recursively
        useUtilityBinArraysToCalculateUpperBounds(transactionsPe, j, itemsToKeep)
               A method to calculate the sub-tree utility and local utility of all items that can extend itemSet P and e
        output(tempPosition, utility)
               A method to output a high-utility itemSet to file or memory depending on what the user chose
        is_equal(transaction1, transaction2)
               A method to Check if two transaction are identical
        useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(dataset)
              A method to calculate the sub tree utility values for single items
        sortDatabase(self, transactions)
              A Method to sort transaction
        sort_transaction(self, trans1, trans2)
              A Method to sort transaction
        useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset)
             A method to calculate local utility values for single itemsets

    **Executing the code on terminal:**
    ------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 EFIM.py <inputFile> <outputFile> <minUtil> <sep>

      Example Usage:

      (.venv) $ python3 EFIM sampleTDB.txt output.txt 35

    .. note:: maxMemory will be considered as Maximum memory used by this program for running

    Sample run of importing the code:
    -------------------------------------
    .. code-block:: python
        
            from PAMI.highUtilityPattern.basic import EFIM as alg

            obj=alg.EFIM("input.txt",35)

            obj.mine()

            Patterns = obj.getPatterns()

            print("Total number of high utility Patterns:", len(Patterns))

            obj.save("output")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)
   
    **Credits:**
    -------------------
        The complete program was written by pradeep pallikila under the supervision of Professor Rage Uday Kiran.
     
    """

    _highUtilityitemSets = []
    _candidateCount = 0
    _utilityBinArrayLU = {}
    _utilityBinArraySU = {}
    _oldNamesToNewNames = {}
    _newNamesToOldNames = {}
    _strToInt = {}
    _intToStr = {}
    _Neighbours = {}
    _temp = [0] * 5000
    _patternCount = int()
    _maxMemory = 0
    #_startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _nFile = " "
    _lno = 0
    _sep = "\t"
    _minUtil = 0
    _memoryUSS = float()
    _memoryRSS = float()
    _startTime = _ab._time.time()

    def __init__(self, iFile, minUtil, sep="\t") -> None:
        super().__init__(iFile, minUtil, sep)
        self.oFile = None
        self._dataset = None
        self._sep = sep
        self._highUtilityitemSets = []
        self._candidateCount = 0
        self._utilityBinArrayLU = {}
        self._utilityBinArraySU = {}
        self._oldNamesToNewNames = {}
        self._newNamesToOldNames = {}
        self._strToInt = {}
        self._intToStr = {}
        self._Neighbours = {}
        self._temp = [0] * 5000
        self._patternCount = 0
        self._maxMemory = 0
        self._endTime = float()
        self._finalPatterns = {}
        self._lno = 0
        self._memoryUSS = float()
        self._memoryRSS = float()

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Start the EFIM algorithm.
        :return: None
        """
        self.mine()

    def mine(self) -> None:
        """
        Start the EFIM algorithm.
        :return: None
        """
        self._startTime = _ab._time.time()
        self._dataset = _Dataset(self._iFile, self._sep)
        self._useUtilityBinArrayToCalculateLocalUtilityFirstTime(self._dataset)
        self._minUtil = int(self._minUtil)
        itemsToKeep = []
        for key in self._utilityBinArrayLU.keys():
            if self._utilityBinArrayLU[key] >= self._minUtil:
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
        self._sortDatabase(self._dataset.getTransactions())
        emptyTransactionCount = 0
        for transaction in self._dataset.getTransactions():
            if len(transaction.getItems()) == 0:
                emptyTransactionCount += 1
        self._dataset.transactions = self._dataset.transactions[emptyTransactionCount:]
        self._useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self._dataset)
        itemsToExplore = []
        for item in itemsToKeep:
            if self._utilityBinArraySU[item] >= self._minUtil:
                itemsToExplore.append(item)
        self._backTrackingEFIM(self._dataset.getTransactions(), itemsToKeep, itemsToExplore, 0)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("High Utility patterns were generated successfully using EFIM algorithm")

    def _backTrackingEFIM(self, transactionsOfP: list, itemsToKeep: list, itemsToExplore: list, prefixLength: int) -> None:
        """
        A method to mine the HUIs Recursively
        :param transactionsOfP: the list of transactions containing the current prefix P
        :type transactionsOfP: list
        :param itemsToKeep: the list of secondary items in the p-projected database
        :type itemsToKeep: list
        :param itemsToExplore: the list of primary items in the p-projected database
        :type itemsToExplore: list
        :param prefixLength: current prefixLength
        :type prefixLength: int
        :return: None
        """
        self._candidateCount += len(itemsToExplore)
        for idx, e in enumerate(itemsToExplore):
            transactionsPe = []
            utilityPe = 0
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
                                previousTransaction = _Transaction(items, utilities, previousTransaction.transactionUtility + projectedTransaction.transactionUtility)
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
            if utilityPe >= self._minUtil:
                self._output(prefixLength, utilityPe)
            self._useUtilityBinArraysToCalculateUpperBounds(transactionsPe, idx, itemsToKeep)
            newItemsToKeep = []
            newItemsToExplore = []
            for l in range(idx + 1, len(itemsToKeep)):
                itemK = itemsToKeep[l]
                if self._utilityBinArraySU[itemK] >= self._minUtil:
                    newItemsToExplore.append(itemK)
                    newItemsToKeep.append(itemK)
                elif self._utilityBinArrayLU[itemK] >= self._minUtil:
                    newItemsToKeep.append(itemK)
            if len(transactionsPe) != 0:
                self._backTrackingEFIM(transactionsPe, newItemsToKeep, newItemsToExplore, prefixLength + 1)

    def _useUtilityBinArraysToCalculateUpperBounds(self, transactionsPe: list, j: int, itemsToKeep: list) -> None:
        """
        A method to  calculate the subtree utility and local utility of all items that can extend itemSet P U {e}
        :param transactionsPe: transactions the projected database for P U {e}
        :type transactionsPe: list
        :param j:the position of j in the list of promising items
        :type j:int
        :param itemsToKeep :the list of promising items
        :type itemsToKeep: list
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

    def _output(self, tempPosition: int, utility: int) -> None:
        """
        Method to print high utility items
        :param tempPosition: position of last item
        :type tempPosition : int
        :param utility: total utility of itemSet
        :type utility: int
        :return: None
        """
        self._patternCount += 1
        s1 = str()
        for i in range(0, tempPosition+1):
            s1 += self._dataset.intToStr.get((self._temp[i]))
            if i != tempPosition:
                s1 += "\t"
        self._finalPatterns[s1] = str(utility)

    def _isEqual(self, transaction1: '_Transaction', transaction2: '_Transaction') -> bool:
        """
         A method to Check if two transaction are identical
         :param  transaction1: the first transaction
         :type  transaction1: Trans
         :param  transaction2:    the second transaction
         :type  transaction2: Trans
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

    def _useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self, dataset: '_Dataset') -> None:
        """
        Scan the initial database to calculate the subtree utility of each item using a utility-bin array
        :param dataset: the transaction database
        :type dataset: list
        :return: None
        """
        for transaction in dataset.getTransactions():
            sumSU = 0
            i = len(transaction.getItems()) - 1
            while i >= 0:
                item = transaction.getItems()[i]
                sumSU += transaction.getUtilities()[i]
                if item in self._utilityBinArraySU.keys():
                    self._utilityBinArraySU[item] += sumSU
                else:
                    self._utilityBinArraySU[item] = sumSU
                i -= 1

    def _sortDatabase(self, transactions: list) -> None:
        """
        A Method to sort transactions
        :param transactions: transaction of items
        :type transactions: Transaction
        :return: None
        """
        cmp_items = _ab._functools.cmp_to_key(self.sort_transaction)
        transactions.sort(key=cmp_items)

    def sort_transaction(self, trans1: '_Transaction', trans2: '_Transaction') -> int:
        """
        A Method to sort transaction
        :param trans1: the first transaction
        :type trans1: Trans
        :param trans2:the second transaction
        :type trans2: Trans
        :return: sorted transaction
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

    def _useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset: '_Dataset') -> None:
        """
        A method to calculate local utility of single itemset
        :param dataset: the transaction database
        :type dataset: dataset
        :return: None
        """
        for transaction in dataset.getTransactions():
            for item in transaction.getItems():
                if item in self._utilityBinArrayLU:
                    self._utilityBinArrayLU[item] += transaction.transactionUtility
                else:
                    self._utilityBinArrayLU[item] = transaction.transactionUtility

    def getPatternsAsDataFrame(self) -> '_pd.DataFrame':
        """
        Storing final patterns in a dataframe
        :return: returning patterns in a dataframe
        :rtype: pd.DataFrame
        """
        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Utility'])

        return dataFrame
    
    def getPatterns(self) -> dict:
        """
        Function to send the set of patterns after completion of the mining process
        :return: returning patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile: str) -> None:
        """
        Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

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
        return self._endTime-self._startTime

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == '__main__':
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:    #includes separator
            _ap = EFIM(_ab._sys.argv[1], int(_ab._sys.argv[3]), _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:    #takes "\t" as a separator
            _ap = EFIM(_ab._sys.argv[1], int(_ab._sys.argv[3]))
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS",  _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = EFIM('/Users/likhitha/Downloads/Utility_T10I4D100K.csv', 50000, '\t')
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save('/Users/likhitha/Downloads/UPGrowth_output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
