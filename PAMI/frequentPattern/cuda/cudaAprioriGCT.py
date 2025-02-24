# cudaAprioriGCT is one of the fundamental algorithm to discover frequent patterns using CUDA in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.
#
#
# **Importing this algorithm into a python program**
# ----------------------------------------------------
#
#             import PAMI.frequentPattern.cuda.cudaAprioriGCT as alg
#
#             obj = alg.cuAprioriGCT(iFile, minSup)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternInDataFrame()
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
"""

from deprecated import deprecated
from PAMI.frequentPattern.basic import abstract as _ab
# import abstract as _ab

import os
import time
import numpy as np
import pycuda.gpuarray as gpuarray
import psutil


class cudaAprioriGCT(_ab._frequentPatterns):
    """
    :Description: cudaAprioriGCT is one of the fundamental algorithm to discover frequent patterns in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.

    :Reference:  Agrawal, R., Imieli ́nski, T., Swami, A.: Mining association rules between sets of items in large databases.
                In: SIGMOD. pp. 207–216 (1993), https://doi.org/10.1145/170035.170072

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int :
                    The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        startTime : float
              To record the start time of the mining process

        endTime : float
              To record the completion time of the mining process

        finalPatterns : dict
              Storing the complete set of patterns in a dictionary variable

        memoryUSS : float
              To store the total amount of USS memory consumed by the program

        memoryRSS : float
              To store the total amount of RSS memory consumed by the program

        Database : list
              To store the transactions of a database in list



    **Methods to execute code on terminal**
    ----------------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 cudaAprioriGCT.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 cudaAprioriGCT.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup will be considered in percentage of database transactions


    **Importing this algorithm into a python program**
    ----------------------------------------------------

    .. code-block:: python

            import PAMI.frequentPattern.cuda.cuAprioriGCT as alg

            obj = alg.cuAprioriGCT(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    **Credits:**
    -------------

                The complete program was written by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """

    __time = 0
    __memRSS = 0
    __memUSS = 0
    __GPU_MEM = 0
    _minSup = 0
    _finalPatterns = {}

    def __init__(self, filePath, minSup, iFile, sep='\t'):
        super().__init__(iFile, minSup, sep)
        self._iFile = filePath
        self._sep = sep
        self._minSup = minSup
        self.__time = 0
        self.__memRSS = 0
        self.__memUSS = 0

    def __creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.__Database = self._iFile['Transactions'].tolist()

            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def __convert(self, value):
        """

        To convert the type of user specified minSup value

        :param value: user specified minSup value

        :type value: int or float or str

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

    def compute_vertical_bitvector_data(self):
        """
        Converting database into bit vector
        """
        # ---build item to idx mapping---#
        idx = 0
        item2idx = {}
        for transaction in self.__Database:
            for item in transaction:
                if not item in item2idx:
                    item2idx[item] = idx
                    idx += 1
        idx2item = {idx: str(int(item)) for item, idx in item2idx.items()}
        # ---build vertical data---#
        vb_data = np.zeros((len(item2idx), len(self.__Database)), dtype=np.uint16)
        for trans_id, transaction in enumerate(self.__Database):
            for item in transaction:
                vb_data[item2idx[item], trans_id] = 1
        vb_data = gpuarray.to_gpu(vb_data.astype(np.uint16))
        return vb_data, idx2item

    def getRuntime(self):
        """
        Calculating the total amount of time taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self.__time

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self.__memRSS

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """
        return self.__memUSS

    def getGPUMemory(self):
        """
        To calculate the total memory consumed by GPU
        :return: return GPU memory
        :rtype: int
        """

        return self.__GPU_MEM

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def get_numberOfPatterns(self):
        return len(self._finalPatterns)

    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe
        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: csvfile
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            if type(x) == tuple:
                pattern = ""
                for item in x:
                    pattern = pattern + str(item) + " "
                s1 = pattern + ":" + str(y)
            else:
                s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self):
        """
        Frequent pattern mining process will start from here
        """
        startTime = time.time()
        basePattern = {}
        final = {}

        self.__creatingItemSets()
        self._minSup = self.__convert(self._minSup)
        minSup = self._minSup
        vb_data, idx2item = self.compute_vertical_bitvector_data()

        for i in range(len(vb_data)):
            if gpuarray.sum(vb_data[i]).get() >= self._minSup:
                basePattern[idx2item[i]] = [i]
                final[idx2item[i]] = gpuarray.sum(vb_data[i]).get()

        while len(basePattern) > 0:
            temp = {}
            keysList = list(basePattern.keys())
            valuesList = list(basePattern.values())
            for i in range(len(basePattern) - 1):
                keyI = keysList[i].split(" ")
                keyI = [int(x) for x in keyI]

                for j in range(i + 1, len(basePattern)):
                    keyJ = keysList[j].split(" ")
                    keyJ = [int(x) for x in keyJ]
                    values = set(valuesList[i])
                    for val in valuesList[j]:
                        values.add(val)
                    values = list(sorted(values))
                    totalArray = vb_data[values[0]]
                    for k in range(1, len(values)):
                        totalArray = totalArray.__mul__(vb_data[values[k]])
                    support = gpuarray.sum(totalArray).get()
                    if support >= self._minSup:
                        combinedKey = " ".join(
                            str(x) for x in sorted(set(keyI) | set(keyJ)))
                        temp[combinedKey] = values
                        final[str(combinedKey)] = support
            basePattern = temp

        self.__time = time.time() - startTime
        self.__memRSS = psutil.Process(os.getpid()).memory_info().rss
        self.__memUSS = psutil.Process(os.getpid()).memory_full_info().uss
        self._finalPatterns = final
        self.__GPU_MEM = vb_data.nbytes

    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of Coverage Patterns:", len(self.getPatterns()))
        print("GPU MEM: ", _ap.getGPUMemory())
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = cudaAprioriGCT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4],_ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = cudaAprioriGCT(_ab._sys.argv[1],_ab._sys.argv[3],_ab._sys.argv[4],"\t")
        _ap.mine()
        _ap.mine()
        print("Total number of Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("GPU MEM: ", _ap.getGPUMemory())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")

