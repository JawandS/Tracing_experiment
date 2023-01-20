import sys


def read_file(file):
    # add file lines to list
    lines = []
    with open(file, 'r') as f:
        for line in f:
            if line != '\n' and line != "":
                if ".txt" in line:
                    lines.append(float(line.split(" ")[0]))
                else:
                    lines.append(float(line))
    return lines


def get_data(lines):
    RUNS = 6  # number of runs in each experiment
    numArr = RUNS * 2
    # split into tracing and not tracing runs
    data = [[] for _ in range(numArr)]  # runs and log size
    for counter in range(0, len(lines)):
        data[counter % numArr].append(lines[counter])
    # get totals
    allJobs = [sum(data[i]) for i in range(0, numArr, 2)]
    totalJobs = sum(allJobs)
    allEvents = [sum(data[i]) for i in range(1, numArr, 2)]
    totalEvents = sum(allEvents)
    # process relative amounts
    relJobs = [round(100 * (float(allJobs[i]) / totalJobs), 5) for i in range(0, len(allJobs))]
    relEvents = [round(100 * (float(allEvents[i]) / totalEvents), 5) for i in range(0, len(allEvents))]
    # return relative values
    return relJobs, relEvents


def main(args):
    run = args[1]
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    relJobs, relEvents = get_data(lines)
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} | time {args[3]} | threads {args[4]} | depth {args[5]} | governor {args[6]}\n")
        f.write("Relative amounts of jobs\n")
        f.write(f"{relJobs}\n")
        f.write("Relative amounts of events\n")
        f.write(f"{relEvents}\n")


if __name__ == "__main__":
    # get the run number
    args = sys.argv
    if len(args) > 1:
        run = args[1]
        main(args)
    else:
        # runs = ["2", "3", "4", "5", "C1", "C2"]
        runs = ["1"]
        for run in runs:
            args = ["", run, 20, "20s", 15, 27, "powersave"]
            main(args)
