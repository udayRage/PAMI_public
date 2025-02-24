# GSP is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
# This program employs GSP property (or downward closure property) to  reduce the search space effectively.
# This algorithm employs breadth-first search technique  to find the complete set of frequent patterns in a transactional database.
#
#
# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             import PAMI.sequentialPatternMining.basic.GSP as alg
#
#             obj = alg.GSP(iFile, minSup)
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
 Copyright (C)  2024 Rage Uday Kiran

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
import collections
import itertools
import pandas as pd
from deprecated import deprecated

from PAMI.sequentialPattern.basic import abstract as _ab

_ab._sys.setrecursionlimit(10000)

class GSP(_ab._sequentialPatterns):
    """
    :Description:

        * GSP is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
        * This program employs GSP property (or downward closure property) to  reduce the search space effectively.
        * This algorithm employs breadth-first search technique  to find the complete set of frequent patterns in a transactional database.


    :Reference:   Srikant, R., Agrawal, R. (1996). Mining sequential patterns: Generalizations and performance improvements. In: Apers, P., Bouzeghoub, M., Gardarin, G. (eds) Advances in Database Technology — EDBT '96. EDBT 1996. Lecture Notes in Computer Science, vol 1057. Springer, Berlin, Heidelberg.
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

       (.venv) $ python3 GSP.py <inputFile> <outputFile> <minSup>

       Example usage:

       (.venv) $ python3 GSP.py sampleDB.txt patterns.txt 10.0


               .. note:: minSup will be considered in times of minSup and count of database transactions

    **Importing this algorithm into a python program**
    ----------------------------------------------------
    .. code-block:: python

            import PAMI.sequentialPattern.basic.GSP as alg

            obj = alg.GSP(iFile, minSup)

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

    _minSup = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _sepSeq = "-1"
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _xLenDatabase={}
    _xLenDatabaseSame = {}
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


        idDatabase=[]
        for line in self._Database:
            x=[]
            for seq in line:
                
                x+=list(itertools.chain.from_iterable(line))
            
            idDatabase+=list(sorted(set(x)))


        newDatabase=collections.Counter(idDatabase)
        newDatabase={i:v for i,v in newDatabase.items() if v>=self._minSup}
        self._finalPatterns={str(i):v for i,v in newDatabase.items()}
        
    def list_split(self,L):
        """
        To convert the list to list separated by sepSeq

        :param L:list pattren in one list
        :return:  return_L:list pattern separated by each sequence  
        """
        return_L,tmp = [],[]
        for val in L:
            if val != self._sepSeq:
                tmp.append(val)
            elif val == self._sepSeq:
                return_L.append(tmp)
                tmp = []
    
        return_L.append(tmp)
        return return_L
    
    def checkPattern(self,pattern,tra):
        """
        To check the pattern is included in tra 
        param pattern:the candidate pattern 
              tra:list     one transaction in data
        :return:  0 :the pattern is not included
                  1 :the pattern is included
        """
        seqNum=0
        
        for i in tra:
            if set(pattern[seqNum]).issubset(set(i)):
                seqNum+=1
                if seqNum>=len(pattern):
                    return 1
        return 0
            
            
        
    def getSup(self,pattern):
        """
        count up the support of the pattern
        :param pattern:list the candidate pattern
        :return:  sup:int  the support of the pattern
        """
        sup=0
        pattern=self.list_split(pattern)
        for seq in self._Database:
            
            sup+=self.checkPattern(pattern,seq)
        return sup
        
    def make2LenDatabase(self):
        """
        To make 2 length frequent patterns by joining two one length patterns by breadth-first search technique  and update xlen Database to sequential database
        :return:  nextPatterns:List  the patterns found
       
        """
        self._xLenDatabase = {}
        keyList=[i for i in self._finalPatterns.keys()]
        keyNumber=0
        nextPatterns=[]
        
        for key1 in keyList:
            newPattern1=[key1,self._sepSeq,key1]
            sup=self.getSup(newPattern1)
            if sup>=self._minSup:
                self._finalPatterns[tuple(newPattern1)]=sup
                nextPatterns.append(newPattern1)
            keyNumber+=1
            for key2 in keyList[keyNumber:]:
                newPattern1=[key1,self._sepSeq,key2]
                sup=self.getSup(newPattern1)
                if sup>=self._minSup:
                    self._finalPatterns[tuple(newPattern1)]=sup
                    nextPatterns.append(newPattern1)
                newPattern2=[key2,self._sepSeq,key1]
                sup=self.getSup(newPattern2)
                if sup>=self._minSup:
                    self._finalPatterns[tuple(newPattern2)]=sup
                    nextPatterns.append(newPattern2)
                newPattern3=list(sorted(set([key1,key2])))
                sup=self.getSup(newPattern3)
                if sup>=self._minSup:
                    self._finalPatterns[tuple(newPattern3)]=sup
                    nextPatterns.append(newPattern3)
        return nextPatterns

    def makeCandidateDatabase(self,patterns):
        """
        make the database to find new candidate
        :param patterns:list the patterns fond before
        :return:  bothBefore:dict   the patterns have same item without last one item
                  bothAfter:dict   the patterns have same item without first one item
        """
        before={}
        after={}
        
        for pattern in patterns:
            if pattern[-2]==self._sepSeq:
                if tuple(pattern[:-2]) not in after.keys():
                    after[tuple(pattern[:-2])]=[pattern[-2:]]
                else:
                    after[tuple(pattern[:-2])].append(pattern[-2:])
            else:
                if tuple(pattern[:-1]) not in after.keys():
                    after[tuple(pattern[:-1])]=[[pattern[-1]]]
                else:
                    after[tuple(pattern[:-1])].append([pattern[-1]])
            if pattern[1]==self._sepSeq:
                if tuple(pattern[2:]) not in before.keys():
                    before[tuple(pattern[2:])]=[pattern[:2]]
                else:
                    before[tuple(pattern[2:])].append(pattern[:2])
            else:
                if tuple(pattern[1:]) not in before.keys():
                    before[tuple(pattern[1:])]=[[pattern[0]]]
                else:
                    before[tuple(pattern[1:])].append([pattern[0]])
        bothBefore={i:v for i,v in before.items() if i in after.keys()}
        bothAfter={i:v for i,v in after.items() if i in before.keys()}
        return bothBefore, bothAfter
        
    def makeCandidate(self,patterns):
        """
        make the candidate patterns
        :param patterns:list the patterns found before
        :return:  newPatterns:list  the candidate pattern
        """
        before,after=self.makeCandidateDatabase(patterns)
        newPatterns=[]
        for common in before.keys():
            for b in before[common]:
                for a in after[common]:
                    newPattern=b+list(common)+a
                    newPatterns.append(newPattern)
        return newPatterns
                
        
            
    
    def makexLenDatabase(self,patterns):
        """
        To make 3 or more length frequent patterns from pattern which the latest word is in different seq  by depth-first search technique  and update xlenDatabase to sequential database

        :param patterns: patterns
        
        """
        patterns=self.makeCandidate(patterns)
        nextPatterns=[]
        for pattern in patterns:
                sup=self.getSup(pattern)
                if sup>=self._minSup:
                    self._finalPatterns[tuple(pattern)]=sup
                    nextPatterns.append(pattern)
        return nextPatterns
                    
        
       

    def mine(self):
        """
        Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self.make1LenDatabase()
        nextPatterns=self.make2LenDatabase()
        while len(nextPatterns)>0:
            nextPatterns= self.makexLenDatabase(nextPatterns)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Sequential Frequent patterns were generated successfully using GSP algorithm ")

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
            s1 = str(x) + ":" + str(y)
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
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = GSP(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = GSP(_ab._sys.argv[1], _ab._sys.argv[3])
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

