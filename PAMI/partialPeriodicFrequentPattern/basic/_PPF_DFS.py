# PPF_DFS is algorithm to mine the partial periodic frequent patterns.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#     from PAMI.partialPeriodicFrequentPattern.basic import PPF_DFS as alg
#
#     obj = alg.PPF_DFS(iFile, minSup)
#
#     obj.mine()
#
#     frequentPatterns = obj.getPatterns()
#
#     print("Total number of Frequent Patterns:", len(frequentPatterns))
#
#     obj.save(oFile)
#
#     Df = obj.getPatternInDataFrame()
#
#     memUSS = obj.getMemoryUSS()
#
#     print("Total Memory in USS:", memUSS)
#
#     memRSS = obj.getMemoryRSS()
#
#     print("Total Memory in RSS", memRSS)
#
#     run = obj.getRuntime()
#
#     print("Total ExecutionTime in seconds:", run)
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

from abc import ABC

from PAMI.partialPeriodicFrequentPattern.basic.abstract import *
#import deprecated

class PPF_DFS(partialPeriodicPatterns, ABC):
    """
    :Description:   PPF_DFS is algorithm to mine the partial periodic frequent patterns.

    :References:    (Has to be added)

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  minSup: str:
                   The user can specify minSup either in count or proportion of database size.
    :param  minPR: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.
    :param  maxPer: str:
                   Controls the maximum number of transactions in which any two items within a pattern can reappear.

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            input file path
        oFile : file
            output file name
        minSup : float
            user defined minSup
        maxPer : float
            user defined maxPer
        minPR : float
            user defined minPR
        tidlist : dict
            it stores tids each item
        last : int
            it represents last time stamp in database
        lno : int
            number of line in database
        mapSupport : dict
            to maintain the information of item and their frequency
        finalPatterns : dict
            it represents to store the patterns
        runTime : float
            storing the total runtime of the mining process
        memoryUSS : float
            storing the total amount of USS memory consumed by the program
        memoryRSS : float
            storing the total amount of RSS memory consumed by the program

    :Methods:

        getPer_Sup(tids)
            caluclate ip / (sup+1)
        getPerSup(tids)
            caluclate ip
        oneItems(path)
            scan all lines in database
        save(prefix,suffix,tidsetx)
            save prefix pattern with support and periodic ratio
        Generation(prefix, itemsets, tidsets)
            Userd to implement prefix class equibalence method to generate the periodic patterns recursively
        mine()
            Mining process will start from here
        getPartialPeriodicPatterns()
            Complete set of patterns will be retrieved with this function
        save(ouputFile)
            Complete set of frequent patterns will be loaded in to an ouput file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to an ouput file
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function

    **Executing code on Terminal:**
    ----------------------------------
        Format:
            >>> python3 PPF_DFS.py <inputFile> <outputFile> <minSup> <maxPer> <minPR>

        Examples:
            >>> python3 PPF_DFS.py sampleDB.txt patterns.txt 10 10 0.5

    **Sample run of the importing code:**
    ---------------------------------------
    ...     code-block:: python

            from PAMI.partialPeriodicFrequentpattern.basic import PPF_DFS as alg

            obj = alg.PPF_DFS(iFile, minSup)

            obj.mine()

            frequentPatterns = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits:**
    -------------
        The complete program was written by S. Nakamura  under the supervision of Professor Rage Uday Kiran.\n

    """

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

    def __creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self.__Database = []
        if isinstance(self._partialPeriodicPatterns__iFile, pd.DataFrame):
            timeStamp, data = [], []
            if self._partialPeriodicPatterns__iFile.empty:
                print("its empty..")
            iList = self._partialPeriodicPatterns__iFile.columns.values.tolist()
            if 'ts' or 'TS' in iList:
                timeStamp = self._partialPeriodicPatterns__iFile['timeStamps'].tolist()
            if 'Transactions' in iList:
                data = self._partialPeriodicPatterns__iFile['Transactions'].tolist()
            if 'Patterns' in iList:
                data = self._partialPeriodicPatterns__iFile['Patterns'].tolist()
            for iList in range(len(data)):
                tr = [timeStamp[iList]]
                tr.append(data[iList])
                self.__Database.append(tr)
            self.__lno = len(self.__Database)

        if isinstance(self._partialPeriodicPatterns__iFile, str):
            if validators.url(self._partialPeriodicPatterns__iFile):
                data = urlopen(self._partialPeriodicPatterns__iFile)
                for line in data:
                    self.__lno += 1
                    line = line.decode("utf-8")
                    temp = [i_.rstrip() for i_ in line.split(self._partialPeriodicPatterns__sep)]
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
    

    def __getPer_Sup(self, tids):
        """
        calculate ip / (sup+1)

        :param tids: it represent tid list
        :type tids: list
        :return: ip / (sup+1)
        """
        # print(lno)
        tids = list(set(tids))
        tids.sort()
        per = 0
        sup = 0
        cur = 0
        if len(tids) == 0:
            return 0
        if abs(0 - tids[0]) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        for j in range(len(tids) - 1):
            k = j + 1
            per = abs(tids[k] - tids[j])
            if per <= self._partialPeriodicPatterns__maxPer:
                sup += 1
            cur = tids[j]
        if abs(self.__last - tids[len(tids) - 1]) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        if sup == 0:
            return 0
        return sup / (len(tids) + 1)

    def _partialPeriodicPatterns__getPerSup(self, tids):
        """
        calculate ip of a pattern

        :param tids: tid list of the pattern
        :type tids: list
        :return: ip
        """
        # print(lno)
        tids = list(set(tids))
        tids.sort()
        per = 0
        sup = 0
        cur = 0
        if len(tids) == 0:
            return 0
        if abs(0 - tids[0]) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        for j in range(len(tids) - 1):
            i = j + 1
            per = abs(tids[i] - tids[j])
            if per <= self._partialPeriodicPatterns__maxPer:
                sup += 1
        if abs(tids[len(tids) - 1] - self.__last) <= self._partialPeriodicPatterns__maxPer:
            sup += 1
        if sup == 0:
            return 0
        return sup

    def __convert(self, value):
        """
        to convert the type of user specified minSup value

        :param value: user specified minSup value
        :return: converted type
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

    def __oneItems(self, path):
        """
        scan all lines of database and create support list

        :param path: it represents input file name
        :return: support list each item
        """
        id1 = 0
        self._partialPeriodicPatterns__maxPer = self.__convert(self._partialPeriodicPatterns__maxPer)
        self._partialPeriodicPatterns__minSup = self.__convert(self._partialPeriodicPatterns__minSup)
        self._partialPeriodicPatterns__minPR = float(self._partialPeriodicPatterns__minPR)
        for line in self.__Database:
            self.__lno += 1
            s = line
            n = int(s[0])
            self.__last = max(self.__last, n)
            for k_ in range(1, len(s)):
                si = s[k_]
                if abs(0 - n) <= self._partialPeriodicPatterns__maxPer:
                    if si not in self.__mapSupport:
                        self.__mapSupport[si] = [1, 1, n]
                        self.__tidlist[si] = [n]
                    else:
                        lp = abs(n - self.__mapSupport[si][2])
                        if lp <= self._partialPeriodicPatterns__maxPer:
                            self.__mapSupport[si][0] += 1
                        self.__mapSupport[si][1] += 1
                        self.__mapSupport[si][2] = n
                        self.__tidlist[si].append(n)
                else:
                    if si not in self.__mapSupport:
                        self.__mapSupport[si] = [0, 1, n]
                        self.__tidlist[si] = [n]
                    else:
                        lp = abs(n - self.__mapSupport[si][2])
                        if lp <= self._partialPeriodicPatterns__maxPer:
                            self.__mapSupport[si][0] += 1
                        self.__mapSupport[si][1] += 1
                        self.__mapSupport[si][2] = n
                        self.__tidlist[si].append(n)
        for x, y in self.__mapSupport.items():
            lp = abs(self.__last - self.__mapSupport[x][2])
            if lp <= self._partialPeriodicPatterns__maxPer:
                self.__mapSupport[x][0] += 1
        self.__mapSupport = {k: [v[1], v[0]] for k, v in self.__mapSupport.items() if
                             v[1] >= self._partialPeriodicPatterns__minSup and v[0] / (self._partialPeriodicPatterns__minSup + 1) >= self._partialPeriodicPatterns__minPR}
        plist = [key for key, value in sorted(self.__mapSupport.items(), key=lambda x_: (x_[1][0], x_[0]), reverse=True)]
        return plist

    def __save(self, prefix, suffix, tidsetx):
        """
        sava prefix patterns with support and periodic ratio
        :param prefix: prefix patterns
        :type prefix: list
        :param suffix: it represents suffix itemsets
        :type suffix: list
        :param tidsetx: it represents prefix tids
        :type tidsetx: list
        """
        tidsetx = list(set(tidsetx))
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        val = self._partialPeriodicPatterns__getPerSup(tidsetx)
        val1 = self.__getPer_Sup(tidsetx)
        if len(tidsetx) >= self._partialPeriodicPatterns__minSup and val / (len(tidsetx) + 1) >= self._partialPeriodicPatterns__minPR:
            self._partialPeriodicPatterns__finalPatterns[tuple(prefix)] = [len(tidsetx), val1]

    def __Generation(self, prefix, itemsets, tidsets):
        """
        here equibalence class is followed amd checks from the patterns generated for periodic frequent patterns.
        :param prefix: main equivalence prefix
        :type prefix: periodic-frequent item or pattern
        :param itemsets: patterns which are items combined with prefix and satisfy the periodicity
                        and frequent with their time stamps
        :type itemsets: list
        :param tidsets: time stamps of the items in the argument itemSets
        :type tidsets: list
        """
        if len(itemsets) == 1:
            item_ = itemsets[0]
            tidi = tidsets[0]
            self.__save(prefix, [item_], tidi)
            return
        for item_ in range(len(itemsets)):
            itemx = itemsets[item_]
            if itemx is None:
                continue
            tidsetx = tidsets[item_]
            classItemsets = []
            classtidsets = []
            itemsetx = [itemx]
            for j in range(item_ + 1, len(itemsets)):
                itemj = itemsets[j]
                tidsetj = tidsets[j]
                y = list(set(tidsetx) & set(tidsetj))
                val = self._partialPeriodicPatterns__getPerSup(y)
                if len(y) >= self._partialPeriodicPatterns__minSup and val / (self._partialPeriodicPatterns__minSup + 1) >= self._partialPeriodicPatterns__minPR:
                    classItemsets.append(itemj)
                    classtidsets.append(y)
            newprefix = list(set(itemsetx)) + prefix
            self.__Generation(newprefix, classItemsets, classtidsets)
            self.__save(prefix, list(set(itemsetx)), tidsetx)

    def startMine(self):
        self.mine()

    def mine(self):
        """
        Main program start with extracting the periodic frequent items from the database and
        performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.
        """
        self.__path = self._partialPeriodicPatterns__iFile
        self._partialPeriodicPatterns__startTime = time.time()
        self.__creatingItemSets()
        plist = self.__oneItems(self.__path)
        self._partialPeriodicPatterns__finalPatterns = {}
        for i__ in range(len(plist)):
            itemx = plist[i__]
            tidsetx = self.__tidlist[itemx]
            itemsetx = [itemx]
            itemsets = []
            tidsets = []
            for j in range(i__ + 1, len(plist)):
                itemj = plist[j]
                tidsetj = self.__tidlist[itemj]
                y1 = list(set(tidsetx) & set(tidsetj))
                val = self._partialPeriodicPatterns__getPerSup(y1)
                if len(y1) >= self._partialPeriodicPatterns__minSup and val / (self._partialPeriodicPatterns__minSup + 1) >= self._partialPeriodicPatterns__minPR:
                    itemsets.append(itemj)
                    tidsets.append(y1)
            self.__Generation(itemsetx, itemsets, tidsets)
            self.__save(None, itemsetx, tidsetx)
        self._partialPeriodicPatterns__endTime = time.time()
        self.__runTime = self._partialPeriodicPatterns__endTime - self._partialPeriodicPatterns__startTime
        process = psutil.Process(os.getpid())
        self._partialPeriodicPatterns__memoryUSS = float()
        self._partialPeriodicPatterns__memoryRSS = float()
        self._partialPeriodicPatterns__memoryUSS = process.memory_full_info().uss
        self._partialPeriodicPatterns__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._partialPeriodicPatterns__memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process
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
        Complete set of frequent patterns will be loaded in to an output file
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
        """ Function to send the set of frequent patterns after completion of the mining process
        :return: returning frequent patterns
        :rtype: dict
        """
        return self._partialPeriodicPatterns__finalPatterns

    def printResults(self):
        """
        this function is used to print the results
        """
        print("Total number of Partial Periodic Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())

if __name__ == '__main__':
    ap = str()
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        if len(sys.argv) == 7:
            ap = PPF_DFS(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        if len(sys.argv) == 6:
            ap = PPF_DFS(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])
        ap.mine()
        print("Total number of Frequent Patterns:", len(ap.getPatterns()))
        ap.save(sys.argv[2])
        print("Total Memory in USS:", ap.getMemoryUSS())
        print("Total Memory in RSS", ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", ap.getRuntime())
    else:
        for i in [350]:
            _ap = PPF_DFS('/Users/tarunsreepada/Downloads/temporal_T10I4D100K.csv', i, 300, 0.7, '\t')
            _ap.mine()
            print("Total number of Maximal Partial Periodic Patterns:", len(_ap.getPatterns()))
            # _ap.save('/Users/Likhitha/Downloads/output.txt')
            _ap.save('/Users/tarunsreepada/Downloads/output3.txt')
            print("Total Memory in USS:", _ap.getMemoryUSS())
            print("Total Memory in RSS", _ap.getMemoryRSS())
            print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")


