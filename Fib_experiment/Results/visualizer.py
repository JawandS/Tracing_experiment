import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# number of python processes
python_counts = dict()
# iterate through files in directory
for file in os.listdir("."):
    # check whether the file is in the desired format
    if file.endswith(".txt") and "by_PID" in file:
        # get run number
        run_number = file.split(".")[0]
        run_number = run_number.split("_")[-1]
        # ready file to string
        with open(file, 'r') as f:
            data = f.read()
        python_counts[int(run_number) + 1] = data.count("python3")
# sort the data
sorted_python_counts = [python_counts[key] for key in sorted(python_counts.keys())]
df = pd.DataFrame({"RunNumber": [idx+1 for idx in range(len(sorted_python_counts))], "NumPython": sorted_python_counts})
# graph the data
fig = sns.scatterplot(data=df, x="RunNumber", y="NumPython")
fig.set(xlabel='Run Number', ylabel='Number of Python Processes')
# display the graph
plt.show()
fig.figure.savefig("../python_counts.png")
