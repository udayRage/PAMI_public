# Local Periodic Patterns, which are patterns (sets of events) that have a periodic behavior in some non predefined
# time-intervals. A pattern is said to be a local periodic pattern if it appears regularly and continuously in some
# time-intervals. The maxSoPer (maximal period of spillovers) measure allows detecting time-intervals of variable
# lengths where a pattern is continuously periodic, while the minDur (minimal duration) measure ensures that those
# time-intervals have a minimum duration.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.localPeriodicPattern.basic import LPPMDepth as alg
#
#             obj = alg.LPPMDepth(iFile, maxPer, maxSoPer, minDur)
#
#             obj.mine()
#
#             localPeriodicPatterns = obj.getPatterns()
#
#             print(f'Total number of local periodic patterns: {len(localPeriodicPatterns)}')
#
#             obj.save(oFile)
#
#             Df = obj.getPatternsAsDataFrame()
#
#             memUSS = obj.getMemoryUSS()
#
#             print(f'Total memory in USS: {memUSS}')
#
#             memRSS = obj.getMemoryRSS()
#
#             print(f'Total memory in RSS: {memRSS}')
#
#             runtime = obj.getRuntime()
#
#             print(f'Total execution time in seconds: {runtime})
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

from PAMI.localPeriodicPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
import pandas as pd
from deprecated import deprecated


