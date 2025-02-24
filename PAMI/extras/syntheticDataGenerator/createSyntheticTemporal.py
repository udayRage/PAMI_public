import random as _rd
#import sys as _sys
class createSyntheticTemporal:
    """
    This class create synthetic temporal database.

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

        createTemporallDatabase(outputFile)
            Create temporal database from DataFrame and store into outputFile

    **Credits:**
    ---------------
             The complete program was written by  P.Likhitha   under the supervision of Professor Rage Uday Kiran.

    """
    
    def __init__(self, transactions: int, items: int, avgTransaction: int) -> None:
        self._totalTransactions = transactions
        self._noOfItems = items
        self._avgTransactionLength = avgTransaction
    
    def createTemporalDatabase(self, outputFile: str) -> None:
        """
        create transactional database and return outputFileName

        :param outputFile: file name or path to store database
        :type outputFile: str
        :return: outputFile name
        """
        count = 1
        writer = open(outputFile, 'w+')
        for i in range(self._totalTransactions):
            length = _rd.randint(1, self._avgTransactionLength + 20)
            st = str(count) + '\t'
            for _ in range(length):
                item = _rd.randint(1, self._noOfItems)
                st = st + str(item) + '\t'
            writer.write("%s \n" % st)
            count += 1
            
if __name__ == "__main__":
    #_ap = str()
    _ap = createSyntheticTemporal(100000, 870, 10)
    _ap.createTemporalDatabase("temporal_T10.txt")
else:
    print("Error! The number of input parameters do not match the total number of parameters provided")
