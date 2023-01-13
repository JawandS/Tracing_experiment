import sys

import pandas as pd
import seaborn as sns

args = sys.argv
if len(args) > 1:
    run_num = args[1]
else:
    run_num = "5"
with open(f"Results/result_{run_num}.txt") as file:
    #  get data
    lines = [line.rstrip() for line in file]
    TIME = 20  # length of each job set
    twoProbes = [TIME / elem for elem in eval(lines[8])]
    tracing = [TIME / elem for elem in eval(lines[10])]
    standard = [TIME / elem for elem in eval(lines[12])]
    runNums = [i + 1 for i in range(len(twoProbes))]
    data_preproc = pd.DataFrame(
        {"Run": runNums, "Two Probes": [((twoProbes[i] / standard[i]) - 1) * 100 for i in range(len(standard))],
         "Tracing": [((tracing[i] / standard[i]) - 1) * 100 for i in range(len(standard))],
         "Standard": [((standard[i] / standard[i]) - 1) * 100 for i in range(len(standard))]})
    # plot data
    fig = sns.scatterplot(x='Run', y='value', hue='variable', data=pd.melt(data_preproc, ['Run']))
    fig.set(xlabel='Run Number', ylabel='Percent Decrease from Standard')
    fig.get_figure().savefig(f"Figures/figure_{run_num}.png")
