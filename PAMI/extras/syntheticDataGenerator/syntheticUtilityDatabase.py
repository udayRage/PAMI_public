import random as _rd
import psutil,os,time

class syntheticUtilityDatabase:
    """
    This class creates a synthetic utility database.

    Attributes:
        totalTransactions :int
                    Number of transactions.
        numOfItems : int
                    Number of items.
        maxUtilRange : int
                    Maximum utility range.
        avgTransactionLength : int
                    The length of average transaction.
        _memoryUSS : float
                    To store the total amount of USS memory consumed by the program
        _memoryRSS : float
                    To store the total amount of RSS memory consumed by the program
        _startTime : float
                    To record the start time of the mining process
        _endTime : float
                    To record the completion time of the mining process

    Methods:
        __init__(totalTransactions, numOfItems, maxUtilRange, avgTransactionLength)
            Constructor to initialize the database parameters.
        createSyntheticUtilityDatabase(outputFile)
            Create utility database and store it in the specified output file.
        createRandomNumbers(n, targetSum)
            Generate a list of random numbers with a specified target sum.
        save(outputFile)
            Save the generated utility database to a CSV file.
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
    Credits:
        The complete program was written by A.Hemanth sree sai under the supervision of Professor Rage Uday Kiran.
    """

    def __init__(self, totalTransactions: int, numOfItems: int, maxUtilRange: int, avgTransactionLength: int) -> None:
        """
        Constructor to initialize the database parameters.

        Parameters:
            totalTransactions (int): Number of transactions.
            numOfItems (int): Number of items.
            maxUtilRange (int): Maximum utility range.
            avgTransactionLength (int): The length of average transaction.
        """
        self.totalTransactions = totalTransactions
        self.numOfItems = numOfItems
        self.maxUtilRange = maxUtilRange
        self.avgTransactionLength = avgTransactionLength
        self.transactions = []
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()

    def createSyntheticUtilityDatabase(self, outputFile: str) -> None:
        """
        Create utility database and store it in the specified output file.

        Parameters:
            outputFile (str): File name or path to store the database.
        """
        self._startTime = time.time()
        if self.avgTransactionLength > self.numOfItems:
            print("Error: avgTransactionLength cannot exceed numOfItems.")
            return

        with open(outputFile, 'w') as writer:
            for _ in range(self.totalTransactions):
                length = _rd.randint(1, self.avgTransactionLength + 20)
                items = [_rd.randint(1, self.numOfItems) for _ in range(length)]
                utilities = [_rd.randint(1, self.maxUtilRange) for _ in range(length)]

                # Generating 13 random numbers with a target sum of 2000
                randomNumbers = self.createRandomNumbers(13, 2000)

                # Checking if avgTransactionLength exceeds numOfItems
                if self.avgTransactionLength > self.numOfItems:
                    print("Error: avgTransactionLength cannot exceed numOfItems.")
                    return

                st = '\t'.join(map(str, items)) + '\t:' + str(sum(utilities)) + ':'
                st1 = '\t'.join(map(str, randomNumbers)) + '\t'

                writer.write(f"{st}{st1}\n")
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        self._endTime = time.time()

    @staticmethod
    def createRandomNumbers(n: int, targetSum: int) -> list[float]:
        """
        Generate a list of random numbers with a specified target sum.

        Parameters:
            n (int): Number of random numbers to generate.
            targetSum (int): Target sum for the generated random numbers.

        Returns:
            list: List of generated random numbers normalized and multiplied by the target sum.
        """
        randNumbers = [_rd.uniform(0, 1) for _ in range(n)]
        randSum = sum(randNumbers)
        normalizedNumbers = [num / randSum for num in randNumbers]
        result = [round(num * targetSum) for num in normalizedNumbers]
        return result

    def save(self, outputFile: str) -> None:
        """
        Save the generated utility database to a CSV file.

        Parameters:
            outputFile (str): File name or path to store the CSV file.
        """
        with open(outputFile, 'w') as f:
            for transaction in self.transactions:
                f.write('\t'.join(map(str, transaction)) + '\n')

    def getMemoryUSS(self) -> float:
        """
        Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self) -> float:
        """
        Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self) -> float:
        """
        Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

if __name__ == "__main__":
    obj = syntheticUtilityDatabase(100000, 870, 100, 10)
    obj.createSyntheticUtilityDatabase("T10_util-12.csv")
    print("create SyntheticUtilityDatabase is complete.")
    print("Total Memory in USS:", obj.getMemoryUSS())
    print("Total Memory in RSS", obj.getMemoryRSS())
    print("Total ExecutionTime in ms:", obj.getRuntime())
else:
    print("Error! The number of input parameters does not match the total number of parameters provided")
