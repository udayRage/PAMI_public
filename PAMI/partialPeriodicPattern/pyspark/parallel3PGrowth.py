# **Importing this algorithm into a python program**
# --------------------------------------------------------
#
#
#             from PAMI.partialPeriodicPattern.pyspark import 4PGrowth as alg
#
#             obj = alg.parallel3PGrowth(iFile, minPS, period,numWorkers)
#
#             obj.mine()
#
#             partialPeriodicPatterns = obj.getPatterns()
#
#             print("Total number of partial periodic Patterns:", len(partialPeriodicPatterns))
#
#             obj.save(oFile)
#
#             Df = obj.getPatternInDf()
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

from PAMI.partialPeriodicPattern.pyspark import abstract as _ab
import validators as _validators
from urllib.request import urlopen as _urlopen
import sys as _sys
from pyspark import SparkContext, SparkConf
import pandas as pd
from deprecated import deprecated

_periodicSupport = float()
_period = float()
_lno = int()

class Node(object):
    """
    A class to represent the node of a tree

    :Attributes:

        item : int
            item of the node
        children : dict
            children of the node
        parent : class
            parent of the node
        tids : list.
            list of tids

    :Methods:

        _getTransactions()
            returns the list of transactions
        addChild(node)
            adds the child node to the parent node    
    
    """
    def __init__(self, item, children):
        """
        :param item : int
            item of the node
        :param children : dict
            children of the node    
        
        """
        self.item = item
        self.children = children 
        self.parent = None 
        self.tids =  []

    def _getTransactions(self):
        """
        returns the list of transactions

        """
        tids = self.tids
        for child in self.children.values():
            for t in child._getTransactions():
                t[0].append(child.item)
                yield t
        if len(tids)>0:
            yield [],tids

    def addChild(self, node): 
        """
        adds the child node to the parent node

        :param node : class
                child node to be added
        """

        self.children[node.item] = node 
        node.parent = self



class Tree(object):
    """
    A class to represent the tree

    :Attributes:

        root : class
            root of the tree
        summaries : dict
            dictionary to store the summaries
        info : dict
            dictionary to store the information

    :Methods:

        add_transaction(transaction,tid)
            adds the transaction to the tree
        add_transaction_summ(transaction,tid_summ)
            adds the transaction to the tree
        get_condition_pattern(alpha)
            returns the condition pattern
        remove_node(node_val)
            removes the node from the tree
        get_ts(j)
            returns the ts
        getTransactions()
            returns the list of transactions
        merge(tree)
            merges the tree
        generate_patterns(prefix,glist,isResponsible = lambda x:True)
            generates the patterns    
    
    """

    def __init__(self):

        self.root = Node(None, {})
        self.summaries = {}
        self.info={}


    def add_transaction(self,transaction,tid):
        """
        adds the transaction to the tree

        :param transaction : list
                transaction to be added
        :param tid : int
                tid of the transaction

        :return: class returns the tree
        
        """
        curr_node=self.root
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node=Node(transaction[i],{})
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else:
                    self.summaries[transaction[i]]=[new_node]                    
                curr_node=new_node                
            else:
                curr_node=curr_node.children[transaction[i]]            
        curr_node.tids.append(tid)
        return self
    
    def add_transaction_summ(self,transaction,tid_summ):
        """
        adds the transaction to the tree

        :param transaction : list
                transaction to be added
        :param tid_summ : list
                tid_summ of the transaction
        :return: class returns the tree
        
        """
        curr_node=self.root
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node=Node(transaction[i],{})
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else:
                    self.summaries[transaction[i]]=[new_node]                    
                curr_node=new_node                
            else:
                curr_node=curr_node.children[transaction[i]]
        curr_node.tids+=tid_summ
        return self
        
    def get_condition_pattern(self,alpha):
        """
        returns the condition pattern

        :param alpha : int
                alpha value

        :return: list
                returns the list of patterns
        """
        final_patterns=[]
        final_sets=[]
        for i in self.summaries[alpha]:
            set1=i.tids
            set2=[]
            while i.parent.item is not None:
                set2.append(i.parent.item)
                i=i.parent
            if len(set2)>0:
                set2.reverse()
                final_patterns.append(set2)
                final_sets.append(set1)
        # print(final_patterns,final_sets)
        x,y,z=cond_trans(final_patterns,final_sets)#find this
        return x,y,z
    
    def remove_node(self,node_val):
        """
        removes the node from the tree

        :param node_val : int
                node value
        
        """
        for i in self.summaries[node_val]:
            i.parent.tids +=i.tids
            del i.parent.children[node_val]
            i=None

    def get_ts(self,j):
        """
        returns the ts
        :param j : int
                j value

        :return: list
                returns the list of ts
        """
        summari=[]
        for i in self.summaries[j]:
            summari+=i.tids
        return summari
    
    def getTransactions(self):
        """
        returns the list of transactions
        :return: list
                returns the list of transactions
        """
        return [x for x in self.root._getTransactions()]

    def merge(self,tree):
        """
        merges the tree

        :param tree : class
                tree to be merged

        :return: class
                returns the merged tree
        """
        for t in tree.getTransactions():
            t[0].reverse()
            self.add_transaction_summ(t[0], t[1])
        return self
  
    def generate_patterns(self,prefix,glist,isResponsible = lambda x:True):
        """
        generates the patterns

        :param prefix : list
                prefix of the pattern
        :param glist : list.
                list of items
        :param isResponsible : lambda function.
                lambda function to check the responsibility

        :return: list
                returns the list of patterns
        
        """
        for j in sorted(self.summaries,key= lambda x: (self.info.get(x),-x)):
            if isResponsible(j):
                rec_pattern=prefix.copy()
                rec_pattern.append(glist[j])
                yield rec_pattern,self.info[j]
                patterns,tids,info=self.get_condition_pattern(j)
                conditional_tree=Tree()
                conditional_tree.info=info
                for pat in range(len(patterns)):
                    conditional_tree.add_transaction_summ(patterns[pat],tids[pat])
                if len(patterns)>=1:
                    for li_m in conditional_tree.generate_patterns(rec_pattern,glist):
                        yield li_m
            self.remove_node(j)

class parallel3PGrowth(_ab._partialPeriodicPatterns):
    """
    :Description:   4PGrowth is fundamental approach to mine the partial periodic patterns in temporal database.

    :Reference:   Discovering Partial Periodic Itemsets in Temporal Databases,SSDBM '17: Proceedings of the 29th International Conference on Scientific and Statistical Database ManagementJune 2017
                  Article No.: 30 Pages 1–6https://doi.org/10.1145/3085504.3085535

    :param  iFile: str :
                   Name of the Input file to mine complete set of frequent pattern's
    :param  oFile: str :
                   Name of the output file to store complete set of frequent patterns
    :param  period: float:
                   Minimum partial periodic...
    :param  periodicSupport: float:
                   Minimum partial periodic...

    :param  sep: str :
                   This variable is used to distinguish items from one another in a transaction. The default seperator is tab space. However, the users can override their default separator.

    :Attributes:

        iFile : file
            Name of the Input file or path of the input file
        oFile : file
            Name of the output file or path of the output file
        periodicSupport: float or int or str
            The user can specify periodicSupport either in count or proportion of database size.
            If the program detects the data type of periodicSupport is integer, then it treats periodicSupport is expressed in count.
            Otherwise, it will be treated as float.
            Example: periodicSupport=10 will be treated as integer, while periodicSupport=10.0 will be treated as float
        period: float or int or str
            The user can specify period either in count or proportion of database size.
            If the program detects the data type of period is integer, then it treats period is expressed in count.
            Otherwise, it will be treated as float.
            Example: period=10 will be treated as integer, while period=10.0 will be treated as float
        sep : str
            This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
            However, the users can override their default separator.
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        Database : list
            To store the transactions of a database in list
        mapSupport : Dictionary
            To maintain the information of item and their frequency
        lno : int
            it represents the total no of transactions
        tree : class
            it represents the Tree class
        finalPatterns : dict
            it represents to store the patterns

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
        creatingItemSets()
            Scans the dataset or dataframes and stores in list format
        partialPeriodicOneItem()
            Extracts the one-frequent patterns from transactions
        updateTransactions()
            updates the transactions by removing the aperiodic items and sort the transactions with items
            by decreasing support
        buildTree()
            constrcuts the main tree by setting the root node as null
        mine()
            main program to mine the partial periodic patterns

    **Executing the code on terminal:**
    ---------------------------------------
    .. code-block:: console


       Format:

       (.venv) $ python3 parallel3PGrowth.py <inputFile> <outputFile> <periodicSupport> <period>
    
       Examples:

       (.venv) $ python3 parallel3PGrowth.py sampleDB.txt patterns.txt 10.0 2.0

    **Sample run of the importing code:**
    -----------------------------------------
    .. code-block:: python

            from PAMI.partialPeriodicPattern.basic import 4PGrowth as alg

            obj = alg.4PGrowth(iFile, periodicSupport, period)

            obj.mine()

            partialPeriodicPatterns = obj.getPatterns()

            print("Total number of partial periodic Patterns:", len(partialPeriodicPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDf()

            memUSS = obj.getMemoryUSS()

            print("Total Memory in USS:", memUSS)

            memRSS = obj.getMemoryRSS()

            print("Total Memory in RSS", memRSS)

                run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)


    **Credits:**
    -----------------
    The complete program was written by me under the supervision of Professor Rage Uday Kiran.\n

    """

    _periodicSupport = float()
    _period = float()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _rank = {}
    _rankdup = {}
    _lno = 0

    numPartitions = 5

    @deprecated("It is recommended to use mine() instead of mine() for mining process")
    def startMine(self):
        """
        Main method where the patterns are mined by constructing tree.
        """
        
        self.mine()

    def mine(self):
        """
        Main method where the patterns are mined by constructing tree.
        """

        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minPS is None:
            raise Exception("Please enter the Minimum Period-Support")

        self._period = self._convert(self._period)
        self._minPS = self._convert(self._minPS)
        minPS = self._minPS
        period = self._period

        APP_NAME = "4PGrowth"
        conf = SparkConf().setAppName(APP_NAME)
        sc = SparkContext(conf=conf).getOrCreate()

        self._startTime = _ab._time.time()

        data = sc.textFile(self._iFile, self.numPartitions).map(lambda x: [y for y in x.strip().split(self._sep)])
        # self.numPartitions = data.getNumPartitions()
        # numPartitions = 50
        freqItems, RecItems = self.getFrequentItems(data)
        # print(RecItems)

        trans = self.getFrequentItemsets(data, freqItems, self._period, self._minPS, dict(RecItems))
        a = trans.collect()

        # print(type(a))
        for k, v in a:
            string = "\t".join(k)
            # print(string,":",v)
            self._finalPatterns[string] = v

        # print(self._finalPatterns)
        #     print(k,":",v)
        # trans.saveAsTextFile('temp')
        self._endTime = _ab._time.time()
        sc.stop()

        # self._creatingItemSets()
        # generatedItems, pfList = self._partialPeriodicOneItem()
        # _minPS, _period, _lno = self._minPS, self._period, len(self._Database)
        # updatedTransactions = self._updateTransactions(generatedItems)
        # for x, y in self._rank.items():
        #     self._rankdup[y] = x
        # info = {self._rank[k]: v for k, v in generatedItems.items()}
        # Tree = self._buildTree(updatedTransactions, info)
        # patterns = Tree._generatePatterns([])
        # self._finalPatterns = {}
        # for i in patterns:
        #     s = self._savePeriodic(i[0])
        #     self._finalPatterns[s] = i[1]
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Partial Periodic Patterns were generated successfully using 4PGrowth algorithm ")

    def _convert(self, value):
        """
        To convert the given user specified value

        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbSize * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbSize * value)
            else:
                value = int(value)
        return value

    def cond_trans(self,cond_pat,cond_tids):
        """
        returns the condition pattern

        :param cond_pat : list
                condition pattern
        :param cond_tids : list
                condition tids

        :return: list
                returns the list of patterns
        """
        pat=[]
        tids=[]
        data1={}
        # print(cond_pat,cond_tids)
        for i in range(len(cond_pat)):
            for j in cond_pat[i]:
                if j in data1:
                    data1[j]=data1[j]+cond_tids[i]
                else:
                    data1[j]=cond_tids[i]

        up_dict={}
        for m in data1:
            up_dict[m]=getps(data1[m])
        up_dict={k: v for k,v in up_dict.items() if v>=minPS}
        count=0
        for p in cond_pat:
            p1=[v for v in p if v in up_dict]
            trans=sorted(p1, key= lambda x: (up_dict.get(x),-x), reverse=True)
            if len(trans)>0:
                pat.append(trans)
                tids.append(cond_tids[count])
            count+=1
        return pat,tids,up_dict

    def getps(self,tid_list):
        """
        returns the periodic support

        :param tid_list : list.
                list of tids
        :return: int
                returns the periodic support
        """
        tid_list.sort()
        tids=tid_list
        cur=tids[0]
        pf=0
        for i in range(1,len(tids)):
            if tids[i]-cur<=self._period:
                pf+=1
            cur=tids[i]
        return pf


    def getPF(self,tid_list):
        """
        returns the periodic support

        :param tid_list : list.
                list of tids

        :return: int
                returns the periodic support
        """
        tid_list.sort()
        tids=tid_list
        cur=tids[0]
        pf=0
        for i in range(1,len(tids)):
            if tids[i]-cur<=self._period:
                pf+=1
            cur=tids[i]
        return pf

    def getFrequentItems(self,data):
        """
        returns the frequent items

        :param data : list
                list of transactions

        :return: list
                returns the list of frequent items
        """
        
        # t1 = time.time()
        singleItems = data.flatMap(lambda x: [(y,[int(x[0])]) for y in x[1:]])
        RecItems=singleItems.reduceByKey(lambda x,y: x + y)\
        .map(lambda c :(c[0],self.getPF(c[1]))).filter(lambda c: c[1]>=self._minPS).collect()
        # RecItems=itemsWtTids.filter(lambda c : getPF(c[1])>=minPS)
        RecItemSorted=[x for (x,y) in sorted(RecItems,key=lambda x : -x[1])]
        # t2 = time.time()
        # print ("size one", t2-t1)
        return RecItemSorted, RecItems

    def getFrequentItemsets(self,data,perFreqItems,per,minPS, PSinfo):
        """
        returns the frequent itemsets

        :param data : list.
                list of transactions
        :param perFreqItems : list.
                list of frequent items
        :param per : int
                period
        :param minPS : int
                minimum periodic support
        :param PSinfo : dict
                dictionary to store the information

        :return: list
                returns the list of frequent itemsets

        """
        # t1 = time.time()
        rank = dict([(index, item) for (item,index) in enumerate(perFreqItems)]) 
        numPartitions = data.getNumPartitions()
        workByPartition = data.flatMap(lambda basket:self.genCondTransactions(basket[0], basket[1:],rank,numPartitions))
        # emptyTree =ppp.Tree()
        c=0
        inf={}
        # print(rank)
        # print(PSinfo)
        v=len(perFreqItems)
        for i in rank:
            inf[rank[i]]=PSinfo[i]
            c+=1
        # print(inf)
        emptyTree = Tree()

        emptyTree.info=inf    
        forest = workByPartition.aggregateByKey(emptyTree,lambda tree,transaction: tree.add_transaction(transaction[1:], transaction[0]),lambda tree1,tree2: tree1.merge(tree2))
        itemsets = forest.flatMap(lambda partId_bonsai: partId_bonsai[1].generate_patterns([],perFreqItems, lambda x: self.getPartitionId(x,numPartitions) == partId_bonsai[0]))
        # t2 = time.time()
        # print ("main", t2-t1)
        return itemsets
    
    def genCondTransactions(self,tid,basket, rank, nPartitions):
        """
        returns the conditional transactions

        :param tid : int
                tid of the transaction
        :param basket : list.
                list of items
        :param rank : dict
                dictionary to store the rank
        :param nPartitions : int
                number of partitions

        :return: list
                returns the list of conditional transactions
        
        """
        #translate into new id's using rank
        filtered = [rank[x] for x in basket if x in rank.keys()]
        #sort basket in ascending rank
        filtered = sorted(filtered)
        output = {}
        pc=0
        for i in range(len(filtered)-1, -1, -1):
            item = filtered[i]
            partition = self.getPartitionId(item, nPartitions)
            if partition not in output.keys():
                output[partition] = [int(tid)]+filtered[:i+1]
                pc+=1
                if pc==nPartitions:
                    break
        return [x for x in output.items()]

    def getPartitionId(self,key, nPartitions):
        return key % nPartitions
    
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
            # print(a,b)
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'minPS'])
        return dataFrame

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: csv file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        print("Total number of Partial Periodic Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:",  self.getRuntime())

    def setPartitions(self,nums):
        self.numPartitions = nums

def cond_trans(cond_pat,cond_tids):
    """
    returns the condition pattern

    :param cond_pat : list
            condition pattern
    :param cond_tids : list
            condition tids

    """
    
    pat=[]
    tids=[]
    data1={}
    # print(cond_pat,cond_tids)
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in data1:
                data1[j]=data1[j]+cond_tids[i]
            else:
                data1[j]=cond_tids[i]

    up_dict={}
    for m in data1:
        up_dict[m]=getps(data1[m])
    up_dict={k: v for k,v in up_dict.items() if v>=minPS}
    count=0
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1, key= lambda x: (up_dict.get(x),-x), reverse=True)
        if len(trans)>0:
            pat.append(trans)
            tids.append(cond_tids[count])
        count+=1
    return pat,tids,up_dict

def getps(tid_list):
    """
    
    returns the periodic support

    :param tid_list : list.
            list of tids

    """
    tid_list.sort()
    tids=tid_list
    cur=tids[0]
    pf=0
    for i in range(1,len(tids)):
        if tids[i]-cur<=period:
            pf+=1
        cur=tids[i]
    return pf


def getPF(self,tid_list):
    tid_list.sort()
    tids=tid_list
    cur=tids[0]
    pf=0
    for i in range(1,len(tids)):
        if tids[i]-cur<=period:
            pf+=1
        cur=tids[i]
    return pf
    
if __name__ == "__main__":
    _ap = str()
    if len(_sys.argv) == 5 or len(_sys.argv) == 6:
        period = 0
        minPS = 0
        if len(_sys.argv) == 6:
            _ap = parallel3PGrowth(_sys.argv[1], _sys.argv[3], _sys.argv[4], _sys.argv[5])
        if len(_sys.argv) == 5:
            _ap = parallel3PGrowth(_sys.argv[1], _sys.argv[3], _sys.argv[4])
        _ap.mine()
        print("Total number of Partial Periodic Patterns:", len(_ap.getPatterns()))
        _ap.save(_sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:",  _ap.getRuntime())
    else:
        print("Error! The number of input parameters do not match the total number of parameters provided")
        minPS = 500
        period = 50000


        _ap = parallel3PGrowth('Temporal_T10I4D100K.csv', minPS, period, '\t')
        _ap.setPartitions(20)
        _ap.mine()
        