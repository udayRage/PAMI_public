# Fuzzy Frequent  Pattern-Miner is desired to find all  frequent fuzzy patterns which is on-trivial and challenging problem to its huge search space.we are using efficient pruning techniques to reduce the search space.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.fuzzyFrequentPattern import FFIMiner as alg
#
#             iFile = 'sampleTDB.txt'
#
#             minSup = 0.25 # can be specified between 0 and 1
#
#             obj = alg.FFIMiner(iFile, minSup, sep)
#
#             obj.mine()
#
#             fuzzyFrequentPattern = obj.getPatterns()
#
#             print("Total number of Fuzzy Frequent Patterns:", len(fuzzyFrequentPattern))
#
#             obj.save("outputFile")
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

from PAMI.fuzzyFrequentPattern.basic import abstract as _ab
from typing import List, Dict, Tuple, Set, Union, Any, Generator
from deprecated import deprecated

class FFIMiner(_ab._fuzzyFrequentPattenrs):
    """
    **About this algorithm**

    :**Description**:   Fuzzy Frequent  Pattern-Miner is desired to find all  frequent fuzzy patterns which is on-trivial and challenging problem
                        to its huge search space.we are using efficient pruning techniques to reduce the search space.

    :**Reference**:   Lin, Chun-Wei & Li, Ting & Fournier Viger, Philippe & Hong, Tzung-Pei. (2015).
                      A fast Algorithm for mining fuzzy frequent itemsets. Journal of Intelligent & Fuzzy Systems. 29.
                      2373-2379. 10.3233/IFS-151936.
                      https://www.researchgate.net/publication/286510908_A_fast_Algorithm_for_mining_fuzzy_frequent_itemSets

    :**parameters**:    - **iFile** (*str*) -- *Name of the Input file to mine complete set of correlated patterns*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of correlated patterns*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:   - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **itemsCnt** (*int*) -- *To record the number of fuzzy spatial itemSets generated.*
                        - **mapItemSum** (*int*) -- *To keep track of sum of Fuzzy Values of items.*
                        - **joinsCnt** (*int*) -- * To keep track of the number of ffi-list that was constructed.*
                        - **BufferSize** (*int*) -- *Represent the size of Buffer.*
                        - **itemSetBuffer** (*list*) -- *To keep track of items in buffer.*

    :**Methods**:    - **mine()** -- *Mining process will start from here.*
                     - **getPatterns()** -- *Complete set of patterns will be retrieved with this function.*
                     - **save(oFile)** -- *Complete set of frequent patterns will be loaded in to a output file.*
                     - **getPatternsAsDataFrame()** -- *Complete set of frequent patterns will be loaded in to a dataframe.*
                     - **getMemoryUSS()** -- *Total amount of USS memory consumed by the mining process will be retrieved from this function.*
                     - **getMemoryRSS()** -- *Total amount of RSS memory consumed by the mining process will be retrieved from this function.*
                     - **getRuntime()** -- *Total amount of runtime taken by the mining process will be retrieved from this function.*
                     - **convert(value)** -- *To convert the given user specified value.*
                     - **compareItems(o1, o2)** -- *A Function that sort all ffi-list in ascending order of Support.*
                     - **FSFIMining(prefix, prefixLen, FSFIM, minSup)** -- *Method generate ffi from prefix.*
                     - **construct(px, py)** -- *A function to construct Fuzzy itemSet from 2 fuzzy itemSets.*
                     - **findElementWithTID(uList, tid)** -- *To find element with same tid as given.*
                     - **WriteOut(prefix, prefixLen, item, sumIUtil)** -- *To Store the pattern.*

    **Execution methods**

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 FFIMiner.py <inputFile> <outputFile> <minSup> <sep>

      Example Usage:

      (.venv) $ python3  FFIMiner.py sampleTDB.txt output.txt 6

    .. note:: minSup can be specified in support count or a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            from PAMI.fuzzyFrequentPattern import FFIMiner as alg

            iFile = 'sampleTDB.txt'

            minSup = 0.25 # can be specified between 0 and 1

            obj = alg.CoMine(iFile, minSup, sep)

            obj.mine()

            fuzzyFrequentPattern = obj.getPatterns()

            print("Total number of Fuzzy Frequent Patterns:", len(fuzzyFrequentPattern))

            obj.save("outputFile")

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    **Credits**

    The complete program was written by B.Sai Chitra and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _fuzFile = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _sep = "\t"

    def __init__(self, iFile: str, minSup: float, sep: str="\t") -> None:
        super().__init__(iFile, minSup, sep)
        self._Database = None
        self._startTime = 0
        self._endTime = 0
        self._dbLen = 0
        self._minSup = minSup
        self._iFile = iFile
        self._sep = sep
        self._finalPatterns = {}
        self._memoryUSS = 0
        self._memoryRSS = 0

    def _creatingItemsets(self) -> None:
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._transactions, self._fuzzyValues, self._Database = [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValues = self._iFile['fuzzyValues'].tolist()
            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    parts[0] = parts[0].strip()
                    parts[1] = parts[1].strip()
                    items = parts[0].split(self._sep)
                    quantities = parts[1].split(self._sep)
                    self._transactions.append([x for x in items])
                    self._fuzzyValues.append([float(x) for x in quantities])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.split("\n")[0]
                            parts = line.split(":")
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            items = parts[0].split(self._sep)
                            quantities = parts[1].split(self._sep)
                            self._transactions.append([x for x in items])
                            self._fuzzyValues.append([float(x) for x in quantities])
                except IOError:
                    print("File Not Found")
                    quit()
    
    def startMine(self):
        self.mine()

    def _convert(self, value) -> Union[int, float]:
        """
        To convert the given user specified value

        :param value: user specified value
        :type value: int or float or str
        :return: converted value
        :rtype: int or float
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbLen * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbLen * value)
            else:
                value = int(value)
        return value
    
    def dfs(self, cands):
        """
        Perform depth-first search (DFS) to find frequent patterns in a database.

        This method recursively combines candidate patterns and calculates their support
        in the database, storing frequent patterns and their support counts.

        :param cands: List of candidate patterns represented as tuples.
        :type cands: list
        :return: None

        This method does not return anything explicitly, but it updates internal
        attributes `_finalPatterns` and `_Database` with frequent patterns and their
        support counts.
        """
        for i in range(len(cands)):
            newCands = []
            for j in range(i + 1, len(cands)):
                newCand = tuple(cands[i] + tuple([cands[j][-1]]))
                # print(items[cands[i]], items[cands[j]])
                newCandItems = {}
                keys = self._Database[cands[i]].keys() & self._Database[cands[j]].keys()
                for k in keys:
                    newCandItems[k] = min(self._Database[cands[i]][k], self._Database[cands[j]][k])
                count = sum(newCandItems.values())
                if count >= self._minSup:
                    newCands.append(newCand)
                    self._finalPatterns[newCand] = count
                    self._Database[newCand] = newCandItems
            if len(newCands) > 1:
                self.dfs(newCands)

    def mine(self):
        """
        Main() function start from here.
        """
        self._startTime = _ab._time.time()
        items = {}
        lineNo = 0
        self._creatingItemsets()

        self._dbLen = len(self._transactions)
        for transactions, fuzzyValues in zip(self._transactions, self._fuzzyValues):
            for item, fuzzyValue in zip(transactions, fuzzyValues):
                item = tuple([item])
                if item not in items:
                    items[item] = {}
                items[item][lineNo] = fuzzyValue
            lineNo += 1

        self._minSup = self._convert(self._minSup)
        self._Database = items.copy()

        supports = {k:sum(v.values()) for k,v in items.items()}
        supports = {k:v for k,v in supports.items() if v >= self._minSup}
        self._Database = {k:v for k,v in items.items() if k in supports}
        self._Database = {k:v for k,v in sorted(self._Database.items(), key=lambda x: sum(x[1].values()), reverse=True)}

        self._finalPatterns = supports.copy()

        cands = list(self._Database.keys())
        self.dfs(cands)

        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss


    def getPatternsAsDataFrame(self) -> _ab._pd.DataFrame:
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        # dataFrame = {}
        # data = []
        # for a, b in self._finalPatterns.items():
        #     data.append([a.replace('\t', ' '), b])
        #     dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        # dataFrame = _fp._pd.DataFrame(list([[" ".join(x), y] for x,y in self._finalPatterns.items()]), columns=['Patterns', 'Support'])
        dataFrame = _ab._pd.DataFrame(list([[" ".join(x), y] for x, y in self._finalPatterns.items()]), columns=['Patterns', 'Support'])
        return dataFrame

    def getPatterns(self) -> dict:
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self) -> float:
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """
        return self._memoryRSS

    def getRuntime(self) -> float:
        """
        Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """
        return self._endTime - self._startTime

    def save(self, outFile) -> dict:
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        :return: dictionary of frequent patterns
        :rtype: dict
        """
        # self._oFile = outFile
        # writer = open(self._oFile, 'w+')
        # for x, y in self._finalPatterns.items():
        #     patternsAndSupport = x.strip() + ":" + str(y)
        #     writer.write("%s \n" % patternsAndSupport)
        with open(outFile, 'w') as f:
            for x, y in self._finalPatterns.items():
                x = "\t".join(x)
                f.write(f"{x}:{y}\n")

    def printResults(self) -> None:
        """
        This function is used to print the results
        """
        print("Total number of Fuzzy Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = FFIMiner('/Users/tarunsreepada/Downloads/Fuzzy_T10I4D100K.csv', 400, '\t')
        # _ap.mine()
        _ap.mine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print(_ap.getPatternsAsDataFrame())
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")

