
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

import abstract as _ab
import cupy as cp
import cudf
from deprecated import deprecated

class gdscuGPPMiner(_ab._partialPeriodicPatterns):
    """
    :Description:  gPPMiner is the fundamental approach to mine the periodic-frequent patterns using GPU.

    :Reference:  N/A

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        minSup: int or float or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        maxPer: int or float or str
            The user can specify maxPer either in count or proportion of database size.
            If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
            Otherwise, it will be treated as float.
            Example: maxPer=10 will be treated as integer, while maxPer=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        Database : list
            To store the transactions of a database in list

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of periodic-frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of periodic-frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function



    **Methods to execute code on terminal**
    ------------------------------------------
            Format:
                        >>>  python3 gPPMiner.py <inputFile> <outputFile> <minSup>
            Example:
                        >>>   python3 gPPMiner.py sampleDB.txt patterns.txt 10.0

            .. note:: minSup will be considered in percentage of database transactions


    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

                from PAMI.periodicFrequentPattern.basic import gPPMiner as alg

                obj = alg.gPPMiner("../basic/sampleTDB.txt", "2", "5")

                obj.mine()

                periodicFrequentPatterns = obj.getPatterns()

                print("Total number of Periodic Frequent Patterns:", len(periodicFrequentPatterns))

                obj.savePatterns("patterns")

                Df = obj.getPatternsAsDataFrame()

                memUSS = obj.getMemoryUSS()

                print("Total Memory in USS:", memUSS)

                memRSS = obj.getMemoryRSS()

                print("Total Memory in RSS", memRSS)

                run = obj.getRuntime()

                print("Total ExecutionTime in seconds:", run)

    **Credits:**
    --------------
                The complete program was written by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.


    """

    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _mapSupport = {}
    _itemsetCount = 0
    _writer = None
    _periodicSupport = str()
    _period = str()


    supportAndPeriod = _ab._cp.RawKernel('''

    #define uint32_t unsigned int

    extern "C" __global__
    void supportAndPeriod(
        uint32_t *bitValues, uint32_t arraySize,
        uint32_t *candidates, uint32_t numberOfKeys, uint32_t keySize,
        uint32_t *period,
        uint32_t maxPeriod, uint32_t maxTimeStamp
        )
    {
        uint32_t tid = threadIdx.x + blockIdx.x * blockDim.x;
        if (tid >= numberOfKeys) return;

        uint32_t intersection = 0;

        uint32_t periodCount = 0;
        uint32_t traversed = 0;

        uint32_t bitRepr[32];
        uint32_t bitRepIndex = 31;

        int flag = 0;


        for (uint32_t i = 0; i < arraySize; i++)
        {
            intersection = 0xFFFFFFFF;
            for (uint32_t j = tid * keySize; j < (tid + 1) * keySize; j++)
            {
                intersection = intersection & bitValues[candidates[j] * arraySize + i];
            }

            // reset bitRepr
            for (uint32_t j = 0; j < 32; j++)
            {
                bitRepr[j] = 0;
            }

            // convert intersection to bitRepr
            bitRepIndex = 31;
            while (intersection > 0)
            {
                bitRepr[bitRepIndex] = intersection % 2;
                intersection = intersection / 2;
                bitRepIndex--;
            }

            for (uint32_t j = 0; j < 32; j++)
            {
                periodCount++;
                traversed++;
                if (bitRepr[j] == 1)
                {
                    if (flag == 0) {
                      flag++;
                    }
                    else{
                      if (periodCount <= maxPeriod) 
                      {
                        period[tid]++;
                      }
                    }
                    periodCount = 0;

                }
                if (traversed == maxTimeStamp + 1)
                {
                    return;
                }
            }
        }

    }

    ''', 'supportAndPeriod')

    def _convert(self, value):
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbSize * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbSize * value)
            else:
                value = int(value)
        return value

    def _creatingOneItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        df = cudf.read_parquet(self._iFile)

        data = df.to_cupy()
        data = cp.ravel(data)

        keys = cp.array([x for x in range(len(df.index))], dtype = cp.uint32)
        numberOfKeys = len(keys)
        period = cp.zeros(numberOfKeys, dtype = cp.uint32)
        arrSize = len(df.columns)
        self._maxTS = arrSize  * 32
        maxTS = self._maxTS

        self.arraySize = arrSize


        self.supportAndPeriod((numberOfKeys//32 + 1,), (32,),
                                    (
                                        data, arrSize,
                                        keys, numberOfKeys, 1,
                                        period,
                                        self._period, maxTS
                                    )
        )
        period = period.get()
        keys = keys.get()

        newKeys = []

        for i in range(len(keys)):
            if period[i] >= self._periodicSupport:
                newKeys.append(keys[i])
                self._finalPatterns[str(keys[i])] = period[i]

        # candidates = newKeys
        candidates = [list([x]) for x in newKeys]
    
        return candidates, data

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):

        self.mine()

    def mine(self):
        self._startTime = _ab._time.time()

        self._period = self._convert(self._period)
        self._periodicSupport = self._convert(self._periodicSupport)
        self._finalPatterns = {}
        candidates, values = self._creatingOneItemSets()
        # candidates = list(ArraysAndItems.keys())
        # candidates = [list(i) for i in candidates]
        # values = list(ArraysAndItems.values())

        # values = _ab._cp.array(values)
        # print(values)

        # print(type(candidates[0]))

        while len(candidates) > 0:
            # print("Number of Candidates:", len(candidates))
            newKeys = []
            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    if candidates[i][:-1] == candidates[j][:-1] and candidates[i][-1] != candidates[j][-1]:
                        newKeys.append(candidates[i] + candidates[j][-1:])
                    else:
                        break

            if len(newKeys) == 0:
                break

            # print(newKeys)

            numberOfKeys = len(newKeys)
            keySize = len(newKeys[0])

            newKeys = _ab._cp.array(newKeys, dtype=_ab._cp.uint32)

            # newKeys = _ab._cp.flatten(newKeys)
            newKeys = _ab._cp.reshape(newKeys, (numberOfKeys * keySize,))

            period = _ab._cp.zeros(numberOfKeys, dtype=_ab._cp.uint32)

            self.supportAndPeriod((numberOfKeys // 32 + 1,), (32,),
                                  (
                                      values, self.arraySize,
                                      newKeys, numberOfKeys, keySize,
                                      period,
                                      self._period, self._maxTS
                                  )
                                  )

            newKeys = _ab._cp.reshape(newKeys, (numberOfKeys, keySize))
            newKeys = _ab._cp.asnumpy(newKeys)
            period = period.get()

            newCandidates = []
            for i in range(len(newKeys)):
                # print(newKeys[i], support[i], period[i])
                if period[i] >= self._periodicSupport:
                    newCandidates.append(list(newKeys[i]))
                    rename = [str(j) for j in newKeys[i]]
                    rename = "\t".join(rename)
                    self._finalPatterns[rename] = period[i]

            # print()

            # print(newCandidates)

            candidates = newCandidates

        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Periodic-Frequent patterns were generated successfully using gPPMiner algorithm ")


    def getMemoryUSS(self):
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

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
        """
        Storing final periodic-frequent patterns in a dataframe

        :return: returning periodic-frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b[0], b[1]])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
        return dataframe

    def save(self, outFile):
        """
        Complete set of periodic-frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            # print(x,y)
            # print(type(x), type(y))
            s1 = x.replace(' ', '\t') + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of periodic-frequent patterns after completion of the mining process

        :return: returning periodic-frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        print("Total number of Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in s:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = gdscuGPPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = gdscuGPPMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        print("Total number of Periodic-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in s:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
