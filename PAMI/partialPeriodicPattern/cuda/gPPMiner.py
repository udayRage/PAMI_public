import os
import csv
import time
import psutil
import numpy as np
from deprecated import deprecated
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

supportAndPeriod = SourceModule(r"""
    
#define uint64_t unsigned long long int

__global__ void supportAndPeriod(uint64_t *bitArray, // containing transactions
                                uint64_t *period, // for period
                                uint64_t *thingsToCompare, // for things to compare
                                uint64_t *thingsToCompareIndex, // for things to compare index
                                uint64_t numberOfThingsToCompare, // for number of things to compare
                                uint64_t numberOfBits, // for number of bits
                                uint64_t numberOfElements, // for number of elements
                                uint64_t maxPeriod, // for max period
                                uint64_t maxTimeStamp){
        
        uint64_t threadIDX = blockIdx.x * blockDim.x + threadIdx.x;

        if (threadIDX > numberOfThingsToCompare-2) return;

        uint64_t holder = 0;
        uint64_t periodCounter = 0;
        uint64_t numbersCounter = 0;
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
                if (bitRepresentation[j] == 1){
                    if (periodCounter <= maxPeriod) period[threadIDX]++;
                    periodCounter = 0;
                }
                if (numbersCounter == maxTimeStamp){
                    return;
                }
            }

        }
        return;

    }

"""
                                )


