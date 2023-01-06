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
    two_run = []
    tracing_run = []
    standard_run = []
    for counter in range(len(lines), 3):
        two_run.append(lines[counter])
        tracing_run.append(lines[counter + 1])
        standard_run.append(lines[counter + 2])
    # process average min and max
    two_info = (round(sum(two_run) / len(two_run), 3), min(two_run), max(two_run))
    tracing_info = (round(sum(tracing_run) / len(tracing_run), 3), min(tracing_run), max(tracing_run))
    standard_info = (round(sum(standard_run) / len(standard_run), 3), min(standard_run), max(standard_run))
    difference_info = (two_run, tracing_run, standard_run)

    def calc_diff(runA, runB):
        round(sum(runA) / sum(runB), 3)

    total_difference = [calc_diff(two_run, standard_run), calc_diff(tracing_run, standard_run), calc_diff(tracing_run, two_run)]
    return two_info, tracing_info, standard_info, difference_info, total_difference


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
    two_info, tracing_info, standard_info, diff_runs, total_difference = get_data(lines)
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} time {args[3]} threads {args[4]} depth {args[5]}\n")
        f.write("              average, min, max\n")
        f.write("Two probes  : " + str(tracing_info) + "\n")
        f.write("Tracing runs: " + str(tracing_info) + "\n")
        f.write("Normal runs : " + str(standard_info) + "\n")
        f.write("Two tracing standard: " + str(diff_runs) + "\n")
        f.write("Two vs standard | tracing vs standard | tracing vs two\n")
        f.write("Total diffs: " + str(total_difference) + "\n")
