# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.contiguousFrequentPattern.basic import PositionMining as alg
#
#             obj =alg.PositionMining(minsup=5,data="Data.csv")
#
#             obj.mine()
#
#             Patterns = obj.getPatterns()
#
#             print("Total number of high utility frequent Patterns:", len(Patterns))
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





import pandas as pd
#import numpy as np
#import math
from PAMI.contiguousFrequentPattern.basic import abstract as _ab
from deprecated import deprecated


class Node:
    def __init__(self,symbol,leaf=False):
        self._val=symbol
        self.children=[None for _ in range(26)]
        self.leaf=leaf
        self.freq={}
        self.count=1
        self.seq=""




class PositionMining:
    """
    About this algorithm
    ====================

    :Description:  describe the algorithm

    :Reference: provide the reference of the algorithm with URL of the paper, if possible

    :param  parameter: parameterType :
                    description of the parameters. Parameters are the variables used in problem definition of the model.

    :Attributes:

        min_IG: float
                minimum threshold for information gain
            
        min_conf: float
                minimum threshold for confidence

        datapath: .csv file consisting of two id,seq fields respectively in order
    

    Credits
    =======
             The complete program was written by Shiridi kumar under the supervision of Professor uday rage.

    """

    def __init__(self,minsup,datapath,maxlength=20):
        self.min_sup=minsup
        self.datapath=datapath
        self.maxlength=maxlength
        self.seq_prefixes = None
        self.data = None
        self.symbol_freq = None
        self.total_length = None
        self._startTime = None
        self._endTime = None
        self._memoryUSS = float()
        self._memoryRSS = float()
        self.table = None
        self.current_candidate = None
        self.frequentPatterns = None
    

    def readData(self):
        df=pd.read_csv(self.datapath)
        vals=df.values
        self.seq_prefixes = {}
        # prev=0
        # self.seq_prefixes[vals[0][0]]=len(vals[0])
        # for i in range(1,len(vals)):
        #     self.seq_prefixes[vals[i]]
        self.data=vals
        # print(self.data)

    def getfreqs(self):
        """
        Initial scan of database where frequent length one candidate will be mined
        """
        self.symbol_freq={"A":set(),"G":set(),"C":set(),"T":set()}
        self.total_length=0
        curr_pos=0
        # print(self.data)
        for i in range(len(self.data)):
            seq=self.data[i][1]
            for j in range(len(seq)):
                self.symbol_freq[seq[j]].add(curr_pos)
                curr_pos+=1
            curr_pos+=1
            self.total_length+=len(seq)

        temp={}
        for i in self.symbol_freq:
            if len(self.symbol_freq[i])>=self.min_sup:
                temp.update({i:self.symbol_freq[i]})
        self.symbol_freq=temp

    
    

    def getPatterns(self):
        """
        Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """

        return self.frequentPatterns


    def getPatternsAsDataFrame(self):
        """
        Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        #dataFrame = {}
        #data = []
        seqs=[]
        sup=[]
        for i in self.frequentPatterns:
            seqs.append(i)
            sup.append(self.frequentPatterns[i])


        dataFrame =pd.DataFrame()
        dataFrame["Patterns"]=seqs
        dataFrame["Support"]=sup
        return dataFrame


    def save(self, outFile):
        """
        Complete set of frequent patterns will be loaded in to an output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        df=self.getPatternsAsDataFrame()
        df.to_csv(outFile)


        
    def get_Klength_patterns(self,k):
        """
        Get frequent patterns of klength

        :param k : length of the pattern
        :type k: dictionary of frequent patterns
        """

        dic={i:len(self.table[k][i]) for i in self.table[k]}
        return dic
    


    def getPattern_positions(self,pattern):
        length=len(pattern)
        positions=self.table[length][pattern]
        return positions

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
        return self._endTime-self._startTime
    
    def printResults(self):
        """
        This function is used to print the results
        """
        print("Total number of High Utility Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


    def join(self,db,length):
        """
        Generating l+1 frequent patterns using two l length frequent patterns

        :param db:current l length frequent patterns table consisting of their positions
        :type db: HashTable
        :param length:current length of the frequent candidates generated
        :type length: positive integer
        """
        for seq1 in db:
            for seq2 in db:
                if seq1!=seq2:
                    if length==1:
                        word=seq1+seq2
                        # print(seq1,seq2,db[seq1],db[seq2])
                        minus_1={i-1 for i in db[seq2]}
                        positions=db[seq1].intersection(minus_1)
                        if len(positions)>=self.min_sup:
                            self.table[length+1].update({word:positions})


                    else:
                        if seq1[1:]== seq2[:-1]:
                            word=seq1+seq2[-1]
                            minus_1={i-1 for i in db[seq2]}
                            positions=db[seq1].intersection(minus_1)
                            if len(positions)>=self.min_sup:
                                self.table[length+1].update({word:positions})
        

    def mineNext_candidates(self):
        """
        Mining frequent patterns along with their positions from length 1 frequent candidates
        """
        while self.current_candidate<self.maxlength-1:
            curr=self.table[self.current_candidate]
            self.join(curr,self.current_candidate)
            self.current_candidate+=1

    @deprecated("It is recommended to use 'mine()' instead of 'mine()' for mining process. Starting from January 2025, 'mine()' will be completely terminated.")
    def startMine(self):
        """
        Pattern mining process will start from here
        """
        # pass
        self.mine()

    def mine(self):
        """
        Pattern mining process will start from here
        """
        # pass
        self._startTime = _ab._time.time()
        self.table = {i: {} for i in range(1, self.maxlength)}
        self.readData()

        self.getfreqs()
        temp = self.symbol_freq
        self.table.update({1: temp})
        self.current_candidate = 1
        self.mineNext_candidates()
        self.frequentPatterns = {}
        for length in self.table:
            temp = self.table[length]
            for pattern in temp:
                self.frequentPatterns.update({pattern: len(temp[pattern])})

        process = _ab._psutil.Process(_ab._os.getpid())
        self._endTime = _ab._time.time()
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss