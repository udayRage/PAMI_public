import random
#import pandas as pd


class generateUtilityTemporal:
    __transactionSize: int
    __numOfItems: int
    __avgTransactionLength: int
    __minUtilityValue: int
    __maxUtilityValue: int
    __minNumOfTimesAnItem: int
    __maxNumOfTimesAnItem: int
    __transactions: list[list[int]]
    __internalUtility: dict[str, list[int]]
    __externalUtility: list[list[int]]

    def __init__(self, transactionSize: int, numOfItems: int, avgTransactionLength: int,
                 minUtilityValue: int, maxUtilityValue: int,
                 minNumOfTimesAnItem: int, maxNumOfTimesAnItem: int) -> None:
        self.__transactionSize = transactionSize
        self.__numOfItems = numOfItems
        self.__avgTransactionLength = avgTransactionLength
        self.__minUtilityValue = minUtilityValue
        self.__maxUtilityValue = maxUtilityValue
        self.__minNumOfTimesAnItem = minNumOfTimesAnItem
        self.__maxNumOfTimesAnItem = maxNumOfTimesAnItem

        self.__transactions = list()
        self.__internalUtility = dict()
        self.__externalUtility = list()

    def generate(self) -> None:
        items = [i+1 for i in range(self.__numOfItems)]
        self.__transactions = [random.sample(items, random.randint(
            1, self.__avgTransactionLength*2)) for _ in range(self.__transactionSize)]
        self.__generateInternalUtility()
        self.__generateExternalUtility()

    def __generateInternalUtility(self) -> None:
        items = [i+1 for i in range(self.__numOfItems)]
        utilityValues = [random.randint(
            self.__minUtilityValue, self.__maxUtilityValue) for _ in range(self.__numOfItems)]
        self.__internalUtility = {
            "items": items, "utilityValues": utilityValues}

    def __generateExternalUtility(self) -> None:
        self.__externalUtility = [[random.randint(self.__minNumOfTimesAnItem, self.__maxNumOfTimesAnItem) for _ in range(
            len(transaction))] for transaction in self.__transactions]

    def save(self, outputFile: str, sep="\t", utilityType="utility") -> None:
        if utilityType == "utility":
            with open(outputFile, 'w') as f:
                for tid, (transaction, exUtils) in enumerate(zip(self.__transactions, self.__externalUtility)):
                    f.write(f"{tid}\t{sep.join(map(str, transaction))}:")
                    utilityValues = [
                        eu*self.__internalUtility["utilityValues"][item-1] for item, eu in zip(transaction, exUtils)]
                    f.write(
                        f"{sum(utilityValues)}:{sep.join(map(str, utilityValues))}\n")

        elif utilityType == "internal":
            with open(outputFile, "w") as f:
                for item, utility in zip(self.__internalUtility["items"], self.__internalUtility["utilityValues"]):
                    f.write(f"{item}{sep}{utility}\n")

        elif utilityType == "external":
            with open(outputFile, "w") as f:
                for transaction, exUtils in zip(self.__transactions, self.__externalUtility):
                    utils = list()
                    count = 0
                    for item in [i+1 for i in range(self.__numOfItems)]:
                        if item in transaction:
                            utils.append(exUtils[count])
                            count += 1
                        else:
                            utils.append(0)
                    f.write(f"{sep.join(map(str,utils))}\n")


if __name__ == "__main__":
    obj = generateUtilityTemporal(10, 10, 5, 10, 100, 1, 10)
    obj.generate()
    obj.save("temporalUtility_test.csv", utilityType="external")
