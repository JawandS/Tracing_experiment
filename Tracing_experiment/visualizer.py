import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def versionOne(run_num):
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        # TIME = 20  # length of each job set
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


def versionTwo(run_num):
    # add bar plots of relative jobs/events for powersave mode
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        relJobs = eval(lines[2])
        relEvents = eval(lines[4])
        df = pd.DataFrame({
            'Type': ["X", "A", "B", "C", "D", "E"],
            'Relative # of Jobs': [elem for elem in relJobs],
            'Relative # of Events': [elem for elem in relEvents]
        })
        fig, ax1 = plt.subplots(figsize=(10, 10))
        tidy = df.melt(id_vars='Type').rename(columns=str.title)
        sns.barplot(x='Type', y='Value', hue='Variable', data=tidy, ax=ax1)
        sns.despine(fig)
        fig.savefig(f"Figures/Powersave/figure_{run_num}.png")


def versionThree(run_num):
    # add bar plots of relative jobs/events for powersave mode
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        relJobs = eval(lines[6])
        relEvents = eval(lines[8])
        df = pd.DataFrame({
            'Type': ["X", "A", "B", "C", "D", "E"],
            'Total Jobs': [elem for elem in relJobs],
        })
        fig, ax1 = plt.subplots(figsize=(10, 10))
        sns.barplot(x='Type', y='Total Jobs', data=df, ax=ax1)
        sns.despine(fig)
        fig.savefig(f"Figures/Powersave/figure_abs_{run_num}.png")


def linePlot(run_num):
    # line plot of the events compared to jobs and probes
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        totalJobs = eval(lines[6])
        totalEvents = eval(lines[8])
        numProbes = [0, 1, 2, 1, 1, 3, 6, 10]
        df = pd.DataFrame({
            'Probe Type': ["X", "A", "B", "C", "D", "E", "F", "G"],
            'Probes': numProbes,
            'Total Events': totalEvents,
            'Total Jobs': totalJobs,
        })
        # plot a scatter plot with regression
        fig, ax1 = plt.subplots(figsize=(10, 10))
        sns.regplot(x='Total Events', y='Total Jobs', data=df, ax=ax1)
        sns.despine(fig)
        fig.savefig(f"Figures/{run_num}_events.png")
        # close the plot
        plt.close()
        # plot probes to jobs
        fig, ax1 = plt.subplots(figsize=(10, 10))
        sns.regplot(x='Probes', y='Total Jobs', data=df, ax=ax1)
        sns.despine(fig)
        fig.savefig(f"Figures/{run_num}_probes.png")


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        run_num = args[1]
        versionThree(run_num)
    else:
        # run_nums = ["2", "3", "4", "5", "C1", "C2"]
        run_nums = ["home_1_ps", "home_2_per"]
        for run_num in run_nums:
            linePlot(run_num)
