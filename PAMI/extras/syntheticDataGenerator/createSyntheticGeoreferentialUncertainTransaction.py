import random as _rd
#import sys as _sys


class createSyntheticGeoreferentialUncertainTransaction:
    """
    This class is to create synthetic geo-referential uncertain transaction database.

    :Attribute:

        totalTransactions : int
            No of transactions
        noOfItems : int 
            No of items
        avgTransactionLength : int
            The length of average transaction
        outputFile: str
            Name of the output file.

    :Methods:

        createGeoreferentialuncertainTransactionDatabase(outputFile)
            Create geo-referential transactional database store into outputFile

    **Credits:**
    --------------
        The complete program was written by  P.Likhitha   under the supervision of Professor Rage Uday Kiran.

    """
    
    def __init__(self, transactions: int, items: int, avgTransaction: int) -> None:
        self._totalTransactions = transactions
        self._noOfItems = items
        self._avgTransactionLength = avgTransaction
    
    def createGeoreferentialUncertainTransactionalDatabase(self, outputFile: str) -> None:
        """
        create transactional database and return outputFileName

        :param outputFile: file name or path to store database
        :type outputFile: str
        :return: outputFile name
        """
        writer = open(outputFile, 'w+')
        items = []
        for i in range(self._noOfItems):
            lat = _rd.randint(1, self._noOfItems)
            lon = _rd.randint(1, self._noOfItems)
            if lat == lon:
                lon = _rd.randint(1, self._noOfItems)
            stt = '(' + str(lat) + ' ' + str(lon) + ')'
            items.append(stt)
        for i in range(self._totalTransactions):
            length = _rd.randint(1, self._avgTransactionLength + 20)
            st = str()
            st1 = str()
            for _ in range(length):
                rd = _rd.randint(0, len(items) - 1)
                item = items[rd]
                probability = _rd.uniform(0, 1)
                st = st + str(item) + '\t'
                st1 = st1 + str(probability) + '\t'
            writer.write("%s" % st)
            writer.write(":")
            writer.write("%s \n" % st1)
            
if __name__ == "__main__":
    #_ap = str()
    _ap = createSyntheticGeoreferentialUncertainTransaction(100000, 870, 10)
    _ap.createGeoreferentialUncertainTransactionalDatabase("T10_geo_un.txt")
else:
    print("Error! The number of input parameters do not match the total number of parameters provided")
