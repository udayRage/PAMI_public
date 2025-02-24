# cuREFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.periodicFrequentPattern.parallel import cuREFIM as alg
#
#             obj = alg.cuREFIM(iFile, minUtil, ratio, '\t')
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
import time
import mmap
import psutil
import cupy as cp
import numpy as np

from PAMI.relativeHighUtilityPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated

searchGPU = cp.RawKernel(r'''

#define uint32_t unsigned int

extern "C" __global__
void searchGPU(uint32_t *items, uint32_t *utils, uint32_t *indexesStart, uint32_t *indexesEnd, uint32_t numTransactions,
                uint32_t *candidates, uint32_t candidateSize, uint32_t numCandidates,
                uint32_t *candidateCost, uint32_t *candidateLocalUtil, uint32_t *candidateSubtreeUtil,
                uint32_t *secondaryReference, uint32_t *secondaries, uint32_t numSecondaries)
{

    uint32_t tid = blockDim.x * blockIdx.x + threadIdx.x;
    if (tid >= numTransactions) return;
    uint32_t *cands = new uint32_t[candidateSize];

    uint32_t start = indexesStart[tid];
    uint32_t end = indexesEnd[tid];

    for (uint32_t i = 0; i < numCandidates; i++) {
        for (uint32_t j = 0; j < candidateSize; j++) {
            cands[j] = candidates[i * candidateSize + j];
        }

        uint32_t found = 0;
        uint32_t foundCost = 0;
        uint32_t foundLoc = 0;

        for (uint32_t j = start; j < end; j++)
        {
            if (items[j] == cands[found])
            {
                found++;
                foundCost += utils[j];
                foundLoc = j;
            }
        }

        if (found != candidateSize) continue;

        atomicAdd(&candidateCost[i], foundCost);

        for (uint32_t j = foundLoc + 1; j < end; j++)
        {
            if (secondaries[secondaryReference[i] * numSecondaries + items[j]])
            {
                foundCost += utils[j];
            }
        }

        uint32_t temp = 0;
        for (uint32_t j = foundLoc + 1; j < end; j++)
        {
            if (secondaries[secondaryReference[i] * numSecondaries + items[j]])
            {
                atomicAdd(&candidateLocalUtil[i * numSecondaries + items[j]], foundCost);
                atomicAdd(&candidateSubtreeUtil[i * numSecondaries + items[j]], foundCost - temp);
                temp += utils[j];
            }
        }
    }

    delete[] cands;

}

''', 'searchGPU')

