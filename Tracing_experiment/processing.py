import sys


def read_file(file):
    # add file lines to list
    lines = []
    with open(file, 'r') as f:
        for line in f:
            if ln := int(line.strip()):
                lines.append(ln)
    return lines


def get_data(lines):
    # split into tracing and not tracing runs
    tracing_run = []
    standard_run = []
    for counter, line in enumerate(lines):
        if counter % 2 == 0:
            tracing_run.append(line)
        else:
            standard_run.append(line)
    # process average min and max
    tracing_info = (round(sum(tracing_run) / len(tracing_run), 3), min(tracing_run), max(tracing_run))
    standard_info = (round(sum(standard_run) / len(standard_run), 3), min(standard_run), max(standard_run))
    difference_info = [standard_run[i] - tracing_run[i] for i in range(len(tracing_run))]
    total_difference = round(sum(standard_run) / sum(tracing_run), 3)
    return tracing_info, standard_info, difference_info, total_difference


if __name__ == "__main__":
    # get the run number
    args = sys.argv
    if len(args) > 1:
        run = args[1]
    else:
        run = '3'
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    tracing_info, standard_info, diff_runs, total_difference = get_data(lines)
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} time {args[3]} threads {args[4]} depth {args[5]}")
        f.write("              average, min, max\n")
        f.write("Tracing runs: " + str(tracing_info) + "\n")
        f.write("Normal runs : " + str(standard_info) + "\n")
        f.write("Differences: " + str(diff_runs) + "\n")
        f.write("Total diff: " + str(total_difference) + "\n")
