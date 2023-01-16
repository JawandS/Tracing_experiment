import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main(run_num):
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        TIME = 20  # length of each job set
        twoProbes = [elem for elem in eval(lines[8])]
        tracing = [elem for elem in eval(lines[10])]
        standard = [elem for elem in eval(lines[12])]
        runNums = [i + 1 for i in range(len(twoProbes))]
        data_preproc = pd.DataFrame(
            {"Run": runNums, "Two Probes": [((twoProbes[i] / standard[i]) - 1) * 100 for i in range(len(standard))],
             "Tracing": [((tracing[i] / standard[i]) - 1) * 100 for i in range(len(standard))],
             "Standard": [((standard[i] / standard[i]) - 1) * 100 for i in range(len(standard))]})
        # plot data
        fig = sns.scatterplot(x='Run', y='value', hue='variable', data=pd.melt(data_preproc, ['Run']))
        fig.set(xlabel='Iteration', ylabel='Change from Standard (%)')
        fig.set_xticks([i for i in range(1, len(runNums) + 1)])
        fig.legend(loc='center right')
        fig.get_figure().savefig(f"Figures/figure_{run_num}.png")
        # close the plot
        plt.close()


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        run_num = args[1]
    else:
        # run_nums = ["2", "3", "4", "5", "C1", "C2"]
        run_nums = ["2"]
        for run_num in run_nums:
            main(run_num)
