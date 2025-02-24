
#  Copyright (C)  2021 Rage Uday Kiran
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import PAMI.sequentialSpatialPattern.basic.abstract as _ab
import sys
import copy
sys.setrecursionlimit(10000)

class spatialPrefixSpan(_ab._sequentialSpatialPatterns):
    """
        Prifix Span is one of the fundamental algorithm to discover sequential frequent patterns in a transactional database.
        This program employs Prifix Span property (or downward closure property) to  reduce the search space effectively.
        This algorithm employs depth-first search technique to find the complete set of frequent patterns in a
        transactional database.
        Reference:
        ----------
           J. Pei, J. Han, B. Mortazavi-Asl, J. Wang, H. Pinto, Q. Chen, U. Dayal, M. Hsu: Mining Sequential Patterns by Pattern-Growth: The PrefixSpan Approach. IEEE Trans. Knowl. Data Eng. 16(11): 1424-1440 (2004)
        ----------
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
            maxLength:int
                to store the maximum length of sequence pattern
            maxGap   :int
                to store the maximum gap of sequence pattern
                gap means the length of interval between two itemsets
            NeighboursMap:dict
                to store the neighbor map(which place is neighbor)
        Methods:
        -------
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
            mapNeighbours()
                read the neighbor file and make neighbor map.

        Executing the code on terminal:
        -------------------------------
            Format:
            ------
             basic:
                python3 PrefixSpan.py <inputFile> <outputFile> <neighborFile> <minSup>
             length:
                python3 PrefixSpan.py <inputFile> <outputFile> <neighborFile> <minSup> "<sep(default="\t")>" <maxLength>
             gap:
                python3 PrefixSpan.py <inputFile> <outputFile> <neighborFile> <minSup> <sep(default="\t")> <maxLength(default=float("inf"))> <maxGap>
            Examples:
            ---------
            basic
                python3 PrefixSpan.py sampleDB.txt output.txt neighbor.txt 10.0   (minSup will be considered in times of minSup and count of database transactions)
                python3 PrefixSpan.py sampleDB.txt output.txt neighbor.txt 10     (minSup will be considered in support count or frequency)
            length
                python3 PrefixSpan.py sampleDB.txt output.txt neighbor.txt 10 "\t" 2 (find the pattern that have two or less itemsets and ten or more support)
            gap
                python3 PrefixSpan.py sampleDB.txt output.txt neighbor.txt 10 "\t" float("inf") 3
            length and gap
                python3 PrefixSpan.py sampleDB.txt output.txt neighbor.txt 10 "\t" 2 3
        Sample run of the importing code:
        ---------------------------------
            import PAMI.frequentPattern.basic.PrefixSpan as alg
            obj = alg.PrefixSpan(iFile, nFile,minSup)
            obj.mine()
            frequentPatterns = obj.getPatterns()
            print("Total number of Frequent Patterns:", len(frequentPatterns))
            obj.savePatterns(oFile)
            Df = obj.getPatternInDataFrame()
            memUSS = obj.getMemoryUSS()
            print("Total Memory in USS:", memUSS)
            memRSS = obj.getMemoryRSS()
            print("Total Memory in RSS", memRSS)
            run = obj.getRuntime()
            print("Total ExecutionTime in seconds:", run)
        Credits:
        --------
            The complete program was written by Suzuki Shota under the supervision of Professor Rage Uday Kiran.
    """
    def __init__(self,iFile,nFile, minSup, sep="\t",maxlen=float("inf"),maxGap=float("inf")):
        super().__init__( iFile,nFile, minSup, sep)


        self._startTime = float()
        self._endTime = float()
        self._finalPatterns = {}
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._Database = []
        self._sepDatabase={}
        self._maxLength=maxlen
        self._maxGap=maxGap
        self._NeighboursMap = {}
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
                    if temp[0] in self._Database.keys():
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
    def _creatingItemSets(self):
        """
            Storing the complete transactions of the database/input file in a database variable
        """
        self._Database = []

        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()

            for k in temp:
                self._Database.append(set(k))
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(set(temp))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split('-1')]
                            temp = [x for x in temp if x ]
                            temp.pop()

                            seq = []
                            for i in temp:
                                if len(i)>1:
                                   for j in list(sorted(set(i.split()))):
                                       seq.append(j)
                                   seq.append(-1)

                                else:
                                    seq.append(i)
                                    seq.append(-1)
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
    def makeNext(self,sepDatabase,startrow):
        """
         To get next pattern by adding head word to next sequence of startrow
        :param sepDatabase: dict
            what words and rows startrow have to add it
        :param startrow:
            the patterns get before
        """
        for head in sepDatabase.keys():
            if head not in self._NeighboursMap.keys():
                continue
            newrow=[i for i in startrow]
            checkrow={i for i in startrow if i!=-1}

            if len(sepDatabase[head])>=self._minSup  and checkrow.issubset(self._NeighboursMap[head]):
                if newrow:
                    newrow.append(-1)
                newrow.append(head)
                newrow.append(-1)
                if str(newrow) not in self._finalPatterns:
                    self._finalPatterns[str(newrow)]=len(sepDatabase[head])
                    give = [head]
                    sepDatabase[head] = self.makeSupDatabase(sepDatabase[head], give)
                    newrow.pop()
                    self.makeSeqDatabaseSame(sepDatabase[head], newrow)
                elif len(sepDatabase[head]) > self._finalPatterns[str(newrow)]:
                    self._finalPatterns[str(newrow)] = len(sepDatabase[head])
                    give = [head]
                    sepDatabase[head] = self.makeSupDatabase(sepDatabase[head], give)
                    newrow.pop()
                    self.makeSeqDatabaseSame(sepDatabase[head], newrow)



    def makeSupDatabase(self,database,head):
        """
         To delete not frequent words without words in latest sequence
        :param database: list
            database of lines have same startrow and head word
        :param head:list
         words in latest sequence
        :return: changed database

        """

        supDatabase={}
        alreadyInData=[]
        newDatabase = []

        for line in database:
            alreadyInLine = []
            for data in line:
                    if data not in alreadyInLine:
                        if data not in alreadyInData:
                            supDatabase[data]=1
                            alreadyInData.append(data)
                        else:
                            supDatabase[data]+=1
                        alreadyInLine.append(data)
        for line in database:
                newLine=[]
                for i in line:
                    if supDatabase[i]>=self._minSup or i in head:
                        if len(newLine)>1:
                            if newLine[-1]!=-1 or i!=-1:
                                newLine.append(i)
                        else:
                            newLine.append(i)
                newDatabase.append(newLine)

        return newDatabase

    def makeNextSame(self,sepDatabase,startrow):
        """
         To get next pattern by adding head word to latest sequence of startrow
        :param sepDatabase: dict
            what words and rows startrow have to add it
        :param startrow:
            the patterns get before
        """
        for head in sepDatabase.keys():
            if head not in self._NeighboursMap.keys():
                continue
            checkrow = {i for i in startrow if i != -1}
            if len(sepDatabase[head])>=self._minSup and checkrow.issubset(self._NeighboursMap[head]):
                newrow = startrow.copy()
                newrow.append(head)
                newrow.append(-1)

                if str(newrow) not in self._finalPatterns.keys():
                    self._finalPatterns[str(newrow)]=len(sepDatabase[head])
                    if -1 in startrow:
                        give = self.getSameSeq(startrow)
                    else:
                        give = startrow.copy()
                    give.append(head)
                    sepDatabase[head] = self.makeSupDatabase(sepDatabase[head], give)
                    newrow.pop()
                    self.makeSeqDatabaseSame(sepDatabase[head], newrow)
                elif len(sepDatabase[head])>self._finalPatterns[str(newrow)]:
                    self._finalPatterns[str(newrow)] = len(sepDatabase[head])
                    if -1 in startrow:
                        give = self.getSameSeq(startrow)
                    else:
                        give = startrow.copy()
                    give.append(head)
                    sepDatabase[head] = self.makeSupDatabase(sepDatabase[head], give)
                    newrow.pop()
                    self.makeSeqDatabaseSame(sepDatabase[head], newrow)








    def makeSeqDatabaseFirst(self,database):
        """
        To make 1 length sequence dataset list which start from same word. It was stored only 1 from 1 line.
        :param database:
                To store the transactions of a database in list
        """
        startrow=[]
        seqDatabase={}

        for line in database:
            alreadyInLine=[]
            for data in range(len(line)):
                if line[data] not in alreadyInLine and line[data]!=-1:
                    if line[data] not in seqDatabase.keys():
                        seqDatabase[line[data]]=[]
                        seqDatabase[line[data]].append(line[data+1:])
                        alreadyInLine.append(line[data])
                    else:
                        seqDatabase[line[data]].append(line[data+1:])
                        alreadyInLine.append(line[data])

        if len(seqDatabase)>0:
            self.makeNext(seqDatabase,startrow)

    def serchSame(self,database,startrow,give):
        """
         To get 2 or more length patterns in same sequence.
        :param database: list
            To store the transactions of a database in list which have same startrow and head word
        :param startrow: list
            the patterns get before
        :param give: list
            the word in latest sequence of startrow
        :return:
        """
        sepDatabaseSame= {startrow[-1]: []}
        for line in database:
            addLine=0
            i=0
            if len(line)>1:
                while line[i]!=-1:
                    if line[i]==startrow[-1]:
                        sepDatabaseSame[startrow[-1]].append(line[i+1:])
                        addLine=1
                        break
                    i+=1
                if addLine!=1:
                    ok=[]
                    while i <len(line):
                        if line[i]==-1:
                            ok=[]
                        elif line[i]==startrow[-1]:
                            ok.append("sk1")
                        for x in give:
                            if x==line[i]:
                                ok.append(x)
                        if len(ok)==1+len(give):
                            sepDatabaseSame[startrow[-1]].append(line[i+1:])
                            break
                        i+=1
        startrow2=[startrow[0]]
        startrow.append(-1)
        if str(startrow) not in self._finalPatterns.keys():
                self.makeNextSame(sepDatabaseSame,startrow2)
        elif self._finalPatterns[str(startrow)]<len(sepDatabaseSame[startrow[-2]]):
            self.makeNextSame(sepDatabaseSame,startrow2)
        return sepDatabaseSame[startrow[-2]]

    def getSameSeq(self,startrow):
        """
         To get words in latest sequence
        :param startrow:
         the patterns get before
        :return:
        """
        give = []
        newrow = startrow.copy()
        while newrow[-1] != -1:
            y = newrow.pop()
            give.append(y)
        return give


    def makeSeqDatabaseSame(self,database,startrow):
        """
            To make sequence dataset list which start from same word(head). It was stored only 1 from 1 line.
            And it separated by having head in latest sequence of startrow or not.

            :param database:
                    To store the transactions of a database in list
            :param startrow: list
                    the patterns get before

            """
        seqDatabase={}
        seqDatabaseSame={}
        seqLength=startrow.count(-1)+1
        for line in database:
            if len(line)>1:
                alreadyInLine=[]
                i = 0
                while line[i] != -1:
                        if line[i] not in seqDatabaseSame:
                            if -1 in startrow:
                                give=self.getSameSeq(startrow)
                            else:
                                give=startrow.copy()
                            newrow= [startrow[-1], line[i]]
                            seqDatabaseSame[line[i]] = self.serchSame(database, newrow,give)

                        i += 1
                same=0
                seqCount=0
                if self._maxLength>seqLength:
                    while len(line)>i and self._maxGap>seqCount:
                        if line[i]!=-1:
                            if line[i] not in alreadyInLine:
                                if line[i] not in seqDatabase:
                                    seqDatabase[line[i]]=[]
                                seqDatabase[line[i]].append(line[i + 1:])
                                alreadyInLine.append(line[i])
                            if line[i]==startrow[-1]:
                                same=1


                            elif same==1 and line[i] not in seqDatabaseSame:
                                if -1 in startrow:
                                    give=self.getSameSeq(startrow)
                                else:
                                    give=startrow.copy()
                                newrow= [startrow[-1], line[i]]
                                seqDatabaseSame[line[i]] = self.serchSame(database, newrow,give)

                        else:
                            same=0
                            seqCount+=1
                        i+=1


        if len(seqDatabase)!=0:
            self.makeNext(seqDatabase,startrow)
        if len(seqDatabaseSame)!=0:
            self.makeNextSame(seqDatabaseSame,startrow)



    def mine(self):
        """
            Frequent pattern mining process will start from here
        """
        self._Database = []
        self._startTime = _ab._time.time()
        self._creatingItemSets()
        self._Database=self.makeSupDatabase(self._Database,"")
        self._minSup = self._convert(self._minSup)
        self._mapNeighbours()
        self.makeSeqDatabaseFirst(self._Database)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Apriori algorithm ")

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
        """Complete set of frequent patterns will be loaded in to a output file
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
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if 5 <= len(_ab._sys.argv) <= 8:
        if len(_ab._sys.argv) == 8:
            _ap = spatialPrefixSpan(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4],_ab._sys.argv[5],_ab._sys.argv[7],_ab._sys.argv[8])
        if len(_ab._sys.argv) == 7:
            _ap = spatialPrefixSpan(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4],_ab._sys.argv[5],_ab._sys.argv[7])
        if len(_ab._sys.argv) == 6:
            _ap = spatialPrefixSpan(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4],_ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = spatialPrefixSpan(_ab._sys.argv[1], _ab._sys.argv[3],_ab._sys.argv[4])
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
        _ap = spatialPrefixSpan('testdayo.txt',"testN.txt",2, ' ')
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
        _ap.save("priOut2.txt")