class GPUEFIM:

    """
    :Description:   EFIM is one of the fastest algorithm to mine High Utility ItemSets from transactional databases.
    
    :Reference:   Zida, S., Fournier-Viger, P., Lin, J.CW. et al. EFIM: a fast and memory efficient algorithm for
                  high-utility itemset mining. Knowl Inf Syst 51, 595–625 (2017). https://doi.org/10.1007/s10115-016-0986-0

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

        inputFile (str): The input file path.
        minUtil (int): The minimum utility threshold.
        sep (str): The separator used in the input file.
        threads (int): The number of threads to use.
        Patterns (dict): A dictionary containing the discovered patterns.
        rename (dict): A dictionary containing the mapping between the item IDs and their names.
        runtime (float): The runtime of the algorithm in seconds.
        memoryRSS (int): The Resident Set Size (RSS) memory usage of the algorithm in bytes.
        memoryUSS (int): The Unique Set Size (USS) memory usage of the algorithm in bytes.

    :Methods:

        read_file(): Read the input file and return the filtered transactions, primary items, and secondary items.
        search(collections): Search for high utility itemsets in the given collections.
        mine(): Start the EFIM algorithm.
        savePatterns(outputFile): Save the patterns discovered by the algorithm to an output file.
        getPatterns(): Get the patterns discovered by the algorithm.
        getRuntime(): Get the runtime of the algorithm.
        getMemoryRSS(): Get the Resident Set Size (RSS) memory usage of the algorithm.
        getMemoryUSS(): Get the Unique Set Size (USS) memory usage of the algorithm.
        printResults(): Print the results of the algorithm.

    """


    def __init__(self, inputFile, minUtil, ratio, sep = '\t'):
        self.runtime = None
        self.start = None
        self.memoryUSS = None
        self.memoryRSS = None
        self.numTransactions = None
        self.secondaryLen = None
        self.indexesEnd = None
        self.indexesStart = None
        self.utils = None
        self.items = None
        self.inputFile = inputFile
        self.minUtil = minUtil
        self.sep = sep
        self.Patterns = {}
        self.rename = {}
        self.ratio = ratio


    # Read input file
    def read_file(self):
        """
        Read the input file and return the filtered transactions, primary items, and secondary items.

        :Returns:

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
        twu = {k: v for k, v in sorted(twu.items(), key=lambda item: item[1], reverse=True)}

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

        indexesStart = [0]
        indexesEnd = []
        items = []
        utils = []

        for key in filtered_transactions.keys():
            # print(indexesStart[-1], end="|")
            indexesEnd.append(indexesStart[-1] + len(filtered_transactions[key][0]))
            items.extend(filtered_transactions[key][0])
            utils.extend(filtered_transactions[key][1])
            # for i in range(len(filtered_transactions[key][0])):
            #     print(str(filtered_transactions[key][0][i]) + ":" + str(filtered_transactions[key][1][i]), end=" ")
            # print("|", indexesEnd[-1])
            indexesStart.append(indexesEnd[-1])

        indexesStart.pop()

        self.items = cp.array(items, dtype=np.uint32)
        self.utils = cp.array(utils, dtype=np.uint32)
        self.indexesStart = cp.array(indexesStart, dtype=np.uint32)
        self.indexesEnd = cp.array(indexesEnd, dtype=np.uint32)

        primary = [key for key in subtree.keys() if subtree[key] >= self.minUtil]

        # secondary is from 0 to len(secondary) - 1
        secondary = [i for i in range(len(secondary) + 1)]

        self.secondaryLen = len(secondary)
        self.numTransactions = len(filtered_transactions)
        
        return primary, secondary

    def search(self, collection, depth):
        """
        Search for frequent patterns in the given collections.

        :Attributes:

            collections (list): The collections to search in.
        """

        storeAll = {}

        while len(collection) > 0:
            candidates = []
            secondaryReference = []
            secondaries = []

            print("Collections: ", len(collection))

            temp = 0
            for item in collection:
                for primary in item[1]:
                    candidates.append(item[0] + [primary])
                    secondaryReference.append(temp)
                temp += 1
                # print(item[2])
                secondaries.extend(item[2])

            candidateSize = len(collection[0][0]) + 1
            numCandidates = len(candidates)
            # print("Candidates: ", numCandidates)

            # flatten candidates
            candidates = [item for sublist in candidates for item in sublist]
            candidates = cp.array(candidates, dtype=np.uint32)

            # print(secondaries)
            secondaries = cp.array(secondaries, dtype=np.uint32)
            secondaryReference = cp.array(secondaryReference, dtype=np.uint32)

            costs = cp.zeros(numCandidates, dtype=np.uint32)
            localUtil = cp.zeros(numCandidates * self.secondaryLen, dtype=np.uint32)
            subtreeUtil = cp.zeros(numCandidates * self.secondaryLen, dtype=np.uint32)

            # items, utils, indexesStart, indexesEnd, numTransactions
            # candidates, candidateSize, numCandidates,
            # candidateCost, candidateLocalUtil, candidateSubtreeUtil, 
            # secondaryReference, secondaries, numSecondaries

            numOfThreads = 32
            numOfBlocks = self.numTransactions // numOfThreads + 1

            searchGPU((numOfBlocks,), (numOfThreads,), 
                    (self.items, self.utils, self.indexesStart, self.indexesEnd, self.numTransactions,
                        candidates, candidateSize, numCandidates,  
                        costs, localUtil, subtreeUtil,
                        secondaryReference, secondaries, self.secondaryLen))
            cp.cuda.runtime.deviceSynchronize()

            # get results from GPU
            candidates = candidates.get()
            costs = costs.get()
            localUtil = localUtil.get()
            subtreeUtil = subtreeUtil.get()

            # resize candidates
            candidates = np.resize(candidates, (numCandidates, candidateSize))
            localUtil = np.resize(localUtil, (numCandidates, self.secondaryLen))
            subtreeUtil = np.resize(subtreeUtil, (numCandidates, self.secondaryLen))

            newCollections = []
            #  collection = [[[], primary, secondary]]  

            for i in range(numCandidates):
                if len(candidates[i]) == 1:
                  storeAll[tuple(candidates[i])] = costs[i]

                # print(candidates[i], costs[i], subtreeUtil[i], localUtil[i])
                if costs[i] >= self.minUtil:
                    if len(candidates[i]) == 1:
                      self.Patterns[tuple(candidates[i])] = [costs[i],1]
                    else:
                      tcos = 0
                      for x in candidates[i]:
                        tcos += storeAll[tuple([x])]
                      ratio = costs[i] / tcos
                      if ratio >= self.ratio:
                        self.Patterns[tuple(candidates[i])] = [costs[i],ratio]
                        
                
                newSubtreeUtil = []
                newLocalUtil = []

                for j in range(len(subtreeUtil[i])):
                    if subtreeUtil[i][j] >= self.minUtil:
                        newSubtreeUtil.append(j)
                if len(newSubtreeUtil) > 0:
                    for j in range(len(localUtil[i])):
                        if localUtil[i][j] >= self.minUtil:
                            newLocalUtil.append(1)
                        else:
                            newLocalUtil.append(0)

                    # print(candidates[i], newSubtreeUtil, newLocalUtil)
                    newCollections.append([list(candidates[i]), newSubtreeUtil, newLocalUtil])
                    # print()
                
            collection = newCollections


    def savePatterns(self, outputFile):
        with open(outputFile, 'w') as f:
            for key, value in self.Patterns.items():
                joined = " ".join(key) + " #UTIL: " + str(value) + "\n"
                f.write(joined)

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Start the EFIM algorithm.

        :return: None
        """

        ps = psutil.Process(os.getpid())

        self.start = time.time()

        primary, secondary = self.read_file()

        collection = [[[], primary, secondary]]

        self.search(collection, 1)

        self.memoryRSS = ps.memory_info().rss
        self.memoryUSS = ps.memory_full_info().uss

        end = time.time()
        self.runtime = end - self.start

        newPatterns = {}
        for key, value in self.Patterns.items():
            newKey = tuple([self.rename[x] for x in key])
            newPatterns[newKey] = value
        
        self.Patterns = newPatterns

    def Mine(self):
        """
        Start the EFIM algorithm.
        :return: None
        """

        ps = psutil.Process(os.getpid())

        self.start = time.time()

        primary, secondary = self.read_file()

        collection = [[[], primary, secondary]]

        self.search(collection, 1)

        self.memoryRSS = ps.memory_info().rss
        self.memoryUSS = ps.memory_full_info().uss

        end = time.time()
        self.runtime = end - self.start

        newPatterns = {}
        for key, value in self.Patterns.items():
            newKey = tuple([self.rename[x] for x in key])
            newPatterns[newKey] = value

        self.Patterns = newPatterns

    def getPatterns(self):
        """
        Get the patterns discovered by the algorithm.

        :return: dict: A dictionary containing the discovered patterns.
        """
        return self.Patterns

    def getRuntime(self):
        """
        Get the runtime of the algorithm.

        :return: float: The runtime in seconds.
        """
        return self.runtime

    def getMemoryRSS(self):
        """
        Get the Resident Set Size (RSS) memory usage of the algorithm.

        :return: int: The RSS memory usage in bytes.
        """
        return self.memoryRSS

    def getMemoryUSS(self):
        """
        Get the Unique Set Size (USS) memory usage of the algorithm.

        :return: int: The USS memory usage in bytes.
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

    inputFile = 'Utility_T10I4D100K.csv'
    minUtil = 150000
    ratio = 0.1

    # inputFile = 'EFIM/chainstore.txt'
    # minUtil = 2500000

    # inputFile = 'EFIM/test.txt'
    # minUtil = 5

    # inputFile = "EFIM/BMS_utility_spmf.txt"
    # minUtil = 2030000

    # inputFile = "EFIM/Utility_pumsb.csv"
    # minUtil = 4500000

    sep = "\t"
    f = GPUEFIM(inputFile, minUtil, ratio, sep)
    f.mine()
    f.savePatterns("output.txt")
    print("# of patterns: " + str(len(f.getPatterns())))
    print("Time taken: " + str(f.getRuntime()))

