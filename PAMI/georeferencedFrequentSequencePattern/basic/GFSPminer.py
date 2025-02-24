# GFSPminer is one of the fundamental algorithm to discover georeferenced sequential frequent patterns in a transactional database.
# This program employs GFSPminer property (or downward closure property) to  reduce the search space effectively.
# This algorithm employs breadth-first search technique when 1-2 length patterns and depth-first search when above 3 length patterns to find the complete set of frequent patterns in a
# transactional database.
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.georeferencedFrequentSequencedPattern.basic import GFSPminer as alg
#
#             obj=alg.GFSPminer("input.txt","Neighbours.txt",35)
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of Spatial High-Utility Patterns:", len(Patterns))
#
#             obj.save("output")
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

from PAMI.georeferencedFrequentSequencePattern.basic import abstract as _ab
import sys
from deprecated import deprecated

sys.setrecursionlimit(10000)


class GFSPminer(_ab._GeorefarencedFequentialPatterns):
    """
    :Description:   GFSPminer is one of the fundamental algorithm to discover georeferenced sequential frequent patterns in a transactional database.
                    This program employs GFSPminer property (or downward closure property) to  reduce the search space effectively.
                    This algorithm employs breadth-first search technique when 1-2 length patterns and depth-first search when above 3 length patterns to find the complete set of frequent patterns in a
                    transactional database.

    :Reference:   Suzuki Shota and Rage Uday kiran: towards efficient discovery of spatially interesting patterns in geo-referenced sequential databases: To be appeared in SSDBM 2023:

    :param  iFile: str :
                   Name of the Input file to mine complete set of Geo-referenced frequent sequence patterns
    :param  oFile: str :
                   Name of the output file to store complete set of Geo-referenced frequent sequence patterns
    :param  minSup: int or float or str :
                   The user can specify minSup either in count or proportion of database size. If the program detects the data type of minSup is integer, then it treats minSup is expressed in count. Otherwise, it will be treated as float.
    :param maxPer: float :
                   The user can specify maxPer in count or proportion of database size. If the program detects the data type of maxPer is integer, then it treats maxPer is expressed in count.
    :param nFile: str :
                   Name of the input file to mine complete set of Geo-referenced frequent sequence patterns
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.


    :Attributes:

        iFile : str
            Input file name or path of the input file
        oFile : str
            Name of the output file or the path of output file
        nFile: str
            Neighbourhood file name
        minSup: float or int or str
            The user can specify minSup either in count or proportion of database size.
            If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
            Otherwise, it will be treated as float.
            Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.
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
        Database : list
            To store the transactions of a database in list
        _xLenDatabase : dict
            To store the datas in different sequence separated by sequence, rownumber, length.
        _xLenDatabaseSame : dict
            To store the datas in same sequence separated by sequence, rownumber, length.
        _NeighboursMap : dict
            To store the neighbors
        _failPatterns : dict
            To store the failed patterns

    :Methods:

        mine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        Prune(startLine)
            check the subsequence from sequence(startLine)
        make1LenDatabase()
            find 1 length frequent pattern from database
        make2LenDatabase()
            find 1 length frequent pattern by convene two 1 len patterns
        makexLenData(x)
            find x-1 length frequent pattern by convene two x len patterns
        makexLenDatabase(rowLen, bs, latestWord)
            To make "rowLen" length frequent patterns from pattern which latest word is in same seq  by joining "rowLen"-1 length patterns by depth-first search technique  and update xlenDatabase to sequential database
        makeSame(rowLen, bs, latestWord, latestWord2)
                to check the pattern is frequent or not (ex a-bc from a-c and a-b )
        makeFaster(rowLen, bs, latestWord, latestWord2):
                to check the pattern is frequent or not (ex a-b-c from a-c a-b)
        makeLater(rowLen, bs, latestWord, latestWord2):
                to check the pattern is frequent or not (ex ac-b from a-b ac)
        makeSame2(rowLen, bs, latestWord, latestWord2):
                to check the pattern is frequent or not (ex a-bc from a-c ab)
        makeSame3(rowLen, bs, latestWord, latestWord2):
                to check the pattern is frequent or not (ex abc from ac ab)
        makexLenDatabaseSame(rowLen, bs, latestWord):
                To make 3 or more length frequent patterns from pattern which latest word is in different seq  by depth-first search technique  and update xlenDatabase to sequential database
        makeNextRow(bs, latestWord, latestWord2):
                   To make pattern row when two patterns have latest word in different sequence
        makeNextRowSame(bs, latestWord, latestWord2):
                    To make pattern row when one pattern have latestWord1 in different sequence and other(latestWord2) in same
        makeNextRowSame2(bs, latestWord, latestWord2):
                    To make pattern row when two patterns have latest word in same sequence
        makeNextRowSame3(bs, latestWord, latestWord2):
              To make pattern row when two patterns have latest word in different sequence and both latest word is in same sequence


    **Executing the code on terminal:**
    ------------------------------------

    .. code-block:: console

      Format:

      (.venv) $ python3 GFSPminer.py <inputFile> <neighborFile> <minSup> (<separator>)

      Example Usage:

      (.venv) $ python3 GFSPminer.py sampleDB.txt sampleNeighbor.txt 10.0

    .. note:: minSup will be considered in percentage of database transactions


    **Sample run of the importing code:**
    --------------------------------------

             import GFSPm as gf

             _ap = gf.GFSPminer('inputFile',"neighborFile",minSup,"separator")

             _ap.mine()

             _Patterns = _ap.getPatterns()

             _memUSS = _ap.getMemoryUSS()

             print("Total Memory in USS:", _memUSS)

             _memRSS = _ap.getMemoryRSS()

             print("Total Memory in RSS", _memRSS)

             _run = _ap.getRuntime()

             print("Total ExecutionTime in ms:", _run)

             print("Total number of Frequent Patterns:", len(_Patterns))

             print("Error! The number of input parameters do not match the total number of parameters provided")

             _ap.save("priOut3.txt")

    **Credits:**
    --------------
    The complete program was written by Shota Suzuki  under the supervision of Professor Rage Uday Kiran.
    """

    _minSup = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _nFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _xLenDatabase = {}
    _xLenDatabaseSame = {}
    _NeighboursMap = {}
    _failPatterns = {}

    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []

        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            temp2 = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()
            if "tid" in i:
                temp2 = self._iFile[''].tolist()
            addList = [temp[0]]
            for k in range(len(temp) - 1):
                if temp2[k] == temp[k + 1]:
                    addList.append(temp[k + 1])
                else:
                    self._Database.append(addList)
                    addList = [temp[k + 1]]
            self._Database.append(addList)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    temp.pop()
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split('-1')]
                            temp = [x for x in temp if x]
                            temp.pop()

                            seq = []
                            for i in temp:
                                k = -2
                                if len(i) > 1:
                                    seq.append(list(sorted(set(i.split()))))

                                else:
                                    seq.append(i)

                            self._Database.append(seq)

                except IOError:
                    print("File Not Found")
                    quit()

    def _convert(self, value):
        """
        To convert the user specified minSup value

        :param value: user specified minSup value
        :type value: int or float or str
        :return: converted type
        :rtype: float
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def _mapNeighbours(self):
        """
        A function to map items to their Neighbours
        """
        self._NeighboursMap = {}
        if isinstance(self._nFile, _ab._pd.DataFrame):
            data, items = [], []
            if self._nFile.empty:
                print("its empty..")
            i = self._nFile.columns.values.tolist()
            if 'item' in i:
                items = self._nFile['items'].tolist()
            if 'Neighbours' in i:
                data = self._nFile['Neighbours'].tolist()
            for k in range(len(items)):
                self._NeighboursMap[items[k]] = data[k]
            # print(self.Database)
        if isinstance(self._nFile, str):
            if _ab._validators.url(self._nFile):
                data = _ab._urlopen(self._nFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._NeighboursMap[temp[0]] = temp[1:]
            else:
                try:
                    with open(self._nFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._NeighboursMap[temp[0]] = temp[1:]
                except IOError:
                    print("File Not Found")
                    quit()

    def Prune(self, startline):
        """
        To check k-1 length patterns are not failed.
        :param startline: start line of the pattern
        :type startline: int
        """
        for i in range(len(startline) - 1):
            if startline[i] != -1 and startline[i] != -2:
                copyline = [j for j in startline]
                if i == 0 and copyline[i + 1] == -1:
                    copyline.remove(copyline[i])
                    copyline.remove(copyline[i])
                elif copyline[i - 1] == -1 and copyline[i + 1] == -1:
                    copyline.remove(copyline[i])
                    copyline.remove(copyline[i])
                else:
                    copyline.remove(copyline[i])
                if str(tuple(copyline)) in self._failPatterns.keys():
                    return 0

        return 1

    def make1LenDatabase(self):
        """
        To make 1 length frequent patterns by breadth-first search technique   and update Database to sequential database
        """

        idDatabase = {}
        alreadyInData = []
        lineNumber = 0
        alreadyInLine = {}
        for line in self._Database:
            seqNumber = 0
            for seq in line:

                for data in seq:
                    if data in alreadyInData:
                        if lineNumber in alreadyInLine[data]:
                            idDatabase[data][lineNumber].append(seqNumber)
                        else:
                            idDatabase[data][lineNumber] = []
                            idDatabase[data][lineNumber].append(seqNumber)
                            alreadyInLine[data].append(lineNumber)
                    else:
                        idDatabase[data] = {}
                        idDatabase[data][lineNumber] = []
                        idDatabase[data][lineNumber].append(seqNumber)
                        alreadyInData.append(data)
                        alreadyInLine[data] = []
                        alreadyInLine[data].append(lineNumber)

                seqNumber += 1
            lineNumber += 1

        newDatabase = {i: idDatabase[i] for i in idDatabase.keys()}
        for key in idDatabase.keys():
            if len(idDatabase[key].keys()) < self._minSup:
                newDatabase.pop(key)
            else:
                self._finalPatterns[str((key, -1))] = len(idDatabase[key].keys())
        self._Database = newDatabase

    def make2LenDatabase(self):
        """
        To make 2 length frequent patterns by joining two one length patterns by breadth-first search technique  and update xlenDatabase to sequential database
        """
        self._xLenDatabase = {}
        keyList = [i for i in self._Database.keys()]
        nextDatabase = {i: {} for i in self._Database.keys()}
        nextDatabaseSame = {i: {} for i in self._Database.keys()}
        keyNumber = -1
        for key1 in keyList:
            keyNumber += 1
            for key2 in keyList[keyNumber:]:
                if key1 != key2:
                    if key1 in self._NeighboursMap.keys() and key2 in self._NeighboursMap.keys():
                        if key1 in self._NeighboursMap[key2]:

                            if len(self._Database[key1].keys()) >= len(self._Database[key1].keys()):
                                nextDatabase[key1][key2] = {}
                                nextDatabase[key2][key1] = {}
                                nextDatabaseSame[key1][key2] = {}

                                for seq in self._Database[key2].keys():
                                    if seq in self._Database[key1].keys():
                                        x = [i for i in self._Database[key1][seq] if i > self._Database[key2][seq][0]]
                                        if len(x) != 0:
                                            nextDatabase[key2][key1][seq] = x
                                        x = [i for i in self._Database[key2][seq] if i > self._Database[key1][seq][0]]
                                        if len(x) != 0:
                                            nextDatabase[key1][key2][seq] = x
                                        x = list(
                                            sorted(set(self._Database[key1][seq]) & set(self._Database[key2][seq])))
                                        if len(x) != 0:
                                            nextDatabaseSame[key1][key2][seq] = x
                            else:
                                nextDatabase[key1][key2] = {}
                                nextDatabase[key2][key1] = {}
                                nextDatabaseSame[key1][key2] = {}

                                for seq in self._Database[key1].keys():
                                    x = [i for i in self._Database[key1][seq] if
                                         i > self._Database[key2][seq][0]]
                                    if len(x) != 0:
                                        nextDatabase[key2][key1][seq] = 0
                                    x = [i for i in self._Database[key2][seq] if
                                         i > self._Database[key1][seq][0]]
                                    if len(x) != 0:
                                        nextDatabase[key1][key2][seq] = x
                                    x = list(
                                        sorted(set(self._Database[key1][seq]) & set(self._Database[key2][seq])))
                                    if len(x) != 0:
                                        nextDatabaseSame[key1][key2][seq] = x
                else:
                    nextDatabase[key1][key2] = {}
                    for seq in self._Database[key2].keys():
                        if len(self._Database[key1][seq]) >= 2:
                            nextDatabase[key1][key2][seq] = self._Database[key2][seq][1:]
        self._xLenDatabase[2] = {tuple([i]): {} for i in nextDatabase.keys()}
        for key1 in nextDatabase.keys():
            for key2 in nextDatabase[key1].keys():
                if len(nextDatabase[key1][key2].keys()) >= self._minSup:
                    self._finalPatterns[str((key1, -1, key2, -1))] = len(nextDatabase[key1][key2].keys())
                    self._xLenDatabase[2][tuple([key1])][key2] = nextDatabase[key1][key2]
                else:
                    self._failPatterns[str((key1, -1, key2, -1))] = len(nextDatabase[key1][key2].keys())
        self._xLenDatabaseSame[2] = {tuple([i]): {} for i in nextDatabaseSame.keys()}
        for key1 in nextDatabaseSame.keys():
            for key2 in nextDatabaseSame[key1].keys():
                if len(nextDatabaseSame[key1][key2].keys()) >= self._minSup:
                    self._finalPatterns[str((key1, key2, -1))] = len(nextDatabaseSame[key1][key2].keys())
                    self._xLenDatabaseSame[2][tuple([key1])][key2] = {i: nextDatabaseSame[key1][key2][i] for i in
                                                                      nextDatabaseSame[key1][key2].keys()}
                    self._xLenDatabaseSame[2][tuple([key2])][key1] = {i: nextDatabaseSame[key1][key2][i] for i in
                                                                      nextDatabaseSame[key1][key2].keys()}
                else:
                    self._failPatterns[str((key1, key2, -1))] = len(nextDatabase[key1][key2].keys())

    def makexLenData(self, x):
        """
        To call each x length patterns to make x+1 length frequent patterns depth-first search technique

        :param x: User specified x value to make it as Sequential Database
        :type x: int
        """
        for i in self._xLenDatabase[x].keys():
            for k in self._xLenDatabase[x][i].keys():
                self.makexLenDatabase(x, i, k)
                if len(self._xLenDatabase[x + 1]) > 0 or len(self._xLenDatabaseSame[x + 1]) > 0:
                    self.makexLenData(x + 1)
                    self._xLenDatabase[x + 1] = {}
                    self._xLenDatabaseSame[x + 1] = {}

        for i in self._xLenDatabaseSame[x].keys():
            for k in self._xLenDatabaseSame[x][i].keys():
                self.makexLenDatabaseSame(x, i, k)
                if len(self._xLenDatabaseSame[x + 1]) > 0 or len(self._xLenDatabase[x + 1]) > 0:
                    self.makexLenData(x + 1)
                    self._xLenDatabaseSame[x + 1] = {}
                    self._xLenDatabase[x + 1] = {}

    def makexLenDatabase(self, rowLen, bs, latestWord):
        """
        To make "rowLen" length frequent patterns from pattern which the latest word is in same seq  by joining "rowLen"-1 length patterns by depth-first search technique  and update xlenDatabase to sequential database

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        """
        if rowLen + 1 not in self._xLenDatabase:
            self._xLenDatabase[rowLen + 1] = {}
            self._xLenDatabaseSame[rowLen + 1] = {}

        for latestWord2 in self._xLenDatabase[rowLen][bs].keys():
            if latestWord != latestWord2:
                if latestWord in self._NeighboursMap[latestWord2]:
                    nextRow, nextbs, nextlate = self.makeNextRowSame3(bs, latestWord, latestWord2)
                    if self.Prune(list(nextRow)) == 1:
                        self.makeSame(rowLen, bs, latestWord, latestWord2)
                    nextRow, nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                    if self.Prune(list(nextRow)) == 1:
                        self.makeLater(rowLen, bs, latestWord, latestWord2)
                    nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                    if self.Prune(list(nextRow)) == 1:
                        self.makeFaster(rowLen, bs, latestWord, latestWord2)



            else:
                _next = {}
                for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                    if len(self._xLenDatabase[rowLen][bs][latestWord][seq]) >= 2:
                        _next[seq] = self._xLenDatabase[rowLen][bs][latestWord][seq][1:]
                if len(_next) >= self._minSup:
                    nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                    if str(nextRow) not in self._finalPatterns.keys():
                        if nextbs not in self._xLenDatabase[rowLen + 1]:
                            self._xLenDatabase[rowLen + 1][nextbs] = {}
                        self._finalPatterns[str(nextRow)] = len(_next)
                        self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
                    else:
                        if nextbs not in self._xLenDatabase[rowLen + 1]:
                            self._xLenDatabase[rowLen + 1][nextbs] = {}
                        self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
                else:
                    nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                    self._failPatterns[str(nextRow)] = len(_next)
        if bs in self._xLenDatabaseSame[rowLen]:
            for latestWord2 in self._xLenDatabaseSame[rowLen][bs]:
                if latestWord in self._NeighboursMap[latestWord2]:
                    nextRow, nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                    if self.Prune(nextRow) == 1:
                        self.makeSame2(rowLen, bs, latestWord, latestWord2)

    def makeSame(self, rowLen, bs, latestWord, latestWord2):
        """
        to check the pattern is frequent or not (ex a-bc from a-c and a-b )

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs: patterns without the latest one
        :type bs: int
        :param latestWord: latest word of patterns
        :type latestWord: str
        :param latestWord2: latest word of other previous pattern in different sequence
        :type latestWord2: str

        """
        if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(
                self._xLenDatabase[rowLen][bs][latestWord2].keys()):
            nextSame = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                        x = list(sorted(set(self._xLenDatabase[rowLen][bs][latestWord][seq]) & set(
                            self._xLenDatabase[rowLen][bs][latestWord2][seq])))
                        if len(x) != 0:
                            nextSame[seq] = x
            if len(nextSame) >= self._minSup:
                nextRow, nextbs, nextlste = self.makeNextRowSame3(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(nextSame)
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextlste] = {i: nextSame[i] for i in nextSame}
                else:
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextlste] = {i: nextSame[i] for i in nextSame}
            else:
                nextRow, nextbs, nextlste = self.makeNextRowSame3(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(nextSame)


        else:
            nextSame = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                        x = list(sorted(set(self._xLenDatabase[rowLen][bs][latestWord][seq]) & set(
                            self._xLenDatabase[rowLen][bs][latestWord2][seq])))
                        if len(x) != 0:
                            nextSame[seq] = x
            if len(nextSame) >= self._minSup:
                nextRow, nextbs, nextlate = self.makeNextRowSame3(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(nextSame)
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextlate] = {i: nextSame[i] for i in nextSame}
                else:
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextlate] = {i: nextSame[i] for i in nextSame}
            else:
                nextRow, nextbs, nextlate = self.makeNextRowSame3(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(nextSame)

    def makeFaster(self, rowLen, bs, latestWord, latestWord2):
        """
        To check the pattern is frequent or not (ex a-b-c from a-c a-b)

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs: patterns without the latest one
        :type bs: int
        :param latestWord: latest word of patterns
        :type latestWord: str
        :param latestWord2: latest word of other previous pattern in different sequence
        :type latestWord2: str
        """
        if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(
                self._xLenDatabase[rowLen][bs][latestWord2].keys()):
            _next = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord2][seq] if
                             i > self._xLenDatabase[rowLen][bs][latestWord][seq][0]]
                        if len(x) != 0:
                            _next[seq] = x
            if len(_next) >= self._minSup:
                nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    self._finalPatterns[str(nextRow)] = len(_next)
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(_next)

        else:
            _next = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord2][seq] if
                             i > self._xLenDatabase[rowLen][bs][latestWord][seq][0]]
                        if len(x) != 0:
                            _next[seq] = x
            if len(_next) >= self._minSup:
                nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(_next)
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(_next)

    def makeLater(self, rowLen, bs, latestWord, latestWord2):
        """
        To check the pattern is frequent or not (ex ac-b from a-b ac)

        :param rowLen : row length of patterns.
        :type rowLen: int
        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """

        if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(
                self._xLenDatabase[rowLen][bs][latestWord2].keys()):
            next2 = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:

                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord][seq] if
                             i > self._xLenDatabase[rowLen][bs][latestWord2][seq][0]]
                        if len(x) != 0:
                            next2[seq] = x
            if len(next2) >= self._minSup:
                nextRow, nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(next2)
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: next2[i] for i in next2}
                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: next2[i] for i in next2}
            else:
                nextRow, nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                self._failPatterns[str(nextRow)] = len(next2)

        else:

            next2 = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                    if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and \
                            self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord][seq] if
                             i > self._xLenDatabase[rowLen][bs][latestWord2][seq][0]]
                        if len(x) != 0:
                            next2[seq] = x
            if len(next2) >= self._minSup:
                nextRow, nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(next2)
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: next2[i] for i in next2}
                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: next2[i] for i in next2}
            else:
                nextRow, nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                self._failPatterns[str(nextRow)] = len(next2)

    def makeSame2(self, rowLen, bs, latestWord, latestWord2):
        """
        to check the pattern is frequent or not (ex a-bc from a-c ab)

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """
        if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(
                self._xLenDatabaseSame[rowLen][bs][latestWord2].keys()):
            _next = {}

            for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                if seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                    if self._xLenDatabaseSame[rowLen][bs][latestWord2][seq]:
                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord][seq] if
                             i > self._xLenDatabaseSame[rowLen][bs][latestWord2][seq][0]]
                        if len(x) != 0:
                            _next[seq] = x
            if len(_next) >= self._minSup:

                nextRow, nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(_next)
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: _next[i] for i in _next}
                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                self._failPatterns[str(nextRow)] = len(_next)

        else:
            _next = {}
            for seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                    if self._xLenDatabaseSame[rowLen][bs][latestWord2][seq]:
                        x = [i for i in self._xLenDatabase[rowLen][bs][latestWord][seq] if
                             i > self._xLenDatabaseSame[rowLen][bs][latestWord2][seq][0]]
                        if len(x) != 0:
                            _next[seq] = x
            if len(_next) >= self._minSup:
                nextRow, nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._finalPatterns[str(nextRow)] = len(_next)
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: _next[i] for i in _next}

                else:
                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                self._failPatterns[str(nextRow)] = len(_next)

    def makeSame3(self, rowLen, bs, latestWord, latestWord2):
        """
        To check the pattern is frequent or not (ex abc from ac ab)

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str

        """
        if len(self._xLenDatabaseSame[rowLen][bs][latestWord].keys()) <= len(
                self._xLenDatabaseSame[rowLen][bs][latestWord2].keys()):
            _next = {}

            for seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                if seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                    x = list(sorted(set(self._xLenDatabaseSame[rowLen][bs][latestWord][seq]) & set(
                        self._xLenDatabaseSame[rowLen][bs][latestWord2][seq])))
                    if len(x) != 0:
                        _next[seq] = x
            if len(_next) >= self._minSup:

                nextRow, nextbs, nextLate = self.makeNextRowSame2(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}

                    self._finalPatterns[str(nextRow)] = len(_next)
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i: _next[i] for i in _next}
                else:
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs, nextLate = self.makeNextRowSame2(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(_next)
        else:
            _next = {}

            for seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                if seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                    x = list(sorted(set(self._xLenDatabaseSame[rowLen][bs][latestWord][seq]) & set(
                        self._xLenDatabaseSame[rowLen][bs][latestWord2][seq])))
                    if len(x) != 0:
                        _next[seq] = x
            if len(_next) >= self._minSup:

                nextRow, nextbs, nextLate = self.makeNextRowSame2(bs, latestWord, latestWord2)
                if str(nextRow) not in self._finalPatterns.keys():
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}

                    self._finalPatterns[str(nextRow)] = len(_next)
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i: _next[i] for i in _next}
                else:
                    if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}
                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i: _next[i] for i in _next}
            else:
                nextRow, nextbs, nextLate = self.makeNextRowSame2(bs, latestWord, latestWord2)
                self._failPatterns[str(nextRow)] = len(_next)

    def makexLenDatabaseSame(self, rowLen, bs, latestWord):
        """
        To make 3 or more length frequent patterns from pattern which the latest word is in different seq  by depth-first search technique  and update xlenDatabase to sequential database

        :param rowLen: row length of patterns.
        :type rowLen: int
        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        """
        if rowLen + 1 not in self._xLenDatabase:
            self._xLenDatabase[rowLen + 1] = {}
            self._xLenDatabaseSame[rowLen + 1] = {}
        if bs in self._xLenDatabase[rowLen]:
            for latestWord2 in self._xLenDatabase[rowLen][bs]:
                if latestWord in self._NeighboursMap[latestWord2]:
                    nextRow, nextbs = self.makeNextRowSame(bs, latestWord, latestWord2)
                    if self.Prune(nextRow) == 1:
                        self.makeSame2(rowLen, bs, latestWord2, latestWord)

        if bs in self._xLenDatabaseSame[rowLen]:
            for latestWord2 in self._xLenDatabaseSame[rowLen][bs]:
                if latestWord2 != latestWord:
                    if latestWord in self._NeighboursMap[latestWord2]:
                        nextRow, nextbs, nextLate = self.makeNextRowSame2(bs, latestWord, latestWord2)
                        if self.Prune(nextRow) == 1:
                            self.makeSame3(rowLen, bs, latestWord, latestWord2)

    def makeNextRow(self, bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns having the latest word in different sequence

        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """

        bs = bs + (-1, latestWord)
        bs2 = bs + (-1, latestWord2, -1)
        return bs2, bs

    def makeNextRowSame(self, bs, latestWord, latestWord2):
        """
        To make pattern row when one pattern having the latestWord in different sequence and other(latestWord2) in same

        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """

        bs = list(bs)
        x = 1
        x2 = [latestWord, ]
        while bs:
            x = bs.pop()
            if x != -1:
                x2.append(x)
            else:
                break
        x2 = list(sorted(set(x2)))
        if len(bs) != 0:
            bs = tuple(bs) + (-1,) + tuple(x2)
        else:
            bs = tuple(x2)
        bs2 = tuple(bs) + (-1, latestWord2, -1)
        return bs2, bs

    def makeNextRowSame2(self, bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns having the latest word in same sequence

        param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """

        bs = list(bs)
        x = 1
        x2 = [latestWord, latestWord2]
        while bs:
            x = bs.pop()
            if x != -1:
                x2.append(x)
            else:
                break
        x2 = list(sorted(set(x2)))
        x3 = x2.pop()
        if len(bs) != 0:
            bs = tuple(bs) + (-1,) + tuple(x2)
        else:
            bs = tuple(x2)
        bs2 = tuple(bs) + (x3, -1)

        return bs2, bs, x3

    def makeNextRowSame3(self, bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns having the latest word in different sequence and both latest word is in same sequence

        :param bs : patterns without the latest one
        :type bs: int
        :param latestWord : latest word of patterns
        :type latestWord: str
        :param latestWord2 : latest word of other previous pattern in different sequence
        :type latestWord2: str
        """

        x = list(sorted({latestWord, latestWord2}))
        x2 = x.pop()
        x3 = x.pop()
        bs = bs + (-1, x3)
        bs2 = bs + (x2, -1)
        return bs2, bs, x2

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Frequent pattern mining process will start from here
        """
        self.mine()

    def mine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._mapNeighbours()
        self._minSup = self._convert(self._minSup)
        self.make1LenDatabase()
        self.make2LenDatabase()
        self.makexLenData(2)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Apriori algorithm ")

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
            data.append([a, b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y)
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
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = GFSPminer(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = GFSPminer(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.mine()
        _ap.mine()
        _Patterns = _ap.getPatterns()
        print("Total number of Frequent Patterns:", len(_Patterns))
        _ap.save(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        _ap = GFSPminer('retail.txt', "file3.txt", 87, ' ')
        _ap.mine()
        _ap.mine()
        _Patterns = _ap.getPatterns()
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
        print("Total number of Frequent Patterns:", len(_Patterns))
        print("Error! The number of input parameters do not match the total number of parameters provided")
        _ap.save("priOut3.txt")
