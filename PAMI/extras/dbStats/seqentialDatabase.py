import statistics
import pandas as pd
import validators
import numpy as np
from urllib.request import urlopen
import PAMI.extras.graph.plotLineGraphFromDictionary as plt


class sequentialDatabase:
    """
    sequentialDatabaseStats is class to get stats of database.
        Attributes:
        ----------
        inputFile : file
            input file path
        database : dict
            store time stamp and its transaction
        lengthList : list
            store length of all transaction
        sep : str
            separator in file. Default is tab space.
        Methods:
        -------
        run()
            execute readDatabase function
        readDatabase()
            read database from input file
        getDatabaseSize()
            get the size of database
        getMinimumTransactionLength()
            get the minimum transaction length
        getAverageTransactionLength()
            get the average transaction length. It is sum of all transaction length divided by database length.
        getMaximumTransactionLength()
            get the maximum transaction length
        getStandardDeviationTransactionLength()
            get the standard deviation of transaction length
        getVarianceTransactionLength()
            get the variance of transaction length
        getSparsity()
            get the sparsity of database
        getSortedListOfItemFrequencies()
            get sorted list of item frequencies
        getSortedListOfTransactionLength()
            get sorted list of transaction length
        save(data, outputFile)
            store data into outputFile
    """

    def __init__(self, inputFile, sep='\t'):
        """
        :param inputFile: input file name or path
        :type inputFile: str
        """
        self.inputFile = inputFile
        self.lengthList = []
        self.sep = sep
        self.database = {}
        self.NumOfSeqList=[]

    def run(self):
        self.readDatabase()

    def readDatabase(self):
        """
        read database from input file and store into database and size of each transaction.
        """
        # self.creatingItemSets()
        numberOfTransaction = 0
        if isinstance(self.inputFile, pd.DataFrame):
            if self.inputFile.empty:
                print("its empty..")
            i = self.inputFile.columns.values.tolist()
            if 'tid' in i and 'Transactions' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
            if 'tid' in i and 'Patterns' in i:
                self.database = self.inputFile.set_index('tid').T.to_dict(orient='records')[0]
            for _data in self.database.keys():
                numberOfTransaction=numberOfTransaction+1
                seqlist = []
                NumOfSeq = 0
                for i in self.database[_data]:
                    if i == "-1":
                        NumOfSeq = NumOfSeq + 1
                    elif i != "-2":
                        seqlist.append(i)
                self.NumOfSeqList.append(NumOfSeq)
                self.database[numberOfTransaction] = seqlist


        if isinstance(self.inputFile, str):
            if validators.url(self.inputFile):
                _data = urlopen(self.inputFile)
                for line in _data:
                    numberOfTransaction += 1
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self.sep)]
                    seqlist = []
                    NumOfSeq = 0
                    for i in temp:
                        if i == "-1":
                            NumOfSeq = NumOfSeq + 1
                        elif i != "-2":
                            seqlist.append(i)
                    self.NumOfSeqList.append(NumOfSeq)
                    self.database[numberOfTransaction] = seqlist
            else:
                try:
                    with open(self.inputFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            numberOfTransaction += 1
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self.sep)]
                            seqlist=[]
                            NumOfSeq=0
                            for i in temp:
                                if i=="-1":
                                    NumOfSeq=NumOfSeq+1
                                elif i!="-2":
                                    seqlist.append(i)
                            self.NumOfSeqList.append(NumOfSeq)
                            self.database[numberOfTransaction] = seqlist
                except IOError:
                    print("File Not Found")
                    quit()
        self.lengthList = [len(s) for s in self.database.values()]

    def getDatabaseSize(self):
        """
        get the size of database
        :return: data base size
        """
        return len(self.database)

    def getTotalNumberOfItems(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return len(self.getSortedListOfItemFrequencies())

    def getTotalNumberOfISeq(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return sum(self.NumOfSeqList)

    def getMinimumTransactionLength(self):
        """
        get the minimum transaction length
        :return: minimum transaction length
        """
        return min(self.lengthList)

    def getMinimumSequenceLength(self):
        """
        get the minimum Sequence length
        :return: minimum Sequence length
        """
        return min(self.NumOfSeqList)

    def getAverageTransactionLength(self):
        """
        get the average transaction length. It is sum of all transaction length divided by database length.
        :return: average transaction length
        """
        totalLength = sum(self.lengthList)
        return totalLength / len(self.database)

    def getAverageItemsInSequenceLength(self):
        """
        get the average Sequence length. It is sum of all transaction length divided by database length.
        :return: average Sequence length
        """
        totalLength = sum(self.NumOfSeqList)
        return sum(self.lengthList)/totalLength

    def getAverageSequenceLength(self):
        """
        get the average Sequence length. It is sum of all Sequence length divided by database length.
        :return: average Sequence length
        """
        totalLength = sum(self.NumOfSeqList)
        return totalLength / len(self.database)

    def getMaximumTransactionLength(self):
        """
        get the maximum transaction length
        :return: maximum transaction length
        """
        return max(self.lengthList)

    def getMaximumSequenceLength(self):
        """
        get the maximum Sequence length
        :return: maximum Sequence length
        """
        return max(self.NumOfSeqList)

    def getStandardDeviationTransactionLength(self):
        """
        get the standard deviation transaction length
        :return: standard deviation transaction length
        """
        return statistics.pstdev(self.lengthList)

    def getStandardDeviationSequenceLength(self):
        """
        get the standard deviation Sequence length
        :return: standard deviation Sequence length
        """
        return statistics.pstdev(self.NumOfSeqList)

    def getVarianceTransactionLength(self):
        """
        get the variance transaction length
        :return: variance transaction length
        """
        return statistics.variance(self.lengthList)

    def getVarianceSequenceLength(self):
        """
        get the variance Sequence length
        :return: variance Sequence length
        """
        return statistics.variance(self.NumOfSeqList)

    def getNumberOfItems(self):
        """
        get the number of items in database.
        :return: number of items
        """
        return len(self.getSortedListOfItemFrequencies())

    def convertDataIntoMatrix(self):
        singleItems = self.getSortedListOfItemFrequencies()
        # big_array = np.zeros((self.getDatabaseSize(), len(self.getSortedListOfItemFrequencies())))
        itemsets = {}
        for i in self.database:
            for item in singleItems:
                if item in itemsets:
                    if item in self.database[i]:
                        itemsets[item].append(1)
                    else:
                        itemsets[item].append(0)
                else:
                    if item in self.database[i]:
                        itemsets[item] = [1]
                    else:
                        itemsets[item] = [0]
        # new = pd.DataFrame.from_dict(itemsets)
        data_ = list(itemsets.values())
        an_array = np.array(data_)
        return an_array

    def getSparsity(self):
        """
        get the sparsity of database. sparsity is percentage of 0 of database.
        :return: database sparsity
        """
        big_array = self.convertDataIntoMatrix()
        n_zeros = np.count_nonzero(big_array == 0)
        return n_zeros / big_array.size

    def getDensity(self):
        """
        get the sparsity of database. sparsity is percentage of 0 of database.
        :return: database sparsity
        """
        big_array = self.convertDataIntoMatrix()
        n_zeros = np.count_nonzero(big_array != 0)
        return n_zeros / big_array.size

    def getSortedListOfItemFrequencies(self):
        """
        get sorted list of item frequencies
        :return: item frequencies
        """
        itemFrequencies = {}
        for tid in self.database:
            for item in self.database[tid]:
                itemFrequencies[item] = itemFrequencies.get(item, 0)
                itemFrequencies[item] += 1
        return {k: v for k, v in sorted(itemFrequencies.items(), key=lambda x: x[1], reverse=True)}

    def getFrequenciesInRange(self):
        fre = self.getSortedListOfItemFrequencies()
        rangeFrequencies = {}
        maximum = max([i for i in fre.values()])
        values = [int(i * maximum / 6) for i in range(1, 6)]
        va = len({key: val for key, val in fre.items() if 0 < val < values[0]})
        rangeFrequencies[va] = values[0]
        for i in range(1, len(values)):
            va = len({key: val for key, val in fre.items() if values[i] > val > values[i - 1]})
            rangeFrequencies[va] = values[i]
        return rangeFrequencies

    def getSequentialLengthDistribution(self):
        """
        get transaction length
        :return: transaction length
        """
        transactionLength = {}
        for length in self.lengthList:
            transactionLength[length] = transactionLength.get(length, 0)
            transactionLength[length] += 1
        return {k: v for k, v in sorted(transactionLength.items(), key=lambda x: x[0])}

    def save(self, data_, outputFile):
        """
        store data into outputFile
        :param data_: input data
        :type data_: dict
        :param outputFile: output file name or path to store
        :type outputFile: str
        """
        with open(outputFile, 'w') as f:
            for key, value in data_.items():
                f.write(f'{key}\t{value}\n')

    def printStats(self):
        print(f'Database size (total no of transactions) : {self.getDatabaseSize()}')
        print(f'Number of items : {self.getNumberOfItems()}')
        print(f'Number of sequence : {self.getTotalNumberOfISeq()}')
        print(f'Average items in sequence : {self.getAverageItemsInSequenceLength()}')
        print(f'Minimum number of events in sequence : {self.getMinimumSequenceLength()}')
        print(f'Average number of events in sequence : {self.getAverageSequenceLength()}')
        print(f'Maximum number of events in sequence: {self.getMaximumSequenceLength()}')
        print(f'Variance in sequence Sizes : {self.getVarianceSequenceLength()}')
        print(f'Minimum Transaction Size : {self.getMinimumTransactionLength()}')
        print(f'Average Transaction Size : {self.getAverageTransactionLength()}')
        print(f'Maximum Transaction Size : {self.getMaximumTransactionLength()}')
        print(f'Standard Deviation Transaction Size : {self.getStandardDeviationTransactionLength()}')
        print(f'Variance in Transaction Sizes : {self.getVarianceTransactionLength()}')
        print(f'Sparsity : {self.getSparsity()}')


    def plotGraphs(self):
        itemFrequencies = self.getFrequenciesInRange()
        transactionLength = self.getSequentialLengthDistribution()
        plt.plotLineGraphFromDictionary(itemFrequencies, 100, 'Frequency', 'No of items', 'frequency')
        plt.plotLineGraphFromDictionary(transactionLength, 100, 'transaction length', 'transaction length', 'frequency')


if __name__ == '__main__':

    data = {'tid': [1, 2, 3, 4, 5, 6, 7],

            'Transactions': [['a', 'd', 'e'], ['b', 'a', 'f', 'g', 'h'], ['b', 'a', 'd', 'f'], ['b', 'a', 'c'],
                             ['a', 'd', 'g', 'k'],

                             ['b', 'd', 'g', 'c', 'i'], ['b', 'd', 'g', 'e', 'j']]}

    # data = pd.DataFrame.from_dict('transactional_T10I4D100K.csv')
    import PAMI.extras.graph.plotLineGraphFromDictionary as plt

    # obj = transactionalDatabaseStats(data)
    obj = sequentialDatabase('retail.txt', ' ')
    obj.run()
    obj.printStats()
    obj.plotGraphs()