class gPPMiner:

    supportAndPeriod = supportAndPeriod.get_function("supportAndPeriod")

    def __init__(self, filePath, periodicSupport, maxPeriod, sep="\t"):
        self.filePath = filePath
        self.sep = sep
        self.periodicSupport = periodicSupport
        self.Patterns = {}
        self.period = maxPeriod
        self.__time = 0
        self.__memRSS = 0
        self.__memUSS = 0
        self.__GPU_MEM = 0
        self.__baseGPUMem = 0

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

        if self.periodicSupport < 0:
            self.periodicSupport = self.maxTimeStamp * self.periodicSupport

        basePattern = dict(
            sorted(basePattern.items(), key=lambda x: len(x[1])))

        return basePattern

    def __getPeriodicSupport(self, array):
        """
        Get the maximum period of the array

        :param array (list): list of the array
        :return: int: maximum period
        """

        # sort the array
        array = sorted(array)

        periodicSupport = 0

        for i in range(1,len(array)):
            if array[i] - array[i-1] <= self.period:
                periodicSupport += 1
            if periodicSupport > self.periodicSupport:
                return periodicSupport
               
        return periodicSupport

    def __generateBitArray(self, fileData):
        """
        Convert the dictionary into a bit array with valid candidates and return it with
        index which can be used to locate the candidates when multiplied with self.lengthOfArray

        :param: fileData (dict): dictionary of the data
        :return: list: bit array
        :return: list: index of the bit array

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
            if self.__getPeriodicSupport(value) >= self.periodicSupport:
                index2id.append(key)
                bits = np.zeros(self.bitsToGen, dtype=np.uint64)
                for item in value:
                    number = np.bitwise_or(np.uint64(0), np.left_shift(np.uint64(1), np.uint64(63 - (item - 1) % 64)))
                    bits[((item - 1) // self.numberOfBits)] = np.bitwise_or(bits[((item - 1) // self.numberOfBits)], number)
                self.lengthOfArray = len(bits)
                bitValues.append(bits)
                index += 1
                self.Patterns[tuple([key])] = self.__getPeriodicSupport(value)
        bitValues = np.array(bitValues, dtype=np.uint64)
        gpuBitArray = cuda.mem_alloc(bitValues.nbytes)
        self.bvnb = bitValues.nbytes
        cuda.memcpy_htod(gpuBitArray, bitValues)
        return gpuBitArray, index2id

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Start the mining process
        """
        self.mine()

    # def __eclat(self, bitValues, keys, index2id):
    #     """
    #     Recursive Eclat
    #
    #     Args:
    #     :param bitValues (list): bit array
    #     :param keys (list): list of keys
    #     :param index2id (list): list of index to id
    #     """
    #     print("Number of Keys: " + str(len(keys)))
    #     locations = [0]
    #     newKeys = []
    #     for i in range(len(keys)):
    #         for j in range(i+1, len(keys)):
    #             if keys[i][:-1] == keys[j][:-1] and keys[i][-1] != keys[j][-1]:
    #                 newCan = keys[i] + [keys[j][-1]]
    #                 newKeys.append(newCan)
    #                 locations.append(locations[-1]+len(newKeys[-1]))
    #             else:
    #                 break
    #
    #     if len(locations) > 1:
    #         locations = np.array(locations, dtype=np.uint64)
    #         newKeys = np.array(newKeys, dtype=np.uint64)
    #         newKeys = newKeys.flatten()
    #         period = np.zeros(len(newKeys), dtype=np.uint64)
    #
    #         totalMemory = period.nbytes + \
    #             newKeys.nbytes + locations.nbytes + self.bvnb
    #         if totalMemory > self.__GPU_MEM:
    #             self.__GPU_MEM = totalMemory - self.__baseGPUMem
    #
    #         gpuPeriod = cuda.mem_alloc(period.nbytes)
    #         gpuNewKeys = cuda.mem_alloc(newKeys.nbytes)
    #         gpuLocations = cuda.mem_alloc(locations.nbytes)
    #         cuda.memcpy_htod(gpuPeriod, period)
    #         cuda.memcpy_htod(gpuNewKeys, newKeys)
    #         cuda.memcpy_htod(gpuLocations, locations)
    #
    #         # print("GPU Launching")
    #         self.supportAndPeriod(bitValues, gpuPeriod,
    #                               gpuNewKeys, gpuLocations, np.uint64(
    #                                   len(locations)),
    #                               np.uint64(self.numberOfBits), np.uint64(
    #                                   self.lengthOfArray),
    #                               np.uint64(self.period), np.uint64(
    #                                   self.maxTimeStamp),
    #                               block=(32, 1, 1), grid=(len(locations)//32+1, 1, 1))
    #
    #         cuda.memcpy_dtoh(period, gpuPeriod)
    #         # print("GPU Finished")
    #
    #         # free
    #         gpuPeriod.free()
    #         gpuNewKeys.free()
    #         gpuLocations.free()
    #
    #         keys = newKeys
    #         newKeys = []
    #         for i in range(len(locations)-1):
    #             # print(support[i], period[i])
    #             # print("i: " + str(i), end="\r")
    #             if period[i] > self.periodicSupport:
    #                 key = keys[locations[i]:locations[i+1]]
    #                 nkey = sorted([index2id[key[i]] for i in range(len(key))])
    #                 if tuple(nkey) not in self.Patterns:
    #                     self.Patterns[tuple(nkey)] = period[i]
    #                     newKeys.append(list(key))
    #         # print()
    #
    #         keys = newKeys
    #         if len(keys) > 1:
    #             self.__eclat(bitValues, keys, index2id)

    def mine(self):
        """
        Start the mining process
        """
        startTime = time.time()
        data = self.__readFile()
        bitValues, index2id = self.__generateBitArray(data)
        keys = []

        for i in range(len(index2id)):
            keys.append([i])

        if len(keys) > 1:
            self.__eclat(bitValues, keys, index2id)

        print(
            "Periodic-Frequent patterns were generated successfully using gPPMiner"
        )
        self.__time = time.time() - startTime
        self.__memRSS = psutil.Process(os.getpid()).memory_info().rss
        self.__memUSS = psutil.Process(os.getpid()).memory_full_info().uss

    def __eclat(self, bitValues, keys, index2id):
        """
        Recursive Eclat

        Args:
        :param bitValues (list): bit array
        :param keys (list): list of keys
        :param index2id (list): list of index to id
        """
        print("Number of Keys: " + str(len(keys)))
        locations = [0]
        newKeys = []
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                if keys[i][:-1] == keys[j][:-1] and keys[i][-1] != keys[j][-1]:
                    newCan = keys[i] + [keys[j][-1]]
                    newKeys.append(newCan)
                    locations.append(locations[-1]+len(newKeys[-1]))
                else:
                    break

        if len(locations) > 1:
            locations = np.array(locations, dtype=np.uint64)
            newKeys = np.array(newKeys, dtype=np.uint64)
            newKeys = newKeys.flatten()
            period = np.zeros(len(newKeys), dtype=np.uint64)

            totalMemory = period.nbytes + \
                newKeys.nbytes + locations.nbytes + self.bvnb
            if totalMemory > self.__GPU_MEM:
                self.__GPU_MEM = totalMemory - self.__baseGPUMem

            gpuPeriod = cuda.mem_alloc(period.nbytes)
            gpuNewKeys = cuda.mem_alloc(newKeys.nbytes)
            gpuLocations = cuda.mem_alloc(locations.nbytes)
            cuda.memcpy_htod(gpuPeriod, period)
            cuda.memcpy_htod(gpuNewKeys, newKeys)
            cuda.memcpy_htod(gpuLocations, locations)

            # print("GPU Launching")
            self.supportAndPeriod(bitValues, gpuPeriod,
                                  gpuNewKeys, gpuLocations, np.uint64(
                                      len(locations)),
                                  np.uint64(self.numberOfBits), np.uint64(
                                      self.lengthOfArray),
                                  np.uint64(self.period), np.uint64(
                                      self.maxTimeStamp),
                                  block=(32, 1, 1), grid=(len(locations)//32+1, 1, 1))

            cuda.memcpy_dtoh(period, gpuPeriod)
            # print("GPU Finished")

            # free
            gpuPeriod.free()
            gpuNewKeys.free()
            gpuLocations.free()

            keys = newKeys
            newKeys = []
            for i in range(len(locations)-1):
                # print(support[i], period[i])
                # print("i: " + str(i), end="\r")
                if period[i] > self.periodicSupport:
                    key = keys[locations[i]:locations[i+1]]
                    nkey = sorted([index2id[key[i]] for i in range(len(key))])
                    if tuple(nkey) not in self.Patterns:
                        self.Patterns[tuple(nkey)] = period[i]
                        newKeys.append(list(key))
            # print()

            keys = newKeys
            if len(keys) > 1:
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


if __name__ == "__main__":
    filePath = "temporal_pumsb.csv"
    sep = "\t"
    periodicSupport = 45000
    period = 10
    obj = gPPMiner(filePath, periodicSupport, period, sep)
    obj.mine()
    print("Time: ", obj.getRuntime())
    print("Patterns: ", len(obj.getPatterns()))
    print("GPU MEM: ", obj.getGPUMemory())
    print("Mem RSS: ", obj.getMemoryRSS())
    print("Mem USS: ", obj.getMemoryUSS())
