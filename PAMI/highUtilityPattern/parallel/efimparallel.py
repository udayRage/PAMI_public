# EFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.highUtilityPattern.parallel import efimparallel as alg
#
#             obj=alg.efimparallel("input.txt",35)
#
#             obj.mine()
#
#             highUtilityPattern = obj.getPatterns()
#
#             print("Total number of Spatial Frequent Patterns:", len(highUtilityPattern))
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

import os
import mmap
import time
import psutil
from joblib import Parallel, delayed
from deprecated import deprecated


from PAMI.highUtilityPattern.parallel import abstract as _ab

class efimParallel(_ab._utilityPatterns):
    """
    :Description:   EFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
    
    :Reference:     Zida, S., Fournier-Viger, P., Lin, J.CW. et al. EFIM: a fast and memory efficient algorithm for
                     high-utility itemset mining. Knowl Inf Syst 51, 595–625 (2017). https://doi.org/10.1007/s10115-016-0986-0

    :param  iFile: str :
                   Name of the Input file to mine complete set of High Utility patterns
    :param  oFile: str :
                   Name of the output file to store complete set of High Utility patterns
    :param minUtil: int :
                   The user given minUtil value.
    :param maxMemory: int
                   Maximum memory used by this program for running
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        inputFile (str):
            The input file path.
        minUtil (int):
            The minimum utility threshold.
        sep (str):
            The separator used in the input file.
        threads (int):
            The number of threads to use.
        Patterns (dict):
            A dictionary containing the discovered patterns.
        rename (dict):
            A dictionary containing the mapping between the item IDs and their names.
        runtime (float):
            The runtime of the algorithm in seconds.
        memoryRSS (int):
            The Resident Set Size (RSS) memory usage of the algorithm in bytes.
        memoryUSS (int):
            The Unique Set Size (USS) memory usage of the algorithm in bytes.

    :Methods:

        read_file():
            Read the input file and return the filtered transactions, primary items, and secondary items.
        binarySearch(arr, item):
            Perform a binary search on the given array to find the given item.
        project(beta, file_data, secondary):
            Project the given beta itemset on the given database.
        search(collections):
            Search for high utility itemsets in the given collections.
        mine():
            Start the EFIM algorithm.
        savePatterns(outputFile):
            Save the patterns discovered by the algorithm to an output file.
        getPatterns():
            Get the patterns discovered by the algorithm.
        getRuntime():
            Get the runtime of the algorithm.
        getMemoryRSS():
            Get the Resident Set Size (RSS) memory usage of the algorithm.
        getMemoryUSS():
            Get the Unique Set Size (USS) memory usage of the algorithm.
        printResults():
            Print the results of the algorithm.

    """

    def __init__(self, iFile, minUtil, sep="\t", threads=1):
        super().__init__(iFile, minUtil, sep)
        self.runtime = None
        self.oFile = None
        self.start = None
        self.memoryUSS = None
        self.memoryRSS = None
        self.inputFile = iFile
        self.minUtil = minUtil
        self.sep = sep
        self.Patterns = {}
        self.rename = {}
        self.threads = threads

    # Read input file
    def _read_file(self):
        """
        Read the input file and return the filtered transactions, primary items, and secondary items.

        :return:

            filtered_transactions (dict): A dictionary containing the filtered transactions.
            primary (set): A set containing the primary items.
            secondary (set): A set containing the secondary items.
        """


        file_data = []
        twu = {}

        with open(self.inputFile, 'r') as f:
            fd = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

            for line in iter(fd.readline, b""):
                line = line.decode('utf-8').strip().split(":")
                
                # Parse and process the line
                line = [x.split(self.sep) for x in line]
                weight = int(line[1][0])

                # Update file data with the parsed items
                file_data.append([line[0], [int(x) for x in line[2]]])

                for k in line[0]:
                    if k not in twu:
                        twu[k] = weight
                    else:
                        twu[k] += weight

        # Filter TWU dictionary based on minUtil (minimum utility threshold)
        twu = {k: v for k, v in twu.items() if v >= self.minUtil}

        # Sort TWU items by utility
        twu = {k: v for k, v in sorted(twu.items(), key=lambda item_: item_[1], reverse=True)}

        strToInt = {}
        t = len(twu)
        for k in twu.keys():
            strToInt[k] = t
            self.rename[t] = k
            t -= 1

        secondary = set(self.rename.keys())

        # Filter and sort transactions
        subtree = {}
        filtered_transactions = {}
        for col in file_data:
            zipped = zip(col[0], col[1])
            transaction = [(strToInt[x], y) for x, y in zipped if x in strToInt]
            transaction = sorted(transaction, key=lambda x: x[0])
            if len(transaction) > 0:
                val = [x[1] for x in transaction]
                key = [x[0] for x in transaction]
                
                fs = frozenset(key)

                if fs not in filtered_transactions:
                    filtered_transactions[fs] = [key, val, 0]
                else:
                    filtered_transactions[fs][1] = [x + y for x, y in zip(filtered_transactions[fs][1], val)]

                subUtil = sum([x[1] for x in transaction])
                temp = 0

                for i in range(len(transaction)):
                    item = key[i]
                    if item not in subtree:
                        subtree[item] = subUtil - temp
                    else:
                        subtree[item] += subUtil - temp
                    temp += val[i]

        primary = [key for key in subtree.keys() if subtree[key] >= self.minUtil]

        return filtered_transactions, primary, secondary
    

    def _binarySearch(self, arr, item):
        """
        Do a binary search on the given array to find the given item.

        :param arr: The array to search in

        :type arr: list

        :param item: The item to search for

        :type item: int

        :return:

            mid (int):
                The index of the item if found, -1 otherwise.

        """

        low = 0
        high = len(arr) - 1
        mid = 0

        while low <= high:
            mid = (high + low) // 2
            if arr[mid] < item:
                low = mid + 1
            elif arr[mid] > item:
                high = mid - 1
            else:
                return mid

        return -1

    def _project(self, beta, file_data, secondary):
        """
        Project the given beta itemset on the given database.

        :param beta: The beta itemset to project

        :type beta: list

        :param file_data: The database to project on

        :type file_data: dict

        :param secondary: The set of secondary items

        :type secondary: set

        :return:

            projected_db (dict): The projected database.
            local_utils (dict): The local utilities of the projected database.
            subtree_utils (dict): The subtree utilities of the projected database.
            utility (int): The utility of the projected database.

        """


        projected_db = {}
        local_utils = {}
        subtree_utils = {}
        utility = 0     

        added = set()

        item = beta[-1]

        temp = [v for k, v in file_data.items() if item in k]
        start = time.time()

        for v in temp:
            index = self._binarySearch(v[0], item)

            curr = v[1][index] + v[2]
            utility += curr

            newKey = []
            newVal = []

            for i in range(index+1, len(v[0])):
                if v[0][i] in secondary:
                    newKey.append(v[0][i])
                    newVal.append(v[1][i])

            if len(newKey) == 0:
                continue

            s = sum(newVal)
            temp = 0

            for i in range(len(newKey)):
                if newKey[i] in added:
                    local_utils[newKey[i]] += s + curr
                    subtree_utils[newKey[i]] += s + curr - temp
                else:
                    local_utils[newKey[i]] = s + curr
                    subtree_utils[newKey[i]] = s + curr - temp
                    added.add(newKey[i])
                
                temp += newVal[i]
            
            fs = frozenset(newKey)

            if fs not in projected_db:
                projected_db[fs] = [newKey, newVal, curr]
            else:
                projected_db[fs][1] = [x + y for x, y in zip(projected_db[fs][1], newVal)]
                projected_db[fs][2] += curr

        nprimary = [key for key in subtree_utils.keys() if subtree_utils[key] >= self.minUtil]
        nsecondary = set([key for key in local_utils.keys() if local_utils[key] >= self.minUtil])

        return beta, projected_db, nsecondary, nprimary, utility
    

    def _search(self, collections):

        """
        Search for frequent patterns in the given collections.

        :param collections: The collections to search in

        :type collections: list
        """

        if self.threads > 1:
            with Parallel(n_jobs=self.threads) as parallel:
                while len(collections) > 0:
                    new_collections = []

                    # print("Num of tasks:", sum(len(collections[i][2]) for i in range(len(collections))))
                    results = parallel(delayed(self._project)(collections[i][0] + [collections[i][2][j]], collections[i][1], collections[i][3]) for i in range(len(collections)) for j in range(len(collections[i][2])))

                    for i in range(len(results)):
                        beta, projected_db, secondary, primary, utility = results[i]
                        if utility >= self.minUtil:
                            pattern = "\t".join([self.rename[x] for x in beta])
                            # self.Patterns[tuple(beta)] = utility
                            self.Patterns[pattern] = utility
                        if len(primary) > 0:
                            new_collections.append([beta, projected_db, primary, secondary])
                    
                    collections = new_collections

        else:
            while len(collections) > 0:
                new_collections = []
                for i in range(len(collections)):
                    for j in range(len(collections[i][2])):
                        beta, projected_db, secondary, primary, utility = self._project(collections[i][0] + [collections[i][2][j]], collections[i][1], collections[i][3])
                        if utility >= self.minUtil:
                            pattern = "\t".join([self.rename[x] for x in beta])
                            # self.Patterns[tuple(beta)] = utility
                            self.Patterns[pattern] = utility
                        if len(primary) > 0:
                            new_collections.append([beta, projected_db, primary, secondary])

                collections = new_collections


    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Start the EFIM algorithm.
        """

        self.mine()

    def mine(self):
        """
        Start the EFIM algorithm.
        """

        ps = psutil.Process(os.getpid())

        self.start = time.time()

        fileData, primary, secondary = self._read_file()

        collection = [[[], fileData, primary, secondary]]

        self._search(collection)

        self.memoryRSS = ps.memory_info().rss
        self.memoryUSS = ps.memory_full_info().uss

        end = time.time()
        self.runtime = end - self.start

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csv file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)
    
    def getPatternsAsDataFrame(self):
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

    def getPatterns(self):
        """
        Get the patterns discovered by the algorithm.

        :return: A dictionary containing the discovered patterns.

        :rtype: dict
        """
        return self.Patterns

    def getRuntime(self):
        """
        Get the runtime of the algorithm.

        :return: The runtime in seconds.

        :rtype: float
        """
        return self.runtime

    def getMemoryRSS(self):
        """
        Get the Resident Set Size (RSS) memory usage of the algorithm.

        :return: The RSS memory usage in bytes.

        :rtype: int
        """
        return self.memoryRSS

    def getMemoryUSS(self):
        """
        Get the Unique Set Size (USS) memory usage of the algorithm.

        :return: The USS memory usage in bytes.

        :rtype: int
        """
        return self.memoryUSS


    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of High Utility Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":

    # inputFile = 'EFIM/accidents_utility_spmf.txt'
    # minUtil = 28000000

    # # inputFile = 'EFIM/chainstore.txt'
    # # minUtil = 2500000

    # # inputFile = 'test.txt'
    # # minUtil = 5

    # # inputFile = "EFIM/BMS_utility_spmf.txt"
    # # minUtil = 2025000

    # # inputFile = "EFIM/Utility_pumsb.csv"
    # # minUtil = 7500000

    # sep = " "
    # f = efimParallel(inputFile, minUtil, sep, 1)
    # f.mine()
    # f.mine()
    # print("# of patterns: " + str(len(f.getPatterns())))
    # print("Time taken: " + str(f.getRuntime()))
    # f.savePatterns("mine.txt")


    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:    #includes separator
            _ap = efimParallel(_ab._sys.argv[1], int(_ab._sys.argv[3]), _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:    #takes "\t" as a separator
            _ap = efimParallel(_ab._sys.argv[1], int(_ab._sys.argv[3]))
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS",  _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = efimParallel('/Users/likhitha/Downloads/Utility_T10I4D100K.csv', 50000, '\t')
        _ap.mine()
        _ap.mine()
        print("Total number of High Utility Patterns:", len(_ap.getPatterns()))
        _ap.save('/Users/likhitha/Downloads/UPGrowth_output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
