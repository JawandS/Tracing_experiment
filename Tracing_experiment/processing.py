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
    # process average min and max
    two_info = (round(sum(two_run) / len(two_run), 3), min(two_run), max(two_run))
    tracing_info = (round(sum(tracing_run) / len(tracing_run), 3), min(tracing_run), max(tracing_run))
    standard_info = (round(sum(standard_run) / len(standard_run), 3), min(standard_run), max(standard_run))
    difference_info = (two_run, tracing_run, standard_run)
    # calculate differences
    total_difference = [round(sum(standard_run) / sum(two_run), 3), round(sum(standard_run) / sum(tracing_run), 3),
                        round(sum(tracing_run) / sum(two_run), 3),
                        round((sum(two_lines) / sum(two_run)) / (sum(tracing_lines) / sum(tracing_run)), 3)]
    return two_info, tracing_info, standard_info, difference_info, total_difference


def main(args):
    runs = args[1]
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    two_info, tracing_info, standard_info, diff_runs, total_difference = get_data(lines)
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} time {args[3]} threads {args[4]} depth {args[5]}\n")
        f.write("              average, min, max\n")
        f.write("Two probes  : " + str(two_info) + "\n")
        f.write("Tracing runs: " + str(tracing_info) + "\n")
        f.write("Normal runs : " + str(standard_info) + "\n")
        f.write("standard / two | standard / tracing | tracing / two | two events / tracing events\n")
        f.write("Total diffs: " + str(total_difference) + "\n")
        f.write("twoProbes=\n")
        f.write(str(diff_runs[0]) + "\n")
        f.write("tracingRuns=\n")
        f.write(str(diff_runs[1]) + "\n")
        f.write("standardRuns=\n")
        f.write(str(diff_runs[2]) + "\n")


if __name__ == "__main__":
    # get the run number
    args = sys.argv
    if len(args) > 1:
        run = args[1]
        main(args)
    else:
        run = "C2"
        args = ["", run, 20, "20s", 15, 27]
        main(args)
