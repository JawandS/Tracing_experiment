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
    # split into tracing and not tracing runs
    two_run = []
    tracing_run = []
    standard_run = []
    two_lines = []  # number of tracing events
    tracing_lines = []  # number of context switches
    for counter in range(0, len(lines), 5):
        two_run.append(lines[counter])
        tracing_run.append(lines[counter + 1])
        standard_run.append(lines[counter + 2])
        two_lines.append(lines[counter + 3])
        tracing_lines.append(lines[counter + 4])
    difference_info = (two_run, tracing_run, standard_run)
    # process average min and max
    two_total = sum(two_run)
    tracing_total = sum(tracing_run)
    standard_total = sum(standard_run)
    two_info = (round(two_total / len(two_run), 3), min(two_run), max(two_run))
    tracing_info = (round(tracing_total / len(tracing_run), 3), min(tracing_run), max(tracing_run))
    standard_info = (round(standard_total / len(standard_run), 3), min(standard_run), max(standard_run))
    # calculate differences
    total_difference = [round((two_total / standard_total) - 1, 3) * 100,
                        round((tracing_total / standard_total) - 1, 3) * 100,
                        round((two_total / tracing_total) - 1, 3) * 100,
                        round(((sum(two_lines) / two_total) / (sum(tracing_lines) / tracing_total)) - 1, 3)]
    return two_info, tracing_info, standard_info, difference_info, total_difference


def main(args):
    run = args[1]
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    two_info, tracing_info, standard_info, diff_runs, total_difference = get_data(lines)
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} time {args[3]} threads {args[4]} depth {args[5]} governor {args[6]}\n")
        f.write("              average, min, max\n")
        f.write("Two probes  : " + str(two_info) + "\n")
        f.write("Tracing runs: " + str(tracing_info) + "\n")
        f.write("Normal runs : " + str(standard_info) + "\n")
        f.write("two v standard | tracing v standard | two v tracing | two events v tracing events\n")
        f.write("Total diffs: " + str(total_difference) + "\n")
        f.write("twoProbes=\n")
        f.write(str(diff_runs[0]) + "\n")
        f.write("tracingRuns=\n")
        f.write(str(diff_runs[1]) + "\n")
        f.write("standardRuns=\n")
        f.write(str(diff_runs[2]) + "\n")


if __name__ == "__main__":
    import visualizer

    # get the run number
    args = sys.argv
    if len(args) > 1:
        run = args[1]
        main(args)
        visualizer.main(run)
    else:
        # runs = ["2", "3", "4", "5", "C1", "C2"]
        runs = ["6"]
        for run in runs:
            args = ["", run, 20, "20s", 15, 27, "powersave"]
            main(args)
            visualizer.main(run)
