

class DataObj:
    def __init__(self, s):
        split = s.split(" ")
        self.entropy = float(split[1].replace("\n", ""))
        self.level = split[0]

    def __lt__(self, other):
        return self.entropy < other.entropy

    def __str__(self):
        return self.level + " " + str(round(self.entropy, 2))


def get_data():
    with open("generatedLevels.txt", "r") as file:
        objList = []
        for line in file:
            objList.append(DataObj(line))
        objList.sort()
        for obj in objList:
            print(obj)

if __name__ == "__main__":
    get_data()