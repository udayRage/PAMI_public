import pandas as pd
import numpy as np
import sys
import time
import os
import psutil

class TemporalDatabase:

    def __init__(self, databaseSize: int,
                 avgItemsPerTransaction: int,
                 numItems: int,
                 sep: str = '\t',
                 occurrenceProbabilityOfSameTimestamp: float = 0.1,
                 occurrenceProbabilityToSkipSubsequentTimestamp: float = 0.1) -> None:

        self.df = None
        self.outputFile = None
        self._memoryRSS = None
        self._memoryUSS = None
        self._runTime = None
        self.current_timestamp = None
        self.db = None
        self.databaseSize = databaseSize
        self.avgItemsPerTransaction = avgItemsPerTransaction
        self.numItems = numItems
        self.sep = sep
        self.occurrenceProbabilityOfSameTimestamp = occurrenceProbabilityOfSameTimestamp
        self.occurrenceProbabilityToSkipSubsequentTimestamp = occurrenceProbabilityToSkipSubsequentTimestamp

    @staticmethod
    def performCoinFlip(probability: float) -> bool:
        """
        Perform a coin flip with the given probability.

        :param probability: Probability of the coin landing heads (i.e., the event occurring).
        :return: True if the coin lands heads, False otherwise.
        """
        result = np.random.choice([0, 1], p=[1 - probability, probability])
        return result == 1

    def tuning(self, array, sumRes) -> list:
        """
        Tune the array to ensure that the sum of the values equals sumRes.
        """
        num_transactions = len(array)
        # Initialize values randomly between 1 and numItems
        values = np.random.randint(1, self.numItems + 1, num_transactions)

        # normalize values to ensure sum equals sumRes
        values = values / np.sum(values) * sumRes
        values = np.round(values).astype(int)


        # Adjust values to ensure sum equals sumRes
        while np.sum(values) != sumRes:
            current_sum = np.sum(values)
            if current_sum > sumRes:
                # Decrease the value of a random index
                indices = np.where(values > 1)[0]
                if len(indices) == 0:
                    raise ValueError("Cannot adjust values to meet sumRes")
                idx = np.random.choice(indices)
                values[idx] -= 1
            else:
                # Increase the value of a random index
                indices = np.where(values < self.numItems)[0]
                if len(indices) == 0:
                    raise ValueError("Cannot adjust values to meet sumRes")
                idx = np.random.choice(indices)
                values[idx] += 1

        # Assign adjusted values back to array
        for i in range(len(array)):
            array[i][1] = values[i]

        return array

    def create(self) -> None:
        """
        Create the temporal database or DataFrame based on the specified type of file.
        """
        start = time.time()

        self.db = []
        lineSize = []


        self.current_timestamp = 0  # Initialize current timestamp
        sumRes = self.databaseSize * self.avgItemsPerTransaction  # Total number of items

        for i in range(self.databaseSize):
            # Determine the timestamp
            if self.performCoinFlip(self.occurrenceProbabilityOfSameTimestamp):
                timestamp = self.current_timestamp
            else:
                if self.performCoinFlip(self.occurrenceProbabilityToSkipSubsequentTimestamp):
                    self.current_timestamp += 2
                else:
                    self.current_timestamp += 1
                timestamp = self.current_timestamp

            self.db.append([timestamp])  # Start the transaction with the timestamp

            lineSize.append([i, 0])  # Initialize lineSize with 0 for each transaction

        # Adjust lineSize to ensure sum of sizes equals sumRes
        lineSize = self.tuning(lineSize, sumRes)

        # For each transaction, generate items
        for i in range(len(lineSize)):
            transaction_index = lineSize[i][0]
            num_items = lineSize[i][1]

            if num_items > self.numItems:
                raise ValueError(
                    "Error: Either increase numItems or decrease avgItemsPerTransaction or modify percentage")
            items = np.random.choice(range(1, self.numItems + 1), num_items, replace=False)
            self.db[transaction_index].extend(items)

        self._runTime = time.time() - start
        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def save(self, outputFile: str = None) -> None:
        """
        Save the temporal database to the specified output file.
        """
        if outputFile is not None:
            self.outputFile = outputFile
        else:
            self.outputFile = "temporalDatabase.txt"

        with open(self.outputFile, 'w') as writer:
            for line in self.db:
                writer.write(self.sep.join(map(str, line)) + '\n')

    def getRuntime(self) -> float:
        """
        Returns the runtime of the algorithm in seconds.
        """
        return self._runTime
    
    def getMemoryRSS(self) -> int:
        """
        """
        return self._memoryRSS
    
    def getMemoryUSS(self) -> int:
        """
        """
        return self._memoryUSS

    def getTransactions(self) -> None:
        """
        Convert the database to a DataFrame.
        """
        # merge all the transactions into a single DataFrame
        timestamps = []
        transactions = []

        for line in self.db:
            timestamps.append(line[0])
            transactions.append(line[1:])

        self.df = pd.DataFrame([timestamps, transactions], index=['Timestamp', 'Items']).T

        return self.df

if __name__ == '__main__':
    if len(sys.argv) == 7:
        obj = TemporalDatabase(
            databaseSize=int(sys.argv[1]),
            avgItemsPerTransaction=int(sys.argv[2]),
            numItems=int(sys.argv[3]),
            occurrenceProbabilityOfSameTimestamp=float(sys.argv[5]),
            occurrenceProbabilityToSkipSubsequentTimestamp=float(sys.argv[6]),
            sep=sys.argv[7]
        )
        obj.create()
        obj.save()
    else:
        print("Usage: python TemporalDatabase.py <databaseSize> <avgItemsPerTransaction> <numItems> <outputFile> <occurrenceProbabilityOfSameTimestamp> <occurrenceProbabilityToSkipSubsequentTimestamp> <sep> ")

        obj = TemporalDatabase(
            databaseSize=100000,
            avgItemsPerTransaction=10,
            numItems=50,
            sep="\t",
            occurrenceProbabilityOfSameTimestamp=0.1,
            occurrenceProbabilityToSkipSubsequentTimestamp=0.1
        )
        obj.create()
        obj.save("temporalDatabase.txt")

        print(obj.getTransactions())

        sys.exit(1)