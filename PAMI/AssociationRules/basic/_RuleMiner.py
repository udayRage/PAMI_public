# RuleMiner code is used to extract the association rules from given frequent patterns.
#
# **Importing this algorithm into a python program**
# ----------------------------------------------------
#
#             import PAMI.AssociationRules.basic import RuleMiner as alg
#
#             obj = alg.RuleMiner(iFile, measure, o.5, "\t")
#
#             obj.mine()
#
#             associationRules = obj.getPatterns()
#
#             print("Total number of Association Rules:", len(associationRules))
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

from PAMI.AssociationRules.basic import abstract as _ab
from deprecated import deprecated

class Confidence:
    """
    Association Rules are derived from frequent patterns using "confidence" metric.
    """
    
    def __init__(self, patterns, singleItems, threshold):
        self._frequentPatterns = patterns
        self._singleItems = singleItems
        self._threshold = threshold
        self._finalPatterns = {}
        
    def _generation(self, prefix, suffix):
        """
        To generate the combinations all association rules.

        :param prefix: the prefix of association rule.
        :type prefix: str
        :param suffix: the suffix of association rule.
        :type suffix: str
        """
        if len(suffix) == 1:
            self._generaeWithConfidence(prefix, suffix[0])
        for i in range(len(suffix)):
            suffix1 = suffix[:i] + suffix[i+1:]
            prefix1 = prefix + ' ' + suffix[i]
            for j in range(i+1, len(suffix)):
                self._generaeWithConfidence(prefix + ' ' + suffix[i], suffix[j])
                #self._generation(prefix+ ' ' +suffix[i], suffix[i+1:]) 
            self._generation(prefix1, suffix1)
            
    def _generaeWithConfidence(self, lhs, rhs):
        """
        To find association rules satisfying user-specified minConf

        :param lhs: the prefix of association rule.
        :type lhs: str
        :param rhs: the suffix of association rule.
        :type rhs: str
        """
        s = lhs + '\t' + rhs
        if self._frequentPatterns.get(s) is None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        if conflhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if confrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
            
    def run(self):
        """
        To generate the combinations all association rules.
        """
        for i in range(len(self._singleItems)):
            suffix = self._singleItems[:i] + self._singleItems[i+1:]
            prefix = self._singleItems[i]
            for j in range(i+1, len(self._singleItems)):
                self._generaeWithConfidence(self._singleItems[i], self._singleItems[j])
            self._generation(prefix, suffix)
    
    
    
class Lift:
    """
    Association Rules are derived from frequent patterns using "lift" metric.
    """
    
    def __init__(self, patterns, singleItems, threshold):
        """
        :param patterns: given frequent patterns
        :type patterns: dict
        :param singleItems: one-length frequent patterns
        :type singleItems: list
        :param threshold: threshold for lifting rules
        :type threshold: float
        """
        self._frequentPatterns = patterns
        self._singleItems = singleItems
        self._threshold = threshold
        self._finalPatterns = {}
        
    def _generation(self, prefix, suffix):
        """
        To generate the combinations all association rules.

        :param prefix: the prefix of association rule.
        :type prefix: str
        :param suffix: the suffix of association rule.
        :type suffix: str
        """
        if len(suffix) == 1:
            self._generateWithLift(prefix, suffix[0])
        for i in range(len(suffix)):
            suffix1 = suffix[:i] + suffix[i+1:]
            prefix1 = prefix + ' ' + suffix[i]
            for j in range(i+1, len(suffix)):
                self._generateWithLift(prefix + ' ' + suffix[i], suffix[j])
                #self._generation(prefix+ ' ' +suffix[i], suffix[i+1:]) 
            self._generation(prefix1, suffix1)
            
    def _generateWithLift(self, lhs, rhs):
        """
        To find association rules satisfying user-specified minConf

        :param lhs: the prefix of association rule.
        :type lhs: str
        :param rhs: the suffix of association rule.
        :type rhs: str
        """
        s = lhs + '\t' + rhs
        if self._frequentPatterns.get(s) is None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        liftlhs = conflhs / self._frequentPatterns[rhs] * self._frequentPatterns[lhs]
        rightrhs = confrhs / self._frequentPatterns[lhs] * self._frequentPatterns[rhs]
        if liftlhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if rightrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
            
    def run(self):
        """
        To generate the combinations all association rules.
        """
        for i in range(len(self._singleItems)):
            suffix = self._singleItems[:i] + self._singleItems[i+1:]
            prefix = self._singleItems[i]
            for j in range(i+1, len(self._singleItems)):
                self._generateWithLift(self._singleItems[i], self._singleItems[j])
            self._generation(prefix, suffix)
    
    
    
