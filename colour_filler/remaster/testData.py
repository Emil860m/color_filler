import pandas as pd
import numpy as np
from scipy.stats import kendalltau


class Stats:
    def __init__(self, line):
        lst = line.split("&")
        for i in lst:
            v = i.split("=")
            if v[0] == "inputs":
                self.inputs = v[1]
            elif v[0] == "resets":
                self.resets = v[1]
            elif v[0] == "time":
                self.time = v[1]


class Session:
    def __init__(self, lines):
        # TODO: Prøv at tilføje ordering på levels og se om ordering har haft effekt på rankings
        # TODO: Analyser også inputs, resets og time data
        self.PXI = {}
        try:
            for i in range(11):
                self.PXI[lines[i + 2].split("=")[0]] = int(lines[i + 2].split("=")[1])
            self.rankings = []
            self.stats = {}
            for i in range(9):
                self.rankings.append(lines[i + 14].split("=")[1])
                self.stats[lines[i + 24].split("?")[0]] = Stats(lines[i + 24].split("?")[1])
        except Exception as e:
            print(e)
            print(lines)
            exit(1)

    def print_this(self):
        for r in self.rankings:
            print(r)


rankings_per_level = {"1;1;1;1|1;1;1a;1|1;1;1b;4p|4b;1p;1;4a": [],
                      "2;2;0;4c|1p;1b;1;4b|1a;2;2;1c|4a;4p;1;1": [],
                      "1;1;1;1;4b|1;1;1a;1;1p|2;1;1;1c;2|0;1;1;1b;4a|0;4p;4c;2;2": [],
                      "4b;1;1;0;0|1;1;1;0;0|1b;1;2;4p;0|1;1a;1;0;0|4a;1p;0;1;0": [],
                      "0;0;1;1;0|1;1;1;1;4c|1;4a;1;1b;4p|1;1a;1c;1;1p|4b;2;1;1;1": [],
                      "0;2;2;1|2;1p;1b;1|2;2;1a;4b|0;4p;4a;2": [],
                      "2;1;2;0;0|1p;1a;1;1;1|1b;1;1;1;1|1;4p;2;4a;2|4b;1;1;1;2": [],
                      "0;0;0;0;0|4p;1;4a;4b;1|2;1p;1;1;0|1;1b;1;1a;1|2;1;1;1;2": [],
                      "2;2;2;4c;4p|4b;1;1b;1p;4a|1d;1a;1c;2;2|1;1;0;1;0|4d;1;1;0;0": []}
sessions = []
with open("ColorFillerData.txt", "r") as file:
    i = 0
    lines = file.readlines()
    linesc = []
    for s in lines:
        linesc.append(s.rstrip())
    while (i + 1) * 32 < len(linesc):
        ses = Session(linesc[i * 33:(i * 33) + 33])
        ses.print_this()
        sessions.append(ses)
        i += 1
for sess in sessions:
    for i in range(9):
        rankings_per_level[sess.rankings[i]].append(i)
df = pd.DataFrame.from_dict(rankings_per_level, orient='index',
                            columns=['Rater' + str(i + 1) for i in range(len(sessions))])
expected_ranking = {
    '4b;1;1;0;0|1;1;1;0;0|1b;1;2;4p;0|1;1a;1;0;0|4a;1p;0;1;0': 0,
    '1;1;1;1|1;1;1a;1|1;1;1b;4p|4b;1p;1;4a': 1,
    '2;2;0;4c|1p;1b;1;4b|1a;2;2;1c|4a;4p;1;1': 2,
    '0;2;2;1|2;1p;1b;1|2;2;1a;4b|0;4p;4a;2': 3,
    '0;0;0;0;0|4p;1;4a;4b;1|2;1p;1;1;0|1;1b;1;1a;1|2;1;1;1;2': 4,
    '2;1;2;0;0|1p;1a;1;1;1|1b;1;1;1;1|1;4p;2;4a;2|4b;1;1;1;2': 5,
    '2;2;2;4c;4p|4b;1;1b;1p;4a|1d;1a;1c;2;2|1;1;0;1;0|4d;1;1;0;0': 6,
    '0;0;1;1;0|1;1;1;1;4c|1;4a;1;1b;4p|1;1a;1c;1;1p|4b;2;1;1;1': 7,
    '1;1;1;1;4b|1;1;1a;1;1p|2;1;1;1c;2|0;1;1;1b;4a|0;4p;4c;2;2': 8
}
print("Ranking matrix:")
print(df)

df['Expected'] = df.index.map(expected_ranking)

print("\nRanking matrix with expected rankings:")
print(df)

# Step 1: ranks array (items x raters)
raters = ['Rater' + str(i + 1) for i in range(len(sessions))]
raters.append('Expected')
ranks = df[raters].to_numpy()

# Step 2: compute Kendall's W manually
n_items, n_raters = ranks.shape

# Sum of ranks for each item
sum_ranks = np.sum(ranks, axis=1)

# Mean of rank sums
mean_rank_sum = np.mean(sum_ranks)

# S: sum of squared deviations
S = np.sum((sum_ranks - mean_rank_sum) ** 2)

# Kendall's W formula
W = 12 * S / (n_raters ** 2 * (n_items ** 3 - n_items))

print(f"\nKendall's W (coefficient of concordance): {W:.4f}")
