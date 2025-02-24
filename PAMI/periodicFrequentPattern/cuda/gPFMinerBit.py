
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from cudaAlgorithms import gPFMinerBit
#
#             obj = gPFMinerBit.gPFMinerBit("data.txt", 2, 3)
#
#             obj.run()
#
#             print(obj.getPatterns())
#
#             print(obj.getRuntime())
#
#             print(obj.getMemoryRSS())
#
#             print(obj.getMemoryUSS())
#
#             print(obj.getGPUMemory())
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
import sys
import csv
import time
import psutil
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

from PAMI.periodicFrequentPattern.basic import abstract as _ab
import pandas as pd
from deprecated import deprecated


supportAndPeriod = SourceModule(r"""

__global__ void supportAndPeriod(unsigned long long int *bitArray, // containing transactions
                                unsigned long long int *support, // for support
                                unsigned long long int *period, // for period
                                unsigned long long int *thingsToCompare, // for things to compare
                                unsigned long long int *thingsToCompareIndex, // for things to compare index
                                unsigned long long int numberOfThingsToCompare, // for number of things to compare
                                unsigned long long int numberOfBits, // for number of bits
                                unsigned long long int numberOfElements, // for number of elements
                                unsigned long long int maxPeriod, // for max period
                                unsigned long long int maxTimeStamp){

        unsigned long long int threadIDX = blockIdx.x * blockDim.x + threadIdx.x;

        if (threadIDX > numberOfThingsToCompare-2) return;

        unsigned long long int holder = 0;
        unsigned long long int supportCounter = 0;
        unsigned long long int periodCounter = 0;
        unsigned long long int numbersCounter = 0;
        short int bitRepresentation[64];
        short int index = numberOfBits - 1;

        for(int i = 0; i < numberOfElements; i++){
            // intersection
            holder = bitArray[thingsToCompare[thingsToCompareIndex[threadIDX]] * numberOfElements + i];
            for (int j = thingsToCompareIndex[threadIDX]+1; j < thingsToCompareIndex[threadIDX + 1]; j++){
                holder = holder & bitArray[thingsToCompare[j] * numberOfElements + i];
            }

            // empty bitRepresentation
            for (int j = 0; j < 64; j++){
                bitRepresentation[j] = 0;
            }

            // conversion to bit representation
            index = numberOfBits - 1;
            while (holder > 0){
                bitRepresentation[index] = holder % 2;
                holder = holder / 2;
                index--;
            }

            // counting period
            for (int j = 0; j < numberOfBits; j++){
                periodCounter++;
                numbersCounter++;
                if (periodCounter > maxPeriod){
                    period[threadIDX] = periodCounter;
                    support[threadIDX] = supportCounter;
                    return;
                }
                if (bitRepresentation[j] == 1){
                    supportCounter++;
                    if (periodCounter > period[threadIDX]) period[threadIDX] = periodCounter;
                    periodCounter = 0;
                }
                if (numbersCounter == maxTimeStamp){
                    support[threadIDX] = supportCounter;
                    period[threadIDX] = periodCounter;
                    return;
                }
            }

        }
        support[threadIDX] = supportCounter;
        period[threadIDX] = periodCounter;
        return;

    }

"""
                                )


