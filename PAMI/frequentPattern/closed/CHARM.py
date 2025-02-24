# CHARM is an algorithm to discover closed frequent patterns in a transactional database. Closed frequent patterns are patterns if there exists no superset that has the same support count as this original itemset . This algorithm employs depth-first search technique to find the complete set of closed frequent patterns in a transactional database.
#
# **Importing this algorithm into a python program**
#
#             from PAMI.frequentPattern.closed import CHARM as alg
#
#             iFile = 'sampleDB.txt'
#
#             minSup = 10  # can also be specified between 0 and 1
#
#             obj = alg.CHARM(iFile, minSup)
#
#             obj.mine()
#
#             frequentPatterns = obj.getPatterns()
#
#             print("Total number of Closed Frequent Patterns:", len(frequentPatterns))
#
#             obj.savePatterns(oFile)
#
#             Df = obj.getPatternsAsDataFrame()
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


from PAMI.frequentPattern.closed import abstract as _ab
from deprecated import deprecated


class CHARM(_ab._frequentPatterns):
    """
    **About this algorithm**

    :**Description**: CHARM is an algorithm to discover closed frequent patterns in a transactional database. Closed frequent patterns are patterns if there exists no superset that has the same support count as this original itemset. This algorithm employs depth-first search technique to find the complete set of closed frequent patterns in a transactional database.

    :**Reference**:  Mohammed J. Zaki and Ching-Jui Hsiao, CHARM: An Efficient Algorithm for Closed Itemset Mining,
                     Proceedings of the 2002 SIAM, SDM. 2002, 457-473, https://doi.org/10.1137/1.9781611972726.27

    :**Parameters**:    - **iFile** (*str or URL or dataFrame*) -- *Name of the Input file to mine complete set of frequent patterns.*
                        - **oFile** (*str*) -- *Name of the output file to store complete set of frequent patterns.*
                        - **minSup** (*int or float or str*) -- *The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.*
                        - **sep** (*str*) -- *This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.*

    :**Attributes**:    - **startTime** (*float*) -- *To record the start time of the mining process.*
                        - **endTime** (*float*) -- *To record the completion time of the mining process.*
                        - **finalPatterns** (*dict*) -- *Storing the complete set of patterns in a dictionary variable.*
                        - **memoryUSS** (*float*) -- *To store the total amount of USS memory consumed by the program.*
                        - **memoryRSS** (*float*) -- *To store the total amount of RSS memory consumed by the program.*
                        - **Database** (*list*) -- *To store the transactions of a database in list.*
                        - **mapSupport** (*Dictionary*) -- *To maintain the information of item and their frequency.*
                        - **tree** (*class*) -- *It represents the Tree class.*
                        - **itemSetCount** (*int*) -- *It represents the total no of patterns.*
                        - **tidList** (*dict*) -- *Stores the timestamps of an item.*
                        - **hashing** (*dict*) -- *Stores the patterns with their support to check for the closed property.*


    **Execution methods**

    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 CHARM.py <inputFile> <outputFile> <minSup>

      Example Usage:

      (.venv) $ python3 CHARM.py sampleDB.txt patterns.txt 10.0

    .. note:: minSup can be specified  in support count or a value between 0 and 1.


    **Calling from a python program**

    .. code-block:: python

            from PAMI.frequentPattern.closed import CHARM as alg

            iFile = 'sampleDB.txt'

            minSup = 10  # can also be specified between 0 and 1

            obj = alg.CHARM(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Closed Frequent Patterns:", len(frequentPatterns))

            obj.savePatterns(oFile)

            Df = obj.getPatternsAsDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)


    **Credits:**

    The complete program was written by P.Likhitha and revised by Tarun Sreepada under the supervision of Professor Rage Uday Kiran.

    """

    _startTime = float()
    _endTime = float()
    _minSup = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _tidList = {}
    _lno = 0
    _mapSupport = {}
    _hashing = {}
    _itemSetCount = 0
    _maxItemId = 0
    _tableSize = 10000
    _writer = None

    def _convert(self, value):
        """

        To convert the type of user specified minSup value

        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._lno * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._lno * value)
            else:
                value = int(value)
        return value

    def _creatingItemsets(self):
        """
        Storing the complete frequent patterns of the database/input file in a database variable
        """
        self._tidList = {}
        self._lno = 0
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()
                self._Database = [i.split(self._sep) for i in self._Database]
            else:
                print("The column name should be Transactions and each line should be separated by tab space or a seperator specified by the user")
            for i in self._Database:
                self._lno += 1
                for j in i:
                    if j not in self._tidList:
                        self._tidList[j] = [self._lno]
                    else:
                        self._tidList[j].append(self._lno)

        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    self._lno += 1
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    for j in temp:
                        if j not in self._tidList:
                            self._tidList[j] = [self._lno]
                        else:
                            self._tidList[j].append(self._lno)
            else:
                try:
                    with open(self._iFile, 'r') as f:
                        for line in f:
                            i = [i.rstrip() for i in line.split(self._sep)]
                            i = [x for x in i if x]
                            self._lno += 1
                            for j in i:
                                if j not in self._tidList:
                                    self._tidList[j] = [self._lno]
                                else:
                                    self._tidList[j].append(self._lno)
                except IOError:
                    print("File Not Found")
        self._minSup = self._convert(self._minSup)
        self._tidList = {k: set(v) for k, v in self._tidList.items() if len(v) >= self._minSup}

        # return keys based off the sum of their location appearances in the database
        _flist = [key for key, value in sorted(self._tidList.items(), key=lambda x: sum(x[1]), reverse=False)]
        return _flist

    def _calculate(self, tidSet):
        """

        To calculate the hashcode of pattern

        :param tidSet: the timestamps of a pattern
        :type tidSet: list
        :rtype: int
        """

        return abs(sum(tidSet)) % self._tableSize

    def _contains(self, itemSet, value, hashcode):
        """

        Check for the closed property(patterns with same support) by checking the hashcode(sum of timestamps),
        if hashcode key in hashing dict is none then returns a false, else returns with true.

        :param itemSet: frequent pattern
        :type itemSet: list
        :param value: support of the pattern
        :type value: int
        :param hashcode: calculated from the timestamps of pattern
        :type hashcode: int
        """
        if self._hashing.get(hashcode) is None:
            return False
        for i in self._hashing[hashcode]:
            itemSetx = i
            if value == self._hashing[hashcode][itemSetx] and set(itemSetx).issuperset(itemSet):
                return True
        return False

    def _save(self, prefix, suffix, tidSetx):
        """

        Check for the closed property (patterns with same support), if found deletes the subsets and stores
        supersets and also saves the patterns that satisfy the closed property

        :param prefix: the prefix of a pattern
        :type prefix: frequent item or pattern
        :param suffix: the suffix of a patterns
        :type suffix: list
        :param tidSetx: the timestamp of a patterns
        :type tidSetx: list
        """
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        prefix = list(set(prefix))
        prefix.sort()
        val = len(tidSetx)
        if val >= self._minSup:
            hashcode = self._calculate(tidSetx)
            if self._contains(prefix, val, hashcode) is False:
                sample = str()
                for i in prefix:
                    sample = sample + i + "\t"
                self._itemSetCount += 1
                self._finalPatterns[sample] = val
            if hashcode not in self._hashing:
                self._hashing[hashcode] = {tuple(prefix): val}
            else:
                self._hashing[hashcode][tuple(prefix)] = val

    def _processEquivalenceClass(self, prefix, itemSets, tidSets):
        """

        Equivalence class is followed  and check for the patterns which satisfies frequent properties.

        :param prefix:  main equivalence prefix
        :type prefix: frequent item or pattern
        :param itemSets: patterns which are items combined with prefix and satisfying the minSup
        :type itemSets: list
        :param tidSets: timestamps of the items in the argument itemSets
        :type tidSets: list
        """
        if len(itemSets) == 1:
            i = itemSets[0]
            tidI = tidSets[0]
            self._save(prefix, [i], tidI)
            return
        if len(itemSets) == 2:
            itemX = itemSets[0]
            tidSetX = tidSets[0]
            itemY = itemSets[1]
            tidSetY = tidSets[1]
            # y1 = list(set(tidSetX).intersection(tidSetY))
            y1 = tidSetX.intersection(tidSetY)
            if len(y1) >= self._minSup:
                suffix = []
                suffix += [itemX, itemY]
                suffix = list(set(suffix))
                self._save(prefix, suffix, y1)
            if len(y1) != len(tidSetX):
                self._save(prefix, [itemX], tidSetX)
            if len(y1) != len(tidSetY):
                self._save(prefix, [itemX], tidSetY)
            return
        for i in range(len(itemSets)):
            itemX = itemSets[i]
            if itemX is None:
                continue
            tidSetX = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetx = [itemX]
            for j in range(i + 1, len(itemSets)):
                itemY = itemSets[j]
                if itemY is None:
                    continue
                tidSetY = tidSets[j]
                y = tidSetX.intersection(tidSetY)
                if len(y) < self._minSup:
                    continue
                if len(tidSetX) == len(tidSetY) and len(y) == len(tidSetX):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    itemSetx.append(itemY)
                elif len(tidSetY) > len(tidSetX) == len(y):
                    itemSetx.append(itemY)
                elif len(tidSetX) > len(tidSetY) and len(y) == len(tidSetY):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    classItemSets.append(itemY)
                    classTidSets.append(y)
                else:
                    classItemSets.append(itemY)
                    classTidSets.append(y)
            if len(classItemSets):
                newPrefix = list(set(itemSetx)) + prefix
                self._processEquivalenceClass(newPrefix, classItemSets, classTidSets)
                self._save(prefix, list(set(itemSetx)), tidSetX)

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Mining process will start from here by extracting the frequent patterns from the database. It performs prefix
        equivalence to generate the combinations and closed frequent patterns.
        """
        self.mine()

    def mine(self):
        """
        Mining process will start from here by extracting the frequent patterns from the database. It performs prefix
        equivalence to generate the combinations and closed frequent patterns.
        """
        self._startTime = _ab._time.time()
        _plist = self._creatingItemsets()
        self._finalPatterns = {}
        self._hashing = {}
        for i in range(len(_plist)):
            itemX = _plist[i]
            if itemX is None:
                continue
            tidSetx = self._tidList[itemX]
            itemSetx = [itemX]
            itemSets = []
            tidSets = []
            for j in range(i + 1, len(_plist)):
                itemY = _plist[j]
                if itemY is None:
                    continue
                tidSetY = self._tidList[itemY]
                y1 = tidSetx.intersection(tidSetY)
                if len(y1) < self._minSup:
                    continue
                if len(tidSetx) == len(tidSetY) and len(y1) == len(tidSetx):
                    _plist.insert(j, None)
                    itemSetx.append(itemY)
                elif len(tidSetY) > len(tidSetx) == len(y1):
                    itemSetx.append(itemY)
                elif len(tidSetx) > len(tidSetY) and len(y1) == len(tidSetY):
                    _plist.insert(j, None)
                    itemSets.append(itemY)
                    tidSets.append(y1)
                else:
                    itemSets.append(itemY)
                    tidSets.append(y1)
            if len(itemSets) > 0:
                self._processEquivalenceClass(itemSetx, itemSets, tidSets)
            self._save(None, itemSetx, tidSetx)
        print("Closed Frequent patterns were generated successfully using CHARM algorithm")
        self._endTime = _ab._time.time()
        _process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = _process.memory_full_info().uss
        self._memoryRSS = _process.memory_info().rss

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

        # dataframe = {}
        # data = []
        # for a, b in self._finalPatterns.items():
        #     data.append([a.replace('\t', ' '), b])
        #     dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])

        dataframe = _ab._pd.DataFrame(list([[x.replace('\t', ' '), y] for x,y in self._finalPatterns.items()]), columns=['Patterns', 'Support'])

        return dataframe

    def save(self, outFile):
        """

        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csvfile
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
        This function is used to print the results
        """
        print("Total number of Closed Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = CHARM(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = CHARM(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _ap.mine()
        print("Total number of Closed Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
