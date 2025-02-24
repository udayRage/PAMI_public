# This code uses "leverage" metric to extract the association rules from given frequent patterns.
#
# **Importing this algorithm into a python program**
#
#             import PAMI.AssociationRules.basic import leverage as alg
#
#             obj = alg.leverage(iFile, minLev)
#
#             obj.mine()
#
#             associationRules = obj.getAssociationRules()
#
#             print("Total number of Association Rules:", len(associationRules))
#
#             obj.save(oFile)
#
#             Df = obj.getAssociationRulesAsDataFrame()
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

from PAMI.AssociationRules.basic import abstract as _ab
from deprecated import deprecated
# increase reucursion depth
import os
import sys
sys.setrecursionlimit(10**4)
from itertools import combinations

class leverage:
    """
    About this algorithm
    ====================

    :**Description**: Association Rules are derived from frequent patterns using "leverage" metric.

    :**Reference**:

    :**Parameters**:    - **iFile** (*str*) -- *Name of the Input file to mine complete set of association rules*
                        - **oFile** (*str*) -- *Name of the Output file to write association rules*
                        - **minLev** (*float*) -- *Minimum leverage to mine all the satisfying association rules. The user can specify the minLev in float between the range of 0 to 1.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **finalPatterns** (*dict*) -- *Storing the complete set of patterns in a dictionary variable.*
                        - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*


    Execution methods
    =================

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 leverage.py <inputFile> <outputFile> <minLev> <sep>

      Example Usage:

      (.venv) $ python3 leverage.py sampleDB.txt patterns.txt 0.5 ' '

    .. note:: minLev can be specified in a value between 0 and 1.
    
    
    **Calling from a python program**

    .. code-block:: python

            import PAMI.AssociationRules.basic import leverage as alg

            obj = alg.leverage(iFile, minLev)

            obj.mine()

            associationRules = obj.getAssociationRules()

            print("Total number of Association Rules:", len(associationRules))

            obj.save(oFile)

            Df = obj.getAssociationRulesAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    Credits
    =======

            The complete program was written by P. Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    _minLev = float()
    _startTime = float()
    _endTime = float()
    _iFile = " "
    _oFile = " "
    _Sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _associationRules = {}

    def __init__(self, iFile, minLev, maxTS, sep):
        """
        :param iFile: input file name or path
        :type iFile: str
        :param minLev: minimum leverage
        :type minLev: float
        :param sep: Delimiter of input file
        :type sep: str
        """
        self._iFile = iFile
        self._minLev = minLev
        self._associationRules = {}
        self._sep = sep
        self._maxTS = maxTS

    def _readPatterns(self):
        """
        Reading the input file and storing all the frequent patterns and their support respectively in a frequentPatterns variable.
        """
        self._associationRules = {}
        if isinstance(self._iFile, _ab._pd.DataFrame):
            pattern, support = [], []
            if self._iFile.empty:
                print("its empty..")
            cols = self._iFile.columns.values.tolist()
            for col in cols:
                if 'pattern' in col.lower():
                    pattern = self._iFile[col].tolist()
                    # print("Using column: ", col, "for pattern")
                if 'support' in col.lower():
                    support = self._iFile[col].tolist()
                    # print("Using column: ", col, "for support")
            for i in range(len(pattern)):
                # if pattern[i] != tuple(): exit()
                if type(pattern[i]) != str:
                    raise ValueError("Pattern should be a tuple. PAMI is going through a major revision.\
                                      Please raise an issue in the github repository regarding this error and provide information regarding input and algorithm.\
                                      In the meanwhile try saving the patterns to a file using (alg).save() and use the file as input. \
                                      If that doesn't work, please raise an issue in the github repository.\
                                      Got pattern: ", pattern[i], "at index: ", i, "in the dataframe, type: ", type(pattern[i]))
                # s = tuple(sorted(pattern[i]))
                s = pattern[i].split(self._sep)
                s = tuple(sorted(s))
                self._associationRules[s] = support[i] / self._maxTS
                
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                f = _ab._urlopen(self._iFile)
                for line in f:
                    line = line.strip()
                    line = line.split(':')
                    s = line[0].split(self._sep)
                    s = tuple(sorted(s))
                    
                    self._associationRules[s] = int(line[1]) / self._maxTS
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            line = line.split(':')
                            s = line[0].split(self._sep)
                            s = [x.strip() for x in s]
                            s = tuple(sorted(s))
                            self._associationRules[s] = int(line[1]) / self._maxTS
                except IOError:
                    print("File Not Found")
                    quit()
        # sorted(k, key=lambda x: self._frequentPatterns[x], reverse=True)
        # return k

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Association rule mining process will start from here
        """
        self.mine()



    def mine(self):
        """
        Association rule mining process will start from here
        """
        self._startTime = _ab._time.time()
        self._readPatterns()

        keys = list(self._associationRules.keys())

        for i in range(len(self._associationRules)):
            key = self._associationRules[keys[i]]
            for idx in range(len(keys[i]) - 1, 0, -1):
                for c in combinations(keys[i], r=idx):
                    antecedent = c
                    # consequent = keys[i] - antecedent
                    consequent = tuple(sorted([x for x in keys[i] if x not in antecedent]))
                    # Lev = key / self._frequentPatterns[antecedent]
                    lev = key - self._associationRules[antecedent] * self._associationRules[consequent]
                    if lev >= self._minLev:
                        self._associationRules[antecedent + tuple(['->']) + keys[i]] = lev

        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Association rules successfully  generated from frequent patterns ")

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

    def getAssociationRulesAsDataFrame(self):
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
        # # dataFrame = dataFrame.replace(r'\r+|\n+|\t+',' ', regex=True)
        # return dataFrame

        # dataFrame = _ab._pd.DataFrame(list(self._associationRules.items()), columns=['Patterns', 'Support'])
        dataFrame = _ab._pd.DataFrame(list([[" ".join(x), y] for x, y in self._associationRules.items()]), columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile: str) -> None:
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csvfile
        :return: None
        """
        with open(outFile, 'w') as f:
            for x, y in self._associationRules.items():
                x = self._sep.join(x)
                f.write(f"{x} : {y}\n")

    def getAssociationRules(self):
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._associationRules

    def printResults(self):
        """
        Function to send the result after completion of the mining process
        """
        print("Total number of Association Rules:", len(self.getAssociationRules()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = leverage(_ab._sys.argv[1], float(_ab._sys.argv[3]), int(_ab._sys.argv[4]),_ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = leverage(_ab._sys.argv[1],float(_ab._sys.argv[3]),int(_ab.sys.argv[4]),sep='\t')
        _ap.mine()
        _ap.mine()
        print("Total number of Association Rules:", len(_ap.getAssociationRules()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
