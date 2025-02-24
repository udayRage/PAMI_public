# ParallelEclat is an algorithm to discover frequent patterns in a transactional database. This program employs parallel apriori property (or downward closure property) to  reduce the search space effectively.
#
# **Importing this algorithm into a python program**
#  ----------------------------------------------------
#
#
#             import PAMI.frequentPattern.pyspark.parallelECLAT as alg
#
#             obj = alg.parallelECLAT(iFile, minSup, numWorkers)
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

from pyspark import SparkConf, SparkContext
# import abstract as _ab
from PAMI.frequentPattern.pyspark import abstract as _ab
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from deprecated import deprecated


class parallelECLAT(_ab._frequentPatterns):
    """
    :Description: ParallelEclat is an algorithm to discover frequent patterns in a transactional database.
     This program employs parallel apriori property (or downward closure property) to  reduce the search space effectively.

    :Reference:

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: int :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.
    :param  numPartitions: int :
                   The number of partitions. On each worker node, an executor process is started and this process performs processing.The processing unit of worker node is partition


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

        lno : int
            the number of transactions


    **Methods to execute code on terminal**
    ----------------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 parallelECLAT.py <inputFile> <outputFile> <minSup> <numWorkers>

      Example Usage:

      (.venv) $ python3 parallelECLAT.py sampleDB.txt patterns.txt 10.0 3

    .. note:: minSup will be considered in percentage of database transactions



    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

            import PAMI.frequentPattern.pyspark.parallelECLAT as alg

            obj = alg.parallelECLAT(iFile, minSup, numWorkers)

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
    ----------------------------------------------------
             The complete program was written by Yudai Masu under the supervision of Professor Rage Uday Kiran.

    """

    _minSup = float()
    _numPartitions = int()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _lno = int()

    def __init__(self, iFile, minSup, numWorkers, sep="\t"):
        super().__init__(iFile, minSup, int(numWorkers), sep)

    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """
        Calculating the total amount of runtime taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

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
            s1 = x + ":" + str(y)
            writer.write("%s \n" % s1)
            
    def printResults(self):
        """
        This method prints all the stats
        """
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def _genPatterns(self, suffix, pattern, data):
        """
        This function is used to generate patterns
        :param suffix: the suffix of the generated ptterns

        :type suffix: str

        :param pattern: the pattern of the generated ptterns

        :type pattern: str

        :param data: the data of the generated ptterns after completion of the mining process

        :type data: str
        """
        freqPatterns = {}
        index = data.index(suffix)
        for i in range(index + 1, len(data)):
            tid = pattern[1].intersection(data[i][1])
            if len(tid) >= self._minSup:
                freqPattern = pattern[0] + ' ' + data[i][0]
                freqPatterns[freqPattern] = len(tid)
                freqPatterns.update(self._genPatterns(data[i], (freqPattern, tid), data))
        return freqPatterns

    # def printResults(self):
    #     """
    #     This function is used to print the results
    #     """
    #     print("Total number of Frequent Patterns:", len(self.getPatterns()))
    #     print("Total Memory in USS:", self.getMemoryUSS())
    #     print("Total Memory in RSS", self.getMemoryRSS())
    #     print("Total ExecutionTime in ms:", self.getRuntime())

    def _convert(self, value):
        """
        To convert the user specified minSup value
        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        """
        print(value, type(value))
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
            print("None")
        print(type(value), value)
        return value

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

        self._startTime = _ab._time.time()
        conf = SparkConf().setAppName("Parallel ECLAT").setMaster("local[*]")
        sc = SparkContext(conf=conf)

        data = sc.textFile(self._iFile, self._numPartitions) \
            .map(lambda line: [int(y) for y in line.rstrip().split(self._sep)]).persist()
        self._lno = data.count()
        self._minSup = self._convert(self._minSup)

        frequentItems = None
        frequentItems = data.zipWithIndex() \
            .flatMap(lambda x: [(str(item), x[1]) for item in x[0]]) \
            .groupByKey() \
            .filter(lambda x: len(x[1]) >= self._minSup) \
            .sortBy(lambda x: len(x[1])) \
            .mapValues(set) \
            .persist()
        data.unpersist()
        # elif 'temporal' in self._iFile:
        #     frequentItems = data.flatMap(lambda trans: [(str(item), trans[0]) for item in trans[1:]]) \
        #         .groupByKey() \
        #         .filter(lambda x: len(x[1]) >= self._minSup) \
        #         .mapValues(set) \
        #         .persist()
        #     data.unpersist()
        # else:
        #     pass
        #     # print("may be not able to process the input file")

        freqItems = dict(frequentItems.collect())
        # print(len(freqItems))
        self._finalPatterns = {k: len(v) for k, v in freqItems.items()}

        freqPatterns = list(frequentItems.map(lambda x: self._genPatterns(x, x, list(freqItems.items())))
                            .filter(lambda x: len(x) != 0).collect())
        for value in freqPatterns:
            self._finalPatterns.update(value)

        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Parallel ECLAT algorithm")
        sc.stop()


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = parallelECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = parallelECLAT(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        _finalPatterns = _ap.getPatterns()
        print("Total number of Frequent Patterns:", len(_finalPatterns))
        _ap.save(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
