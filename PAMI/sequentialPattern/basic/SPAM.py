# SPAM is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
# This program employs SPAM property (or downward closure property) to  reduce the search space effectively.
#  This algorithm employs breadth-first search technique  to find the complete set of frequent patterns in a sequential database.
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             import PAMI.sequentialPattern.basic.SPAM as alg
#
#             obj = alg.SPAM(iFile, minSup)
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


import pandas as pd
from deprecated import deprecated

from PAMI.sequentialPattern.basic import abstract as _ab
_ab._sys.setrecursionlimit(10000)

class SPAM(_ab._sequentialPatterns):
    """
    :Description:    SPAM is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
                     This program employs SPAM property (or downward closure property) to  reduce the search space effectively.
                     This algorithm employs breadth-first search technique  to find the complete set of frequent patterns in a sequential database.

    :Reference:   J. Ayres, J. Gehrke, T.Yiu, and J. Flannick. Sequential Pattern Mining Using Bitmaps. In Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. Edmonton, Alberta, Canada, July 2002.

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
            minSup : float or int or str
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
                To store the sequences of a database in list
            _idDatabase : dict
                To store the sequences of a database by bit map
            _maxSeqLen:
                the maximum length of subsequence in sequence.
            _seqSep   :str
                separator to separate each itemset

    :Methods:

            _creatingItemSets():
                Storing the complete sequences of the database/input file in a database variable
            _convert(value):
                To convert the user specified minSup value
            make2BitDatabase():
                To make 1 length frequent patterns by breadth-first search technique   and update Database to sequential database
            DfsPruning(items,sStep,iStep):
                the main algorithm of spam. This can search sstep and istep items and find next patterns, its sstep, and its istep. And call this function again by using them. Recursion until there are no more items available for exploration.
            Sstep(s):
                To convert bit to ssteo bit.The first time you get 1, you set it to 0 and subsequent ones to 1.(like 010101=>001111, 00001001=>00000111)
            mine()
                Mining process will start from here
            getPatterns()
                Complete set of patterns will be retrieved with this function
            savePatterns(oFile)
                Complete set of frequent patterns will be loaded in to a output file
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


    **Executing the code on terminal**:
    ----------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 SPAM.py <inputFile> <outputFile> <minSup> (<separator>)

       Examples usage:

       (.venv) $ python3 SPAM.py sampleDB.txt patterns.txt 10.0


               .. note:: minSup will be considered in times of minSup and count of database transactions

    **Sample run of the importing code**:
    -------------------------------------
            import PAMI.sequentialPattern.basic.SPAM as alg

            obj = alg.SPAM(iFile, minSup)

            obj.mine()

            sequentialPatternMining = obj.getPatterns()

            print("Total number of Frequent Patterns:", len(frequentPatterns))

            obj.savePatterns(oFile)

            Df = obj.getPatternInDataFrame()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

            run = obj.getRuntime()

            print("Total ExecutionTime in seconds:", run)

    **Credits**:
    ------------
            The complete program was written by Shota Suzuki  under the supervision of Professor Rage Uday Kiran.
    """

    _minSup = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _idDatabase={}
    _maxSeqLen=0
    _sepSeq=""
    def _creatingItemSets(self):
        """
        Storing the complete sequences of the database/input file in a database variable
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


    def make2BitDatabase(self):
        """
        To make 1 length frequent patterns by breadth-first search technique   and update Database to sequential database
        """
        self._maxSeqLen=max([len(i) for i in self._Database])
        lineNumber=0
        idDatabase={}
        for line in self._Database:
            seqNumber=1
            for seq in line:

                for data in seq:
                    if data in idDatabase:
                        while lineNumber+1!=len(idDatabase[data]):
                            idDatabase[data].append(0)
                        idDatabase[data][lineNumber]+=int(2**(self._maxSeqLen-seqNumber))

                    else:
                        idDatabase[data]=[]
                        while lineNumber+1!=len(idDatabase[data]):
                            idDatabase[data].append(0)
                        idDatabase[data][lineNumber]+=(int(2 ** (self._maxSeqLen-seqNumber)))

                seqNumber+=1
            lineNumber+=1
        for key,val in idDatabase.items():

            sup=self.countSup(val)
            while lineNumber+1!=len(idDatabase[key]):
                            idDatabase[key].append(0)
            if sup>=self._minSup:
                self._finalPatterns[str(key)+self._sep+"-2"]=sup
                self._idDatabase[str(key)]=val

    def DfsPruning(self,items,sStep,iStep):
        """
        the main algorithm of spam. This can search sstep and istep items and find next patterns, its sstep, and its istep. And call this function again by using them. Recursion until there are no more items available for exploration.

        :Attributes:

        items : str
            The pattrens I got before
        sStep : list
            Items presumed to have "sstep" relationship with "items".(sstep is What appears later like a-b and a-c)
        iStep : list
            Items presumed to have "istep" relationship with "items"(istep is What appears in same time like ab and ac)

        """
        Snext=[]
        Inext=[]
        ns = self.Sstep(self._idDatabase[items])
        for i in sStep:
            nnext=[]
            for k in  range(len(self._idDatabase[items])):
                nandi=ns[k] & self._idDatabase[i][k]
                nnext.append(nandi)


            sup=self.countSup(nnext)
            if sup>=self._minSup:
                key=items+self._sep+self._sepSeq+self._sep+i
                self._finalPatterns[key+self._sep+self._sepSeq+self._sep+"-2"]=sup
                self._idDatabase[key]=nnext
                Snext.append(i)

        for i in Snext:
            key = items+self._sep+self._sepSeq+self._sep+i
            self.DfsPruning(key,Snext,[k for k in Snext if self._Database.index(i)<self._Database.index(k)])
        for i in iStep:
            nnext = []

            for k in range(len(self._idDatabase[items])):
                nandi = self._idDatabase[items][k] & self._idDatabase[i][k]
                nnext.append(nandi)
            sup=self.countSup(nnext)
            if sup>=self._minSup:
                key=items+self._sep+str(i)
                self._finalPatterns[key+self._sep+self._sepSeq+self._sep+"-2"]=sup
                self._idDatabase[key]=nnext
                Inext.append(i)
        for i in Inext:
            key = items +self._sep +str(i)
            self.DfsPruning(key,Snext,[k for k in Inext if self._Database.index(i)<self._Database.index(k)])

    def Sstep(self,s):
        """
        To convert bit to Sstep bit.The first time you get 1, you set it to 0 and subsequent ones to 1.(like 010101=>001111, 00001001=>00000111)


        :param s:list
            to store each bit sequence
        :return:
            nextS:list to store the bit sequence converted by sstep

        """
        nextS=[]
        for bins in s:
            binS=str(bin(bins))


            LenNum=2
            for i in range(len(binS)-2):
                if binS[LenNum] == "1":

                    binS = binS[:LenNum] + "0" + binS[LenNum + 1:]
                    while len(binS)-1!=LenNum:
                        LenNum += 1
                        binS = binS[:LenNum] + "1" + binS[LenNum + 1:]
                    break
                LenNum+=1
            nextS.append(int(binS, 0))


        return nextS

    def countSup(self,n):
        """
        count support

        :param n:list
                to store each bit sequence
        :return:
            count: int support of this list
        """
        count=0
        for i in n:
            if "1" in str(bin(i)):
                count+=1
        return count

    def startMine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self.make2BitDatabase()
        self._Database = [i for i in self._idDatabase.keys()]
        for i in self._Database:
            x=[]
            for j in self._Database:
                if self._Database.index(i)<self._Database.index(j):
                    x.append(j)

            self.DfsPruning(i,self._Database,x)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using SPAM algorithm ")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function
        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function
        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process
        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe
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
        """Complete set of frequent patterns will be loaded in to an output file
        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process
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
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = SPAM(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = SPAM(_ab._sys.argv[1], _ab._sys.argv[3])
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
