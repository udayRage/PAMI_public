# SequentialDatabase is to get stats of database like avarage, minimun, maximum  and so on
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#             from PAMI.extras.stats import sequentialDatabase as db
#
#             obj = db.sequentialDatabase(iFile, "\t")
#
#             obj.save(oFile)
#
#             obj.run()
#
#             obj.printStats()
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

import statistics
import validators
from urllib.request import urlopen
import PAMI.extras.graph.plotLineGraphFromDictionary as plt
import sys
from typing import List, Dict, Tuple, Set, Union, Any, Generator


class sequentialDatabase:
    """
    SequentialDatabase is to get stats of database like avarage, minimun, maximum  and so on.

    :Attributes:

        :param inputFile: file :
               input file path
        :param sep: str
               separator in file. Default is tab space.

    :Methods:

        readDatabase():
            read sequential database from input file and store into database and size of each sequence and subsequences.
        getDatabaseSize(self):
            get the size of database
        getTotalNumberOfItems(self):
            get the number of items in database.
        getMinimumSequenceLength(self):
            get the minimum sequence length
        getAverageSubsequencePerSequenceLength(self):
            get the average subsequence length per sequence length. It is sum of all subsequence length divided by sequence length.
        getAverageItemPerSubsequenceLength(self):
            get the average Item length per subsequence. It is sum of all item length divided by subsequence length.
        getMaximumSequenceLength(self):
            get the maximum sequence length
        getStandardDeviationSubsequenceLength(self):
            get the standard deviation subsequence length
        getVarianceSequenceLength(self):
            get the variance Sequence length
        getSequenceSize(self):
            get the size of sequence
        getMinimumSubsequenceLength(self):
            get the minimum subsequence length
        getAverageItemPerSequenceLength(self):
            get the average item length per sequence. It is sum of all item length divided by sequence length.
        getMaximumSubsequenceLength(self):
            get the maximum subsequence length
        getStandardDeviationSubsequenceLength(self):
            get the standard deviation subsequence length
        getVarianceSubsequenceLength(self):
            get the variance subSequence length
        getSortedListOfItemFrequencies(self):
            get sorted list of item frequencies
        getFrequenciesInRange(self):
            get sorted list of item frequencies in some range
        getSequencialLengthDistribution(self):
            get Sequence length Distribution
        getSubsequencialLengthDistribution(self):
            get subSequence length distribution
        printStats(self):
            to print the all status of sequence database
        plotGraphs(self):
            to plot the  distribution about items, subsequences in sequence and items in subsequence

    **Importing this algorithm into a python program**
    --------------------------------------------------------
    .. code-block:: python

            from PAMI.extras.dbStats import SequentialDatabase as db

            obj = db.SequentialDatabase(iFile, "\t")

            obj.save(oFile)

            obj.run()

            obj.printStats()


    **Executing the code on terminal:**
    -------------------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 sequentialDatabase.py <inputFile>

      Example Usage:

      (.venv) $ python3 sequentialDatabase.py sampleDB.txt



    **Sample run of the importing code:**
    ----------------------------------------------------
        import PAMI.extra.DBstats.SequentialDatabase as alg
        _ap=alg.SequentialDatabase(inputfile,sep)
        _ap.readDatabase()
        _ap.printStats()
        _ap.plotGraphs()
    **Credits:**
    ---------------------
        The complete program was written by Shota Suzuki  under the supervision of Professor Rage Uday Kiran.
    """

    def __init__(self, inputFile: str, sep: str='\t') -> None:
        """
        :param inputFile: input file name or path
        :type inputFile: str
        :param sep: separator character for input file
        :type sep: str
        :return: None
        """
        self.inputFile = inputFile
        self.seqLengthList = []
        self.subSeqLengthList = []
        self.sep = sep
        self.database = {}

    def readDatabase(self) -> None:
        """
        read sequential database from input file and store into database and size of each sequence and subsequences.
        """
        if isinstance(self.inputFile, str):
            if validators.url(self.inputFile):
                data = urlopen(self.inputFile)
                rowNum=0
                for line in data:
                    line.strip()
                    temp = [i.rstrip() for i in line.split('-1')]
                    temp = [x for x in temp if x]
                    temp.pop()
                    seq = []
                    self.seqLengthList.append(len(temp))
                    self.subSeqLengthList.append([len(i) for i in temp])
                    for i in temp:
                        if len(i) > 1:
                            tempSorted=list(sorted(set(i.split())))
                            seq.append(tempSorted)
                        else:
                            seq.append(i)
                    rowNum+=1
                    if seq:
                        self.database[rowNum]=seq
            else:
                with open(self.inputFile, 'r') as f:
                    rowNum = 0
                    for line in f:
                        temp = [i.rstrip(self.sep) for i in line.split('-1')]
                        temp = [x for x in temp if x]
                        temp.pop()
                        seq = []
                        self.seqLengthList.append(len(temp))
                        subseq=[]
                        for i in temp:
                            if len(i) > 1:
                                tempSorted = list(sorted(set(i.split())))
                                subseq.append(len(tempSorted))
                                seq.append(tempSorted)
                            else:
                                seq.append(i)
                                subseq.append(len(i))
                        if subseq:
                            self.subSeqLengthList.append(subseq)
                        rowNum += 1
                        if seq:
                            self.database[rowNum] = seq


    def getDatabaseSize(self) -> int:
        """
        get the size of database
        :return: dataset size
        :rtype: int
        """
        return len(self.database)

    def getTotalNumberOfItems(self) -> int:
        """
        get the number of items in database.
        :return: number of items
        :rtype: int
        """
        return len(self.getSortedListOfItemFrequencies())

    def getMinimumSequenceLength(self) -> int:
        """
        get the minimum sequence length
        :return: minimum sequence length
        :rtype: int
        """
        return min(self.seqLengthList)

    def getAverageSubsequencePerSequenceLength(self) -> float:
        """
        get the average subsequence length per sequence length. It is sum of all subsequence length divided by sequence length.
        :return: average subsequence length per sequence length
        :rtype: float
        """
        totalLength = sum(self.seqLengthList)
        return totalLength / len(self.database)

    def getAverageItemPerSubsequenceLength(self) -> float:

        """
        get the average Item length per subsequence. It is sum of all item length divided by subsequence length.
        :return: average Item length per subsequence
        :rtype: float
        """

        totalLength = sum(list(map(sum,self.subSeqLengthList)))
        return totalLength / sum(self.seqLengthList)

    def getMaximumSequenceLength(self) -> int:
        """
        get the maximum sequence length
        :return: maximum sequence length
        :rtype: int
        """
        return max(self.seqLengthList)

    def getStandardDeviationSequenceLength(self) -> float:
        """
        get the standard deviation sequence length
        :return: standard deviation sequence length
        :rtype: float
        """
        return statistics.pstdev(self.seqLengthList)

    def getVarianceSequenceLength(self) -> float:
        """
        get the variance Sequence length
        :return: variance Sequence length
        :rtype: float
        """
        return statistics.variance(self.seqLengthList)

    def getSequenceSize(self) -> int:
        """
        get the size of sequence
        :return: sequences size
        :rtype: int
        """
        return sum(self.seqLengthList)

    def getMinimumSubsequenceLength(self) -> int:
        """
        get the minimum subsequence length
        :return: minimum subsequence length
        :rtype: int
        """
        return min(list(map(min,self.subSeqLengthList)))

    def getAverageItemPerSequenceLength(self) -> float:
        """
        get the average item length per sequence. It is sum of all item length divided by sequence length.
        :return: average item length per sequence
        :rtype: float
        """
        totalLength = sum(list(map(sum,self.subSeqLengthList)))
        return totalLength / len(self.database)

    def getMaximumSubsequenceLength(self) -> int:
        """
        get the maximum subsequence length
        :return: maximum subsequence length
        :rtype: int
        """
        return max(list(map(max,self.subSeqLengthList)))

    def getStandardDeviationSubsequenceLength(self) -> float:
        """
        get the standard deviation subsequence length
        :return: standard deviation subsequence length
        :rtype: float
        """
        allList=[]
        for i in self.subSeqLengthList:
            allList=allList+i
        return statistics.pstdev(allList)

    def getVarianceSubsequenceLength(self) -> float:
        """
        get the variance subSequence length
        :return: variance subSequence length
        :rtype: float
        """
        allList = []
        for i in self.subSeqLengthList:
            allList = allList + i
        return statistics.variance(allList)

    def getSortedListOfItemFrequencies(self) -> Dict[str, int]:
        """
        get sorted list of item frequencies
        :return: item frequencies
        :rtype: dict
        """
        itemFrequencies = {}
        for seq in self.database:
            for sub in self.database[seq]:
                for item in sub:
                    itemFrequencies[item] = itemFrequencies.get(item, 0)
                    itemFrequencies[item] += 1
        return {k: v for k, v in sorted(itemFrequencies.items(), key=lambda x: x[1], reverse=True)}

    def getFrequenciesInRange(self) -> Dict[int, int]:
        """
        get sorted list of item frequencies in some range
        :return: item separated by its frequencies
        :rtype: dict
        """
        fre = self.getSortedListOfItemFrequencies()
        rangeFrequencies = {}
        maximum = max([i for i in fre.values()])
        values = [int(i * maximum / 6) for i in range(1, 6)]
        va = len({key: val for key, val in fre.items() if 0 < val < values[0]})
        rangeFrequencies[values[0]] = va
        for i in range(1, len(values)):
            va = len({key: val for key, val in fre.items() if values[i] > val > values[i - 1]})
            rangeFrequencies[values[i]] = va
        return rangeFrequencies

    def getSequencialLengthDistribution(self) -> Dict[int, int]:
        """
        get Sequence length Distribution
        :return: Sequence length
        :rtype: dict
        """
        transactionLength = {}
        for length in self.seqLengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def getSubsequencialLengthDistribution(self) -> Dict[int, int]:
        """
        get subSequence length distribution
        :return: subSequence length
        :rtype: dict
        """
        transactionLength = {}
        for sublen in self.subSeqLengthList:
            for length in sublen:
                transactionLength[length] = transactionLength.get(length, 0)
                transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def run(self) -> None:
        self.readDatabase()

    def printStats(self) -> None:
        """
        To print the all status of sequence database
        """
        print(f'Database size (total no of sequence) : {self.getDatabaseSize()}')
        print(f'Number of items : {self.getTotalNumberOfItems()}')
        print(f'Minimum Sequence Size : {self.getMinimumSequenceLength()}')
        print(f'Average Sequence Size : {self.getAverageSubsequencePerSequenceLength()}')
        print(f'Maximum Sequence Size : {self.getMaximumSequenceLength()}')
        print(f'Standard Deviation Sequence Size : {self.getStandardDeviationSequenceLength()}')
        print(f'Variance in Sequence Sizes : {self.getVarianceSequenceLength()}')
        print(f'Sequence size (total no of subsequence) : {self.getSequenceSize()}')
        print(f'Minimum subSequence Size : {self.getMinimumSubsequenceLength()}')
        print(f'Average subSequence Size : {self.getAverageItemPerSubsequenceLength()}')
        print(f'Maximum subSequence Size : {self.getMaximumSubsequenceLength()}')
        print(f'Standard Deviation Sequence Size : {self.getStandardDeviationSubsequenceLength()}')
        print(f'Variance in Sequence Sizes : {self.getVarianceSubsequenceLength()}')

    def plotGraphs(self) -> None:
        """
        To plot the  distribution about items, subsequences in sequence and items in subsequence
        """
        itemFrequencies = self.getFrequenciesInRange()
        seqLen = self.getSequencialLengthDistribution()
        subLen=self.getSubsequencialLengthDistribution()
        plt.plotLineGraphFromDictionary(itemFrequencies, 100, 'Frequency', 'No of items', 'frequency')
        plt.plotLineGraphFromDictionary(seqLen, 100, 'sequence length', 'sequence length', 'frequency')
        plt.plotLineGraphFromDictionary(subLen, 100, 'subsequence length', 'subsequence length', 'frequency')

if __name__ == '__main__':
    _ap=str()
    if len(sys.argv)==3 or len(sys.argv)==2:
        if len(sys.argv)==3:
            _ap=sequentialDatabase(sys.argv[1],sys.argv[2])
        if len(sys.argv) == 2:
            _ap = sequentialDatabase(sys.argv[1])
        _ap.run()
        _ap.printStats()
        _ap.plotGraphs()
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