class Leverage:
    """
    Association Rules are derived from frequent patterns using "leverage" metric.
    """
    
    def __init__(self, patterns, singleItems, threshold):
        """
        :param patterns: given frequent patterns
        :type patterns: dict
        :param singleItems: one-length frequent patterns
        :type singleItems: list
        :param threshold: threshold for lifting rules
        :type threshold: float
        """
        self._frequentPatterns = patterns
        self._singleItems = singleItems
        self._threshold = threshold
        self._finalPatterns = {}
        
    def _generation(self, prefix, suffix):
        """
        To generate the combinations all association rules.

        :param prefix: the prefix of association rule.
        :type prefix: str
        :param suffix: the suffix of association rule.
        :type suffix: str
        """
        if len(suffix) == 1:
            self._generateWithLeverage(prefix, suffix[0])
        for i in range(len(suffix)):
            suffix1 = suffix[:i] + suffix[i+1:]
            prefix1 = prefix + ' ' + suffix[i]
            for j in range(i+1, len(suffix)):
                self._generateWithLeverage(prefix + ' ' + suffix[i], suffix[j])
            self._generation(prefix1, suffix1)
            
    def _generateWithLeverage(self, lhs, rhs):
        """
        To find association rules satisfying user-specified minConf

        :param lhs: the prefix of association rule.
        :type lhs: str
        :param rhs: the suffix of association rule.
        :type rhs: str
        """
        s = lhs + '\t' + rhs
        if self._frequentPatterns.get(s) is None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        liftlhs = conflhs - self._frequentPatterns[rhs] * self._frequentPatterns[lhs]
        rightrhs = confrhs - self._frequentPatterns[lhs] * self._frequentPatterns[rhs]
        if liftlhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if rightrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
            
    def run(self):
        """
        To generate the combinations all association rules.
        """
        for i in range(len(self._singleItems)):
            suffix = self._singleItems[:i] + self._singleItems[i+1:]
            prefix = self._singleItems[i]
            for j in range(i+1, len(self._singleItems)):
                self._generateWithLeverage(self._singleItems[i], self._singleItems[j])
            self._generation(prefix, suffix)

class RuleMiner:
    """
    About this algorithm
    ====================

    :Description: RuleMiner code is used to extract the association rules from given frequent patterns

    :Reference:


    :param  iFile: str :
                   Name of the Input file to mine complete set of association rules
    :param  oFile: str :
                   Name of the output file to store complete set of association rules
    :param  minConf: float :
                   The user can specify the minConf in float between the range of 0 to 1.
    :param  frequentPattern: list or dict :
                   frequent patterns are stored in the form of list or dictionary
    :param  measure: str :
                   condition to calculate the strength of rule
    :param  threshold: int :
                   condition to satisfy
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


    Execution methods
    =================

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 RuleMiner.py <inputFile> <outputFile> <minConf> <sep>

      Example Usage:

      (.venv) $ python3 RuleMiner.py sampleDB.txt patterns.txt 0.5 ' '

    .. note:: minConf can be specified in a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            import PAMI.AssociationRules.basic import RuleMiner as alg

            obj = alg.RuleMiner(iFile, measure, o.5, "\t")

            obj.mine()

            associationRules = obj.getPatterns()

            print("Total number of Association Rules:", len(associationRules))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    :Methods:

            mine()
    """

    def __init__(self, iFile, measure, threshold, sep):
        """
        :param iFile: input file name or path
        :type iFile: str
        :param measure: measure
        :type measure: str
        :param threshold: threshold for lifting rules
        :type threshold: float
        :param sep: Delimiter of input file
        :type sep: str
        """
        self._iFile = iFile
        self._measure = measure
        self._threshold = threshold
        self._finalPatterns = {}
        self._sep = sep
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._startTime = None
        self._endTime = None
        self._oFile = str
    
    def _readPatterns(self):
        """
        Reading the input file and storing all the frequent patterns and their support respectively in a frequentPatterns variable.
        """
        self._frequentPatterns = {}
        k = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            pattern, support = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'pattern' in i:
                pattern = self._iFile['pattern'].tolist()
            if 'support' in i:
                support = self._iFile['support'].tolist()
            for i in range(len(pattern)):
                s = '\t'.join(pattern[i])
                self._frequentPattern[s] = support[i]
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.strip()
                    line = line.split(':')
                    s = line[0].split(self._sep)
                    s = '\t'.join(s)
                    self._frequentPatterns[s.strip()] = int(line[1])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            line = line.split(':')
                            s = line[0].split(self._sep)
                            for j in s:
                                if j not in k:
                                    k.append(j)
                            s = '\t'.join(s)
                            self._frequentPatterns[s.strip()] = int(line[1])
                except IOError:
                    print("File Not Found")
                    quit()
        return k

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
        k = self._readPatterns()
        if self._measure == 'confidence':
            a = Confidence(self._frequentPatterns, k, self._threshold)
            a.run()
            self._finalPatterns = a._finalPatterns
        if self._measure == 'lift':
            a = Lift(self._frequentPatterns, k, self._threshold)
            a.run()
            self._finalPatterns = a._finalPatterns
        if self._measure == 'leverage':
            a = Leverage(self._frequentPatterns, k, self._threshold)
            a.run()
            self._finalPatterns = a._finalPatterns
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

    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        # dataFrame = dataFrame.replace(r'\r+|\n+|\t+',' ', regex=True)
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        """
        Function to send the result after completion of the mining process
        """
        print("Total number of Association Rules:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = RuleMiner(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = RuleMiner(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]),sep='\t')
        _ap.mine()
        _ap.mine()
        print("Total number of Association Rules:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = RuleMiner('sensorOutput.txt', "lift", 0.5, '\t')
        _ap.mine()
        _ap.mine()
        _ap.save('output.txt')
        _ap.printResults()
        print("Error! The number of input parameters do not match the total number of parameters provided")
