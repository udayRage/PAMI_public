import random as _rd
#import sys as _sys


class createSyntheticUncertainTransaction:
    """
    This class create synthetic transaction database.

    :Attribute:

        totalTransactions : int
            No of transactions
        noOfItems : int 
            No of items
        avgTransactionLength : str
            The length of average transaction
        outputFile: str
            Name of the output file.

    :Methods:

        createUncertainTransactionalDatabase(outputFile)
            Create uncertain transactional database and store into outputFile

    **Credits:**
    -------------
        The complete program was written by  P.Likhitha   under the supervision of Professor Rage Uday Kiran.

    """
    
    def __init__(self, transactions: int, items: int, avgTransaction: int) -> None:
        self._totalTransactions = transactions
        self._noOfItems = items
        self._avgTransactionLength = avgTransaction
    
    def createUncertainTransactionalDatabase(self, outputFile: str) -> None:
        """
        create transactional database and return outputFileName

        :param outputFile: file name or path to store database
        :type outputFile: str
        :return: outputFile name
        """
        writer = open(outputFile, 'w+')
        for i in range(self._totalTransactions):
            length = _rd.randint(1, self._avgTransactionLength + 20)
            st = str()
            st1 = str()
            for _ in range(length):
                item = _rd.randint(1, self._noOfItems)
                probability = _rd.uniform(0, 1)
                st = st + str(item) + '\t'
                st1 = st1 + str(probability) + '\t'
            writer.write("%s:" % st)
            writer.write("%s \n" % st1)
            
            
if __name__ == "__main__":
    #_ap = str()
    _ap = createSyntheticUncertainTransaction(100000, 870, 10)
    _ap.createUncertainTransactionalDatabase("T10_uncertain.txt")
else:
    print("Error! The number of input parameters do not match the total number of parameters provided")
