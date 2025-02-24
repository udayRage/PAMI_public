# SPADE is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
# This program employs SPADE property (or downward closure property) to  reduce the search space effectively.
# This algorithm employs breadth-first search technique when 1-2 length patterns and depth-first search when above 3 length patterns to find the complete set of frequent patterns in a transactional database.
#SPADEPlus has two additional number MAXgap(the maximum distance of sequence between pattern item) and maxLength(the maximum length of patterns) 
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             import PAMI.sequentialPattern.basic.SPADEPlus as alg
#
#             obj = alg.SPADEPlus(iFile, minSup,maxGap=**,maxLen=**)
#
#             obj.mine()
#
#             sequentialPatternMining = obj.getPatterns()
#
#             print("Total number of Frequent Patterns:", len(frequentPatterns))
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


import pandas as pd
from deprecated import deprecated

from PAMI.sequentialPattern.basic import abstract as _ab

_ab._sys.setrecursionlimit(10000)

class SPADEPlus(_ab._sequentialPatterns):
    """
    :Description:

        * SPADE is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
        * This program employs SPADE property (or downward closure property) to  reduce the search space effectively.
        * This algorithm employs breadth-first search technique when 1-2 length patterns and depth-first serch when above 3 length patterns to find the complete set of frequent patterns in a transactional database.

    :Reference:   Mohammed J. Zaki. 2001. SPADE: An Efficient Algorithm for Mining Frequent Sequences. Mach. Learn. 42, 1-2 (January 2001), 31-60. DOI=10.1023/A:1007652502315 http://dx.doi.org/10.1023/A:1007652502315

    :param  iFile: str :
                   Name of the Input file to mine complete set of  Sequential frequent patterns
    :param  oFile: str :
                   Name of the output file to store complete set of  Sequential frequent patterns
    :param  minSup: float or int or str :
                    minSup measure constraints the minimum number of transactions in a database where a pattern must appear
                    Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

            iFile : str
                Input file name or path of the input file
            oFile : str
                Name of the output file or the path of output file
            minSup: float or int or str
                The user can specify minSup either in count or proportion of database size.
                If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
                Otherwise, it will be treated as float.
                Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
            sep : str
                This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
                However, the users can override their default separator.
            startTime:float
                To record the start time of the mining process
            endTime:float
                To record the completion time of the mining process
            finalPatterns: dict
                Storing the complete set of patterns in a dictionary variable
            memoryUSS : float
                To store the total amount of USS memory consumed by the program
            memoryRSS : float
                To store the total amount of RSS memory consumed by the program
            Database : list
                To store the transactions of a database in list
            _xLenDatabase: dict
                To store the datas in different sequence separated by sequence, rownumber, length.
            _xLenDatabaseSame : dict
                To store the datas in same sequence separated by sequence, rownumber, length.
            _seqSep   :str
                separator to separate each itemset
            _maxLen:int
                to store the maximum length of sequence pattern
            _maxGap   :int
                to store the maximum gap of sequence pattern
                gap means the length of interval between two itemsets

    :Methods:

            mine()
                Mining process will start from here
            getPatterns()
                Complete set of patterns will be retrieved with this function
            savePatterns(oFile)
                Complete set of frequent patterns will be loaded in to an output file
            getPatternsAsDataFrame()
                Complete set of frequent patterns will be loaded in to a dataframe
            getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
            getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
            getRuntime()
                Total amount of runtime taken by the mining process will be retrieved from this function
            candidateToFrequent(candidateList)
                Generates frequent patterns from the candidate patterns
            frequentToCandidate(frequentList, length)
                Generates candidate patterns from the frequent patterns

    **Methods to execute code on terminal**
    -------------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 SPADE.py <inputFile> <outputFile> <minSup>

       Example usage:

       (.venv) $ python3 SPADE.py sampleDB.txt patterns.txt 10.0


               .. note:: minSup will be considered in times of minSup and count of database transactions

    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

            import PAMI.sequentialPatternMining.basic.SPADE as alg

            obj = alg.SPADE(iFile, minSup)

            obj.mine()

            sequentialPatternMining = obj.getPatterns()

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
    ---------------

              The complete program was written by Suzuki Shota under the supervision of Professor Rage  Uday Kiran.

    """

    def __init__(self,iFile, minSup, sep="\t",maxlen=float("inf"),maxGap=float("inf"),sepSeq="-1"):
        super().__init__( iFile, minSup, sep,sepSeq)


        self._startTime = float()
        self._endTime = float()
        self._finalPatterns = {}
        self.seqSeq=""
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._Database = []
        self._sepDatabase={}
        self._maxLen=maxlen
        self._maxGap=maxGap
        self._xLenDatabase={}
        self._xLenDatabaseSame = {}
         
    def _creatingItemSets(self):
        """
        Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []
        temp2 = None

        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()
            if "tid" in i:
                temp2=self._iFile[''].tolist()
            addList= [temp[0]]
            for k in range(len(temp)-1):
                if temp2[k]==temp[k+1]:
                    addList.append(temp[k+1])
                else:
                    self._Database.append(addList)
                    addList= [temp[k + 1]]
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
                            temp = [i.rstrip() for i in line.split(self._sepSeq)]
                            temp = [x for x in temp if x ]

                            seq = []
                            for i in temp:
                                k = -2
                                if len(i)>1:
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
        :return: converted type
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


    def make1LenDatabase(self):
        """
        To make 1 length frequent patterns by breadth-first search technique   and update Database to sequential database
        """

        idDatabase={}
        alreadyInData=[]
        lineNumber=0
        alreadyInLine={}
        for line in self._Database:
            seqNumber=0
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
                        idDatabase[data]={}
                        idDatabase[data][lineNumber]=[]
                        idDatabase[data][lineNumber].append(seqNumber)
                        alreadyInData.append(data)
                        alreadyInLine[data]=[]
                        alreadyInLine[data].append(lineNumber)



                seqNumber+=1
            lineNumber+=1

        newDatabase={i :idDatabase[i] for i in idDatabase.keys()}
        for key in idDatabase.keys():
            if len(idDatabase[key].keys())<self._minSup:
                newDatabase.pop(key)
            else:
                self._finalPatterns[str(key)]=len(idDatabase[key].keys())
        self._Database=newDatabase
    def checkGap(self,time1,time2):
        item=[]
        nextList=time1
        for i in time2:
            
            for k in nextList:
                if i-k<=self._maxGap:
                    if i-k>0:
                        item.append(i)
                        break
                else:
                    time1.remove(k)
            nextList=time1
                    
        return item 

    def make2LenDatabase(self):
        """
        To make 2 length frequent patterns by joining two one length patterns by breadth-first search technique  and update xlen Database to sequential database
        """
        self._xLenDatabase = {}
        keyList=[i for i in self._Database.keys()]
        nextDatabase={i:{} for i in self._Database.keys()}
        nextDatabaseSame={i:{} for i in self._Database.keys()}
        keyNumber=-1
        for key1 in keyList:
            keyNumber+=1
            for key2 in keyList[keyNumber:]:
                if key1!=key2:


                    if len(self._Database[key1].keys())>=len(self._Database[key1].keys()):
                        nextDatabase[key1][key2] = {}
                        nextDatabase[key2][key1] = {}
                        nextDatabaseSame[key1][key2] = {}

                        for seq in self._Database[key2].keys():
                            if seq in self._Database[key1].keys():
                                x=self.checkGap(self._Database[key2][seq],self._Database[key1][seq])
                                if len(x) != 0:
                                    nextDatabase[key2][key1][seq]=x
                                x = self.checkGap(self._Database[key1][seq],self._Database[key2][seq])
                                if len(x) != 0:
                                    nextDatabase[key1][key2][seq]=x
                                x=list(sorted(set(self._Database[key1][seq])&set(self._Database[key2][seq])))
                                if len(x)!=0:
                                    nextDatabaseSame[key1][key2][seq]=x
                    else:
                        nextDatabase[key1][key2] = {}
                        nextDatabase[key2][key1] = {}
                        nextDatabaseSame[key1][key2] = {}

                        for seq in self._Database[key1].keys():
                            x = self.checkGap(self._Database[key2][seq],self._Database[key1][seq])
                            if len(x)!=0:
                                nextDatabase[key2][key1][seq]=0
                            x = self.checkGap(self._Database[key1][seq],self._Database[key2][seq])
                            if len(x)!=0:
                                nextDatabase[key1][key2][seq]=x
                            x= list(
                                sorted(set(self._Database[key1][seq]) & set(self._Database[key2][seq])))
                            if len(x)!=0:
                                nextDatabaseSame[key1][key2][seq]=x
                else:
                    nextDatabase[key1][key2] = {}
                    for seq in self._Database[key2].keys():
                        if len(self._Database[key1][seq])>=2:
                            nextDatabase[key1][key2][seq]= self.checkGap(self._Database[key1][seq],self._Database[key2][seq])
        self._xLenDatabase[2] = {tuple([i]): {} for i in nextDatabase.keys()}
        for key1 in nextDatabase.keys():
            for key2 in nextDatabase[key1].keys():
                if len(nextDatabase[key1][key2].keys())>=self._minSup:
                    self._finalPatterns[str((key1,self._sepSeq,key2,self._sepSeq))]=len(nextDatabase[key1][key2].keys())
                    self._xLenDatabase[2][tuple([key1])][key2]=nextDatabase[key1][key2]
        self._xLenDatabaseSame[2]={tuple([i]): {} for i in nextDatabaseSame.keys()}
        for key1 in nextDatabaseSame.keys():
            for key2 in nextDatabaseSame[key1].keys():
                if len(nextDatabaseSame[key1][key2].keys()) >= self._minSup:
                    self._finalPatterns[str((key1,key2,self._sepSeq))]=len(nextDatabaseSame[key1][key2].keys())
                    self._xLenDatabaseSame[2][tuple([key1])][key2]={i:nextDatabaseSame[key1][key2][i] for i in nextDatabaseSame[key1][key2].keys()}
                    self._xLenDatabaseSame[2][tuple([key2])][key1] = {i: nextDatabaseSame[key1][key2][i] for i in nextDatabaseSame[key1][key2].keys()}

    def make3LenDatabase(self):
        """
        To call each 2 length patterns to make 3 length frequent patterns depth-first search technique
        """
        for i in self._xLenDatabase[2].keys():
            for k in self._xLenDatabase[2][i].keys():
                self.makexLenDatabase(2,i,k)
        for i in self._xLenDatabaseSame[2].keys():
            for k in self._xLenDatabaseSame[2][i].keys():
                self.makexLenDatabaseSame(2,i,k)

    def makexLenDatabase(self, rowLen, bs, latestWord):
            """
            To make "rowLen" length frequent patterns from pattern which the latest word is in same seq  by joining "rowLen"self._sepSeq length patterns by depth-first search technique  and update xlenDatabase to sequential database

            :param rowLen: row length of patterns.
            :param bs : patterns without the latest one
            :param latestWord : latest word of patterns
            """
            if rowLen+1 not in self._xLenDatabase:
                self._xLenDatabase[rowLen+1]={}
                self._xLenDatabaseSame[rowLen+1]={}
            for latestWord2 in self._xLenDatabase[rowLen][bs].keys():
                if latestWord != latestWord2:
                    
                    if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(self._xLenDatabase[rowLen][bs][latestWord2].keys()):
                        next1={}
                        next2={}
                        nextSame={}

                        for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                            if seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                                if self._xLenDatabase[rowLen][bs][latestWord2][seq]!=[] and self._xLenDatabase[rowLen][bs][latestWord][seq]!=[]:
                                    if rowLen<self._maxLen:
                                        x = self.checkGap(self._xLenDatabase[rowLen][bs][latestWord][seq],self._xLenDatabase[rowLen][bs][latestWord2][seq])
                                        if len(x) != 0:
                                            next1[seq] = x
                                        x = self.checkGap(self._xLenDatabase[rowLen][bs][latestWord2][seq],self._xLenDatabase[rowLen][bs][latestWord][seq])
                                        if len(x) != 0:
                                            next2[seq] = x
                                    x = list(sorted(set(self._xLenDatabase[rowLen][bs][latestWord][seq]) & set(
                                        self._xLenDatabase[rowLen][bs][latestWord2][seq])))
                                    if len(x) != 0:
                                        nextSame[seq] = x
                        if len(next1)>=self._minSup:
                            nextRow,nextbs= self.makeNextRow(bs,latestWord,latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                self._finalPatterns[str(nextRow)] = len(next1)
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen + 1][nextbs]={}
                                self._xLenDatabase[rowLen+1][nextbs][latestWord2]={i:next1[i] for i in next1}
                                self.makexLenDatabase(rowLen+1,nextbs,latestWord2)
                        if len(next2)>=self._minSup:
                            nextRow,nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen + 1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(next2)
                                self._xLenDatabase[rowLen+1][nextbs][latestWord] = {i:next2[i] for i in next2 }
                                self.makexLenDatabase(rowLen+1, nextbs, latestWord)
                        if len(nextSame) >= self._minSup:
                            nextRow,nextbs ,nextlste= self.makeNextRowSame3(bs, latestWord, latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                                    self._xLenDatabaseSame[rowLen + 1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(nextSame)
                                self._xLenDatabaseSame[rowLen+1][nextbs][nextlste]={i:nextSame[i] for i in nextSame }
                                self.makexLenDatabaseSame(rowLen+1, nextbs, nextlste)

                    else:
                        next1 = {}
                        next2 = {}
                        nextSame = {}

                        for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                            if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                                if self._xLenDatabase[rowLen][bs][latestWord2][seq] != [] and self._xLenDatabase[rowLen][bs][latestWord][seq] != []:
                                    if rowLen<self._maxLen:
                                        x = self.checkGap(self._xLenDatabase[rowLen][bs][latestWord][seq],self._xLenDatabase[rowLen][bs][latestWord2][seq])
                                        if len(x)!=0:
                                            next1[seq]=x
                                        x= self.checkGap(self._xLenDatabase[rowLen][bs][latestWord2][seq],self._xLenDatabase[rowLen][bs][latestWord][seq])
                                        if len(x)!=0:
                                            next2[seq]=x
                                    x= list(sorted(set(self._xLenDatabase[rowLen][bs][latestWord][seq]) & set(
                                            self._xLenDatabase[rowLen][bs][latestWord2][seq])))
                                    if len(x)!=0:
                                        nextSame[seq]=x
                        if len(next1) >= self._minSup:
                            nextRow,nextbs = self.makeNextRow(bs, latestWord, latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen+1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(next1)
                                self._xLenDatabase[rowLen + 1][nextbs][latestWord2] ={i:next1[i] for i in next1}
                                self.makexLenDatabase(rowLen+1, nextbs, latestWord2)
                        if len(next2) >= self._minSup:
                            nextRow,nextbs = self.makeNextRow(bs, latestWord2, latestWord)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen + 1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(next2)
                                self._xLenDatabase[rowLen+1][nextbs][latestWord] = {i:next2[i] for i in next2 }
                                self.makexLenDatabase(rowLen+1, nextbs, latestWord)
                        if len(nextSame) >= self._minSup:
                            nextRow,nextbs,nextlate = self.makeNextRowSame3(bs,latestWord,latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabaseSame[rowLen + 1]:
                                    self._xLenDatabaseSame[rowLen + 1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(nextSame)
                                self._xLenDatabaseSame[rowLen+1][nextbs][nextlate] = {i:nextSame[i] for i in nextSame}
                                self.makexLenDatabaseSame(rowLen+1, nextbs, nextlate)

                else:
                    next1= {}
                    if rowLen<self._maxLen:
                        for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                            if len(self._xLenDatabase[rowLen][bs][latestWord][seq])>=2:
                                next1[seq]= self.checkGap(self._xLenDatabase[rowLen][bs][latestWord][seq], self._xLenDatabase[rowLen][bs][latestWord][seq])
                        if len(next1) >= self._minSup:
                            nextRow, nextbs= self.makeNextRow(bs,latestWord,latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen+1]:
                                    self._xLenDatabase[rowLen+1][nextbs]={}
                                self._finalPatterns[str(nextRow)] = len(next1)
                                self._xLenDatabase[rowLen+1][nextbs][latestWord2] ={i:next1[i] for i in next1}
                                self.makexLenDatabase(rowLen+1, nextbs, latestWord2)
            if bs in self._xLenDatabaseSame[rowLen]:
                for latestWord2 in self._xLenDatabaseSame[rowLen][bs]:


                        if len(self._xLenDatabase[rowLen][bs][latestWord].keys()) <= len(
                                self._xLenDatabaseSame[rowLen][bs][latestWord2].keys()):
                            next1 = {}

                            for seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                                if seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                                    if self._xLenDatabaseSame[rowLen][bs][latestWord2][seq]:
                                        x=self.checkGap(self._xLenDatabaseSame[rowLen][bs][latestWord2][seq],self._xLenDatabase[rowLen][bs][latestWord][seq])
                                        if len(x) != 0:
                                            next1[seq] = x
                            if len(next1) >= self._minSup:

                                nextRow ,nextbs= self.makeNextRowSame(bs, latestWord2, latestWord)
                                if str(nextRow) not in self._finalPatterns.keys():
                                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                                    self._finalPatterns[str(nextRow)] = len(next1)
                                    self._xLenDatabase[rowLen + 1][nextbs][latestWord] = {i:next1[i] for i in next1}
                                    self.makexLenDatabase(rowLen + 1, nextbs, latestWord)

                        else:
                            next1 = {}
                            for seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                                if seq in self._xLenDatabase[rowLen][bs][latestWord].keys():
                                    if self._xLenDatabaseSame[rowLen][bs][latestWord2][seq]:
                                        x= self.checkGap(self._xLenDatabaseSame[rowLen][bs][latestWord2][seq],self._xLenDatabase[rowLen][bs][latestWord][seq])
                                        if len(x) != 0:
                                            next1[seq] = x
                            if len(next1) >= self._minSup:
                                nextRow,nextbs = self.makeNextRowSame(bs, latestWord2, latestWord)
                                if str(nextRow) not in self._finalPatterns.keys():
                                    if nextbs not in self._xLenDatabase[rowLen + 1]:
                                        self._xLenDatabase[rowLen + 1][nextbs] = {}
                                    self._finalPatterns[str(nextRow)] = len(next1)
                                    self._xLenDatabase[rowLen+1][nextbs][latestWord] = {i:next1[i] for i in next1}
                                    self.makexLenDatabase(rowLen + 1, nextbs,latestWord)

    def makexLenDatabaseSame(self, rowLen, bs, latestWord):
        """
        To make 3 or more length frequent patterns from pattern which the latest word is in different seq  by depth-first search technique  and update xlenDatabase to sequential database

        :param rowLen: row length of previous patterns.
        :param bs : previous patterns without the latest one
        :param latestWord : latest word of previous patterns
        """
        if rowLen + 1 not in self._xLenDatabase:
            self._xLenDatabase[rowLen + 1] = {}
            self._xLenDatabaseSame[rowLen + 1] = {}
       
        if bs in self._xLenDatabase[rowLen]:
            for latestWord2 in self._xLenDatabase[rowLen][bs]:
                if rowLen<self._maxLen:
                    if len(self._xLenDatabaseSame[rowLen][bs][latestWord].keys()) <= len(self._xLenDatabase[rowLen][bs][latestWord2].keys()):
                        next1 = {}
    
                        for seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                            if seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                                if self._xLenDatabaseSame[rowLen][bs][latestWord][seq]:
                                    x= self.checkGap(self._xLenDatabaseSame[rowLen][bs][latestWord][seq],self._xLenDatabase[rowLen][bs][latestWord2][seq])
                                    if len(x) != 0:
                                        next1[seq] = x
                        if len(next1) >= self._minSup:
                            nextRow ,nextbs= self.makeNextRowSame(bs, latestWord, latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen + 1][nextbs] = {}
                                self._finalPatterns[str(nextRow)] = len(next1)
                                self._xLenDatabase[rowLen + 1][nextbs][latestWord2]= {i:next1[i] for i in next1}
                                self.makexLenDatabase(rowLen + 1, nextbs, latestWord2)
    
                    else:
                        next1 = {}
    
                        for seq in self._xLenDatabase[rowLen][bs][latestWord2].keys():
                            if seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                                if self._xLenDatabaseSame[rowLen][bs][latestWord][seq]:
                                    x= self.checkGap(self._xLenDatabaseSame[rowLen][bs][latestWord][seq],self._xLenDatabase[rowLen][bs][latestWord2][seq])
                                    if len(x) != 0:
                                        next1[seq] = x
                        if len(next1) >= self._minSup:
                            nextRow,nextbs = self.makeNextRowSame(bs, latestWord, latestWord2)
                            if str(nextRow) not in self._finalPatterns.keys():
                                if nextbs not in self._xLenDatabase[rowLen + 1]:
                                    self._xLenDatabase[rowLen + 1][nextbs] = {}
                                self._finalPatterns[str(nextRow)] = len(next1)
                                self._xLenDatabase[rowLen + 1][nextbs][latestWord2] = {i:next1[i] for i in next1}
                                self.makexLenDatabase(rowLen + 1,nextbs, latestWord2)
        if bs in self._xLenDatabaseSame[rowLen]:
            for latestWord2 in self._xLenDatabaseSame[rowLen][bs]:
                if latestWord2!=latestWord:
                    if len(self._xLenDatabaseSame[rowLen][bs][latestWord].keys()) <= len(
                            self._xLenDatabaseSame[rowLen][bs][latestWord2].keys()):
                        next1 = {}

                        for seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                            if seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                                x= list(sorted(set(self._xLenDatabaseSame[rowLen][bs][latestWord][seq]) & set(
                                        self._xLenDatabaseSame[rowLen][bs][latestWord2][seq])))
                                if len(x) != 0:
                                    next1[seq] = x
                        if len(next1) >= self._minSup:

                                nextRow, nextbs,nextLate= self.makeNextRowSame2(bs, latestWord, latestWord2)
                                if str(nextRow) not in self._finalPatterns.keys():
                                    if nextbs not in self._xLenDatabaseSame[rowLen+1]:
                                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}

                                    self._finalPatterns[str(nextRow)] = len(next1)
                                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i:next1[i] for i in next1}
                                    self.makexLenDatabaseSame(rowLen + 1, nextbs, nextLate)
                    else:
                        next1 = {}

                        for seq in self._xLenDatabaseSame[rowLen][bs][latestWord2].keys():
                            if seq in self._xLenDatabaseSame[rowLen][bs][latestWord].keys():
                                x= list(sorted(set(self._xLenDatabaseSame[rowLen][bs][latestWord][seq]) & set(
                                        self._xLenDatabaseSame[rowLen][bs][latestWord2][seq])))
                                if len(x) != 0:
                                    next1[seq] = x
                        if len(next1) >= self._minSup:

                                nextRow, nextbs,nextLate= self.makeNextRowSame2(bs, latestWord, latestWord2)
                                if str(nextRow) not in self._finalPatterns.keys():
                                    if nextbs not in self._xLenDatabaseSame[rowLen+1]:
                                        self._xLenDatabaseSame[rowLen + 1][nextbs] = {}

                                    self._finalPatterns[str(nextRow)] = len(next1)
                                    self._xLenDatabaseSame[rowLen + 1][nextbs][nextLate] = {i:next1[i] for i in next1}
                                    self.makexLenDatabaseSame(rowLen + 1, nextbs, nextLate)

    def makeNextRow(self,bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns have the latest word in different sequence

        :param bs : previous pattern without the latest one
        :param latestWord : latest word of one previous pattern
        :param latestWord2 : latest word of other previous pattern
        """

        bs=bs+(self._sepSeq,latestWord)
        bs2=bs+(self._sepSeq,latestWord2,self._sepSeq)
        return bs2,bs

    def makeNextRowSame(self,bs, latestWord, latestWord2):
        """
        To make pattern row when one pattern have the latestWord1 in different sequence and other(latestWord2) in same

        :param bs : previous pattern without the latest one
        :param latestWord : latest word of one previous pattern in same sequence
        :param latestWord2 : latest word of other previous pattern in different sequence
        """

        bs=list(bs)
        x=1
        x2=[latestWord,]
        while bs:
            x=bs.pop()
            if x!=self._sepSeq:
                x2.append(x)
            else:
                break
        x2=list(sorted(set(x2)))
        if len(bs)!=0:
            bs=tuple(bs)+(self._sepSeq,)+tuple(x2)
        else:
            bs=tuple(x2)
        bs2=tuple(bs)+(self._sepSeq,latestWord2,self._sepSeq)
        return bs2,bs


    def makeNextRowSame2(self,bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns have the latest word in same sequence

        :param bs : previous pattern without the latest one
        :param latestWord : latest word of one previous pattern
        :param latestWord2 : latest word of the other previous pattern
        """

        bs = list(bs)
        x = 1
        x2 = [latestWord, latestWord2]
        while bs:
            x = bs.pop()
            if x != self._sepSeq:
                x2.append(x)
            else:
                break
        x2 = list(sorted(set(x2)))
        x3 = x2.pop()
        if len(bs)!=0:
            bs = tuple(bs)+(self._sepSeq,)+ tuple(x2)
        else:
            bs = tuple(x2)
        bs2 = tuple(bs) + (x3, self._sepSeq)

        return bs2, bs, x3


    def makeNextRowSame3(self, bs, latestWord, latestWord2):
        """
        To make pattern row when two patterns have the latest word in different sequence and both latest word is in same sequence

        :param bs : previous pattern without the latest one
        :param latestWord : latest word of one previous pattern
        :param latestWord2 : latest word of other previous pattern
        """

        x = list(sorted({latestWord, latestWord2}))
        x2 = x.pop()
        x3=x.pop()
        bs = bs + (self._sepSeq,x3)
        bs2 = bs + (x2,)
        return  bs2,bs,x2

    def startMine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self.make1LenDatabase()
        self.make2LenDatabase()
        self.make3LenDatabase()
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Sequential Frequent patterns were generated successfully using SPADE algorithm ")

    def mine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self.make1LenDatabase()
        self.make2LenDatabase()
        self.make3LenDatabase()
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Sequential Frequent patterns were generated successfully using SPADE algorithm ")

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
        This function is used to prnt the results
        """
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) >= 4 or len(_ab._sys.argv) <= 7:
        if len(_ab._sys.argv) == 7:
            _ap = SPADEPlus(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6])
        if len(_ab._sys.argv) == 6:
            _ap = SPADEPlus(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = SPADEPlus(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = SPADEPlus(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.mine()
        _Patterns = _ap.getPatterns()
        print("Total number of Frequent Patterns:", len(_Patterns))
        _ap.savePatterns(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in ms:", _run)
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
       

