# cudaEclatGCT is one of the fundamental algorithm to discover frequent patterns in a transactional database. It stores the database in compressed fp-tree decreasing the memory usage and extracts the patterns from tree.It  employs downward closure property to  reduce the search space effectively.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.frequentPattern.cuda.cudaEclatGCT as alg
#
#             obj = alg.FPGrowth(iFile, minSup)
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

#minSup = str()
_ab._sys.setrecursionlimit(20000)

import os
import csv
import time
import numpy as np
import pycuda.gpuarray as _gpuarray
import pycuda.autoinit
import psutil


class cudaEclatGCT:
    """
    :Description: Apriori is one of the fundamental algorithm to discover frequent patterns in a transactional database. This program employs apriori property (or downward closure property) to  reduce the search space effectively. This algorithm employs breadth-first search technique to find the complete set of frequent patterns in a transactional database.

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

      (.venv) $ python3 cudaEclatGCT.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 cudaEclatGCT.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup will be considered in percentage of database transactions


    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

            import PAMI.frequentPattern.cuda.cuAprioriBit as alg

            obj = alg.cuAprioriBit(iFile, minSup)

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

    def __init__(self, filePath, minSup, sep='\t'):
        self._iFile = filePath
        self._sep = sep
        self._minSup = minSup
        self.__time = 0
        self.__memRSS = 0
        self.__memUSS = 0

    """def read_data(self, data_path, sep):


        data = []
        if not os.path.isfile(data_path):
            raise ValueError('Invalid data path.' + data_path)
        with open(data_path, 'r') as f:
            file = csv.reader(f, delimiter=sep, quotechar='\r')
            lineNo = 1
            for row in file:
                data.append([str(item) for item in row if item != ''])
                lineNo += 1
        return data, lineNo"""

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
        Converting  database into bit vector
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
        vb_data = _gpuarray.to_gpu(vb_data.astype(np.uint16))
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

    def eclat(self, basePattern, final, vb_data, idx2item, item2idx):
        """
        param basePattern: base pattern used for the mining process after completion of the mining process
        type basePattern:
        param final: final pattern used for the mining process after completion of the mining process
        type final:
        param vb_data: vb_data used for the mining process after completion of the mining process
        type vb_data:
        param idx2item: idx2item used for the mining process after completion of the mining process
        type idx2item:
        param item2idx: item2idx used for the mining process after completion of the mining process
        type item2idx:
        """
        newBasePattern = []
        for i in range(0, len(basePattern)):
            item1 = basePattern[i]
            i1_list = item1.split()
            for j in range(i + 1, len(basePattern)):
                item2 = basePattern[j]
                i2_list = item2.split()
                if i1_list[:-1] == i2_list[:-1]:
                    unionOfKey = list(set(i1_list) | set(i2_list))
                    unionOfKey.sort()
                    valueList = []
                    for key in unionOfKey:
                        valueList.append(item2idx[key])
                    total = vb_data[valueList[0]]
                    for k in range(1, len(valueList)):
                        total = total.__mul__(vb_data[valueList[k]])
                    support = _gpuarray.sum(total).get()
                    if support >= self._minSup:
                        newBasePattern.append(" ".join(unionOfKey))
                        final[" ".join(unionOfKey)] = support

        if len(newBasePattern) > 0:
            self.eclat(newBasePattern, final, vb_data, idx2item, item2idx)

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
        basePattern = []
        final = {}

        self.__creatingItemSets()
        self._minSup = self.__convert(self._minSup)
        #minSup = self._minSup
        vb_data, idx2item = self.compute_vertical_bitvector_data()

        for i in range(len(vb_data)):
            if _gpuarray.sum(vb_data[i]).get() >= self._minSup:
                basePattern.append(idx2item[i])
                final[idx2item[i]] = _gpuarray.sum(vb_data[i]).get()

        # reverse idx2item
        item2idx = {idx2item[i]: i for i in idx2item}
        self.eclat(basePattern, final, vb_data, idx2item, item2idx)
        self.__time = time.time() - startTime
        self.__memRSS = psutil.Process(os.getpid()).memory_info().rss
        self.__memUSS = psutil.Process(os.getpid()).memory_full_info().uss
        self._finalPatterns = final
        self.__GPU_MEM = vb_data.nbytes


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = cudaEclatGCT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = cudaEclatGCT(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        print("Total number of Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ap._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("GPU MEM: ", _ap.getGPUMemory())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