class gPFMinerBit:

    """
    :Description:   ECLAT is one of the fundamental algorithm to discover frequent patterns in a transactional database.
                    This algorithm applies ECLAT as well as calculates periodicity to find patterns in a temporal database.
                    This program employs downward closure property to  reduce the search space effectively.
                    This algorithm employs depth-first search technique to find the complete set of frequent patterns in a
                    temporal database.

    :Reference:   Penugonda Ravikumar 1,2,† , Palla Likhitha 2,† , Bathala Venus Vikranth Raj 2,† , Rage Uday Kiran 1,3,* ,† , Yutaka Watanobe 1 and Koji Zettsu 3. "Efficient Discovery of Periodic-Frequent Patterns in Columnar Temporal Databases.https://www.mdpi.com/2079-9292/10/12/1478

    :param  iFile: str :
                   Name of the Input file to mine complete set of periodic frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of periodic frequent pattern's
    :param  minSup: str:
                   Controls the minimum number of transactions in which every item must appear in a database.
    :param  maxPer: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        filePath : str
             path of the file

        minSup : int
             minimum support

        maxPeriod : (int)
             maximum period

        sep : str, optional
         separator

        Patterns : dict, optional
            dictionary of the patterns. Defaults to {}.

        maxTimeStamp : int, optional
           maximum timestamp. Defaults to 0.

        __time : int, optional
           time taken to execute the algorithm. Defaults to 0.

        __memRSS : int, optional
           memory used by the program. Defaults to 0.

        __memUSS : int, optional
           memory used by the program. Defaults to 0.

        __GPU_MEM : int, optional
           GPU memory used by the program. Defaults to 0.

        __baseGPUMem : int, optional
           base GPU memory used by the program. Defaults to 0.


    **Importing this algorithm into a python program**
    ------------------------------------------------------------
    .. code-block:: python

         from cudaAlgorithms import gPFMinerBit

         obj = gPFMinerBit.gPFMinerBit("data.txt", 2, 3)

         obj.run()

         print(obj.getPatterns())

         print(obj.getRuntime())

         print(obj.getMemoryRSS())

         print(obj.getMemoryUSS())

         print(obj.getGPUMemory())

    **Running from the command line:**
    ---------------------------------------
   .. code-block:: console


       Format:

       (.venv) $ python3 gPFMinerBit.py data.txt 2 3 output.txt


               .. note:: minSup will be considered in percentage of database transactions

    **Credits:**
    ---------------
        This program is created by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.
        
    """

    # supportAndPeriod = supportAndPeriod.get_function("supportAndPeriod")

    def __init__(self, filePath, minSup, maxPeriod, sep="\t"):
        self.filePath = filePath
        self.sep = sep
        self.minSup = minSup
        self.Patterns = {}
        self.maxPeriod = maxPeriod
        self.__time = 0
        self.__memRSS = 0
        self.__memUSS = 0
        self.__GPU_MEM = 0
        self.__baseGPUMem = 0
        """
         :Methods:
        
        __readFile(): Read the file and return the data in a dictionary

        __getMaxPeriod(): Get the maximum period of the patterns

        __generateBitArray(): Generate the bit array

        getRuntime(): Get the runtime of the algorithm

        getMemoryRSS(): Get the memory used by the program

        getMemoryUSS(): Get the memory used by the program

        getGPUMemory(): Get the GPU memory used by the program

        getPatterns(): Get the patterns"""

    def __readFile(self):
        """
        Read the file and return the data in a dictionary

        :return: dict: dictionary of the data
        """
        basePattern = {}
        with open(self.filePath, "r") as f:
            reader = csv.reader(f, delimiter=self.sep)
            for row in reader:
                line = [str(item) for item in row if item != ""]
                self.maxTimeStamp = int(line[0])
                line = line[1:]
                for item in line:
                    if item not in basePattern:
                        basePattern[item] = [self.maxTimeStamp]
                    else:
                        basePattern[item].append(self.maxTimeStamp)

        basePattern = dict(
            sorted(basePattern.items(), key=lambda x: len(x[1]), reverse=True))

        return basePattern

    def __getMaxPeriod(self, array):
        """
        Get the maximum period of the array

        :param array (list): list of the array
        :return: int: maximum period
        """

        cur = 0
        per = 0
        # sort the array
        array = sorted(array)
        array.append(self.maxTimeStamp)

        for tid in array:
            per = max(per, tid - cur)
            if per > self.maxPeriod:
                break
            cur = tid
        return per

    def __generateBitArray(self, fileData):
        """
        Convert the dictionary into a bit array with valid candidates and return it with
        index which can be used to locate the candidates when multiplied with self.lengthOfArray

        :param fileData (dict): dictionary of the data

        :return:
            list: bit array
            list: index of the bit array
        """
        self.bitsToGen = 0
        self.numberOfBits = 64
        if self.maxTimeStamp % self.numberOfBits == 0:
            self.bitsToGen = self.maxTimeStamp // self.numberOfBits
        else:
            self.bitsToGen = self.maxTimeStamp // self.numberOfBits + 1
        index = 0
        index2id = []
        bitValues = []
        for key, value in fileData.items():
            if len(value) >= self.minSup and self.__getMaxPeriod(value) <= self.maxPeriod:
                index2id.append(key)
                bits = [0] * self.bitsToGen * self.numberOfBits
                for item in value:
                    bits[item - 1] = 1
                bitVal = []
                prev = 0
                current = self.numberOfBits
                while current <= self.bitsToGen * self.numberOfBits:
                    # get bit array from prev to current
                    bit = bits[prev:current]
                    prev = current
                    current += self.numberOfBits
                    # convert the bit array to integer
                    bitVal.append(int("".join(str(x) for x in bit), 2))
                self.lengthOfArray = len(bitVal)
                bitValues.append(bitVal)
                index += 1
                self.Patterns[tuple([key])] = [len(
                    value), self.__getMaxPeriod(value)]
        # print(bitValues[0][0:10])
        bitValues = np.array(bitValues, dtype=np.uint64)
        # print(bitValues[0:10])
        gpuBitArray = cuda.mem_alloc(bitValues.nbytes)
        self.bvnb = bitValues.nbytes
        cuda.memcpy_htod(gpuBitArray, bitValues)
        return gpuBitArray, index2id

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Start the mining process
        """
        startTime = time.time()
        data = self.__readFile()
        bitValues, index2id = self.__generateBitArray(data)

        keys = [[i] for i in range(len(index2id))]

        if len(keys) > 1:
            self.__eclat(bitValues, keys, index2id)

        print(
            "Periodic-Frequent patterns were generated successfully using gPFMinerBit"
        )
        self.__time = time.time() - startTime
        self.__memRSS = psutil.Process(os.getpid()).memory_info().rss
        self.__memUSS = psutil.Process(os.getpid()).memory_full_info().uss

    def Mine(self):
        """
        Start the mining process
        """
        startTime = time.time()
        data = self.__readFile()
        bitValues, index2id = self.__generateBitArray(data)

        keys = [[i] for i in range(len(index2id))]

        if len(keys) > 1:
            self.__eclat(bitValues, keys, index2id)

        print(
            "Periodic-Frequent patterns were generated successfully using gPFMinerBit"
        )
        self.__time = time.time() - startTime
        self.__memRSS = psutil.Process(os.getpid()).memory_info().rss
        self.__memUSS = psutil.Process(os.getpid()).memory_full_info().uss

    def __eclat(self, bitValues, keys, index2id):
        """
        Recursive Eclat

        :param bitValues (list): bit array
        :param keys (list): list of keys
        :param index2id (list): list of index to id
        """
        print("Number of Keys: " + str(len(keys)))
        locations = [0]
        newKeys = []
        for i in range(len(keys)):
            # print("Key: " + str(i))
            # iKey = keys[i]
            for j in range(i+1, len(keys)):
                # jKey = keys[j]
                if keys[i][:-1] == keys[j][:-1] and keys[i][-1] != keys[j][-1]:
                    newCan = keys[i] + [keys[j][-1]]
                    newKeys.append(newCan)
                    locations.append(locations[-1]+len(newKeys[-1]))
                else:
                    break

        locations = np.array(locations, dtype=np.uint64)
        newKeys = np.array(newKeys, dtype=np.uint64)
        newKeys = newKeys.flatten()
        support = np.zeros(len(newKeys), dtype=np.uint64)
        period = np.zeros(len(newKeys), dtype=np.uint64)

        if len(locations) > 1:
            totalMemory = support.nbytes + period.nbytes + \
                newKeys.nbytes + locations.nbytes + self.bvnb
            if totalMemory > self.__GPU_MEM:
                self.__GPU_MEM = totalMemory - self.__baseGPUMem

            gpuSupport = cuda.mem_alloc(support.nbytes)
            gpuPeriod = cuda.mem_alloc(period.nbytes)
            gpuNewKeys = cuda.mem_alloc(newKeys.nbytes)
            gpuLocations = cuda.mem_alloc(locations.nbytes)

            cuda.memcpy_htod(gpuSupport, support)
            cuda.memcpy_htod(gpuPeriod, period)
            cuda.memcpy_htod(gpuNewKeys, newKeys)
            cuda.memcpy_htod(gpuLocations, locations)

            # print("Number of New Keys: " + str(len(newKeys)))

            self.supportAndPeriod(bitValues, gpuSupport, gpuPeriod,
                                  gpuNewKeys, gpuLocations, np.uint64(
                                      len(locations)),
                                  np.uint64(self.numberOfBits), np.uint64(
                                      self.lengthOfArray),
                                  np.uint64(self.maxPeriod), np.uint64(
                                      self.maxTimeStamp),
                                  block=(32, 1, 1), grid=(len(locations)//32+1, 1, 1))

            cuda.memcpy_dtoh(support, gpuSupport)
            cuda.memcpy_dtoh(period, gpuPeriod)

            # free
            gpuSupport.free()
            gpuPeriod.free()
            gpuNewKeys.free()
            gpuLocations.free()

            keys = newKeys
            newKeys = []

            counter = 0
            top = 5
            for i in range(len(locations)-1):
                # print(support[i], period[i])
                # if i == 0:
                #     key = keys[locations[i]:locations[i+1]]
                #     nkey = sorted([index2id[key[i]] for i in range(len(key))])
                #     print(key, nkey, support[i], period[i])
                if support[i] >= self.minSup and period[i] <= self.maxPeriod:
                    key = keys[locations[i]:locations[i+1]]
                    
                    nkey = list([index2id[key[i]] for i in range(len(key))])
                    if tuple(nkey) not in self.Patterns:
                        self.Patterns[tuple(nkey)] = [support[i], period[i]]
                        newKeys.append(list(key))
                        # if counter < top:
                        #     print(nkey, support[i], period[i])
                        #     counter += 1


            keys = newKeys
            if len(keys) > 0:
                self.__eclat(bitValues, keys, index2id)

    def getRuntime(self):
        return self.__time

    def getMemoryRSS(self):
        return self.__memRSS

    def getMemoryUSS(self):
        return self.__memUSS

    def getGPUMemory(self):
        return self.__GPU_MEM

    def getPatterns(self):
        return self.Patterns
    
    def savePatterns(self, fileName):
        with open(fileName, "w") as f:
            for key in self.Patterns:
                f.write(str(key) + "\t" + str(self.Patterns[key][0]) + "\t" + str(self.Patterns[key][1]) + "\n")


if __name__ == "__main__":
    # filePath = "temporal_T10I4D100K.csv"
    # sep = "\t"
    # support = 50
    # maxPeriod = 25000
    # obj = gPFMinerBit(filePath, support, maxPeriod, sep)
    # obj.mine()
    # print("Time: ", obj.getRuntime())
    # print("Patterns: ", len(obj.getPatterns()))
    # print("GPU MEM: ", obj.getGPUMemory())
    # print("Mem RSS: ", obj.getMemoryRSS())
    # print("Mem USS: ", obj.getMemoryUSS())
    if len(sys.argv) != 6:
        print("Usage: python3 gPFMinerBit.py <input file> <min support> <max period> <separator> <output file>")
        sys.exit(1)
    filePath = sys.argv[1]
    support = int(sys.argv[2])
    maxPeriod = int(sys.argv[3])
    sep = sys.argv[4]
    output = sys.argv[5]
    obj = gPFMinerBit(filePath, support, maxPeriod, sep)
    obj.mine()
    obj.savePatterns(output)
    print("Time: ", obj.getRuntime())
    print("Patterns: ", len(obj.getPatterns()))
    print("GPU MEM: ", obj.getGPUMemory())
    print("Mem RSS: ", obj.getMemoryRSS())
    print("Mem USS: ", obj.getMemoryUSS())

