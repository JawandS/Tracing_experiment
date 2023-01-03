def read_file(file):
    # add file lines to list
    lines = []
    with open(file, 'r') as f:
        for line in f:
            if ln := line.strip():
                lines.append(float(ln), 3)
    return lines


def get_data(lines):
    # split into tracing and not tracing runs
    tracing_runs = []
    model_runs = []
    for counter, line in enumerate(lines):
        if counter % 2 == 0:
            tracing_runs.append(line)
        else:
            model_runs.append(line)
    # process average min and max
    tracing_info = (round(sum(tracing_runs) / len(tracing_runs), 5), min(tracing_runs), max(tracing_runs))
    model_info = (round(sum(model_runs) / len(model_runs), 5), min(model_runs), max(model_runs))
    difference_info = (round(tracing_info[0] - model_info[0], 5), round(tracing_info[1] - model_info[1], 5),
                       round(tracing_info[2] - model_info[2], 5))
    return tracing_info, model_info, difference_info


if __name__ == "__main__":
    # get the run number
    import sys

    args = sys.argv
    if len(args) > 1:
        run = args[1]
    else:
        run = '1'
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    tracing_info, model_info, difference_info = get_data(lines)
    # write results to file
    with open("Results/result" + run + ".txt", 'w') as f:
        f.write("average, min, max\n")
        f.write("Tracing: " + str(tracing_info) + "\n")
        f.write("Model: " + str(model_info) + "\n")
        f.write("Model: " + str(difference_info) + "\n")