class LPPMDepth(_ab._localPeriodicPatterns):

    """
    :Description:

        Local Periodic Patterns, which are patterns (sets of events) that have a periodic behavior in some non predefined
        time-intervals. A pattern is said to be a local periodic pattern if it appears regularly and continuously in some
        time-intervals. The maxSoPer (maximal period of spillovers) measure allows detecting time-intervals of variable
        lengths where a pattern is continuously periodic, while the minDur (minimal duration) measure ensures that those
        time-intervals have a minimum duration.

    :Reference:

        Fournier-Viger, P., Yang, P., Kiran, R. U., Ventura, S., Luna, J. M.. (2020). Mining Local Periodic Patterns in
        a Discrete Sequence. Information Sciences, Elsevier, to appear. [ppt] DOI: 10.1016/j.ins.2020.09.044

    :param  iFile: str :
                   Name of the Input file to mine complete set of local periodic pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of local periodic patterns
    :param  minDur: str:
                   Minimal duration in seconds between consecutive periods of time-intervals where a pattern is continuously periodic.
    :param  maxPer: float:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.
    :param  maxSoPer: float:
                   Controls the maximum number of time periods between consecutive periods of time-intervals where a pattern is continuously periodic.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : str
            Input file name or path of the input file
        oFile : str
            Output file name or path of the output file
        maxPer : float
            User defined maxPer value.
        maxSoPer : float
            User defined maxSoPer value.
        minDur : float
            User defined minDur value.
        tsmin : int / date
            First time stamp of input data.
        tsmax : int / date
            Last time stamp of input data.
        startTime : float
            Time when start of execution the algorithm.
        endTime : float
            Time when end of execution the algorithm.
        finalPatterns : dict
            To store local periodic patterns and its PTL.
        tsList : dict
            To store items and its time stamp as bit vector.
        sep : str
            separator used to distinguish items from each other. The default separator is tab space.

    :Methods:

        createTSlist()
            Create the TSlist as bit vector from input data.
        generateLPP()
            Generate 1 length local periodic pattens by TSlist and execute depth first search.
        calculatePTL(tsList)
            Calculate PTL from input tsList as bit vector
        LPPMDepthSearch(extensionOfP)
            Mining local periodic patterns using depth first search.
        mine()
            Mining process will start from here.
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function.
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function.
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function.
        getLocalPeriodicPatterns()
            return local periodic patterns and its PTL
        save(oFile)
            Complete set of local periodic patterns will be loaded in to an output file.
        getPatternsAsDataFrame()
            Complete set of local periodic patterns will be loaded in to a dataframe.

    **Executing the code on terminal:**
    --------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 LPPMDepth.py <inputFile> <outputFile> <maxPer> <minSoPer> <minDur>

      Example Usage:

      (.venv) $ python3 LPPMDepth.py sampleDB.txt patterns.txt 0.3 0.4 0.5

    .. note: minDur will be considered as time interval between two consecutive periods


    **Sample run of importing the code:**
    ----------------------------------------
    .. code-block:: python

            from PAMI.localPeriodicPattern.basic import LPPMDepth as alg

            obj = alg.LPPMDepth(iFile, maxPer, maxSoPer, minDur)

            obj.mine()

            localPeriodicPatterns = obj.getPatterns()

            print(f'Total number of local periodic patterns: {len(localPeriodicPatterns)}')

            obj.save(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print(f'Total memory in USS: {memUSS}')

            memRSS = obj.getMemoryRSS()

            print(f'Total memory in RSS: {memRSS}')

            runtime = obj.getRuntime()

            print(f'Total execution time in seconds: {runtime})

    **Credits:**
    -------------
        The complete program was written by So Nakamura under the supervision of Professor Rage Uday Kiran.
    """
    
    _localPeriodicPatterns__iFile = ''
    _localPeriodicPatterns__oFile = ''
    _localPeriodicPatterns__maxPer = str()
    _localPeriodicPatterns__maxSoPer = str()
    _localPeriodicPatterns__minDur = str()
    __tsmin = 0
    __tsmax = 0
    _localPeriodicPatterns__startTime = float()
    _localPeriodicPatterns__endTime = float()
    _localPeriodicPatterns__memoryUSS = float()
    _localPeriodicPatterns__memoryRSS = float()
    _localPeriodicPatterns__finalPatterns = {}
    __tsList = {}
    _localPeriodicPatterns__sep = ' '
    __Database = []

    def __creatingItemSets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._localPeriodicPatterns__iFile, _ab._pd.DataFrame):
            if self._localPeriodicPatterns__iFile.empty:
                print("its empty..")
            i = self._localPeriodicPatterns__iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.__Database = self._localPeriodicPatterns__iFile['Transactions'].tolist()
            if 'Patterns' in i:
                self.__Database = self._localPeriodicPatterns__iFile['Patterns'].tolist()

        if isinstance(self._localPeriodicPatterns__iFile, str):
            if _ab._validators.url(self._localPeriodicPatterns__iFile):
                data = _ab._urlopen(self._localPeriodicPatterns__iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._localPeriodicPatterns__sep)]
                    temp = [x for x in temp if x]
                    self.__Database.append(temp)
            else:
                try:
                    with open(self._localPeriodicPatterns__iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._localPeriodicPatterns__sep)]
                            temp = [x for x in temp if x]
                            self.__Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def __createTSlist(self) -> None:
        """
        Create tsList as bit vector from temporal data.
        """
        count = 1
        bitVector = None
        for line in self.__Database:
            bitVector = 0b1 << count
            bitVector = bitVector | 0b1
            ts = line[0]
            for item in line[1:]:
                if self.__tsList.get(item):
                    different = abs(bitVector.bit_length() - self.__tsList[item].bit_length())
                    self.__tsList[item] = self.__tsList[item] << different
                    self.__tsList[item] = self.__tsList[item] | 0b1
                else:
                    self.__tsList[item] = bitVector
            count += 1
            self.__tsmax = int(ts)
        for item in self.__tsList:
            different = abs(bitVector.bit_length() - self.__tsList[item].bit_length())
            self.__tsList[item] = self.__tsList[item] << different
        self._localPeriodicPatterns__maxPer = self.__convert(self._localPeriodicPatterns__maxPer)
        self._localPeriodicPatterns__maxSoPer = self.__convert(self._localPeriodicPatterns__maxSoPer)
        self._localPeriodicPatterns__minDur = self.__convert(self._localPeriodicPatterns__minDur)

    def __generateLPP(self) -> None:
        """
        Generate local periodic items from bit vector tsList.
        When finish generating local periodic items, execute mining depth first search.
        """
        I = set()
        PTL = {}
        for item in self.__tsList:
            PTL[item] = set()
            ts = list(bin(self.__tsList[item]))
            ts = ts[2:]
            start = -1
            currentTs = 1
            tsPre = ' '
            soPer = ' '
            for t in ts[currentTs:]:
                if t == '0':
                    currentTs += 1
                    continue
                else:
                    tsPre = currentTs
                    currentTs += 1
                    break
            for t in ts[currentTs:]:
                if t == '0':
                    currentTs += 1
                    continue
                else:
                    per = currentTs - tsPre
                    if per <= self._localPeriodicPatterns__maxPer and start == -1:
                        start = tsPre
                        soPer = self._localPeriodicPatterns__maxSoPer
                    if start != -1:
                        soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                        if soPer > self._localPeriodicPatterns__maxSoPer:
                            if tsPre - start >= self._localPeriodicPatterns__minDur:
                                PTL[item].add((start, tsPre))
                            """else:
                                bitVector = 0b1 << currentTs
                                different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                                bitVector = bitVector | 0b1
                                bitVector = bitVector << different
                                self.tsList[item] = self.tsList[item] | bitVector"""
                            start = -1
                    tsPre = currentTs
                    currentTs += 1
            if start != -1:
                soPer = max(0, soPer + self.__tsmax - tsPre - self._localPeriodicPatterns__maxPer)
                if soPer > self._localPeriodicPatterns__maxSoPer and tsPre - start >= self._localPeriodicPatterns__minDur:
                    PTL[item].add((start, tsPre))
                """else:
                    bitVector = 0b1 << currentTs+1
                    different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                    bitVector = bitVector | 0b1
                    bitVector = bitVector << different
                    self.tsList[item] = self.tsList[item] | bitVector"""
                if soPer <= self._localPeriodicPatterns__maxSoPer and self.__tsmax - start >= self._localPeriodicPatterns__minDur:
                    PTL[item].add((start, self.__tsmax))
                """else:
                    bitVector = 0b1 << currentTs+1
                    different = abs(self.tsList[item].bit_length() - bitVector.bit_length())
                    bitVector = bitVector | 0b1
                    bitVector = bitVector << different
                    self.tsList[item] = self.tsList[item] | bitVector"""
            if len(PTL[item]) > 0:
                I |= {item}
                self._localPeriodicPatterns__finalPatterns[item] = PTL[item]
        I = sorted(list(I))
        # I = set(I)
        self.__LPPMDepthSearch(I)

    def __calculatePTL(self, tsList: int) -> Set[Tuple[int, int]]:
        """
        calculate PTL from tsList as bit vector.

        :param tsList: it is one item's tsList which is used bit vector.
        :type tsList: int
        :return: it is PTL of input item.
        :rtype: set
        """
        tsList = list(bin(tsList))
        tsList = tsList[2:]
        start = -1
        currentTs = 1
        PTL = set()
        tsPre = ' '
        soPer = ' '
        for ts in tsList[currentTs:]:
            if ts == '0':
                currentTs += 1
                continue
            else:
                tsPre = currentTs
                currentTs += 1
                break
        for ts in tsList[currentTs:]:
            if ts == '0':
                currentTs += 1
                continue
            else:
                per = currentTs - tsPre
                if per <= self._localPeriodicPatterns__maxPer and start == -1:
                    start = tsPre
                    soPer = self._localPeriodicPatterns__maxSoPer
                if start != -1:
                    soPer = max(0, soPer + per - self._localPeriodicPatterns__maxPer)
                    if soPer > self._localPeriodicPatterns__maxSoPer:
                        if tsPre - start >= self._localPeriodicPatterns__minDur:
                            PTL.add((start, tsPre))
                        start = -1
                tsPre = currentTs
                currentTs += 1
        if start != -1:
            soPer = max(0, soPer + self.__tsmax - tsPre - self._localPeriodicPatterns__maxPer)
            if soPer > self._localPeriodicPatterns__maxSoPer and tsPre - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, tsPre))
            if soPer <= self._localPeriodicPatterns__maxSoPer and self.__tsmax - start >= self._localPeriodicPatterns__minDur:
                PTL.add((start, tsPre))
        return PTL

    def __LPPMDepthSearch(self, extensionsOfP: List[Union[Tuple[str, ...], str]]) -> None:
        """
        Mining n-length local periodic pattens from n-1-length patterns by depth first search.

        :param extensionsOfP: it is n-1 length patterns list.
        :type extensionsOfP: list
        :return: None
        """
        for x in range(len(extensionsOfP)-1):
            extensionsOfPx = set()
            for y in range(x+1,len(extensionsOfP)):
                tspxy = self.__tsList[extensionsOfP[x]] & self.__tsList[extensionsOfP[y]]
                PTL = self.__calculatePTL(tspxy)
                if len(PTL) > 0:
                    if type(extensionsOfP[x]) == str:
                        pattern = (extensionsOfP[x], extensionsOfP[y])
                        self._localPeriodicPatterns__finalPatterns[pattern] = PTL
                        self.__tsList[pattern] = tspxy
                        extensionsOfPx.add(pattern)
                    else:
                        px = [item for item in extensionsOfP[x]]
                        py = [item for item in extensionsOfP[y]]
                        pattern = set(px + py)
                        self._localPeriodicPatterns__finalPatterns[tuple(pattern)] = PTL
                        self.__tsList[tuple(pattern)] = tspxy
                        extensionsOfPx.add(tuple(pattern))
            if extensionsOfPx:
                self.__LPPMDepthSearch(list(extensionsOfPx))

    def __convert(self, value: Union[int, float, str]) -> Union[int, float]:
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        :rtype: int or float
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

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self) -> None:
        """
        Mining process start from here. This function calls createTSlist and generateLPP.
        """
        self.mine()

    def mine(self) -> None:
        """
        Mining process start from here. This function calls createTSlist and generateLPP.
        """
        self._localPeriodicPatterns__startTime = _ab._time.time()
        self._localPeriodicPatterns__finalPatterns = {}
        self.__creatingItemSets()
        self._localPeriodicPatterns__maxPer = self.__convert(self._localPeriodicPatterns__maxPer)
        self._localPeriodicPatterns__maxSoPer = self.__convert(self._localPeriodicPatterns__maxSoPer)
        self._localPeriodicPatterns__minDur = self.__convert(self._localPeriodicPatterns__minDur)
        self.__createTSlist()
        self.__generateLPP()
        self._localPeriodicPatterns__endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._localPeriodicPatterns__memoryRSS = float()
        self._localPeriodicPatterns__memoryUSS = float()
        self._localPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._localPeriodicPatterns__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__memoryUSS

    def getMemoryRSS(self) -> float:
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__memoryRSS

    def getRuntime(self) -> float:
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._localPeriodicPatterns__endTime - self._localPeriodicPatterns__startTime

    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final local periodic patterns in a dataframe

        :return: returning local periodic patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._localPeriodicPatterns__finalPatterns.items():
            pat = str()
            for i in a:
                pat = pat + i + ' '
            data.append([pat, b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'PTL'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """
        Complete set of local periodic patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: None
        """
        self._localPeriodicPatterns__oFile = outFile
        writer = open(self._localPeriodicPatterns__oFile, 'w+')
        for x, y in self._localPeriodicPatterns__finalPatterns.items():
            pat = str()
            for i in x:
                pat = pat + i + '\t'
            pat = pat + ":"
            for i in y:
                pat = pat + str(i) + '\t'
            patternsAndPTL = pat.strip()
            writer.write("%s \n" % patternsAndPTL)

    def getPatterns(self) -> Dict[Union[Tuple[str, ...], str], Set[Tuple[int, int]]]:
        """
        Function to send the set of local periodic patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._localPeriodicPatterns__finalPatterns

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Local Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())



if __name__ == '__main__':
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = LPPMDepth(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]), _ab._sys.argv[5])
            _ap.mine()
            _ap.save(_ab._sys.argv[2])
        if len(_ab._sys.argv) == 5:
            _ap = LPPMDepth(_ab._sys.argv[1], _ab._sys.argv[2], float(_ab._sys.argv[3]), _ab._sys.argv[4])
            _ap.mine()

        print("Total number of Local Periodic Patterns:", len(_ap.getPatterns()))
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
