import random as _rd
#import sys as _sys


class createSyntheticGeoreferentialTransaction:
    """
    This class create synthetic geo-referential transaction database.

    :Attribute:

        totalTransactions : int
            No of transactions
        items : int 
            No of items
        avgTransactionLength : str
            The length of average transaction
        outputFile: str
            Name of the output file.

    :Methods:

        createGeoreferentialTransactionDatabase(outputFile)
            Create geo-referential transactional database and store into outputFile


    **Credits:**
    --------------
             The complete program was written by  P.Likhitha   under the supervision of Professor Rage Uday Kiran.

    """
    
    def __init__(self, transactions, items, avgTransaction):
        self._totalTransactions = transactions
        self._noOfItems = items
        self._avgTransactionLength = avgTransaction
    
    def createGeoreferentialTransactionalDatabase(self, outputFile):
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
            for _ in range(length):
                rd = _rd.randint(0, len(items) - 1)
                item = items[rd]
                st = st + str(item) + '\t'
            writer.write("%s \n" % st)
            
if __name__ == "__main__":
    #_ap = str()
    _ap = createSyntheticGeoreferentialTransaction(100000, 870, 10)
    _ap.createGeoreferentialTransactionalDatabase("T10_geo.txt")
else:
    print("Error! The number of input parameters do not match the total number of parameters provided")
