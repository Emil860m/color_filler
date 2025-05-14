import random


class DataObj:
    def __init__(self, s):
        split = s.split(" ")
        self.entropy = float(split[1].replace("\n", ""))
        self.level = split[0]

    def __lt__(self, other):
        return self.entropy < other.entropy

    def __str__(self):
        return self.level + "\t" + str(round(self.entropy, 2))


def get_data():
    with open("generatedLevels.txt", "r") as file:
        objList = []
        for line in file:
            objList.append(DataObj(line))
        objList.sort()
        # print(objList[int(len(objList) / 3)])
        # print(objList[int(len(objList) / 3) * 2])
        # print(objList[len(objList) - 1])
        low = []
        mid = []
        high = []
        for obj in objList:
            if obj.entropy <= 15.0:
                low.append(obj)
            elif obj.entropy >= 30.0:
                high.append(obj)
            else:
                mid.append(obj)
        random.shuffle(low)
        random.shuffle(mid)
        random.shuffle(high)
        for i in range(3):
            print(low[i])
            print(mid[i])
            print(high[i])
        # for obj in objList:
        #     print(obj)

if __name__ == "__main__":
    get_data()