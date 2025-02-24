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

from abc import ABC

# import abstract as _ab

from PAMI.partialPeriodicFrequentPattern.basic.abstract import *
import cupy as cp
import numpy as np
import pandas as pd
from deprecated import deprecated

class cuGPPMiner(partialPeriodicPatterns, ABC):
  __path = ' '
  _partialPeriodicPatterns__iFile = ' '
  _partialPeriodicPatterns__oFile = ' '
  _partialPeriodicPatterns__sep = str()
  _partialPeriodicPatterns__minSup = str()
  _partialPeriodicPatterns__maxPer = str()
  _partialPeriodicPatterns__minPR = str()
  __tidlist = {}
  __last = 0
  __lno = 0
  __mapSupport = {}
  _partialPeriodicPatterns__finalPatterns = {}
  __runTime = float()
  _partialPeriodicPatterns__memoryUSS = float()
  _partialPeriodicPatterns__memoryRSS = float()
  _partialPeriodicPatterns__startTime = float()
  _partialPeriodicPatterns__endTime = float()
  __Database = []
  _memoryRSS = float()
  _memoryUSS = float()

  supportAndPeriod = cp.RawKernel('''

    #define uint32_t unsigned int

    extern "C" __global__
    void supportAndPeriod(
        uint32_t *bitValues, uint32_t arraySize,
        uint32_t *candidates, uint32_t numberOfKeys, uint32_t keySize,
        uint32_t *period, uint32_t *support,
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
                  support[tid]++;

                  if (periodCount <= maxPeriod)
                  {
                    period[tid]++;
                  }

                  periodCount = 0;

                }
                if (traversed == maxTimeStamp + 1)
                {
                    if (periodCount <= maxPeriod)
                    {
                      period[tid]++;
                    }
                    return;
                }
            }
        }

    }

    ''', 'supportAndPeriod')

  def __convert(self, value):
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

  def getMemoryUSS(self):
      """
      Total amount of USS memory consumed by the mining process will be retrieved from this function

      :return: returning USS memory consumed by the mining process
      :rtype: float
      """

      return self._partialPeriodicPatterns__memoryUSS

  def getMemoryRSS(self):
      """
      Total amount of RSS memory consumed by the mining process will be retrieved from this function

      :return: returning RSS memory consumed by the mining process
      :rtype: float
      """

      return self._partialPeriodicPatterns__memoryRSS

  def getRuntime(self):
      """
      Calculating the total amount of runtime taken by the mining process

      :return: returning total amount of runtime taken by the mining process
      :rtype: float
      """

      return self.__runTime

  def getPatternsAsDataFrame(self):
      """
      Storing final frequent patterns in a dataframe

      :return: returning frequent patterns in a dataframe
      :rtype: pd.DataFrame
      """

      dataframe = {}
      data = []
      for a, b in self._partialPeriodicPatterns__finalPatterns.items():
          if len(a) == 1:
              pattern = f'{a[0]}'
          else:
              pattern = f'{a[0]}'
              for item in a[1:]:
                  pattern = pattern + f' {item}'
          data.append([pattern, b[0], b[1]])
          dataframe = pd.DataFrame(data, columns=['Patterns', 'Support', 'Periodicity'])
      return dataframe

  def save(self, outFile):
      """
      Complete set of frequent patterns will be loaded in to a output file

      :param outFile: name of the output file
      :type outFile: csv file
      """
      self._partialPeriodicPatterns__oFile = outFile
      writer = open(self._partialPeriodicPatterns__oFile, 'w+')
      for x, y in self._partialPeriodicPatterns__finalPatterns.items():
          if len(x) == 1:
              writer.write(f'{x[0]}:{y[0]}:{y[1]}\n')
          else:
              writer.write(f'{x[0]}')
              for item in x[1:]:
                  writer.write(f'\t{item}')
              writer.write(f':{y[0]}:{y[1]}\n')
          # s1 = str(x) + ":" + str(y)
          # writer.write("%s \n" % s1)

  def getPatterns(self):
      """
      Function to send the set of frequent patterns after completion of the mining process

      :return: returning frequent patterns
      :rtype: dict
      """
      return self._partialPeriodicPatterns__finalPatterns

  def printResults(self):
      print("Total number of Partial Periodic Frequent Patterns:", len(self.getPatterns()))
      print("Total Memory in USS:", self.getMemoryUSS())
      print("Total Memory in RSS", self.getMemoryRSS())
      print("Total ExecutionTime in ms:", self.getRuntime())

  def __creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._partialPeriodicPatterns__iFile, pd.DataFrame):
            timeStamp, data = [], []
            if self._partialPeriodicPatterns__iFile.empty:
                print("its empty..")
            i = self._partialPeriodicPatterns__iFile.columns.values.tolist()
            if 'ts' or 'TS' in i:
                timeStamp = self._partialPeriodicPatterns__iFile['timeStamps'].tolist()
            if 'Transactions' in i:
                data = self._partialPeriodicPatterns__iFile['Transactions'].tolist()
            if 'Patterns' in i:
                data = self._partialPeriodicPatterns__iFile['Patterns'].tolist()
            for i in range(len(data)):
                tr = [timeStamp[i]]
                tr.append(data[i])
                self.__Database.append(tr)
            self.__lno = len(self.__Database)

        if isinstance(self._partialPeriodicPatterns__iFile, str):
            if validators.url(self._partialPeriodicPatterns__iFile):
                data = urlopen(self._partialPeriodicPatterns__iFile)
                for line in data:
                    self.__lno += 1
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._partialPeriodicPatterns__iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            self.__lno += 1
                            temp = [i.rstrip() for i in line.split(self._partialPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

        ArraysAndItems = {}

        maxTID = 0
        for i in range(len(self.__Database)):
            tid = int(self.__Database[i][0])
            for j in self.__Database[i][1:]:
                j = tuple([j])
                if j not in ArraysAndItems:
                    ArraysAndItems[j] = [tid]
                else:
                    ArraysAndItems[j].append(tid)
                maxTID = max(maxTID, tid)

        # sorted_dict = sorted(my_dict.items(), key=lambda item: len(item[1]))
        ArraysAndItems = dict(sorted(ArraysAndItems.items(), key = lambda item: len(item[1]), reverse = True))

        self._maxTS = maxTID
        self._dbSize = maxTID

        newArraysAndItems = {}

        arraySize = maxTID // 32 + 1 if maxTID % 32 != 0 else maxTID // 32
        self.arraySize = arraySize

        self._rename = {}
        number = 0

        for k,v in ArraysAndItems.items():
          if len(v) >= self._partialPeriodicPatterns__minSup:
            nv = v.copy()
            nv = cp.array(nv, dtype=np.uint32)
            nv = cp.sort(nv)
            differences = cp.diff(nv)
            # maxDiff = cp.max(differences)
            perSup = cp.count_nonzero(differences <= self._partialPeriodicPatterns__maxPer).get()
            bitRep = np.zeros(arraySize, dtype=np.uint32)
            for i in range(len(v)):
                bitRep[v[i] // 32] |= 1 << 31 - (v[i] % 32)
            # print(k,v, end = " ")
            # for i in range(len(bitRep)):
            #     print(np.binary_repr(bitRep[i], width=32), end = " ")
            # print()
            newArraysAndItems[tuple([number])] = bitRep
            self._rename[number] = str(k[0])
            number += 1
            satisfy = self._partialPeriodicPatterns__minPR * (self._partialPeriodicPatterns__minSup + 1)
            ratio = perSup / (len(v) + 1)
            if ratio >= self._partialPeriodicPatterns__minPR:
                # print(len(v),perSup)
                # print(k, len(v), v, nv, differences, maxDiff)
                self._partialPeriodicPatterns__finalPatterns["\t".join(k)] = [len(v),ratio]
                # newArraysAndItems[k] = np.array(v, dtype=np.uint32)

        return newArraysAndItems

  @deprecated("It is recommended to use mine() instead of mine() for mining process")
  def startMine(self):
    """
    Main program start with extracting the periodic frequent items from the database and
    performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.
    """
    self.mine()

  def Mine(self):
    """
    Main program start with extracting the periodic frequent items from the database and
    performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.
    """
    self.__path = self._partialPeriodicPatterns__iFile
    self._partialPeriodicPatterns__startTime = time.time()
    self._partialPeriodicPatterns__finalPatterns = {}
    self._partialPeriodicPatterns__maxPer = self.__convert(self._partialPeriodicPatterns__maxPer)
    self._partialPeriodicPatterns__minSup = self.__convert(self._partialPeriodicPatterns__minSup)
    self._partialPeriodicPatterns__minPR = float(self._partialPeriodicPatterns__minPR)

    ArraysAndItems = self.__creatingItemSets()

    # for k,v in a.items():
    #   print(k,':',v)

    candidates = list(ArraysAndItems.keys())
    candidates = [list(i) for i in candidates]
    values = list(ArraysAndItems.values())
    values = cp.array(values)

    while len(candidates) > 0:
      print("Number of Candidates:", len(candidates))
      newKeys = []
      for i in range(len(candidates)):
          for j in range(i+1, len(candidates)):
                  if candidates[i][:-1] == candidates[j][:-1] and candidates[i][-1] != candidates[j][-1]:
                      newKeys.append(candidates[i] + candidates[j][-1:])
                  else:
                      break

      if len(newKeys) == 0:
          break

      # print(newKeys)

      numberOfKeys = len(newKeys)
      keySize = len(newKeys[0])

      newKeys = cp.array(newKeys, dtype=cp.uint32)

      # newKeys = cp.flatten(newKeys)
      newKeys = cp.reshape(newKeys, (numberOfKeys * keySize,))

      period = cp.zeros(numberOfKeys, dtype=cp.uint32)
      support = cp.zeros(numberOfKeys, dtype=cp.uint32)

      self.supportAndPeriod((numberOfKeys//32 + 1,), (32,),
                              (
                                  values, self.arraySize,
                                  newKeys, numberOfKeys, keySize,
                                  period, support,
                                  self._partialPeriodicPatterns__maxPer, self._maxTS
                              )
      )

      newKeys = cp.reshape(newKeys, (numberOfKeys, keySize))
      newKeys = cp.asnumpy(newKeys)
      period = period.get()
      support = support.get()

      satisfy = self._partialPeriodicPatterns__minPR * (self._partialPeriodicPatterns__minSup + 1)

      newCandidates = []
      for i in range(len(newKeys)):
        ratio = (period[i])/(support[i] + 1)
        if support[i] >= self._partialPeriodicPatterns__minSup:
          newCandidates.append(list(newKeys[i]))
        if ratio >= self._partialPeriodicPatterns__minPR:
          rename = "\t".join([self._rename[j] for j in newKeys[i]])
          # print(rename, ":", period[i]/support[i], support[i], period[i])
          self._partialPeriodicPatterns__finalPatterns[rename] = [support[i],ratio]


      # for i in range(len(newKeys)):
      #     # print(newKeys[i], support[i], period[i])
      #     if period[i]/(self._partialPeriodicPatterns__minSup + 1) >= self._partialPeriodicPatterns__minPR and support[i] >= self._partialPeriodicPatterns__minSup:
      #         newCandidates.append(list(newKeys[i]))
      #         rename = [self._rename[j] for j in newKeys[i]]
      #         rename = "\t".join(rename)
      #         if period[i] / support[i] >= self._partialPeriodicPatterns__minPR:
      #           # print(rename, period[i]/support[i], support[i], period[i])
      #           self._partialPeriodicPatterns__finalPatterns[rename] = period[i]

      # print()

      # print(newCandidates)

      candidates = newCandidates

    self.__runTime = time.time() - self._partialPeriodicPatterns__startTime
    process = psutil.Process(os.getpid())

    self._memoryUSS = process.memory_full_info().uss
    self._memoryRSS = process.memory_info().rss
    print("Periodic-Frequent patterns were generated successfully using gPPMiner algorithm ")

if __name__ == '__main__':
    ap = str()
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        if len(sys.argv) == 7:
            ap = cuGPPMiner(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        if len(sys.argv) == 6:
            ap = cuGPPMiner(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
        ap.mine()
        print("Total number of Frequent Patterns:", len(ap.getPatterns()))
        ap.save(sys.argv[2])
        print("Total Memory in USS:", ap.getMemoryUSS())
        print("Total Memory in RSS", ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", ap.getRuntime())
    else:
        # for i in [1000, 2000, 3000, 4000, 5000]:
        _ap = cuGPPMiner('Temporal_T10I4D100K.csv', 50, 2000, 0.7, '\t')
        _ap.mine()
        print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
        # _ap.save('output.txt')
        df2 = _ap.getPatterns()
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")