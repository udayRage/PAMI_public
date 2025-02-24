import numpy as np
import pandas as pd
import random
import psutil, os, time


class UtilityDatabase:
    def __init__(self, databaseSize, numItems, avgItemsPerTransaction,
                 minInternalUtilityValue, maxInternalUtilityValue,
                 minExternalUtilityValue, maxExternalUtilityValue):
        self.databaseSize = databaseSize
        self.numItems = numItems
        self.avgItemsPerTransaction = avgItemsPerTransaction
        self.minInternalUtilityValue = minInternalUtilityValue
        self.maxInternalUtilityValue = maxInternalUtilityValue
        self.minExternalUtilityValue = minExternalUtilityValue
        self.maxExternalUtilityValue = maxExternalUtilityValue
        self.entries = []
        self.ExternalUtilityData = self.GenerateExternalUtilityData()
        self._startTime = float()
        self._endTime = float()
        self._memoryUSS = float()
        self._memoryRSS = float()

    def GenerateExternalUtilityData(self):
        items = range(1, self.numItems + 1)
        ExternalUtilityData = {f'item{item}': random.randint(100, 900) for item in items}
        return ExternalUtilityData

    def create(self):
        self._startTime = time.time()
        for entry_id in range(1, self.databaseSize + 1):
            #entry_length = np.random.randint(1, self.avgItemsPerTransaction * 2)
            entry = np.random.randint(self.minInternalUtilityValue, self.maxInternalUtilityValue + 1,
                                      size=self.numItems)
            entry_sum = entry.sum()
            self.entries.append((entry, entry_sum))
        self._endTime = time.time()

    def save(self, fileName):
        with open(fileName, 'w') as file:
            for idx, (entry, entry_sum) in enumerate(self.entries, start=1):
                entry_str = '\t'.join(map(str, entry))
                file.write(f'{idx}\t{entry_str}\t{entry_sum}\n')

    def getMemoryUSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryUSS = process.memory_full_info().uss
        return self._memoryUSS

    def getMemoryRSS(self) -> float:

        process = psutil.Process(os.getpid())
        self._memoryRSS = process.memory_info().rss
        return self._memoryRSS

    def getRuntime(self) -> float:
        return self._endTime - self._startTime

    def SaveItemsInternalUtilityValues(self, fileName):
        items = random.sample(range(1, self.numItems + 1), self.numItems)
        internal_utility_data = [np.random.randint(self.minInternalUtilityValue, self.maxInternalUtilityValue + 1) for _
                                 in items]
        data = {'Item': items, 'Internal Utility Value': internal_utility_data}
        df = pd.DataFrame(data)
        df.to_csv(fileName, sep='\t', index=False)

    def Saveitemsexternalutilityvalues(self, fileName):
        items = random.sample(range(1, self.numItems + 1), self.numItems)
        data = {'Item': [f'item{item}' for item in items],
                'External Utility Value': list(self.ExternalUtilityData.values())}
        df = pd.DataFrame(data)
        df.to_csv(fileName, sep='\t', index=False)

    def GetUtilityData(self):
        data = {'Entry ID': range(1, len(self.entries) + 1),
                'Entries': [entry for entry, _ in self.entries],
                'Sum': [entry_sum for _, entry_sum in self.entries]}
        df = pd.DataFrame(data)
        return df

    def GetInternalUtilityData(self):
        items = random.sample(range(1, self.numItems + 1), self.numItems)
        InternalUtilityData = [np.random.randint(self.minInternalUtilityValue, self.maxInternalUtilityValue + 1) for _
                                 in items]
        data = {'Item': items, 'Internal Utility Value': InternalUtilityData}
        df = pd.DataFrame(data)
        return df

    def GetExternalUtilityData(self):
        items = random.sample(range(1, self.numItems + 1), self.numItems)
        data = {'Item': [f'item{item}' for item in items],
                'External Utility Value': list(self.ExternalUtilityData.values())}
        df = pd.DataFrame(data)
        return df

    def GenerateAndPrintItemPairs(self):
        items = random.sample(range(1, self.numItems + 1), 2)
        item1_id = f'item{items[0]}'
        item2_id = f'item{items[1]}'
        item1_value = self.ExternalUtilityData[item1_id]
        item2_value = self.ExternalUtilityData[item2_id]
        sum_values = item1_value + item2_value
        print(f"{item1_id} value: {item1_value}\t{item2_id} value: {item2_value}\tSum of values: {sum_values}")

        # Separate the sum with ' : '
        print(f"{item1_value}:{item2_value}:{sum_values}")


if __name__ == "__main__":
    data_generator = UtilityDatabase(100000, 2000, 10, 1, 100, 1, 10)
    data_generator.create()
    data_generator.save("utility_data-6.csv")
    data_generator.SaveItemsInternalUtilityValues("items_internal_utility.csv")
    data_generator.Saveitemsexternalutilityvalues("items_external_utility.csv")
    utilityDataFrame = data_generator.GetUtilityData()
    print('Runtime: ' + str(data_generator.getRuntime()))
    print('Memory (RSS): ' + str(data_generator.getMemoryRSS()))
    print('Memory (USS): ' + str(data_generator.getMemoryUSS()))
    InternalUtilityData_ = data_generator.GetInternalUtilityData()
    ExternalUtilityData_ = data_generator.GetExternalUtilityData()

    for _ in range(10):  # Print pairs for demonstration, adjust the range as needed
        data_generator.GenerateAndPrintItemPairs()



















































