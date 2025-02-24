import random as _rd
#import sys as _sys


class createSyntheticUtility:
    """

    This class create synthetic utility database.

    :Attribute:

        totalTransactions : int
            No of transactions
        noOfItems : int 
            No of items
        maxUtilRange: int
            Maximum utility range
        avgTransactionLength : int
            The length of average transaction
        outputFile: str
            Name of the output file.

    :Methods:

        createUtilityDatabase(outputFile)
            Create utility database from DataFrame and store into outputFile

    **Credits:**
    ---------------
             The complete program was written by  P.Likhitha under the supervision of Professor Rage Uday Kiran.

    """
    
    def __init__(self, transactions: int, items: int, maxUtilRange: int, avgTransaction: int) -> None:
        self._totalTransactions = transactions
        self._noOfItems = items
        self._maxUtilRange = maxUtilRange
        self._avgTransactionLength = avgTransaction
    
    def createUtilityDatabase(self, outputFile: str) -> None:
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
            su = []
            for _ in range(length):
                item = _rd.randint(1, self._noOfItems)
                utility = _rd.randint(1, self._maxUtilRange) 
                st = st + str(item) + '\t'
                su.append(utility)
                st1 = st1 + str(utility) + '\t'
            summation = sum([i for i in su])
            st = st + ":" + str(summation) + ":"
            writer.write("%s" % st)
            writer.write("%s \n" % st1)
            
if __name__ == "__main__":
    #_ap = str()
    _ap = createSyntheticUtility(100000, 870, 100, 10)
    _ap.createUtilityDatabase("T10_util.txt")
else:
    print("Error! The number of input parameters do not match the total number of parameters provided")
